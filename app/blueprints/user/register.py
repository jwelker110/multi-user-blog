import re
from string import lower

from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash, pw
from app.models import User
from app.forms import RegisterForm

temp = 'user_register.html'


class RegisterHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # make sure we aren't logged in right meow
        user = self.session.get('user')
        if user is not None:
            self.redirect('/')
            return

        # let's set the CSRF token
        token = self.generate_csrf()
        reg_form = RegisterForm(data={'csrf_token': token})
        self.r(reg_form)

    def post(self):
        user = self.session.get('user')
        if user is not None:
            self.redirect('/')
            return

        form = RegisterForm(self.request.params)

        # validate form
        if not form.validate():
            self.r(form)
            return

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again'))
            return

        # check for an existing account
        # using the lowercase username as a key
        # to ensure users are unique
        username = form.username.data
        username = re.sub(r'[\!\@\#\$\%\^\&\*\-_=\+\?<>,\.\"\':;\{\}\[\]|\\~\/`]', '', username)

        try:
            user = Key("User", lower(username)).get()
        except:
            user = None

        # exists = User.query(User.username_lower == lower(form.username.data)).get()
        if user is not None:
            self.r(form, flashes=flash('That username is taken'))
            return

        # create the user
        try:
            user = User(
                username=username,
                password=pw.gen_hash(form.password.data),
            )
            user.key = Key("User", lower(user.username))
            user.put()
            # the user has been created, sign them in
            self.session['user'] = user.username
            # create a hash with our secret so we know the cookie is legit later
            self.generate_sig(user.username)
            self.redirect('/')
            return
        except:  # guess something happened eh?
            self.r(form, flashes=flash())
            return
