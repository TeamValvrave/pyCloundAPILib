#!/usr/bin/python

# -*- coding: utf-8 -*-

"""
Here is an example showing how to use data get/set functions:

string node.getData(string name)
boolean node.setData(string name, string value)
string list node.getHistoricalData(string name, **p)
"""

import time
from optparse import OptionParser
import sys
from node import Node
from config import cloud_configs

VERSION = '0.3'

test_payload_lens = (8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096)

def do_write_test(cloud_name, config, data_name, data_len, verify_test, test_count):
	print("Benchmark data set %d-byte with %s ..." % (data_len, cloud_name))

	node = Node(cloud_name, config)
	data_id = node.dataId(data_name)
	data_val = "valvrave" * (data_len / 8)

	test_ok = True
	start_time = time.time()
	for i in range(test_count):
		if not node.setData(data_id, data_val):
			print("Fail to set data %s = %s" % (data_name, data_val))
			test_ok = False
			break
		else:
			print("Data set %d/%d\r" % (i + 1, test_count)),
			sys.stdout.flush()
			if verify_test and do_read_test(cloud, data_name, data_len, 1, data_val) == False:
				test_ok = False
				break
	end_time = time.time()

	if test_ok:
		print("\nAverage data set time %fs consumed for %d bytes" % ((end_time - start_time) / test_count, data_len))
		return data_val
	else:
		print("\nData set time failed for %d bytes at %d/%d" % (data_len, i + 1, test_count))
		return None

def do_read_test(cloud_name, config, data_name, data_len, test_count, data_val = None):
	if data_val:
		print("Benchmark data get %d-byte with %s ..." % (data_len, cloud_name))
	else:
		print("Benchmark data get with %s ..." % cloud_name)

	node = Node(cloud_name, config)
	data_id = node.dataId(data_name)

	test_ok = True
	start_time = time.time()
	val = None
	for i in range(test_count):
		val = node.getData(data_id)
		if not val:
			print("Fail to get data %s" % data_name)
			test_ok = False
			break
		else:
			if data_val and data_val != val:
				print("Data returned doesn't match up")
				test_ok = False
				break
			print("Data get %d/%d\r" % (i + 1, test_count)),
	end_time = time.time()

	if test_ok:
		print("\nAverage data get time %fs consumed for %d bytes" % ((end_time - start_time) / test_count, len(val)))
		return True
	else:
		print("\nData get time failed for %d bytes at %d/%d" % (len(data_val), i + 1, test_count))
		return False

def do_history_test(cloud_name, config, data_name, test_count):
	print("Benchmark historical data get with %s ..." % cloud_name)

	node = Node(cloud_name, config)
	test_ok = True

	start_time = time.time()
	for i in range(test_count):
		r = node.getHistoricalData(data_name, assetId = 476, dataItemIds = [ 437 ])
		if not r:
			test_ok = False
			break
	end_time = time.time()

	if test_ok:
		print("\nAverage data get time %fs consumed" % ((end_time - start_time) / test_count))
		return True
	else:
		print("\nData get time failed at %d/%d" % (i + 1, test_count))
		return False

def benchmark(cloud_name, config, read_test, write_test, test_count, verify_test, history_test):
	data_name = "vlv_benchmark"

	# Back to back test
	if write_test:
		for data_len in test_payload_lens:
			data_val = do_write_test(cloud_name, config, data_name, data_len, verify_test, test_count)

			if read_test:
				do_read_test(cloud_name, config, data_name, data_len, test_count, data_val)
	elif read_test:
		do_read_test(cloud_name, config, data_name, 0, test_count, None)

	if history_test:
		do_history_test(cloud_name, config, data_name, test_count)

def parse_args():
	parser = OptionParser(usage='%prog -s cloud_name [-h] [--version] [-r] [-w] [-n]',
						  version='%prog ' + VERSION)
	parser.add_option('-s', '--cloud', dest='cloud_name', action='store',
					  default="Mashery", help='Specify the cloud service used in benchmark [%default]')
	parser.add_option('-r', '--read-test', dest='read_test', action='store_true',
					  default=False, help='Run data item read test [%default]')
	parser.add_option('-w', '--write-test', dest='write_test', action='store_true',
					  default=False, help='Run data item write test [%default]')
	parser.add_option('-p', '--verify', dest='verify_test', action='store_true',
					  default=False, help='Read back the data after a write [%default]')
	parser.add_option('-n', '--test-count', dest='test_count', action='store',
					  default=1, help='The number of test loop [%default]')
	parser.add_option('-g', '--read-history', dest='history_test', action='store_true',
					  default=False, help='Read back the historical data [%default]')

	opts, args = parser.parse_args()

	if len(args):
		parser.print_help()
		sys.exit(-1)

	if not opts.cloud_name in cloud_configs.keys():
		print("ERROR: Please specify a cloud name %s used to access cloud services" % repr(tuple(cloud_configs.keys())))
		sys.exit(-1)

	if not opts.read_test and not opts.write_test and not opts.history_test:
		print("ERROR: Please specify a test item")
		sys.exit(-1)

	if int(opts.test_count) <= 0:
		print("ERROR: Please specify a valid test count")
		sys.exit(-1)

	return opts

if __name__ == '__main__':
	opts = parse_args()
	benchmark(opts.cloud_name, cloud_configs[opts.cloud_name], opts.read_test, \
		opts.write_test, int(opts.test_count), opts.verify_test, opts.history_test)