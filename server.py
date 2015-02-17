#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from node import Node
import mashery_api
import utils
from config import mashery_cloud_config

# Example data table
serverExampleDataItems = {
	"vlv_test_string": { "id": None, "val": None },	# test data
}

def serverSetup(data_table = None):
	if not data_table:
		assert(False)

	asset = mashery_api.Asset(mashery_cloud_config)
	r = asset.findOne(mashery_cloud_config["asset"], mashery_cloud_config["model"])
	if not r:
		print("Not found the server %s (model: %s)" % (mashery_cloud_config["asset"], mashery_cloud_config["model"]))
		return False

	server_asset_id = r['systemId']
	#print("server asset id = %s" % server_asset_id)
	#print("server model id = %s" % r["model"]["systemId"])

	dataitem = mashery_api.DataItem(mashery_cloud_config)
	r = dataitem.findCurrentValues({ "assetId": server_asset_id	})

	# This stub variable must have.
	if not "vlv_stub" in data_table.keys():
		data_table["vlv_stub"] = { "id": None, "val": None }

	node = Node(mashery_cloud_config)
	# Find if the server variables were created.
	for dataItemValue in r["dataItemValues"]:
		dataItem = dataItemValue["dataItem"]
		#print("[%s] Data \"%s\" = %s, type %s" % (dataItem["systemId"], dataItem["name"], dataItemValue["value"], dataItem["type"]))
		if not dataItem["name"] in data_table.keys():
			continue
		d = data_table[dataItem["name"]]
		d["id"] = int(dataItem["systemId"])
		# Override the existing value store in cloud
		if d.get("attr") == "update" and d["val"] != dataItemValue["value"]:
			node.setData(node.dataId(dataItem["name"]), d["val"])
		else:
			d["val"] = dataItemValue["value"]

	# Create the server variables if necessary.
	# FIXME:
	# 1. use bulk create.
	# 2. use create to get id anyway even existing one.
	for k in data_table.keys():
		# Skip the existing variables.
		if data_table[k]["id"]:
			continue

		r = dataitem.create(name = k, model_name = mashery_cloud_config["model"], type = "STRING")
		if not r:
			print("Unable to create variable ", k, "due to ", r["failures"])
			assert(False)

		if r["successful"]:
			data_table[k]["id"] = int(r["succeeded"][0]["id"])

		r = utils.setData(node.dataId(k), data_table[k]["val"])
		if not r:
			print("Unable to set variable %s" % k)
			assert(False)

		#print json.loads(r)

if __name__=="__main__":
	# Before accessing the data items by both server and client, make sure they
	# were created. Define a data table here and setup them.
	dataItems = {
		# @<name> (string): Server variable name
		# @id (integer): The internal identifier. Don't touch it.
		# @attr (string): Attribute for a data item.
		# - update: Even the data item has been created, use the pre-defined value
		#	here to override the current value stored in cloud.
		# - None: Get the value stored in cloud.
		"vlv_server_test_data": { "id": None, "val": "test1", "attr": "update" },
		"vlv_server_test_data2": { "id": None, "val": "89", "attr": "update" },
		"vlv_server_test_data3": { "id": None, "val": "43" },
	}
	serverSetup(dataItems)

	# Check if the data items are created as expected.
	for k, v in dataItems.items():
		print("Data item %s: id %d, value %s, attr %s" % (k, v["id"], v["val"], v.get("attr")))
