from lib.wtforms.form import Form
from lib.wtforms.fields.simple import HiddenField, TextAreaField
from lib.wtforms import validators


class CommentForm(Form):
    comment = TextAreaField('Comment',
                            [validators.length(max=120, message='Comments must be less than 120 characters.'),
                             validators.required(message='Please enter your comment.')])
    key = HiddenField()
    csrf_token = HiddenField()
