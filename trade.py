import pandas

from position import position_status
from datetime import datetime
import fivepaisa_client
import pandas as pd
import app
import vwap_engine
import db

# starting the trade after checking the current position

def start_trade(client):
    count=0
    position = position_status(client)
    if position['Status'] == 'Success':
        pos_df = pd.DataFrame(position['Data'])
        if len(pos_df)==1:
            stock = pos_df.iloc[0]['ScripName']
            ScripCode = pos_df.iloc[0]['ScripCode']
            BuyAvgRate = pos_df.iloc[0]['BuyAvgRate']
            SellAvgRate = pos_df.iloc[0]['SellAvgRate']
            Qty = pos_df.iloc[0]['NetQty']

            if Qty >= 0 and datetime.datetime.now().time().strftime('%H:%M') == '15:25':
                client.squareoff_all()
            else:
                print(f'No exit time and Qty is {Qty} & {datetime.datetime.now().time().strftime("%H:%M")}')






        if len(pos_df)==2:
            stock = pos_df.iloc[0]['ScripName']
            ScripCode = pos_df.iloc[0]['ScripCode']
            BuyAvgRate = pos_df.iloc[0]['BuyAvgRate']
            SellAvgRate = pos_df.iloc[0]['SellAvgRate']
            Qty = pos_df.iloc[0]['NetQty']

            # reading the details of 2nd stock
            stock1 = pos_df.iloc[1]['ScripName']
            ScripCode1 = pos_df.iloc[1]['ScripCode']
            BuyAvgRate1 = pos_df.iloc[1]['BuyAvgRate']
            SellAvgRate1 = pos_df.iloc[1]['SellAvgRate']
            Qty1 = pos_df.iloc[1]['NetQty']

            if Qty >= 0 and Qty1 >=0 and datetime.datetime.now().time().strftime('%H:%M') == '15:25':
                client.squareoff_all()
            else:
                print(f'No exit time and Qty is {Qty}, {Qty1} & {datetime.datetime.now().time().strftime("%H:%M")}')

        #taking the position

        if len(pos_df)==0 and count <=2:

            # getting value of previous close price



            req_list = [
                {"Exch": "N", "ExchType": "C", "ScripCode": 4963},
                {"Exch": "N", "ExchType": "C", "ScripCode": 1922}
            ]

            market_price = client.fetch_market_price(req_list)

            # getting the current price from market

            df_market_price = pd.DataFrame(market_price)
            current_price1 = df_market_price[0]['LastTradedPrice']
            current_price2 = df_market_price[1]['LastTradedPrice']

            Target_price = current_price1 + current_price1*0.004

            # getting the volume

            volume1 = df_market_price[0]['Volume']
            volume2 = df_market_price[1]['Volume']


            first_symbol= "KOTAKBANK"
            second_symbol = "ICICIBANK"


            vwap_price1 = vwap_engine.vwap(first_symbol)
            vwap_price2 = vwap_engine.vwap(second_symbol)

            previous_closing_price1 = vwap_engine.previous_closing_price(first_symbol)
            previous_closing_price2 = vwap_engine.previous_closing_price(second_symbol)




            if current_price1 > vwap_price1 and current_price1 > previous_closing_price1:
                order_details = client.bo_order(OrderType='B', Exchange='N', ExchangeType='C', ScripCode=df_market_price[0]['ScripCode'], Qty=1, LimitPrice= current_price1,
                                TargetPrice=Target_price, StopLossPrice=vwap_price1, LimitPriceForSL=vwap_price1, TrailingSL=0.1)

                current_date = datetime.now().strftime("%d-%m-%Y")
                current_time = datetime.now().strftime("%H:%M:%S")

                order_list = {order_details['ScripCode'],current_date,current_time,order_details['Qty'],order_details['OrderType'],"System",order_details['Price']}
                trade_details = pd.DataFrame([order_list])

                #expected_cols = ['symbol', 'trade_date', 'trade_time', 'quantity', 'trade_type', 'user','price']

                #inserting the columns in the database

                try:
                    insert = db.insert_trades_df(trade_details)
                    if insert:
                        print("insert success")
                except Exception as e:
                    print("insert failed", str(e))



                count += 1
            if current_price2 > vwap_price2 and current_price2 > previous_closing_price2:
                order_details= client.bo_order(OrderType='B', Exchange='N', ExchangeType='C',
                                ScripCode=df_market_price[1]['ScripCode'], Qty=1, LimitPrice=current_price2,
                                TargetPrice=Target_price, StopLossPrice=vwap_price2, LimitPriceForSL=vwap_price1,
                                TrailingSL=0.1)

                current_date = datetime.now().strftime("%d-%m-%Y")
                current_time = datetime.now().strftime("%H:%M:%S")

                trade_details = pd.DataFrame(order_details)
                try:
                    insert = db.insert_trades_df(trade_details)
                    if insert:
                        print("insert success")
                except Exception as e:
                    print("insert failed", str(e))


                count += 1





























