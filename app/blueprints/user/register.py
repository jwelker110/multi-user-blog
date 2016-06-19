from string import lower

from app.helpers import Helper, flash, pw
from app.models import User
from app.forms import RegisterForm

temp = 'user_register.html'


class RegisterHandler(Helper):
    def r(self, form=None, template=temp, **kw):
        self.render(template, form=form, **kw)

    def get(self):
        # let's set the CSRF token
        token = self.generate_csrf()
        reg_form = RegisterForm(data={'csrf_token': token})
        self.r(reg_form)

    def post(self):
        user = self.request.cookies.get('user')
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
        exists = User.query(User.username == form.username.data).get()
        if exists is not None:
            self.r(form, flashes=flash('That username is taken'))
            return

        # create the user
        try:
            user = User(
                username=form.username,
                username_lower=lower(form.username),
                password=pw.gen_hash(form.password),
            )

            user.put()
            self.redirect('/', True)
            return
        except:  # guess something happened eh?
            self.r(form, flashes=flash())
            return