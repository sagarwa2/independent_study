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
	print BUCKET_NAME,START_INDEX,END_INDEX,PATH
	current_bucket = s3.Bucket(BUCKET_NAME)
	all_images = current_bucket.objects.all()
	num_images = sum(1 for _ in all_images)
	all_images = current_bucket.objects.all()
	st = 0
	for obj in all_images:
		if st >= START_INDEX and st <= END_INDEX:
			# download file
			path_to_download = os.path.join(PATH, obj.key)
			print obj.key,path_to_download
			s3.Bucket(BUCKET_NAME).download_file(obj.key, path_to_download)
		st+=1			
if __name__ == '__main__':
	arguments = sys.argv
	print arguments
	# 1st argument is bucket name
	# 2nd argument is start range
	# 3rd argument is end range
	# 4th argument in path
	BUCKET_NAME = sys.argv[1]
	if BUCKET_NAME[0]=='"':
		BUCKET_NAME = BUCKET_NAME[1:]
	if BUCKET_NAME[len(BUCKET_NAME)-1]=='"':
		BUCKET_NAME = BUCKET_NAME[0:len(BUCKET_NAME)-1]
	START_INDEX = int(sys.argv[2])
	END_INDEX = int(sys.argv[3])
	PATH = sys.argv[4]
	download()
