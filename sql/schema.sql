CREATE DATABASE commodities;
USE commodities;

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