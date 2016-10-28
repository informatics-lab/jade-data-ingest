# jade-data-ingest

Watches a queue for new data.
Interrogates the new data to get metadata and sends that to an elastic search instance.
No error handling in scripts, rather docker manages container restart and redrive policy prevents processing same message more than 4 times.
Currently points at test bucket "jade-ingest-test-theo"

To run locally:
```
docker run -d \
-e AWSSECRETACCESSKEY=$AWSSECRETACCESSKEY \
-e AWSACCESSKEYID=$AWSACCESSKEYID \
-e AWS_SECRET_ACCESS_KEY=$AWSSECRETACCESSKEY \
-e AWS_ACCESS_KEY_ID=$AWSACCESSKEYID \
-e QUEUE_NAME='mogreps-data-in' \
jade-data-ingest
```

Add terraform remote:

```
terraform remote config -backend=s3 -backend-config="bucket=informatics-jade-terraform" -backend-config="key=jade-data-ingest/devel/terraform.tfstate" -backend-config="region=eu-west-1"
```
