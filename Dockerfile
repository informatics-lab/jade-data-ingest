FROM quay.io/informaticslab/conda

WORKDIR /root

# Python 3 + tools
RUN conda install -y boto3
RUN conda install -y -c scitools iris

ADD ingest.py /root/ingest.py

CMD python /root/ingest.py