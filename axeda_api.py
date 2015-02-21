# -*- coding: utf-8 -*-

import json
from xml.etree import ElementTree
import utils
from cloud import Cloud

class TypeabstractPlatformObjectBase(dict):
	def __init__(self, c):
		dict.__init__(self, c)

class TypeAbstractPlatformObject(TypeabstractPlatformObjectBase):
	"""
	Format: attributes
	@id: string
	@systemId: string
	@label: string
	@detail: string
	@restUrl: string
	"""
	def __init__(self, id, systemId, label, detail, restUrl):
		TypeabstractPlatformObjectBase.__init__(self, [
			("id", id),
			("systemId", systemId),
			("label", label),
			("detail", detail),
			("restUrl", restUrl)
		])

	def toJson(self):
		return json.dumps(self)

	def toXml(self):
		pass

class TypeDataItemReference(TypeAbstractPlatformObject):
	def __init__(self, id, systemId, label, detail, restUrl):
		TypeAbstractPlatformObject.__init__(self, id, systemId, label, detail, restUrl)

class TypeDataItemCollection(TypeabstractPlatformObjectBase):
	"""
	Format:
	@dataItem: list of DataItemReference
	"""
	def __init__(self, dataItemRefernences):
		for i in dataItemRefernences:
			TypeAbstractPlatformObject(i)
		dict.__init__(self, list(dataItemRefernences))

class ExecutionResult(dict):
	pass

class AssetCriteria(dict):
	"""
	Format:
	@gatewayId: string
	@name: string
	@modelNumber: string
	@serialNumber: string
	@organizationName: string
	@locationName: string
	@regionName: string
	@assetGroupName: string
	@systemName: string
	@gatewayName: string
	@gatewayOnly: boolean
	@backupAgentsOnly: boolean
	@packageName: string
	@packageVersion: string
	@withoutPackage: boolean
	@muted: boolean
	@conditionId: string
	@toLastContactDate: dateTime
	@fromLastContactDate: dateTime
	@toRegistrationDate: dateTime
	@fromRegistrationDate: dateTime
	@dataItem: DataItemValueCriteria
	@hasEventsSince: dateTime
	@geofence: GeofenceCriteria
	@showAssetsWithAlarms: boolean
	@propertyName: string
	@item: string list
	"""
	def __init__(self, criteria):
		dict.__init__(self, criteria)

class Criteria(dict):
	"""
	Format:
	@name: string
	@alias: string
	@modelId: int
	Model system id.
	@types: list
	@readOnly: bool
	@visible: bool
	@forwarded: bool
	@historicalOnly: null
	@pageSize: null
	@pageNumber: int
	Using the pageNumber pagination property affects which found object
	is returned by the findOne method. For example, pageNumber=1 returns the
	first matching found object, while pageNumber=3 returns the 3rd matching
	found object, etc.
	@sortAscending: bool
	@sortPropertyName: string
	e.g, "name"
	"""
	def __init__(self, criteria):
		dict.__init__(self, criteria)

class HistoricalDataItemValueCriteria(dict):
	"""
	Format: <xs:extension base="tns:AbstractSearchCriteria">
	@assetId: string
	@dataItemIds: list
	@  item: string
	@startDate: dateTime
	@endDate: dateTime
	"""
	def __init__(self, criteria):
		dict.__init__(self, criteria)

class CurrentDataItemValueCriteria(dict):
	"""
	Format:
	@name: string
	@alias: string
	@assetId: string
	Asset system id.
	@types: list
	@readOnly: boolean
	@visible: boolean
	@forwarded: boolean
	@historicalOnly: boolean
	@pageSize: int
	@pageNumber: int
	Using the pageNumber pagination property affects which found object
	is returned by the findOne method. For example, pageNumber=1 returns the
	first matching found object, while pageNumber=3 returns the 3rd matching
	found object, etc.
	@sortAscending: bool
	@sortPropertyName: string
	e.g, "name"
	"""
	def __init__(self, criteria):
		dict.__init__(self, criteria)

class Axeda(Cloud):
	"""
	Axeda platform REST APIs
	https://<host>/artisan/apidocs/v1/
	https://<host>/artisan/apidocs/v2/
	"""
	def __init__(self, config):
		Cloud.__init__(self, "Axeda", config)

		if self.get('name') == None:
			assert(False)

		if self.get('username') == None:
			assert(False)

		if self.get('password') == None:
			assert(False)

		if not self.get("asset"):
			assert(False)

		if not self.get("model"):
			assert(False)

		self.config = config

		self.username = self.get('username')
		self.password = self.get('password')
		self.timeout = self.get('timeout')
		self.session_id = None

		if self.get('ssl') != None:
			self.ssl = self.get('ssl')
		else:
			self.ssl = None

		# Use json or xml?
		if self.get('json') == None:
			self.json = True
		else:
			self.json = self.get('json')

		if self.ssl == True:
			self.v1_url_prefix = 'https'
			self.v2_url_prefix = 'https'
		else:
			self.v1_url_prefix = 'http'
			self.v2_url_prefix = 'http'
		self.v1_url_prefix += '://' + config['name'] + '/services/v1/rest/'
		self.v2_url_prefix += '://' + config['name'] + '/services/v2/rest/'

		if not self.json:
			self.name_space = 'http://type.v1.webservices.sl.axeda.com'
			ElementTree.register_namespace('', self.name_space)
			#ElementTree.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
		else:
			self.name_space = None

	def checkParameter(self, opts):
		for o in opts:
			if not o:
				assert(False)

	def setURL(self, api):
		url = self.url_prefix + api

		if False:
			if self.session_id:
				url += '?sessionid=' + self.session_id
			else:
				url += '?username=' + self.username + '&password=' + self.password

		return url

	def setHeaders(self, json = None):
		# Always return json response
		headers = { "Accept": "application/json" }
		if json == True or (json == None and self.json):
			headers["Content-Type"] = "application/json"
		else:
			headers["Content-Type"] = "application/xml"
		# By default, return xml response or plain text by certain scripto

		if self.session_id:
			headers["x_axeda_wss_sessionid"] = self.session_id
		else:
			headers["x_axeda_wss_username"] = self.username
			headers["x_axeda_wss_password"] = self.password

		return headers

	def auth(self):
		return Auth(self.config)

	def scripto(self):
		return Scripto(self.config)

class Auth(Axeda):
	"""
	API
	https://<host>/services/v1/rest/Auth?_wadl
	"""
	def __init__(self, config):
		Axeda.__init__(self, config, False)
		self.url_prefix = self.v1_url_prefix + 'Auth/'

	def login(self, username = None, password = None, timeout = 1800):
		"""
		Creates a new session (sessionId) for the related authenticated user.

		Note that when Axeda Platform creates a session for a user, a timeout is
		defined for that session. The session will be valid only while the session
		is effective; if the session times out, additional calls to the Web services
		will return “access defined” errors. Your code should implement error
		handling to ensure the session is still valid.
		"""
		if not username:
			username = self.username

		if not password:
			password = self.password

		if not timeout:
			timeout = self.timeout

		url = self.url_prefix + 'login?principal.username=' + username + \
			'&password=' + password + '&sessionTimeout=' + str(timeout)

		if self.json:
			headers = { 'Accept': 'application/json' }
		else:
			headers = None

		r = utils.get(url, headers = headers, ssl = self.ssl)
		if r.status_code != 200:
			return False

		if self.json:
			self.session_id = str(json.loads(r.content)['wsSessionInfo']['sessionId'])
		else:
			self.session_id = str(utils.parse_xml(r.content, 'sessionId', self.name_space))

		if self.session_id:
			return True
		else:
			return False

	def logout(self, sessionid = None):
		"""
		Ends the session for the related user. Invalidates the specified SessionId
		such that it can no	longer be used.
		"""
		if not self.session_id and not sessionid:
			return False

		url = self.url_prefix + 'logout?sessionid='
		if sessionid:
			url += sessionid
		else:
			url += self.session_id

		r = utils.get(url, ssl = self.ssl)
		if r.status_code != 204:
			return False
		else:
			self.session_id = None
			return True

class Scripto(Axeda):
	"""
	API
	https://<host>/services/v1/rest/Scripto/?_wadl
	"""
	def __init__(self, config, sessionid = None):
		Axeda.__init__(self, config)
		self.url_prefix = self.v1_url_prefix + 'Scripto/'
		self.session_id = sessionid

	def execute(self, app, data = None):
		self.checkParameter((app,))

		url = self.setURL('execute/' + app)

		headers = self.setHeaders(json = False)

		r = self.getRequest(url, headers, data)
		if r.status_code == 200:
			return r.content
		else:
			return None
