from google.appengine.ext import db


class Comment(db.Model):
    author = db.StringProperty(required=True)
    content = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

