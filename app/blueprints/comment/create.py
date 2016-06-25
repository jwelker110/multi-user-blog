from google.appengine.ext.ndb import Key

from app.helpers import Helper
from app.forms import CommentForm
from app.models import Comment


class CommentCreateHandler(Helper):
    def post(self):
        # make sure our user is here
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login')
            return

        form = CommentForm(self.request.params)

        if not form.validate():
            form.csrf_token.data = self.generate_csrf()
            self.redirect(self.request.referer)
            return

        k = form.key.data

        try:
            # grab the post
            post = Key(urlsafe=k).get()
        except:
            post = None

        if post is None:
            self.redirect(self.request.referer)
            return

        try:
            comment = Comment(
                parent=post.key,
                author=user,
                content=form.comment.data
            )
            comment.put()
            self.redirect(self.request.referer)
            return
        except Exception as e:
            print e.message
            self.redirect(self.request.referer)
            return
