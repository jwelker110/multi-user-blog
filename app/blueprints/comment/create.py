from google.appengine.ext.ndb import Key

from app.helpers import Helper, user_required
from app.forms import CommentForm
from app.models import Comment


class CommentCreateHandler(Helper):
    @user_required()
    def post(self, user):
        # grab the form
        form = CommentForm(self.request.params)

        # check the form
        if not form.validate():
            form.csrf_token.data = self.generate_csrf()
            self.redirect(self.request.referer)
            return

        # need the key
        k = form.key.data

        try:
            # grab the post from the given key
            post = Key(urlsafe=k).get()
        except:
            post = None

        # key was invalid. No alert to user because this
        # shouldn't happen under normal navigation
        if post is None:
            self.redirect(self.request.referer)
            return

        try:
            # create the comment
            comment = Comment(
                parent=post.key,
                author=user,
                content=form.comment.data
            )
            comment.put()
            # go back to the post
            self.redirect(self.request.referer)
            return
        except Exception as e:
            # go back to post if we fail :(
            self.redirect(self.request.referer)
            return
