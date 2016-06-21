from app.helpers import Helper, flash
from app.models import Post

temp = 'index.html'


class DefaultHandler(Helper):
    def r(self, posts=None, offset=0, limit=0, template=temp, **kw):
        self.render(template, posts=posts, offset=offset, limit=limit, **kw)

    def get(self):
        flashes = []
        limit = 20
        offset = self.request.get_range('offset', min_value=0, max_value=100000, default=0)

        # let's get the most recent posts
        posts = Post.query().order(-Post.created).fetch(limit, offset=offset)

        if len(posts) is 0 and offset > 0:
            flashes = flash('No more posts available.')
            offset -= limit
            posts = Post.query().order(-Post.created).fetch(limit, offset=offset)

        self.r(posts, offset, limit, flashes=flashes)


