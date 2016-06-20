from string import lower

from app.helpers import Helper
from app.models import Post, Comment
from app.forms import CommentForm

temp = 'post.html'


class PostHandler(Helper):
    def r(self, form=None, post=None, comments=None, template=temp, **kw):
        self.render(template, form=form, post=post, comments=comments, **kw)

    def get(self):
        title = self.request.path.split('/')[2]
        print title

        form = CommentForm(data={'csrf_token': self.generate_csrf()})

        post = Post.query(Post.title_lower == lower(title)).get()
        comments = None
        if post is not None:
            comments = Comment.query(ancestor=post.key).fetch()
        self.r(form, post, comments)
