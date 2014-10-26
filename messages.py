from dirlock import DirLock
import pickle

class MessageList:
	# A message list is basically an ordered dictionary 
	def __init__(self):
		self.messagedict = dict() # Maps names to messages
		self.messageorder = []
	def set(self, name, msg):
		assert set(self.messageorder) == set(self.messagedict.keys())
		if name in self.messagedict.keys()
			self.messagedict[name] = msg
		else:
			self.messagedict[name] = msg
			self.messageorder += [name]
	def get(self, name):
		return self.messagedict[name]

	def remove(self, name):
		assert set(self.messageorder) == set(self.messagedict.keys())
		del self.messagedict[name]
		self.messagelist.remove(name)

	def __iter__(self):
		return ((name, self.messagedict[name]) for name in self.messageorder)

