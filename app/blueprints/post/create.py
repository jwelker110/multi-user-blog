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
            self.r(form)
            return

        author = User.query(User.username == user).get()
        # check if this post has been created before
        exists = Post.query(Post.title_lower == lower(form.title.data)).get()
        if exists is not None:
            self.r(form, flashes=flash('A post with this title already exists.'))
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
            self.redirect('/post/%s/view' % post.title, True)
            return
        except:
            self.r(form)
            return



