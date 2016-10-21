# jade-data-ingest

Watches a queue for new data.
Interrogates the new data to get metadata and sends that to an elastic search instance.

```


docker run -d \
-e AWSSECRETACCESSKEY=$AWSSECRETACCESSKEY \
-e AWSACCESSKEYID=$AWSACCESSKEYID \
-e AWS_SECRET_ACCESS_KEY=$AWSSECRETACCESSKEY \
-e AWS_ACCESS_KEY_ID=$AWSACCESSKEYID \
-e QUEUE_NAME='mogreps-data-in' \
jade-data-ingest
```

