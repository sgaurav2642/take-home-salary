import os
import pandas as pd
import db
#from py5paisa import FivePaisaClient
import json
import requests
import config
import calculate_tax
from config import AUTH_TOKEN
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

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




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)






