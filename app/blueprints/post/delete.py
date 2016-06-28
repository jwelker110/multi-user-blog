from google.appengine.ext.ndb import Key, put_multi, delete_multi

from app.helpers import Helper, flash, user_required
from app.forms import PostDeleteForm
from app.models import Comment, Like

temp = 'post_delete.html'


class PostDeleteHandler(Helper):
    def r(self, form=None, post=None, template=temp, **kw):
        self.render(template, form=form, post=post, **kw)

    @user_required()
    def get(self, user):
        # grab title from URL
        k = self.request.get('key', None)

        # no key? no problem
        if k is None:
            self.redirect('/')
            return

        # does the post actually exist??
        post = Key(urlsafe=k).get()
        if post is None:
            self.redirect('/')
            return

        # the post exists, is it owned by the user?
        if post.author != user:
            self.redirect('/')
            return

        # owned by user and exists. Good.
        form = PostDeleteForm(data={
            'csrf_token': self.generate_csrf(),
            'key': post.key.urlsafe()
        })

        self.r(form, post)

    @user_required()
    def post(self, user):
        # grab the form
        form = PostDeleteForm(self.request.params)

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again.'))
            return

        # get the post please
        try:
            post = Key(urlsafe=form.key.data).get()
        except:
            post = None

        # as usual, this really shouldn't
        # be None unless unnatural navigation
        if post is None:
            self.redirect('/')
            return

        # the post exists, is it owned by the user?
        if post.author != user:
            self.redirect('/')
            return

        # check if the user is the owner or not
        if post.author != user:
            self.redirect('/')
            return

        # everything checks out so let's remove the post
        # first though, we need to remove the comments
        # assoc with the post and the likes
        # TODO query these entities to make sure they are removed
        comments = Comment.query(ancestor=post.key).fetch()
        ks = put_multi(comments)
        delete_multi(ks)

        likes = Like.query(Like.post == post.key).fetch()
        ks = put_multi(likes)
        delete_multi(ks)

        # got everything else removed, let's
        # remove the post
        try:
            post.key.delete()
            self.redirect('/')
            return
        except Exception as e:
            # let them try again
            form.csrf_token.data = self.generate_csrf()
            self.r(form, post, flashes=flash())
            return
