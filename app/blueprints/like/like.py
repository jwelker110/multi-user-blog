from google.appengine.ext.ndb import Key

from app.helpers import Helper, user_required
from app.forms import LikeForm
from app.models import Like, User


class LikeHandler(Helper):
    @user_required()
    def post(self, user):
        # grab the form
        form = LikeForm(self.request.params)
        username = user

        # grab the user (for their key)
        user = User.query(User.username == username).get()

        if user is None:
            self.redirect('/user/login')
            return

        # grab the post via what should be it's key
        try:
            post = Key(urlsafe=form.key.data).get()
        except Exception as e:
            post = None

        if post is None:
            self.redirect('/')
            return

        # is the post liked by this user already?
        try:
            liked = Like.query(Like.owner == user.key, Like.post == Key(urlsafe=form.key.data)).get()
        except Exception as e:
            print e.message
            liked = None

        # let's set the Like entity up and like the post
        try:
            if liked is None:  # hasn't been liked yet
                liked = Like(
                    owner=user.key,
                    post=Key(urlsafe=form.key.data),
                    liked=True
                )
                liked.put()
            else:
                liked.liked = True if liked.liked is False else False
                liked.put()

            # inc/dec the post likes
            if liked.liked is True:
                post.likes += 1
            else:
                post.likes -= 1

            post.put()
            # go back to the post!
            self.redirect('/post/view?key=%s' % post.key.urlsafe())
            return
        except Exception as e:
            # go back to the post even if we fail to like it
            self.redirect('/post/view?key=%s' % post.key.urlsafe())
            return
