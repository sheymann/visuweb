# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Cache system for the social graph. 
Each node neighborhood is stored in a JSON file compressed in GZIP.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import gzip
import os.path
import re
from stat import *
import time

from logger import Logger
from config import CONFIG


class Cache:
    def __init__(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def __cleanName__(self, url):
        fname = re.sub('^https?://','',url.lower())
        fname = re.sub('[^A-Za-z0-9]', '_', fname) + ".json.gz"
        return fname
    
    def cache(self, node, json):
        '''Cache data formatted in json'''
        fname = self.__cleanName__(node)
        f = gzip.open(os.path.join("cache", fname), 'wb')
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
        recent = now - (CONFIG.cache_time * 24 * 60 * 60)
        fileTime = os.stat(path)[ST_MTIME]
        return os.path.exists(path) and fileTime > recent
    
    def load(self, node):
        '''Load data formatted in json'''
        fname = self.__cleanName__(node)
        if not self.isCached(node):
            raise Exception("not in cache: "+fname)
        json = ""
        f = gzip.open(os.path.join("cache", fname), 'rb')
        json = f.read()
        f.close()
        return json

