CREATE TABLE prices (
  symbol    VARCHAR(8),
  datetime  DATETIME,
  price     DECIMAL(12,4),
  PRIMARY KEY(symbol, datetime)
);

CREATE TABLE sentiment (
  topic         VARCHAR(32),
  datetime      DATETIME,
  post_count    INT,
  avg_sentiment FLOAT,
  PRIMARY KEY(topic, datetime)
);