# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Empty configuration file.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import os


class CONFIG:
    class WEB:
	    pass
    class API:
	    pass

CONFIG.static_dir = os.path.join(os.path.dirname(__file__), "static")
CONFIG.cookie_secret = ""   # generate a cookie using cookie_generator.py
CONFIG.cache_time = 7  	    # cache retention in number of days
CONFIG.parallel_jobs = 5  	# number of parallel queries to social networks

CONFIG.API.port = "8888"    # port used by this server to serve the api
CONFIG.WEB.port = "8080"    # port used by this server to serve the frontend

CONFIG.WEB.captcha_public_key = ""
CONFIG.WEB.captcha_private_key = ""

