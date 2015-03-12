﻿pyCloudAPILib - written by Lans Zhang <jia.zhang@windriver.com>

- Overview
- Changelogs
- Examples
- Note

[Overview]
This python library provides the support for a various of cloud API and gives
an unique interface for application.

Currently, this library support Axeda Platform and Wind River Mashery API manager.

In the context of this library, all machines connected to cloud are deems as
nodes, either a role of server or client.

[Examples]
- benchmark_getsetdata.py
This example code demonstrates how to call get/set function to operate a data
item stored in cloud and benchmark the get/set performance. Type
benchmark_getsetdata.py -h for help.

- config.py
Pre-defined cloud settings.

[Note]
Please ignore this warnning during runtime if https is used:

urllib3\connectionpool.py:734: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificat e verification is strongly advised. See: https://urllib3.readthedocs.org/en/late
st/security.html
  InsecureRequestWarning)

[Changelogs]
2015/02/21: ver 0.0.3
* Add node.getHistoricalData() support

2015/02/21: ver 0.0.2
* Remove server.py.
* Code cleanup.
* Enhance benchmark_getsetdata.py.
* Add the API support for Axeda Platform.

2015/02/16: ver 0.0.1
* Initial version, supporting Wind River Mashery API manager for get/set data
item.