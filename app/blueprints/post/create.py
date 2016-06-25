from string import lower
import re

from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash
from app.forms import PostForm
from app.models import Post


temp = 'post_create.html'


class PostCreateHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # make sure we are logged in right meow
        user = self.session.get('user')
        if user is None:
            self.redirect('/user/login')
            return

        form = PostForm(data={'csrf_token': self.generate_csrf()})

        self.r(form)

    def post(self):
        # make sure we are logged in right meow
        user = self.validate_user()
        if user is None:
            self.redirect('/user/login')
            return

        form = PostForm(self.request.params)

        # check if the person exists in the db or not
        try:
            user = Key("User", lower(user)).get()
        except:
            user = None

        # author = User.query(User.username_lower == lower(user)).get()
        if user is None:
            self.invalidate_sig()
            self.redirect('/user/login')
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

        t = form.title.data
        t = re.sub(r'[\!\@\#\$\%\^\&\*\-_=\+\?<>,\.\"\':;\{\}\[\]|\\~\/`]', '', t)

        try:
            # let's create the post
            post = Post(
                title=t,
                title_lower=lower(t),
                author=user.username,
                author_lower=lower(user.username),
                subject=form.subject.data,
                content=form.content.data
            )
            post.put()
            self.r(PostForm(data={'csrf_token': self.generate_csrf()}),
                   flashes=flash('Your new post can be viewed <a href="/post/view?key=%s">here</a>.' % post.key.urlsafe(), 'success'))
            return
        except Exception as e:
            print e.message
            self.r(form)
            return



