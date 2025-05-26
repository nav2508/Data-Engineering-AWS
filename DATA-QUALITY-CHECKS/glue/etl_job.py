import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Sample ETL: read, transform, write
input_df = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": ["s3://data-validation-and-quality-checks/input/"]},
    format="csv",
    format_options={"withHeader": True}
)

mapped_df = input_df.rename_field("CustomerID", "id")

output_path = "s3://data-validation-and-quality-checks/output/"
glueContext.write_dynamic_frame.from_options(
    frame=mapped_df,
    connection_type="s3",
    connection_options={"path": output_path},
    format="csv"
)

job.commit()