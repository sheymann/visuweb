# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Référence la liste des services et distribue les requêtes sur les serveurs disponibles.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import random
import urllib2
from config import CONFIG

class Lookup:
    __servers__ = ["localhost:8888"]                # list of available servers to distribute the data fetching
    __status__ =            "/api/status/"
    __push_node__ =         "/api/push/node/q="     # ex: http://localhost:8888/push/node/q=http://twitter.com/gexf
    __fetch_node__ =        "/api/fetch/node/q="  	# ex: http://localhost:8888/fetch/node/q=http://twitter.com/gexf
    __push_notification__ = "/api/push/notif/"      # ex: http://localhost:8888/push/notif/map=http://twitter.com/gexf&amp;user=gephi

    class PATTERN:
        pass
    
    def __init__(self):
        self.PATTERN.status = self.__status__
        self.PATTERN.push_node = self.__push_node__ + "([A-Za-z0-9:/.,=?_%\-]+)"
        self.PATTERN.fetch_node = self.__fetch_node__ + "([A-Za-z0-9:/.,=?_%\-]+)"
        self.PATTERN.push_notification = self.__push_notification__ + "map=([A-Za-z0-9:/.,=?_%\-]+)&amp;user=([A-Za-z0-9]+)"

    def __query__(self, url):
        request = urllib2.Request(url, headers={'User-Agent' : "VisuWeb 1.0"}) 
        connexion = urllib2.urlopen( request )
        return connexion.read()

    def pushNode(self, node):
        url = "http://" + self.__servers__[random.randint(0,len(self.__servers__)-1)] + self.__push_node__ + node
        return self.__query__(url)  #should be "ok"
    
    def fetchNode(self, node):
        url = "http://" + self.__servers__[random.randint(0,len(self.__servers__)-1)] + self.__fetch_node__ + node
        return self.__query__(url)  #should return a json
    
    def pushNotification(self, map_id, user):
        url = "http://" + self.__servers__[random.randint(0,len(self.__servers__)-1)] + self.__push_notification__ + "map=" + map_id + "&amp;user=" + user
        return self.__query__(url)  #should be "ok"

    def status(self):
        url = "http://" + "localhost" + CONFIG.API.port + self.__status__
        return self.__query__(url)  #should be "ok"


if __name__ == "__main__":
    print Lookup().PATTERN.push_node

