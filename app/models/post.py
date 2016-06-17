from google.appengine.ext import db


class Post(db.Model):
    title = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    subject = db.StringProperty()
    content = db.TextProperty(required=True)
    image_url = db.StringProperty()
