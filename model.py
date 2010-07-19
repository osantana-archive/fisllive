from google.appengine.ext import db

class Message(db.Model):
    timestamp = db.DateTimeProperty(auto_now=True,
                                    auto_now_add=True)
    message = db.StringProperty(multiline=True)

