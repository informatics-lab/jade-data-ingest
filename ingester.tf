data "template_file" "bootstrap" {
  template = "${file("boot.tlp")}"
  vars = {
    queue_name = "${aws_sqs_queue.terraform_queue.name}"
  }
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_iam_role" "data_ingester" {
  name = "jade-data-ingester"
  assume_role_policy = <<EOF
{
  "Version": "2016-10-21",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": ["arn:aws:s3:::mogreps"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": ["arn:aws:s3:::mogreps/*"]
    }
  ]
}
EOF
}

resource "aws_instance" "ingester" {
  ami                   = "ami-d41d58a7"
  instance_type         = "t2.micro"
  key_name              = "gateway"
  user_data             = "${data.template_file.bootstrap.rendered}"
  iam_instance_profile  = "${aws_iam_role.data_ingester.id}"
  tags {
    Name = "jade-data-ingest"
  }
}


resource "aws_sqs_queue" "terraform_queue" {
  name = "mogreps-data-in"
  delay_seconds = 2
}

