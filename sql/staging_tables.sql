CREATE TABLE staging_prices (
  symbol    VARCHAR(8),
  datetime  DATETIME,
  price     DECIMAL(12,4)
);

CREATE TABLE staging_reddit (
  topic        VARCHAR(32),
  created_utc  BIGINT,
  score        FLOAT,
  PRIMARY KEY(topic, created_utc)
);