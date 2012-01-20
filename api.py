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

from exceptions import *
from notification_map import NotificationMultimap
from logger import Logger
from cache import Cache
from job_queue import JobQueue
from lookup import Lookup
from config import CONFIG

settings = {
    "static_path": CONFIG.static_dir,
    "twitter_consumer_key": "Q636WeJdWBEXSfMTTZbw",
    "twitter_consumer_secret": "l3bVkk2H1e0KFlImQLQkuJRn9uICkzpNE36TJH59yjY"
}

queue = JobQueue()


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ok")

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
    def initialize(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def get(self, node):
        #TODO securiser l'accès via un token?
        #try:
            # ex node: "http://twitter.com/mentatseb"
            # Check if the username exists
            #request = urllib2.Request(node, headers={'User-Agent' : "VisuWeb 1.0"}) 
            #connexion = urllib2.urlopen( request )
            #connexion.read()
        while queue.isLocked():
            sleep(0.1)
        queue.put(node)
        self.write("ok")
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
    __cache__ = Cache()
    @tornado.web.asynchronous
    def get(self, node):
        self.__node__ = node
        #TODO securiser l'accès via un token?
        # If the node has been checked recently then pump in the cache,
        # otherwise fetch fresh data on the Web.
        if self.__cache__.isCached(node):
            json = self.__cache__.load(node)
            self.on_response_cache(json)
        else:
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch("http://socialgraph.apis.google.com/lookup?q="+node+"&edi=1", callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        self.write(response.body)
        self.__cache__.cache(self.__node__, response.body)
        self.finish()
        
    def on_response_cache(self, response):
        self.write(response)
        self.finish()


class PushNotificationHandler(tornado.web.RequestHandler):
    def get(self, map_id, user):
        nm = NotificationMultimap()
        nm[map_id] = user
        self.write("ok")


application = tornado.web.Application([
    (r""+Lookup().PATTERN.status, StatusHandler),
    (r""+Lookup().PATTERN.push_node, PushNodeHandler),
    (r""+Lookup().PATTERN.fetch_node, FetchNodeHandler),
    (r""+Lookup().PATTERN.push_notification, PushNotificationHandler),
    (r"/api/tweet/([A-Za-z0-9]+)", TwitterAuthHandler), #TODO
    (r"/", tornado.web.StaticFileHandler,
     dict(path=settings['static_path']))
], **settings)

if __name__ == "__main__":
    application.listen(CONFIG.API.port)
    tornado.ioloop.IOLoop.instance().start()

