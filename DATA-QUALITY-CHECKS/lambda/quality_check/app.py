import boto3
import pandas as pd
import io
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = "data-validation-and-quality-checks"
    key = "output/data.csv"

    obj = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    results = {
        "row_count": len(df),
        "null_check": int(df['id'].isnull().sum()),
        "duplicate_check": int(df.duplicated(subset=['id']).sum()),
    }

    if results["null_check"] > 0 or results["duplicate_check"] > 0:
        alert_lambda = boto3.client('lambda')
        alert_lambda.invoke(
            FunctionName="log-alert-lambda",
            InvocationType='Event',
            Payload=json.dumps(results)
        )

    s3.put_object(
        Bucket=bucket,
        Key="quality-logs/check_results.json",
        Body=json.dumps(results)
    )

    return {"status": "Validation complete", "results": results}