import pandas as pd
import datetime
import pymysql
from sqlalchemy import create_engine,text
import config

def insert_trades_df(df: pd.DataFrame) -> int:
    """
    Insert trades from a DataFrame into the database.
    Required columns: symbol, trade_date, trade_time, quantity, trade_type, user
    """
    engine = create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )

    # Ensure DataFrame has correct columns
    expected_cols = ['symbol', 'trade_date', 'trade_time', 'quantity', 'trade_type', 'user','price']
    missing = set(expected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df.to_sql('trades', con=engine, if_exists='append', index=False)
    return len(df)

def insert_stocks(df: pd.DataFrame) -> int:
    engine = create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )
    expected_cols = ['id', 'symbol', 'price','volume','date','time']
    missing = set(expected_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df.to_sql('market_data', con=engine, if_exists='append', index=False)
    return len(df)

def get_stocks(symbol: str) -> pd.DataFrame:
    engine = create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
    )
    expected_cols = ['id', 'symbol', 'price','volume','date','time']

    today = datetime.now().date()
    yesterday = today - datetime.timedelta(days=1)

    query = text("""
           SELECT id, symbol, price, volume, date, time
           FROM market_data
           WHERE symbol = :symbol
           AND date BETWEEN :yesterday AND :today ORDER BY date desc
       """)

    df = pd.read_sql(query, con=engine, params=(symbol,yesterday,today))
    return df







