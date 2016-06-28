from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash, user_required
from app.forms import CommentForm

temp = 'comment_edit.html'


class CommentEditHandler(Helper):
    def r(self, form=None, post=None, template=temp, **kw):
        self.render(template, form=form, post=post, **kw)

    @user_required()
    def get(self, user):
        # grab the comment key
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        # grab the comment
        try:
            comment = Key(urlsafe=k).get()
        except:
            comment = None

        if comment is None:
            self.redirect('/')
            return

        if comment.author != user:
            self.redirect('/')
            return

        post = comment.key.parent().get()

        form = CommentForm(data={
            'csrf_token': self.generate_csrf(),
            'key': comment.key.urlsafe(),
            'comment': comment.content
        })

        self.r(form, post)

    @user_required()
    def post(self, user):
        # grab the form
        form = CommentForm(self.request.params)

        if not form.validate():
            form.csrf_token.data = self.generate_csrf()
            self.r(form)
            return

        # get the comment
        try:
            comment = Key(urlsafe=form.key.data).get()
        except:
            # invalid key
            comment = None

        if comment is None:
            self.redirect('/')
            return

        if comment.author != user:
            self.redirect('/')
            return

        # better be a post here or else!
        post = comment.key.parent().get()
        if post is None:
            self.redirect('/')
            return

        # update the comment
        try:
            comment.content = form.comment.data
            comment.put()
            self.redirect('/post/view?key=%s' % post.key.urlsafe())
            return
        except:
            # let's give them another chance
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash())
            return
