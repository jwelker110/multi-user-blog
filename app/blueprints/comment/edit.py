from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash
from app.forms import CommentForm

temp = 'comment_edit.html'


class CommentEditHandler(Helper):
    def r(self, form=None, post=None, template=temp, **kw):
        self.render(template, form=form, post=post, **kw)

    def get(self):
        # check the user
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login', True)
            return

        # grab the comment key
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/', True)
            return

        comment = Key(urlsafe=k).get()
        if comment is None:
            self.redirect('/', True)
            return

        if comment.author != user:
            self.redirect('/', True)
            return

        post = comment.key.parent().get()

        form = CommentForm(data={
            'csrf_token': self.generate_csrf(),
            'key': comment.key.urlsafe(),
            'comment': comment.content
        })

        self.r(form, post)

    def post(self):
        # check the user
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login', True)
            return

        # grab the form
        form =CommentForm(self.request.params)

        if not form.validate():
            form.csrf_token.data = self.generate_csrf()
            self.r(form)
            return

        comment = Key(urlsafe=form.key.data).get()
        if comment is None:
            self.redirect('/', True)
            return

        if comment.author != user:
            self.redirect('/', True)
            return

        post = comment.key.parent().get()
        if post is None:
            self.redirect('/', True)
            return

        try:
            comment.content = form.comment.data
            comment.put()
            self.redirect('/post/view?key=%s' % post.key.urlsafe(), True)
            return
        except:
            self.r(form, flashes=flash())
            return
