# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Logger

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import logging
#import auxiliary_module

class Logger:
	def __init__(self, modulename = ""):
		# create logger with 'spam_application'
		self.logger = logging.getLogger('tweetmap/'+modulename)
		self.logger.setLevel(logging.DEBUG)
		# create file handler which logs even debug messages
		fhd = logging.FileHandler('tweetmap-debug.log')
		fhd.setLevel(logging.DEBUG)
		# create file handler which logs warning messages
		fhw = logging.FileHandler('tweetmap-warning.log')
		fhw.setLevel(logging.WARNING)
		# create file handler which logs info messages
		fhi = logging.FileHandler('tweetmap-info.log')
		fhi.setLevel(logging.INFO)
		# create console handler with a higher log level
		ch = logging.StreamHandler()
		ch.setLevel(logging.ERROR)
		# create formatter and add it to the handlers
		formatter = logging.Formatter('%(asctime)s %(name)-22s %(levelname)-10s %(message)s')
		fhd.setFormatter(formatter)
		fhw.setFormatter(formatter)
		fhi.setFormatter(formatter)
		ch.setFormatter(formatter)
		# add the handlers to the logger
		self.logger.addHandler(fhd)
		self.logger.addHandler(fhw)
		self.logger.addHandler(fhi)
		self.logger.addHandler(ch)
	
	def get(self):
		return self.logger
	
	def info(self, msg, *args, **kwargs):
		self.logger.info(msg, *args, **kwargs)
	
	def warn(self, msg, *args, **kwargs):
		self.logger.warn(msg, *args, **kwargs)
	
	def error(self, msg, *args, **kwargs):
		self.logger.error(msg, *args, **kwargs)
	
	def critical(self, msg, *args, **kwargs):
		self.logger.critical(msg, *args, **kwargs)
	
	def exception(self, msg, *args):
		self.logger.exception(msg, *args)


