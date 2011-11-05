# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Ecoute la queue et consomme des usernames.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import os.path
import re
from time import sleep
from logger import Logger
from queue import Queue
from graph import GraphBuilder, GraphUtils


class Overmind:
	__logger__ = Logger("Overmind")
	
	def run(self):
		queue = Queue()
		graphUtils = GraphUtils()
		while True:
			# Main loop
			while queue.isLocked():
				sleep(0.1)
			if len(queue) != 0:
				item = queue.consume()
				builder = GraphBuilder()
				graph = builder.build(item)
				citem = self.__getCanonicalitemName__(item)
				GraphUtils().write_gexf(graph, os.path.join("static", citem + ".gexf"))
				self.__logger__.info("Graph made for "+item)
			else:
				#Read the queue directory again if the queue is empty
				queue = Queue()
			#Wait 1s
			sleep(1)
	
	def __getCanonicalitemName__(self, name):
		cname = re.sub('^https?://','',name.lower())
		cname = re.sub('[^A-Za-z0-9]', '_', cname)
		return cname


if __name__ == "__main__":
	Overmind().run()

