from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash, user_required
from app.forms import CommentDeleteForm

temp = 'comment_delete.html'


class CommentDeleteHandler(Helper):
    def r(self, form=None, post=None, comment=None, template=temp, **kw):
        self.render(template, form=form, post=post, comment=comment, **kw)

    @user_required()
    def get(self, user):
        # grab the key. Shouldn't be None unless unnatural
        # navigation
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        # let's create the form
        form = CommentDeleteForm(data={
            'key': k,
            'csrf_token': self.generate_csrf()
        })

        # grab the comment
        try:
            comment = Key(urlsafe=k).get()
        except:
            comment = None

        # can't delete what we don't have
        # unnatural navigation (tisk tisk)
        if comment is None:
            self.redirect('/')
            return

        # grab the post
        post = comment.key.parent().get()
        # same as above. Can't delete nothing.
        if post is None:
            self.redirect('/')
            return

        self.r(form, post, comment)

    @user_required()
    def post(self, user):
        # let's get the form
        form = CommentDeleteForm(self.request.params)

        # validate the form please
        if not form.validate():
            self.redirect(self.request.referer)
            return

        try:
            # grab the comment
            comment = Key(urlsafe=form.key.data).get()
        except:
            # really this shouldn't be None
            # unless unnatural nav
            comment = None

        # go back home
        if comment is None:
            self.redirect('/')
            return

        # this isn't the users comment!
        if comment.author != user:
            self.redirect('/')
            return

        # alright let's delete the comment
        try:
            comment.key.delete()
            self.redirect('/')
            return
        except Exception as e:
            # we'll give them another chance
            form.csrf_token.data = self.generate_csrf()
            self.r(form, comment, flashes=flash())
            return
