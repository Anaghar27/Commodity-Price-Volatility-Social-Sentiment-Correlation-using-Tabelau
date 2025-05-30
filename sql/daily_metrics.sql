CREATE OR REPLACE VIEW daily_metrics AS
SELECT
  DATE(p.datetime)                AS date,
  p.symbol,
  STDDEV_SAMP(p.price)            AS daily_volatility,
  AVG(s.avg_sentiment)            AS daily_sentiment,
  SUM(s.post_count)               AS total_posts
FROM prices p
LEFT JOIN sentiment s
  ON s.topic = p.symbol
  AND DATE(s.datetime) = DATE(p.datetime)
GROUP BY
  p.symbol,
  DATE(p.datetime);