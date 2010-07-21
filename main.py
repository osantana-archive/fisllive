#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# FISL Live
# =========
# Copyright (c) 2010, Triveos Tecnologia Ltda.
# License: AGPLv3

import logging

from os.path import *
from datetime import datetime

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

 # from GAE Samples (to serialize models to JSON)
import json

# from gaeutilities.appspot.com
from appengine_utilities import sessions


class Message(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class Page(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            linktext = 'Logout'
            user = users.get_current_user()
        else:
            url = users.create_login_url(self.request.uri)
            linktext = 'Login'
            user = "Anonymous Coward"

        path = join(dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, locals()))
        
    def post(self):
        content = self.request.get('content')
        if content:
            message = Message()
            if users.get_current_user():
                message.author = users.get_current_user()
            message.content = self.request.get('content')
            message.put()
        self.redirect("/")

    
class Messages(webapp.RequestHandler):
    def get(self, mode=""):
        messages_query = Message.all().order('date')

        session = sessions.Session()
        if mode != "/all":
            if 'last' in session:
                messages_query.filter("date >", session['last'])

        session["last"] = datetime.utcnow()

        result = json.encode(messages_query.fetch(20))
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'  
        self.response.out.write(result)

if __name__ == "__main__":
    application = webapp.WSGIApplication([
        ('/', Page),
        ('/messages(.*)', Messages),
    ], debug=True)
    util.run_wsgi_app(application)

# vim:ts=4:sw=4:et:sm:si:ai