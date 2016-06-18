from google.appengine.ext import ndb


class Comment(ndb.Model):
    author = ndb.StringProperty(required=True)
    content = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)

