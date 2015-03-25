pyCloudAPILib - written by Lans Zhang <jia.zhang@windriver.com>

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
Pre-defined cloud settings for Wind River Axeda server and Mashery API manager.

[Note]
python-requests and ssl modules have a bug on handling SSL URL of mashery API
manager. pyCloudAPILib masks the SSL warning but it essentionally causes a
performance impact. To remove the impact, apply the patch patch/requests-fix-matching-special-URL-for-SSL-certificate.patch
to python-requests module.

Then modify config.py and change the following line
"ssl": False,
to
"ssl": True,

[Changelogs]
2015/03/25: ver 0.0.4
* README cleanup

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