from google.appengine.ext import ndb


class Like(ndb.Model):
    owner = ndb.KeyProperty(kind='User', required=True)
    post = ndb.KeyProperty(kind='Post', required=True)
    liked = ndb.BooleanProperty(default=False)
