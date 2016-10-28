data "template_file" "bootstrap" {
  template = "${file("boot.tlp")}"
  vars = {
    queue_name = "${aws_sqs_queue.to_ingest_queue.name}"
  }
}

variable "queue_name" {
  default = "mogreps-data-in"
}

resource "aws_instance" "ingester" {
  ami                   = "ami-d41d58a7"
  instance_type         = "t2.micro"
  key_name              = "gateway"
  user_data             = "${data.template_file.bootstrap.rendered}"
  iam_instance_profile  = "jade-data-ingest"
  tags {
    Name = "jade-data-ingest"
  }
}


resource "aws_sqs_queue" "to_ingest_queue" {
  name = "${var.queue_name}"
  delay_seconds = 2
  redrive_policy = "{\"deadLetterTargetArn\":\"${aws_sqs_queue.dlq.arn}\",\"maxReceiveCount\":5}"
  policy = <<POLICY
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "sqs:SendMessage"
            ],
            "Condition": {
                "ArnEquals": {
                    "aws:SourceArn": "${aws_s3_bucket.bucket.arn}"
                }
            },
            "Resource": [
                "arn:aws:sqs:*:*:${var.queue_name}"
            ]
        }
    ]
}
POLICY
}

resource "aws_sqs_queue" "dlq" {
  name = "DLQ-${var.queue_name}"
}

resource "aws_s3_bucket" "bucket" {
  bucket = "jade-ingest-test-theo"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "${aws_s3_bucket.bucket.id}"
  queue {
    queue_arn = "${aws_sqs_queue.to_ingest_queue.arn}"
    events = ["s3:ObjectCreated:*"]
  }
}

