import os, pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

# 1. Load joined data with 24h rolling volatility
query = """
SELECT p.symbol, p.datetime, p.price,
       STDDEV_SAMP(p2.price) OVER (
         PARTITION BY p.symbol
         ORDER BY p.datetime
         ROWS BETWEEN 23 PRECEDING AND CURRENT ROW
       ) AS vol_24h,
       s.post_count, s.avg_sentiment
  FROM prices p
  LEFT JOIN sentiment s
    ON s.topic=p.symbol AND s.datetime=p.datetime
  LEFT JOIN prices p2
    ON p2.symbol=p.symbol
   AND p2.datetime BETWEEN DATE_SUB(p.datetime, INTERVAL 23 HOUR) AND p.datetime
"""
df = pd.read_sql(query, engine, parse_dates=["datetime"])

# 2. Correlation heatmap
corr = df[["vol_24h","avg_sentiment","post_count"]].corr()
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True)
plt.title("Volatility ↔ Sentiment Correlation")
plt.show()

# 3. Daily time-series plots
symbols = ["CL=F", "GC=F", "SI=F"]

for sym in symbols:
    sub = df[df.symbol == sym]
    if sub.empty:
        print(f"Skipping {sym}: no raw data loaded", flush=True)
        continue
        
    daily = (
        sub
        .set_index("datetime")
        .resample("D")
        .mean(numeric_only=True)
    )

    daily = daily.dropna(how="all", subset=["vol_24h","avg_sentiment"])
    if daily.empty:
        print(f"Skipping {sym}: no daily data after aggregation", flush=True)
        continue

    print(f"Plotting {sym}: {len(daily)} days", flush=True)
    fig, ax = plt.subplots()
    daily[["vol_24h","avg_sentiment"]].plot(
        ax=ax,
        title=f"{sym} Daily Averages",
        xlabel="Date",
        ylabel="Value"
    )
    plt.show()

# 4. Returns distribution
df["return"] = df.groupby("symbol")["price"].pct_change()
plt.figure(figsize=(6,4))
df["return"].dropna().hist(bins=50)
plt.title("Hourly Returns Distribution")
plt.show()