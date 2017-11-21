#!/bin/bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
DOWNLOAD_DIRECTORY="/home/ubuntu/downloads"
# GET INSTANCE ID
INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
# GET RESPONSE
RESPONSE_VAL=curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/get_task
ST_RANGE=echo RESPONSE_VAL | jq '.st_range'
END_RANGE=echo RESPONSE_VAL | jq '.end_range'
BUCKET_NAME=echo RESPONSE_VAL | jq '.bucket'
# DOWNLOAD FILES
python /home/ubuntu/independent_study/download_worker $BUCKET_NAME $ST_RANGE $END_RANGE $DOWNLOAD_DIRECTORY

# FILES DOWNLOADED, USE YOUR OWN SCRIPT NOW