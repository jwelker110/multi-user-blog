from google.appengine.ext import ndb


class Post(ndb.Model):
    title = ndb.StringProperty(required=True)
    title_lower = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    author_lower = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    subject = ndb.StringProperty()
    content = ndb.TextProperty(required=True)
