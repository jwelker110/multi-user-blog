from urllib import unquote
from string import lower

from app.helpers import Helper, flash
from app.models import Post

temp = 'user_post.html'


class AuthorHandler(Helper):
    def r(self, posts=None, offset=0, limit=0, title='Author\'s', template=temp, **kw):
        self.render(template, posts=posts, offset=offset, limit=limit, title=title, **kw)

    def get(self):
        flashes = []
        limit = 20
        offset = self.request.get_range('offset', min_value=0, max_value=100000, default=0)
        user = self.request.path.split('/')[2]
        user = unquote(user)

        # let's get the most recent posts
        posts = Post.query(Post.author_lower == lower(user)).order(-Post.created).fetch(limit, offset=offset)

        if len(posts) is 0 and offset > 0:
            flashes = flash('No more posts available.')
            offset -= limit
            posts = Post.query().order(-Post.created).fetch(limit, offset=offset)

        self.r(posts, offset, limit, user, flashes=flashes)
