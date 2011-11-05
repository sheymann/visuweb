# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Référence la liste des services.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import os

class WEB:
	pass

class API:
	pass

class SERVICES:
	pass

class GENERAL:
	pass

WEB.port = "8080"
WEB.captcha_public_key = ""
WEB.captcha_private_key = ""

API.servers = ["localhost:8888"]  	# list of available servers to distribute the data fetching
API.port = "8888"  					# port of this server instance
API.cache_time = 7  				# days
API.parallel_jobs = 5  				# number of parallel queries to social networks

SERVICES.push_node = "/push/q="  	# ex: http://localhost:8888/push/q=http://twitter.com/mentatseb
SERVICES.fetch_node = "/fetch/q="  	# ex: http://localhost:8888/fetch/q=http://twitter.com/mentatseb

GENERAL.static_dir = os.path.join(os.path.dirname(__file__), "static")

