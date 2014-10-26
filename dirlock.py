import os, time
# Implements locking using os.mkdir, which is atomic on POSIX systems.
# Example usage:
# lock = DirLock("foo") # Tries to make a directory named "foo"
# with lock:
#  ...
#
class DirLock:
	def __init__(self, path):
		self.path = path
	def __enter__(self):
		while True:
			try:
				os.mkdir(self.path)
				break
			except OSError, e:
				if e.errno == 17: # File exists -- we're already locked
					time.sleep(1) # Try again later.
				else:
					raise e
	def __exit__(self, exc_type, exc_value, trace):
		os.rmdir(self.path)
