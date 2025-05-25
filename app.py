import os
from sched import scheduler

import pandas as pd
from apscheduler.jobstores.base import JobLookupError

import db
#from py5paisa import FivePaisaClient
from apscheduler.triggers.cron import CronTrigger
import logging
import json
import requests
import calculate_tax
import datetime

import fivepaisa_client
import trade
from config import AUTH_TOKEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)



def take_home_salary(gross, variable, tax_regime, section80c, home_loan, hra_received, rent_paid, nps):
   tax_regime = tax_regime
   if tax_regime == "New":
      tax= calculate_tax.new_tax_regime(gross, variable)
      return tax
   else:
       tax= calculate_tax.old_tax_regime(gross,variable, section80c, home_loan, hra_received, rent_paid, nps)
       return tax

#baseurl = "https://gorest.co.in/public/v2/users"

@app.route('/')
def index():
    return render_template('index.html')  # This looks for templates/index.html


#auth_token = "bearer 53c961fbfd2f25d6677ebde66af0c9bd290af8d3e5257dcd5930ff798c40b321"
@app.route('/salary', methods=['GET', 'POST'])
def calculate_salary():
    data= request.get_json()

    gross=data.get("gross", 0)
    variable=data.get("variable", 0)
    tax_regime=data.get("tax_regime", "Old")
    section80c=data.get("section80c", 0)
    home_loan=data.get("home_loan", 0)
    nps=data.get("NPS2", 0)
    rent_paid=data.get("rent_paid", 0)
    hra_received=data.get("hra_received", 0)
    other_deduction3=data.get("other_deduction3", 0)


    tax= take_home_salary(gross, variable, tax_regime, section80c, home_loan, hra_received, rent_paid, nps)
    pf=0.12*0.5*gross #provident fund and gratutity to be deducted
    gratuity = 0.0481*0.5*gross
    net_salary= gross-tax-variable-pf-gratuity
    monthly_salary = net_salary/12
    print(monthly_salary)
    return jsonify(monthly_salary=monthly_salary)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    """
    Accept JSON (object or list) → convert to DataFrame → insert into MySQL.
    """
    payload = request.get_json(force=True)

    # Normalize to list
    if isinstance(payload, dict):
        payload = [payload]
    elif not isinstance(payload, list):
        return jsonify(error="Invalid payload format"), 400

    try:
        df = pd.DataFrame(payload)
        # Add default "user" if not present
        if 'user' not in df.columns:
            df['user'] = 'manual'

        inserted_rows = db.insert_trades_df(df)
        return jsonify(status="success", rows=inserted_rows), 201

    except Exception as exc:
        app.logger.error("Insert failed: %s", exc, exc_info=True)
        return jsonify(status="error", message=str(exc)), 500

def start_trade_logic(client):
    """This is what APScheduler will call each time."""
    trade.start_trade(client)
    print("Trade function ran at", datetime.now().strftime("%H:%M:%S"))

@app.route('/start_trade', methods=['POST'])
def start_trade():
    """
    Body JSON:
        {
          "totp": "123456"
        }
    Schedules start_trade_logic() every weekday at 09:20.
    """
    data = request.get_json(force=True)
    totp = data.get("totp")
    if not totp:
        return jsonify({"error": "TOTP field missing"}), 400

    # --- login --- #
    try:
        client = fivepaisa_client.get_client(totp)
    except Exception as exc:
        return jsonify({"error": f"Login failed: {exc}"}), 500

    # --- remove any old job with same id --- #
    try:
        scheduler.remove_job('trade-job')
    except JobLookupError:
        pass

    # --- add new cron job (weekday 09:20 IST) --- #
    scheduler.add_job(
        func=start_trade_logic,          # DO NOT call it here
        args=[client],                   # pass client to the job
        trigger=CronTrigger(day_of_week='mon-fri', hour=9, minute=20),
        id='trade-job',
        replace_existing=True
    )

    return (
        jsonify({"status": "Trade job scheduled for 09:20 AM (Mon-Fri)"}),
        200
    )





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






