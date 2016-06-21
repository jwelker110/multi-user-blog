from string import lower

from app.helpers import Helper, flash
from app.forms import PostForm
from app.models import Post, User


temp = 'post_create.html'


class PostCreateHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # make sure we are logged in right meow
        user = self.session.get('user')
        if user is None:
            self.redirect('/user/login', True)
            return

        form = PostForm(data={'csrf_token': self.generate_csrf()})

        self.r(form)

    def post(self):
        # make sure we are logged in right meow
        # validate the cookie itself, since we need to be sure
        # they are who they say they are
        if not self.validate_sig():
            self.invalidate_sig()
            self.redirect('/user/login', True)
            return
        user = self.retrieve_sig_data()

        form = PostForm(self.request.params)

        # validate form
        if not form.validate():
            self.r(form)
            return

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again.'))
            return

        author = User.query(User.username == user).get()
        if author is None:
            self.invalidate_sig()
            self.r(form, flashes=flash('Please sign back in and try again'))
            return
        # check if this post has been created before
        exists = Post.query(Post.title_lower == lower(form.title.data)).get()
        if exists is not None:
            self.r(form, flashes=flash('Your title must be unique.', 'warning'))
            return

        try:
            # let's create the post
            post = Post(
                title=form.title.data,
                title_lower=lower(form.title.data),
                author=author.username,
                subject=form.subject.data,
                content=form.content.data
            )
            post.put()
            self.r(PostForm(data={'csrf_token': self.generate_csrf()}),
                   flashes=flash('Your new post can be viewed <a href="/post/%s/view">here</a>.' % post.title, 'success'))
            return
        except Exception as e:
            print e.message
            self.r(form)
            return



