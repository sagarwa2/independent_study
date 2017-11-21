
from flask import Flask, render_template, request, url_for,jsonify
import boto3
from random import randint
from request_wrapper import JOB

app = Flask(__name__)

current_running_requests = {
}
finished_jobs = []

@app.route('/')
def submit_job_to_scheduler():
	# TODO: run background master request
    return render_template('index.html')

@app.route('/submit_job',methods=['POST'])
def get_job_request():
	s3_url = request.form['source_bucket']
	num_workers = request.form['num_workers']
	ami_number = request.form['ami_number']
	instance_type = request.form['instance_type']
	if not instance_type:
		instance_type = "t2.micro"
	
	print s3_url,num_workers,ami_number,instance_type
	# generate a job-id
	job_id = get_unique_request_id()

	# create a request object
	new_req_obj = JOB(job_id,s3_url,ami_number,num_workers,instance_type)
	
	# add to map
	current_running_requests[job_id] = new_req_obj

	# run workers
	new_req_obj.run_num_workers()

@app.route('/end_task',methods=['POST'])
def end_task():
	instance_id = request.form['instance_id']
	# change status of job to running on first call
	associated_job_id = get_job_id_from_instance_id(instance_id)
	req_obj = current_running_requests[associated_job_id]
	req_task = req_obj.mapping_dictionary[instance_id]
	req_task.set_task_finished()

	# check each job finished
	if req_obj.check_job_finished():
		req_obj.set_job_finished()
		finished_jobs.append(associated_job_id)
	return jsonify({"status":200})

@app.route('/get_task',methods=['POST'])
def get_task():
	instance_id = request.form['instance_id']
	associated_job_id = get_job_id_from_instance_id(instance_id)
	req_obj = current_running_requests[associated_job_id]
	bucket_name = req_obj.bucket_name
	req_task = req_obj.mapping_dictionary[instance_id]
	
	# set it to running
	req_task.set_task_running()

	# set job running
	req_obj.set_job_running()
 	return jsonify({"st_range":req_task.st_index,"end_range":req_task.end_index,"bucket":bucket_name})

def get_unique_request_id():
	req_id = randint(0,9223372036854775806)
	while req_id in current_running_requests:
		req_id = randint(0,9223372036854775806)
	return str(req_id)

def get_job_id_from_instance_id(instance_id):
	print instance_id
	ec2 = boto3.resource('ec2')
	ec2instance = ec2.Instance(instance_id)
	job_id = None
	for tags in ec2instance.tags:
		if tags['Key'] == "job":
			job_id = tags['Value']
			break
	return job_id
