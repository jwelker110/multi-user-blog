from lib.wtforms.form import Form
from lib.wtforms.fields.core import StringField
from lib.wtforms.fields.simple import HiddenField
from lib.wtforms import validators


class CommentForm(Form):
    comment = StringField('Comment',
                          [validators.length(max=120, message='Comments must be less than 120 characters.'),
                           validators.required(message='Please enter your message.')])
    csrf_token = HiddenField()
