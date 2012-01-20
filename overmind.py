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
from job_queue import JobQueue
from notification_map import NotificationMultimap
from graph import GraphBuilder, GraphUtils
from lookup import Lookup
from exceptions import *

#TODO mettre la boucle en script bash
class Overmind:
    def __init__(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def run(self):
        queue = JobQueue()
        utils = GraphUtils()
        builder = GraphBuilder()
        nm = NotificationMultimap()
        while True:
            # Main loop
            while queue.isLocked():
                sleep(0.1)
            item = None
            if queue:
                try:
                    item = queue.get()
                    graph = builder.build(item)
                    citem = self.__getCanonicalItem__(item)
                    utils.write_gexf(graph, os.path.join("static", citem + ".gexf"))
                    #utils.write_json(graph, os.path.join("static", citem + ".json"))
                    self.__logger__.info("Graph made for "+item)
                    # Notify registered Twitter users
                    twitter_usernames = nm[item]
                    for user in twitter_usernames:
                        try:
                            answer = Lookup().pushNotification(user)
                        except IOError, e:
                            self.__logger__.error(str(e))
                except Exception, e:
                    if item:
                        queue.put(item)
                    self.__logger__.error(str(e))
            else:
                #Wait 1s
                sleep(1)
                #Read the queue directory again if the queue is empty
                queue = JobQueue()
    
    def __getCanonicalItem__(self, name):
        cname = re.sub('^https?://','',name.lower())
        cname = re.sub('[^A-Za-z0-9]', '_', cname)
        return cname


if __name__ == "__main__":
    Overmind().run()

