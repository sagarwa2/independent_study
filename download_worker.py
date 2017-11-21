import boto3
import botocore
import sys
import os

BUCKET_NAME = None
START_INDEX = None
END_INDEX = None
PATH = None

def download():
	s3 = boto3.resource('s3')
	current_bucket = s3.Bucket(BUCKET_NAME)
	all_images = current_bucket.objects.all()
	num_images = sum(1 for _ in all_images)
	all_images = current_bucket.objects.all()
	st = 0
	for obj in all_images:
		if st >= START_INDEX and st <= END_INDEX:
			# download file
			path_to_download = os.path.join(PATH, obj.key)
			s3.Bucket(BUCKET_NAME).download_file(obj.key, path_to_download)
			
if __name__ == '__main__':
	arguments = sys.argv
	# 1st argument is bucket name
	# 2nd argument is start range
	# 3rd argument is end range
	# 4th argument in path
	BUCKET_NAME = sys.argv[1]
	START_INDEX = sys.argv[2]
	END_INDEX = sys.argv[3]
	PATH = sys.argv[4]
