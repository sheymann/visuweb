# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Gère le cache.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import os.path
import re
from stat import *
import time

from logger import Logger
from config import API


class GraphCache:
	__logger__ = Logger("GraphCache")
	def __cleanName__(self, url):
		fname = re.sub('^https?://','',url.lower())
		fname = re.sub('[^A-Za-z0-9]', '_', fname)
		return fname
	
	def cache(self, node, json):
		'''Cache data formatted in json'''
		fname = self.__cleanName__(node)
		f = open(os.path.join("cache", fname), 'w')
		f.write(json)
		f.close()
		self.__logger__.info("cached: %s", fname)
	
	def isCached(self, node):
		'''Return true if the data is in cache and has been updated less than API.cache_time days'''
		fname = self.__cleanName__(node)
		path = os.path.join("cache", fname)
		if not os.path.exists(path):
			return False
		now = int(time.time())
		recent = now - (API.cache_time * 24 * 60 * 60)
		fileTime = os.stat(path)[ST_MTIME]
		return os.path.exists(path) and fileTime > recent
	
	def load(self, node):
		'''Load data formatted in json'''
		fname = self.__cleanName__(node)
		if not self.isCached(node):
			raise Exception("not in cache: "+fname)
		f = open(os.path.join("cache", fname), 'r')
		json = f.read()
		f.close()
		return json

