from string import lower
from hashlib import sha256

from app.helpers import Helper, flash, pw, SECRET
from app.models import User
from app.forms import LoginForm

temp = 'user_login.html'


class LoginHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # let's set the CSRF token
        token = self.generate_csrf()
        reg_form = LoginForm(data={'csrf_token': token})
        self.r(reg_form)

    def post(self):
        form = LoginForm(self.request.params)

        # validate form
        if not form.validate():
            self.r(form)
            return

        # validate csrf
        if not self.validate_csrf(form.csrf_token.data):
            form.csrf_token.data = self.generate_csrf()
            self.r(form, flashes=flash('Please submit the form again'))
            return

        # check whether user account exists
        exists = User.query(User.username_lower == lower(form.username.data)).get()
        if exists is None:
            self.r(form, flashes=flash('Could not sign in. Verify username and password are correct and try again.'))
            return

        # the user exists, sign them in.
        self.session['user'] = exists.username
        # create a hash with our secret so we know the cookie is legit later
        sig = self.generate_sig(exists.username)
        self.response.set_cookie('user', sig)
        self.redirect('/')
        return
