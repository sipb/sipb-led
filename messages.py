from dirlock import DirLock
#import ledsign.newline, ledsign.EOM
import pickle

def initialize(filename="/var/tmp/led-messages"):
	""" Sets up a new file with a messagelist in it.
	"""
	m = MessageList()
	with DirLock("/tmp/messages.lock"):
		with open(filename, 'w') as f:
			pickle.dump(m,f)

def setmsg(name, msg, filename="/var/tmp/led-messages"):
	""" Sets the message named name to msg.
	"""
	with DirLock("/tmp/messages.lock"):
		with open(filename, 'r') as f:
			m = pickle.load(f)
		m.set(name,msg)
		updatesign(m)
		with open(filename, 'w') as f:
			pickle.dump(m,f)

def remove(name, filename="/var/tmp/led-messages"):
	""" Remove the message named name.
	"""
	with DirLock("/tmp/messages.lock"):
		with open(filename, 'r') as f:
			m = pickle.load(f)
		m.remove(name)
		updatesign(m)
		with open(filename, 'w') as f:
			pickle.dump(m,f)

def list(filename="/var/tmp/led-messages"):
	with DirLock("/tmp/messages.lock"):
		with open(filename, 'r') as f:
			m = pickle.load(f)
			for (name, msg) in m:
				print(name + ": " + msg)

def updatesign(msglist):
	print "Updating sign to..."
	print "\\rH".join(msg for (name,msg) in msglist) + "\\r\\r\\r" 
	try:
		import socket
		sock = socket.create_connection(("localhost",41337))
		sock.send("\\rH".join(msg for (name,msg) in msglist) + "\\r\\r\\r")
	finally:
		sock.close()

class MessageList:
	# A message list is basically an ordered dictionary 
	def __init__(self):
		self.messagedict = dict() # Maps names to messages
		self.messageorder = []
	def set(self, name, msg):
		assert set(self.messageorder) == set(self.messagedict.keys())
		if name in self.messagedict.keys():
			self.messagedict[name] = msg
		else:
			self.messagedict[name] = msg
			self.messageorder += [name]
	def get(self, name):
		return self.messagedict[name]

	def remove(self, name):
		assert set(self.messageorder) == set(self.messagedict.keys())
		del self.messagedict[name]
		self.messageorder.remove(name)

	def __iter__(self):
		return ((name, self.messagedict[name]) for name in self.messageorder)

