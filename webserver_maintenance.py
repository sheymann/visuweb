# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Main Web Server.

Requires Python 2.7
"""

import tornado.ioloop
import tornado.web

from config import CONFIG

settings = {
    "static_path": CONFIG.static_dir,
    "cookie_secret": CONFIG.cookie_secret,
#    "login_url": "/login",
    "xsrf_cookies": True,
}


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template/maintenance.html")

application = tornado.web.Application([
    (r"/.*", HomeHandler),
    (r"/", tornado.web.StaticFileHandler,
     dict(path=settings['static_path']))
], **settings)


if __name__ == "__main__":
    application.listen(CONFIG.WEB.port)
    tornado.ioloop.IOLoop.instance().start()

