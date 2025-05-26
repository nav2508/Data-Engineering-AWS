import json
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn='arn:aws:sns:your-region:account-id:data-quality-alerts',
        Subject='Data Quality Issue Detected',
        Message=json.dumps(event)
    )
    return {"status": "Alert sent"}