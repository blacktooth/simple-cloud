import sqlite3, time, random, sys, base64, json, string, settings

class auth:
	def check(self, username, password):
		try:
			userid = settings.db.select('auth', what = 'id', where = "username=$username AND password=$password", vars=locals())
			if bool(userid.list()):
				return True
			else:
				return False	
		except:
			print sys.exc_info()
	def add(self, username, password):
		try:
			settings.db.insert('auth', username = username, password = md5.new(password).hexdigest());
			return True
		except:
			return False

class device:
	__device_info = {
	'device_string':None,
	'device_exists':None,
	'registered_ip':None,
	'registered_time':None,
	'_type':None,
	'userid':None
	}
	def __init__(self):
		self.__device_info['device_exists'] = False
	def __init__(self, device_string):
		try:
			device_info = settings.db.select('devices', where = "device_string=$device_string", vars = {'device_string':device_string})
			if bool(device_info.list()):
				for row in device_info.list():
					self.__device_info.update(row)
				self.__device_info['device_exists'] = True
			else:
				self.__device_info['device_exists'] = False
		except:
			print sys.exc_info()
	def is_known(self):
		if self.__device_info['device_exists']:
			return True
		else: 
			return False
	def __add(self):
		if not self.__device_info['device_exists']:
			try:
				settings.db.insert('devices', device_string = self.__device_info['device_string'], userid = self.__device_info['userid'], _type = self.__device_info['_type'], registered_ip = self.__device_info['registered_ip'], registered_time = self.__device_info['registered_time']);
				self.__device_info['device_exists'] = True
			except:
				print sys.exc_info()
	def __generate_string(self):
		device_string = ""
		for i in range(0, 32):
			device_string += random.choice(list(string.hexdigits))
		if not device(device_string).is_known():
			return device_string
		else:
			self.__generate_string()
	def register(self, meta):
		self.__device_info.update(meta)
		self.__device_info['device_string'] = self.__generate_string()
		self.__device_info['registered_time'] = time.time()
		self.__add()
	def type(self):
		return __device_info['_type']
	def device_string(self):
		return __device_info['device_string']
	def user(self):
		return __device_info['userid']
	def registered_ip(self):
		return __device_info['registered_ip']
	def registered_time(self):
		return __device_info['registered_time']

class request:
	__request_data = {
	'id': None,
	'content' : None,
	'device_string' : None,
	'origin_ip' : None,
	'sent_time' : None,
	'queued_time' : None,
	'priority' : None,
	'delivered' : None,
	'is_valid' : None
	}
	def __init__(self, request_data):
		#Decode the base64 encoded request and convert the obtained JSON string to Dict
		try:
			self.__request_data.update(json.loads(base64.urlsafe_b64decode(request_data)))
			self.__request_data['is_valid'] = self.__check_content() and self.__check_device_string() and self.__check_sent_time() and self.__check_priority()
		except TypeError:
			print 'Invalid request!'
			print sys.exc_info()
			self.__invalidate()
		except:
			print sys.exc_info()
			self.__invalidate()
	def __add(self):
		if self.__request_data['is_valid']:
			try:
				self.__request_data['id'] = settings.db.insert('messages', id = settings.web.db.SQLLiteral('NULL'), content = self.__request_data['content'], device_string = self.__request_data['device_string'], origin_ip = self.__request_data['origin_ip'], sent_time = self.__request_data['sent_time'], queued_time = self.__request_data['queued_time'], priority = self.__request_data['priority'], delivered = self.__request_data['delivered'])
			except:
				print sys.exc_info()
	def __invalidate(self):
		self.__request_data['is_valid'] = False
	##Need More checks here
	def __check_content(self):
		if len(self.__request_data['content']) > settings.MESSAGE_LEN:
			return False
		else:
			return True
	#Critical function
	def __check_device_string(self):
		dev = device(self.__request_data['device_string'])
		if dev.is_known():
			return True
		else:
			return False
	##Check for valid timestamp
	def __check_sent_time(self):
		if self.__request_data['sent_time'] is None:
			return False
		else:
			return True
	def __check_priority(self):
		try:
			if int(self.__request_data['priority']) not in range(0, 6):
				return False
			else:
				return True
		except:
			return False
	def __status(self):
		try:	
			results = settings.db.select('messages', what = 'delivered', where = 'id=$id', vars = self.__request_data)
			self.__request_data['delivered'] = results.list()[0]['delivered']
		except:
			print sys.exc_info()

	def queue(self):
		self.__request_data['origin_ip'] = settings.web.ctx['ip']
		self.__request_data['delivered'] = 0
		self.__request_data['queued_time'] = time.time()
		self.__add()
	def is_valid(self):
		if self.__request_data['is_valid']:
			return True
		else:
			return False
	def status(self):
		self.__status()
		return self.__request_data['delivered']
