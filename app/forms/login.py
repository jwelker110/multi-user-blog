from lib.wtforms.form import Form
from lib.wtforms.fields.core import StringField
from lib.wtforms.fields.simple import PasswordField, HiddenField
from lib.wtforms import validators


class LoginForm(Form):
    username = StringField('Username',
                           [validators.Length(min=5, max=15, message='Username must be 5-15 chars'),
                            validators.required()])
    password = PasswordField('Password',
                             [validators.length(min=8, max=30, message='Password must be 8-30 chars'),
                              validators.required()])
    csrf_token = HiddenField()
