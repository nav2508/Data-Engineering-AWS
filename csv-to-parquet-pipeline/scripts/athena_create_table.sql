CREATE EXTERNAL TABLE IF NOT EXISTS csv_parquet_data (
  id STRING,
  name STRING,
  date_column STRING
)
PARTITIONED BY (year STRING, month STRING)
STORED AS PARQUET
LOCATION 's3://parquet-data-bucket25/transformed/';