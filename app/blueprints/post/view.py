from google.appengine.ext.ndb import Key

from app.helpers import Helper
from app.models import Comment
from app.forms import CommentForm

temp = 'post.html'


class PostHandler(Helper):
    def r(self, form=None, post=None, comments=None, template=temp, **kw):
        self.render(template, form=form, post=post, comments=comments, **kw)

    def get(self):
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        form = CommentForm(data={
            'key': k,
            'csrf_token': self.generate_csrf()
        })
        try:
            post = Key(urlsafe=k).get()
        except:
            self.r()
            return
        comments = None
        if post is not None:
            comments = Comment.query(ancestor=post.key).order(-Comment.created).fetch()
        self.r(form, post, comments)
