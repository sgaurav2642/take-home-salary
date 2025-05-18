import pandas as pd

import pymysql
from sqlalchemy import create_engine
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
