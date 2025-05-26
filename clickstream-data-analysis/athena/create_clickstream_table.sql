CREATE EXTERNAL TABLE IF NOT EXISTS clickstream (
  user_id STRING,
  page STRING,
  timestamp STRING,
  session_id STRING
)
PARTITIONED BY (`year` string, `month` string, `day` string)
STORED AS JSON
LOCATION 's3://clickstream-data-logs/clickstream/'
TBLPROPERTIES ("projection.enabled" = "true");