import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import datetime

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'S3_INPUT_PATH'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read CSV
input_path = args['S3_INPUT_PATH']
df = spark.read.option("header", "true").csv(input_path)

# Add partitions (year/month)
df = df.withColumn("year", df["date_column"].substr(1, 4)) \
       .withColumn("month", df["date_column"].substr(6, 2))  # Customize this based on your schema

# Write Parquet
output_path = "s3://parquet-data-bucket25/transformed/"
df.write.mode("overwrite").partitionBy("year", "month").parquet(output_path)

job.commit()