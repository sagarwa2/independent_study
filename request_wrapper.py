import boto3
from task_state import TaskState

class JOB(object):
	
	"""docstring for RequestWrapper"""
	
	bucket_url  = None
	num_workers = None
	ami_number = None
	instance_type = None
	mapping_dictionary = None
	list_of_instances = None
	id = None
	status = None

	# status - 0 - created, 1 - running, 2 - finished, -1 - aborted

	def __init__(self,job_id, bucket,ami,num_workers,instance_type):
		self.id = job_id
		self.mapping_dictionary = {}
		self.bucket_url = bucket
		self.ami_number = ami
		self.num_workers = num_workers
		self.instance_type = instance_type
		self.status = 0
	
	def assign_tasks(self):
		# keep the state of each machine working
		s3 = boto3.resource('s3')
		current_bucket = s3.Bucket(self.bucket_url)
		# request s3 to get the number of images
		all_images = current_bucket.objects.all()
		num_images = sum(1 for _ in all_images)
		# divide among the instances
		st_idx = 0
		instance_idx = 0
		work_each_worker = num_images / num_workers
		extra_work = num_images % num_workers
		while st_idx < num_images and instance_idx < self.num_workers:
			
			end_range = st_idx + work_each_worker
			if instance_idx == (num_workers - 1):
				end_range = end_range + extra_work
			# assign in the dictionary
			print st_idx,instance_idx,end_range
			new_task = TaskState(st_idx,end_range)
			self.mapping_dictionary[self.list_of_instances[instance_idx]] = new_task

			# update meta data
			st_idx += end_range
			instance_idx += 1

		print self.mapping_dictionary

	def run_num_workers(self):
		client = boto3.client('ec2')
		ec2 = boto3.resource('ec2')
		instance_ids = ec2.create_instances(
			ImageId = self.ami_number,
			InstanceType = self.instance_type,
			MinCount = self.num_workers,
			TagSpecifications=[
				{
					'ResourceType':'instance',
					'Tags':[
						{
							'Key': 'job',
							'Value': self.id
						}
					]
				}
			]
		)
		self.list_of_instances = instance_ids
		self.assign_tasks()
		# wait for the machine to run