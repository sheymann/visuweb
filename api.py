# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
API Server.

Requires Python 2.7
"""

import tornado.auth
import tornado.ioloop
import tornado.escape
import tornado.httpclient
import tornado.web
import urllib2
from time import sleep

from logger import Logger
from cache import GraphCache
from queue import Queue
from config import API, SERVICES, GENERAL

queue = Queue()

settings = {
    "static_path": GENERAL.static_dir,
    "twitter_consumer_key": "Q636WeJdWBEXSfMTTZbw",
    "twitter_consumer_secret": "l3bVkk2H1e0KFlImQLQkuJRn9uICkzpNE36TJH59yjY"
}


# App: https://dev.twitter.com/apps/1357631/settings
class TwitterAuthHandler(tornado.web.RequestHandler, tornado.auth.TwitterMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, username, link):
        self.twitter_request(
            "/statuses/update",
            post_args={"status": "Testing Tornado Web Server"}, # "d @" + username +" the visualization is ready: " + link
            access_token=user["access_token"],
            callback=self.async_callback(self._on_post))

    def _on_post(self, new_entry):
        if not new_entry:
            # Call failed; perhaps missing permission?
            self.authorize_redirect()
            return
        self.finish("Posted a message!")


class PushNodeHandler(tornado.web.RequestHandler):
    __logger__ = Logger("PushNodeHandler")
    def get(self, node):
        #try:
            # ex node: "http://twitter.com/mentatseb"
            # Check if the username exists
            #request = urllib2.Request(node, headers={'User-Agent' : "VisuWeb 1.0"}) 
            #connexion = urllib2.urlopen( request )
            #connexion.read()
        while queue.isLocked():
            sleep(0.1)
        queue.product(node)
        self.write("ok")  #Your request for the map " + node + " has been taken into account. Please wait until it's done :)
        #except IOError, e:
            #self.__logger__.error(str(e)+" on "+node)
            #if hasattr(e, 'reason'):
                # print 'We failed to reach a server.'
                #self.write(e.reason)
            #elif hasattr(e, 'code'):
                # print 'The server couldn\'t fulfill the request.'
                #self.write(e.code)


class FetchNodeHandler(tornado.web.RequestHandler):
    '''Fetch a node and its inbound links from Google SocialGraph API'''
    @tornado.web.asynchronous
    def get(self, node):
        self.__node__ = node
        # If the node has been checked recently then pump in the cache,
        # otherwise fetch fresh data on the Web.
        if GraphCache().isCached(node):
            json = GraphCache().load(node)
            self.on_response_cache(json)
        else:
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch("http://socialgraph.apis.google.com/lookup?q="+node+"&edi=1", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        self.write(response.body)
        GraphCache().cache(self.__node__, response.body)
        self.finish()
        
    def on_response_cache(self, response):
        self.write(response)
        self.finish()


application = tornado.web.Application([
    (r""+SERVICES.push_node+"([A-Za-z0-9:/.,=?_%\-]+)", PushNodeHandler),
    (r""+SERVICES.fetch_node+"([A-Za-z0-9:/.,=?_%\-]+)", FetchNodeHandler),
    (r"/tweet/([A-Za-z0-9]+)", TwitterAuthHandler),
    (r"/", tornado.web.StaticFileHandler,
     dict(path=settings['static_path']))
], **settings)

if __name__ == "__main__":
    application.listen(API.port)
    tornado.ioloop.IOLoop.instance().start()

