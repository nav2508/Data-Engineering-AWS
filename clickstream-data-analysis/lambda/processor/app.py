import json
import boto3
import os
import uuid
from datetime import datetime, timedelta

s3 = boto3.client("s3")
bucket = os.environ["S3_BUCKET"]
SESSION_TIMEOUT = 30

user_sessions = {}

def lambda_handler(event, context):
    sessionized = []
    now = datetime.utcnow()
    
    for record in event['Records']:
        payload = json.loads(base64.b64decode(record['kinesis']['data']).decode('utf-8'))
        user_id = payload["user_id"]
        page = payload["page"]
        ts = datetime.fromisoformat(payload["timestamp"])

        last_event = user_sessions.get(user_id)
        if not last_event or (ts - last_event[0]) > timedelta(minutes=SESSION_TIMEOUT):
            session_id = str(uuid.uuid4())
        else:
            session_id = last_event[1]

        user_sessions[user_id] = (ts, session_id)

        sessionized.append({
            "user_id": user_id,
            "page": page,
            "timestamp": ts.isoformat(),
            "session_id": session_id
        })

    filename = f"clickstream/year={now.year}/month={now.month}/day={now.day}/session-{now.timestamp()}.json"
    s3.put_object(Bucket=bucket, Key=filename, Body=json.dumps(sessionized))

    return {"status": "ok"}