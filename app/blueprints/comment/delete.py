from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash
from app.forms import CommentDeleteForm

temp = 'comment_delete.html'


class CommentDeleteHandler(Helper):
    def r(self, form=None, post=None, comment=None, template=temp, **kw):
        self.render(template, form=form, post=post, comment=comment, **kw)

    def get(self):
        # is the user logged in???
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login')
            return

        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        form = CommentDeleteForm(data={
            'key': k,
            'csrf_token': self.generate_csrf()
        })

        # grab the comment
        comment = Key(urlsafe=k).get()

        if comment is None:
            self.redirect('/')
            return

        # grab the post
        post = comment.key.parent().get()
        if post is None:
            self.redirect('/')
            return

        self.r(form, post, comment)

    def post(self):
        # make sure the user is logged in
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login')
            return

        form = CommentDeleteForm(self.request.params)

        if not form.validate():
            self.redirect('/')
            return

        try:
            # grab the comment
            comment = Key(urlsafe=form.key.data).get()
        except:
            comment = None

        if comment is None:
            self.redirect('/')
            return

        if comment.author != user:
            self.redirect('/')
            return

        # alright let's delete the comment
        try:
            comment.key.delete()
            self.redirect('/')
            return
        except Exception as e:
            print e.message
            form.csrf_token.data = self.generate_csrf()
            self.r(form, comment, flashes=flash())
            return
