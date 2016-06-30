from string import lower
import re

from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash, user_required
from app.forms import PostEditForm


temp = 'post_edit.html'


class PostEditHandler(Helper):
    def r(self, form=None, post=None, template=temp, **kw):
        self.render(template, form=form, post=post, **kw)

    @user_required()
    def get(self, user):
        # get the title of the post
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        try:
            # get the post please
            post = Key(urlsafe=k).get()
        except:
            # key is invalid
            post = None

        # unnatural nav
        if post is None:
            self.r(flashes=flash('Post does not exist'))
            return

        # check if the user is the owner or not
        if post.author != user:
            self.redirect('/')
            return

        # get the form ready
        form = PostEditForm(data={
            'csrf_token': self.generate_csrf(),
            'key': k,
            'title': post.title,
            'subject': post.subject,
            'content': post.content
        })

        self.r(form, post)

    @user_required()
    def post(self, user):
        # grab the form
        form = PostEditForm(self.request.params)

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again.'))
            return

        # validate form
        if not form.validate():
            self.r(form)
            return

        # get the post please
        post = Key(urlsafe=form.key.data).get()
        if post is None:
            self.r(flashes=flash('Post does not exist'))
            return

        # check if the user is the owner or not
        if post.author != user:
            self.redirect('/')
            return

        try:
            # let's update the post
            t = form.title.data
            # t = re.sub(r'[\!\@\#\$\%\^\&\*\-_=\+\?<>,\.\"\':;\{\}\[\]|\\~\/`]', '', t)
            post.title = t
            post.title_lower = lower(t)
            post.subject = form.subject.data
            post.content = form.content.data
            post.put()
            self.redirect('/author/%s' % post.author)
            return
        except Exception as e:
            form.csrf_token.data = self.generate_csrf()
            self.r(form)
            return
