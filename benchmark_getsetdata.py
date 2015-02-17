#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
Here is an example showing how to use data get/set functions:

boolen node.getData(string name)
string node.setData(string name, string value)
"""

import time
from node import Node
from config import mashery_cloud_config

data_name = "vlv_benchmark"
test_count = 50
test_payload_lens = (8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096)

node = Node(mashery_cloud_config)
data_id = node.dataId(data_name)

# Benchmark tests
for i in test_payload_lens:
	data_val = "valvrave" * (i / 8)

	print("Data set benchmark ...")
	start_time = time.time()
	for i in range(test_count):
		if not node.setData(data_id, data_val):
			print("Fail to set data %s = %s" % (data_name, data_val))
			break
		else:
			print("Data set %d/%d\r" % (i + 1, test_count)),
	end_time = time.time()
	if i + 1 == test_count:
		print("\nAverage data set time %fs consumed for %d bytes)" % ((end_time - start_time) / test_count, len(data_val)))
	else:
		break

	print("Data get benchmark ...")
	start_time = time.time()
	for i in range(test_count):
		if not node.getData(data_id):
			print("Fail to get data %s" % data_name)
			break
		else:
			print("Data get %d/%d\r" % (i + 1, test_count)),
	end_time = time.time()
	if i + 1 == test_count:
		print("\nAverage data get time %fs consumed for %d bytes)\n" % ((end_time - start_time) / test_count, len(data_val)))
	else:
		break
