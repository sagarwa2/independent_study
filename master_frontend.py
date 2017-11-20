
from flask import Flask, render_template, request, url_for
import boto3
from random import randint
from request_wrapper import JOB

app = Flask(__name__)

current_running_requests = {}

@app.route('/')
def submit_job_to_scheduler():
	# TODO: run background master request
    return render_template('index.html')

@app.route('/submit_job',methods=['POST'])
def get_job_request():
	s3_url = request.form['source_bucket']
	num_workers = request.form['num_workers']
	ami_number = request.form['ami_number']
	instance_type = request.form['ami_number']
	if not instance_type:
		instance_type = "t2.micro"
	
	print s3_url,num_workers,ami_number,instance_type
	# generate a job-id
	job_id = get_unique_request_id()

	# create a request object
	new_req_obj = JOB(job_id,s3_url,ami_number,num_workers,instance_type)
	new_req_obj.run_num_workers()

@app.route('/update_job_status',methods=['POST'])
def update_job_status():
	job_id = request.form['job_id']
	instance_id = request.form['instance_id']
	# change status of job to running on first call

@app.route('/get_task',methods=['POST'])
def get_task():
	instance_id = request.form['instance_id']
	associated_job_id = get_job_id_from_instance_id(instance_id)
	print instance_id,associated_job_id

def get_unique_request_id():
	req_id = randint(0,9223372036854775806)
	while req_id in current_running_requests:
		req_id = randint(0,9223372036854775806)
	return req_id

def get_job_id_from_instance_id(instance_id):
	ec2 = boto3.resource('ec2')
	ec2instance = ec2.Instance(instance_id)
	job_id = None
    for tags in ec2instance.tags:
    	if tags['Key'] == "job":
    		job_id = tags['Value']
    		break
    return job_id