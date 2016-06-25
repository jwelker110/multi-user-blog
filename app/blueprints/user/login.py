import re
from string import lower

from google.appengine.ext.ndb import Key

from app.helpers import Helper, flash, pw
from app.forms import LoginForm

temp = 'user_login.html'


class LoginHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # make sure we aren't logged in right meow
        user = self.validate_user()
        if user is not None:
            self.redirect('/')
            return

        # let's set the CSRF token
        token = self.generate_csrf()
        reg_form = LoginForm(data={'csrf_token': token})
        self.r(reg_form)

    def post(self):
        user = self.session.get('user')
        if user is not None:
            self.redirect('/')
            return

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
        username = form.username.data
        username = re.sub(r'[\!\@\#\$\%\^\&\*\-_=\+\?<>,\.\"\':;\{\}\[\]|\\~\/`]', '', username)

        try:
            user = Key("User", lower(username)).get()
        except:
            user = None

        if user is None:
            self.r(form, flashes=flash('Could not sign in. Verify username and password are correct and try again.'))
            return

        # check whether passwords are correct or not
        if not pw.is_pw(form.password.data, user.password):
            self.r(form, flashes=flash('Could not sign in. Verify username and password are correct and try again.'))
            return

        # the user exists, sign them in.
        self.session['user'] = user.username
        # create a hash with our secret so we know the cookie is legit later
        self.generate_sig(user.username)
        self.redirect('/')
        return
