import pandas as pd
import db
import datetime

def vwap(symbol):

    stock_data = db.get_stocks(symbol)
    lookback = 10

    first_n_values = stock_data.head(lookback)

    vwap_price = (first_n_values['price'] * first_n_values['volume']).sum()/first_n_values['volume'].sum()

    return vwap_price






import datetime

def previous_closing_price(symbol):
    # Fetch the DataFrame for the given symbol
    stock_data = db.get_stocks(symbol)  # Assumes it returns a DataFrame with 'date', 'time', and 'price'

    # Define yesterday's date and 3:30 PM time
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    target_time = datetime.time(hour=15, minute=30)

    # Filter for rows matching yesterday's date and 3:30 PM
    mask = (stock_data['date'] == pd.to_datetime(yesterday)) & (stock_data['time'] == pd.to_datetime(target_time))
    filtered_data = stock_data.loc[mask]

    if not filtered_data.empty:
        return filtered_data.iloc[0]['price']
    else:
        return None  # or raise an exception/log a warning if price is not found








