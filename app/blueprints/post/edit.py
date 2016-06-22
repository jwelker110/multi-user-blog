from string import lower
from urllib import unquote
import re

from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash
from app.forms import PostEditForm
from app.models import Post


temp = 'post_edit.html'


class PostEditHandler(Helper):
    def r(self, form=None, post=None, template=temp, **kw):
        self.render(template, form=form, post=post, **kw)

    def get(self):
        # make sure the user is the same we have on our session
        user = self.validate_user()
        if user is None:
            self.invalidate_sig()
            self.redirect('/user/login', True)
            return

        # get the title of the post
        title = self.request.path.split('/')[2]
        title = unquote(title)

        # get the post please
        post = Post.query(Post.title_lower == lower(title)).get()
        if post is None:
            self.r(flashes=flash('Post does not exist'))
            return
        k = post.key.urlsafe()

        # check if the user is the owner or not
        if post.author != user:
            self.redirect('/', True)
            return

        form = PostEditForm(data={
            'csrf_token': self.generate_csrf(),
            'key': k,
            'title': post.title,
            'subject': post.subject,
            'content': post.content
        })

        self.r(form, post)

    def post(self):
        # make sure the user is who we think
        user = self.validate_user()
        if user is None:
            self.invalidate_sig()
            self.redirect('/user/login', True)
            return

        form = PostEditForm(self.request.params)

        # get the post please
        post = Key(urlsafe=form.key.data).get()
        if post is None:
            self.r(flashes=flash('Post does not exist'))
            return

        # check if the user is the owner or not
        if post.author != user:
            self.redirect('/', True)
            return

        # validate form
        if not form.validate():
            self.r(form)
            return

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again.'))
            return

        try:
            # let's update the post
            t = form.title.data
            t = re.sub(r'[\!\@\#\$\%\^\&\*\-_=\+\?<>,\.\"\':;\{\}\[\]|\\~\/`]', '', t)
            post.title = t
            post.title_lower = lower(t)
            post.subject = form.subject.data
            post.content = form.content.data
            # going to grab the future object so we can block
            post.put()
            self.redirect('/author/%s' % post.author, True)
            return
        except Exception as e:
            print e.message
            self.r(form)
            return
