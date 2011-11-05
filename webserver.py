# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Main Web Server.

Requires Python 2.7
"""

import os
import random
import tornado.ioloop
import tornado.escape
#import tornado.httpclient
import tornado.web
import urllib2
from recaptcha.client import captcha

from logger import Logger
from config import API, WEB, SERVICES, GENERAL

settings = {
    "static_path": GENERAL.static_dir,
    "cookie_secret": "pyQ3R7V+SrmUr+uncWxVGjmMfQotd0HYkw7LfWLyoEI=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        recaptcha = captcha.displayhtml(WEB.captcha_public_key)
        self.render("template/home.html", captcha=recaptcha)
    def post(self):
        response = captcha.submit(
            self.get_argument("recaptcha_challenge_field"),
            self.get_argument("recaptcha_response_field"),
            WEB.captcha_private_key,
            req.remote_addr,
            )
        if not response.is_valid:
            self.write("Captcha is invalid.")
        else:
            self.render("template/home.html", captcha=None)


class TwitterMapHandler(tornado.web.RequestHandler):
    def get(self, username):
        gexf = "twitter_com_"+username.lower()+".gexf"
        path = os.path.join("static", gexf)
        if os.path.exists(path):
            self.render("template/template-twitter.html", username=username, gexf=gexf)
        else:
            self.render("template/template-request.html", username=username, error=None)


class TwitterCreateMapHandler(tornado.web.RequestHandler):
    __url__ = "http://"+API.servers[random.randint(0,len(API.servers)-1)]+SERVICES.push_node
    __logger__ = Logger("TwitterCreateMapHandler")
    def post(self):
        username = self.get_argument("username")
        gexf = "twitter_com_"+username.lower()+".gexf"
        # Does the gexf exist?
        path = os.path.join("static", gexf)
        if os.path.exists(path):
            self.redirect('/twitter/'+username)
        else:
            # Push a new job through the API
            error = None
            try:
                request = urllib2.Request(self.__url__ + tornado.escape.url_escape("http://twitter.com/"+username), headers={'User-Agent' : "VisuWeb 1.0"}) 
                connexion = urllib2.urlopen( request )
                answer = connexion.read()  #should be "ok"
                if answer == "ok":
                    self.redirect('/twitter/'+username)
                else:
                    error = answer
            except IOError, e:
                self.__logger__.error(str(e)+" on "+self.__url__+username)
                error = str(e)
            self.render("template/template-request.html", username=username, error=error)


class TwitterPdfHandler(tornado.web.RequestHandler):
    def get(self, username):
        self.render("template/template-twitter-pdf.html", username=username+"'s twitter network")


class FormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/twitter/([A-Za-z0-9]+)", TwitterMapHandler),
    (r"/twitter/create/", TwitterCreateMapHandler),
    (r"/twitter/pdf/([A-Za-z0-9]+)", TwitterPdfHandler),
    (r"/", tornado.web.StaticFileHandler,
     dict(path=settings['static_path']))
], **settings)


if __name__ == "__main__":
    application.listen(WEB.port)
    tornado.ioloop.IOLoop.instance().start()

