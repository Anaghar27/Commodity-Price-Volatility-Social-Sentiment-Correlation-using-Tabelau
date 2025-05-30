import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

sql1 = """
INSERT INTO prices (symbol, datetime, price)
SELECT
  symbol,
  DATE_FORMAT(datetime, '%Y-%m-%d %H:00:00') AS datetime,
  AVG(price) AS price
FROM staging_prices
GROUP BY
  symbol,
  DATE_FORMAT(datetime, '%Y-%m-%d %H:00:00')
ON DUPLICATE KEY UPDATE
  price = VALUES(price);
"""

sql2 = """
INSERT INTO sentiment (topic, datetime, post_count, avg_sentiment)
SELECT
  topic,
  DATE_FORMAT(FROM_UNIXTIME(created_utc), '%Y-%m-%d %H:00:00') AS datetime,
  COUNT(*)   AS post_count,
  AVG(score) AS avg_sentiment
FROM staging_reddit
GROUP BY
  topic,
  DATE_FORMAT(FROM_UNIXTIME(created_utc), '%Y-%m-%d %H:00:00')
ON DUPLICATE KEY UPDATE
  post_count    = VALUES(post_count),
  avg_sentiment = VALUES(avg_sentiment);
"""

with engine.begin() as conn:
    conn.execute(text(sql1))
    conn.execute(text(sql2))
