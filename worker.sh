#!/bin/bash
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
DOWNLOAD_DIRECTORY="/home/ubuntu/downloads"
# GET INSTANCE ID
INSTANCE_ID=$(curl http://169.254.169.254/latest/meta-data/instance-id)
# GET RESPONSE
ST_RANGE=$(curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/get_task |jq '.st_range')
END_RANGE=$(curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/get_task |jq '.end_range')
BUCKET_NAME=$(curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/get_task |jq '.bucket')
# DOWNLOAD FILES
python /home/ubuntu/independent_study/download_worker.py $BUCKET_NAME $ST_RANGE $END_RANGE $DOWNLOAD_DIRECTORY

# FILES DOWNLOADED, USE YOUR OWN SCRIPT NOW

# set task to end
curl -d "instance_id=$INSTANCE_ID" -X POST http://54.147.64.78:8080/end_task