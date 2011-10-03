import base64

class message:
	msg_string = ""
	def __init__(self, msg_string):
		self.msg_string = base64.urlsafe_b64decode(msg_string) 
	def set(self, msg_string):
		self.msg_string = msg_string
	def get(self):
		return base64.urlsafe_b64encode(self.msg_string)
	def get_text(self):
		return self.msg_string

