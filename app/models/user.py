from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    username_lower = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    joined = ndb.DateTimeProperty(auto_now_add=True)
