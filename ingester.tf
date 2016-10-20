provider "aws" {
  region = "eu-west-1"
}

resource "aws_instance" "ingester" {
  ami                   = "ami-d41d58a7"
  instance_type         = "t2.micro"
  key_name              = "gateway"
  user_data             = "${data.template_file.bootstrap.rendered}"
  tags {
    Name = "jade-data-ingest"
  }
}

data "template_file" "bootstrap" {
  template = "${file("ingester.tf")}"
  vars = {
    ip = "0.0.0.0"
  }
}
