class TaskState(object):
	"""docstring for TaskState"""
	st_index = None
	end_index = None
	state = None

	# job states - 0 - created, 1 - running, 2 - finished, -1 - failed

	def __init__(self,st_index,end_index):
		self.st_index = st_index
		self.end_index = end_index
		self.is_running = 0

	def set_task_running(self):
		self.state = 1

	def set_task_finished(self):
		self.state = 2

	def set_task_failed(self):
		self.state = -1