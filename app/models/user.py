from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    username_lower = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    email = db.EmailProperty()
    joined = db.DateTimeProperty(auto_now_add=True)
