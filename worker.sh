#!/bin/bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8

INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/get_task
