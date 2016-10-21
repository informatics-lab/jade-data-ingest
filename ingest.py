import boto3
import os
import json
import time
sqs = boto3.resource('sqs', region_name='eu-west-1')
queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])


def log(msg):
    print(msg)

def process_message(msg):
    msg = json.loads(msg.body)
    for r in msg['Records']:
        bucket = r['s3']['bucket']['name']
        key = r['s3']['object']['key']
        log("found %s in bucket %s" % (key, bucket))

def process_all_messages():
    for msg in queue.receive_messages():
        try:
            process_message(msg)
            log("Message processed, will delete")
            msg.delete()
        except Exception as e:
            log("error on delete:")
            log(e)

if __name__ == '__main__':
    while True:
        process_all_messages()
        time.sleep(10)