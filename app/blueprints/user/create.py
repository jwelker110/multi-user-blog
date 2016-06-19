from string import lower

from app.helpers import Helper, flash, pw
from app.models import User
from app.forms import LoginForm, RegisterForm


class CreateUserHandler(Helper):
    def r(self, login_form=None, register_form=None, template='user_create.html', **kw):
        self.render(template, login_form=login_form, register_form=register_form, **kw)

    def get(self):
        # let's set the CSRF token
        token = self.generate_csrf()
        reg_form = RegisterForm(data={'csrf_token': token})
        log_form = LoginForm(data={'csrf_token': token})
        self.r(log_form, reg_form)

    def post(self):
        reg_form = RegisterForm(self.request.params)
        log_form = LoginForm(data={'csrf_token': reg_form.csrf_token.data})

        # validate form
        if not reg_form.validate():
            self.r(log_form, reg_form)
            return

        # validate csrf
        if not self.validate_csrf(reg_form.csrf_token.data):
            self.r(log_form, reg_form, flashes=flash('Please refresh the page and try again'))
            return

        # check for an existing account
        exists = User.query(User.username == reg_form.username.data).get()
        if exists is not None:
            self.r(log_form, reg_form, flashes=flash('That username is taken'))
            return

        # create the user
        try:
            user = User(
                username=reg_form.username,
                username_lower=lower(reg_form.username),
                password=pw.gen_hash(reg_form.password),
            )

            user.put()
            self.redirect('/', True)
            return
        except:  # guess something happened eh?
            self.r(log_form, reg_form, flashes=flash())
            return
