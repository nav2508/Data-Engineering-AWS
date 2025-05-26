import boto3
import os

glue_client = boto3.client('glue')

def lambda_handler(event, context):
    job_name = os.environ['GLUE_JOB_NAME']
    for record in event['Records']:
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        # Start Glue job
        response = glue_client.start_job_run(
            JobName=job_name,
            Arguments={
                '--S3_INPUT_PATH': f's3://{s3_bucket}/{s3_key}',
            }
        )
        return {
            'statusCode': 200,
            'body': f"Glue job {job_name} started with run ID {response['JobRunId']}"
        }