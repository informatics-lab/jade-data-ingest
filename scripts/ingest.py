import boto3
import os
import json
import time
import tempfile
import metadata_to_elastic_search
import uuid
import requests

sqs = boto3.resource('sqs', region_name='eu-west-1')
s3 = boto3.resource('s3', region_name='eu-west-1')
queue = sqs.get_queue_by_name(QueueName=os.environ['QUEUE_NAME'])
search_url = 'http://elasticsearch.informaticslab.co.uk'
index = 'metoffice'


def log(msg):
    print(msg)

def set_up_index_or_nothing():
    """Check if we have the met office index and create it if not"""
    r = requests.get('{url}/{index}'.format(url=search_url, index=index))
    if 'error' in r.json(): # Assume this means the index isn't set up.
        data = {
            "mappings": {
                "mogreps": {
                    "properties": {
                        "model_run": { "type": "date", "format": "epoch_second" },
                        "validity_time": { "type": "date", "format": "epoch_second" }}}}}
        r = requests.put('{url}/{index}'.format(url=search_url, index=index), data=data)
        assert r.json()['acknowledged'] == True
        print("Created index {}".format(index))

def save_meta_to_search(metadata):
    response = requests.put(
        '{url}/{index}/mogreps/{uid}'.format(url=search_url, index=index, uid=str(uuid.uuid1())),
        data=json.dumps(metadata)
    )
    if not 'created' in  response.json() and response.json()['created']:
        raise Exception("Failied to upload metadata. Responce was:\n{}\nmetadata was:\n{}".format(
            response.json(), metadata))

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
        metadata_to_elastic_search.process_file(filepath, bucket, key)
        os.remove(filepath)

def process_all_messages():
    for msg in queue.receive_messages():
        process_message(msg)
        log("Message processed, will delete")
        msg.delete()

if __name__ == '__main__':
    set_up_index_or_nothing()
    while True:
        process_all_messages()
        time.sleep(10)