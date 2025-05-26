import boto3
import json
import uuid
import time
import random
from datetime import datetime

stream_name = "clickstream-data"
kinesis = boto3.client("kinesis", region_name="us-east-1")

users = [str(uuid.uuid4()) for _ in range(10)]
pages = ["/", "/home", "/products", "/about", "/contact", "/checkout"]

while True:
    user = random.choice(users)
    page = random.choice(pages)
    ts = datetime.utcnow().isoformat()

    event = {
        "user_id": user,
        "page": page,
        "timestamp": ts
    }

    kinesis.put_record(
        StreamName=stream_name,
        Data=json.dumps(event),
        PartitionKey=user
    )

    time.sleep(0.5)