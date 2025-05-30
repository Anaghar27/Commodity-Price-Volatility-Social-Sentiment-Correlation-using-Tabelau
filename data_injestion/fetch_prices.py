import os, pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

symbols = ["CL=F", "GC=F", "SI=F"]  # crude oil, gold, silver

def fetch_and_store():
    df_list = []
    for sym in symbols:
        hist = yf.Ticker(sym).history(period="7d", interval="1h")[["Close"]]
        hist = hist.rename(columns={"Close": "price"}).reset_index()
        hist["symbol"] = sym
        df_list.append(hist)
    all_prices = pd.concat(df_list)
    all_prices.to_sql("staging_prices", engine, if_exists="replace", index=False)

if __name__ == "__main__":
    fetch_and_store()