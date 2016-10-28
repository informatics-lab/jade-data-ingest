import boto3
import os
import json
import time
import tempfile
import metadata_to_elastic_search
import uuid

sqs = boto3.resource('sqs', region_name='eu-west-1')
s3 = boto3.resource('s3', region_name='eu-west-1')
queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])

def log(msg):
    print(msg)

def download_file(bucket, key):
    filepath = os.path.join(tempfile.gettempdir(), str(uuid.uuid1()) +'.nc')
    s3.meta.client.download_file(bucket, key, filepath)
    return filepath

def process_message(msg):
    msg = json.loads(msg.body)
    for r in msg['Records']:
        bucket = r['s3']['bucket']['name']
        key = r['s3']['object']['key']
        log("found %s in bucket %s" % (key, bucket))
        filepath = download_file(bucket, key)
        log(metadata_to_elastic_search.process_file(filepath))
        os.remove(filepath)

def process_all_messages():
    for msg in queue.receive_messages():
        process_message(msg)
        log("Message processed, will delete")
        msg.delete()

if __name__ == '__main__':
    while True:
        process_all_messages()
        time.sleep(10)