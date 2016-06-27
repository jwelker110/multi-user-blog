from string import lower

from google.appengine.ext.ndb import Key

from app.helpers import Helper
from app.models import Comment, Like
from app.forms import CommentForm, LikeForm
from app.models import User

temp = 'post.html'


class PostHandler(Helper):
    def r(self, form=None, like_form=None, post=None, comments=None, liked=None, template=temp, **kw):
        self.render(template, form=form, likeForm=like_form, post=post, comments=comments, liked=liked, **kw)

    def get(self):
        # get the user
        user = self.validate_user()
        # we have the user and need to access their key to see if they liked the post
        # if they are not signed in then we don't show if they liked or not
        if user is not None:
            user = User.query(User.username == user).get()
            if user is not None:
                user = user.key

        # get the post key
        k = self.request.get('key', None)
        if k is None:
            self.redirect('/')
            return

        # create our form data for likes/comments
        formData = {
            'key': k,
            'csrf_token': self.generate_csrf()
        }

        # create our comment form
        form = CommentForm(data=formData)
        # create our like form
        like_form = LikeForm(data=formData)

        # try to retrieve the post based on the key
        try:
            post = Key(urlsafe=k).get()
        except:
            post = None

        # don't have the comments yet, or likes
        comments = None
        liked = None
        if post is not None:
            # grab the comments please
            comments = Comment.query(ancestor=post.key).order(-Comment.created).fetch()
            # grab likes
            # we also need to see if this user has "liked" the post already
            liked = Like.query(Like.owner == user, Like.post == post.key).get()
        self.r(form, like_form, post, comments, liked)
