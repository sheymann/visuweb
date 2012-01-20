# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Main Web Server.

Requires Python 2.7
"""

import os
import tornado.ioloop
import tornado.escape
#import tornado.httpclient
import tornado.web
from tornado.web import HTTPError
import urllib2
from recaptcha.client import captcha

from exceptions import *
from logger import Logger
from lookup import Lookup
from config import CONFIG

settings = {
    "static_path": CONFIG.static_dir,
    "cookie_secret": CONFIG.cookie_secret,
#    "login_url": "/login",
    "xsrf_cookies": True,
}


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
        self.render("template/home.html", captcha=recaptcha, error=None)


class ViewTwitterMapHandler(tornado.web.RequestHandler):
    def get(self, username):
        gexf = "twitter_com_"+username.lower()+".gexf"
        path = os.path.join("static", gexf)
        if os.path.exists(path):
            self.render("template/view-twitter.html", username=username, gexf=gexf)
        else:
            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
            self.render("template/request-twitter.html", username=username, error=None, captcha=recaptcha)


class CreateTwitterMapHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def post(self):
        try:
            username = self.get_argument("username")
        except HTTPError, e:
            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
            self.render("template/home.html", captcha=recaptcha, error="The username is required.")
#        try:
#            recaptcha_challenge = self.get_argument("recaptcha_challenge_field")
#            recaptcha_response = self.get_argument("recaptcha_response_field")
#        except HTTPError, e:
#            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
#            self.render("template/home.html", captcha=recaptcha, error="The captcha must be filled.")
#        
#        response = captcha.submit(
#            recaptcha_challenge,
#            recaptcha_response,
#            WEB.captcha_private_key,
#            self.request.remote_ip
#            )
#        
#        if not response.is_valid:
#            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
#            self.render("template/home.html", captcha=recaptcha, error="The captcha is incorrect.")
#        else:
        #CAPTCHA valid
        gexf = "twitter_com_"+username.lower()+".gexf"
        # Does the gexf exist?
        path = os.path.join("static", gexf)
        if os.path.exists(path):
            self.redirect('/view/twitter/'+username)
        else:
            # Push a new job through the API
            try:
                answer = Lookup().pushNode(tornado.escape.url_escape("http://twitter.com/" + username))
                if answer == "ok":
                    self.redirect('/view/twitter/'+username)
                else:
                    recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
                    self.render("template/request-twitter.html", username=username, error=answer, captcha=recaptcha)
            except IOError, e:
                self.__logger__.error(str(e))
                error = str(e)
                recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
                self.render("template/request-twitter.html", username=username, error=error, captcha=recaptcha)


class OrderTwitterPdfHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template/order-twitter-pdf.html")


class OrderPdfHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/order/twitter/pdf/', permanent=True)


class FinishOrderTwitterPdfHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template/finish-order-twitter-pdf.html", captcha=None)


class AddNotificationHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def post(self):
        try:
            map_id = self.get_argument("map_id")
            notified_username = self.get_argument("notified_username")
#        try:
#            recaptcha_challenge = self.get_argument("recaptcha_challenge_field")
#            recaptcha_response = self.get_argument("recaptcha_response_field")
#        except HTTPError, e:
#            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
#            self.render("template/request-twitter.html", captcha=recaptcha, error="The captcha must be filled.")
#        
#        response = captcha.submit(
#            recaptcha_challenge,
#            recaptcha_response,
#            WEB.captcha_private_key,
#            self.request.remote_ip
#            )
#        
#        if not response.is_valid:
#            recaptcha = captcha.displayhtml(CONFIG.WEB.captcha_public_key)
#            self.render("template/request-twitter.html", captcha=recaptcha, error="The captcha is incorrect.")
#        else:
        #CAPTCHA valid
            # Push a new notification through the API
            try:
                answer = Lookup().pushNotification(tornado.escape.url_escape(map_id), notified_username)
                if answer == "ok":
                    self.render("template/generic-msg.html", msg="@visu_web will send a direct message to @"+notified_username+" once the job is done.")
                else:
                    self.render("template/generic-msg.html", msg=answer)
            except IOError, e:
                self.__logger__.error(str(e))
                self.render("template/generic-msg.html", msg=str(e))
        except HTTPError, e:
            self.render("template/generic-msg.html", msg="Your Twitter username is required.")


application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/view/twitter/([A-Za-z0-9]+)", ViewTwitterMapHandler),
    (r"/create/twitter/", CreateTwitterMapHandler),
    (r"/order/twitter/pdf/", OrderTwitterPdfHandler),
    (r"/finish-order/twitter/pdf/", FinishOrderTwitterPdfHandler),
    (r"/order/pdf/", OrderPdfHandler),
    (r"/add-notification/", AddNotificationHandler),
    (r"/", tornado.web.StaticFileHandler,
     dict(path=settings['static_path']))
], **settings)


if __name__ == "__main__":
    application.listen(CONFIG.WEB.port)
    tornado.ioloop.IOLoop.instance().start()

