# -*- coding: utf-8 -*-

from mashery_api import *
from axeda_api import *

class Node():
	"""
	A node indicates a machine or whatever connected to cloud.
	Its role may be client, server or whatever.
	"""
	def __init__(self, name, config):
		if not name:
			assert(False)

		if not config:
			assert(False)

		self.config = config
		if name == "Mashery":
			self.cloud = Mashery(config)
		elif name == "Axeda":
			self.cloud = Axeda(config)
			pass
		else:
			print("cloud is not configured")
			assert(False)

	def dataId(self, name):
		return name

	def setData(self, id, value):
		scripto = self.cloud.scripto()
		r = scripto.execute('vlvFastSetPlatformData', data = {
			"dataItemName": id,
			"dataItemValue": str(value)
		})

		if r:
			return json.loads(r).get("msg") == "success"
		else:
			return False

	def getData(self, id):
		scripto = self.cloud.scripto()
		r = scripto.execute('vlvFastGetPlatformData', data = {
			"dataItemName": id,
		})

		if r:
			r = json.loads(r)
			if r.get("msg") == "success":
				return r.get("val")

		return None
