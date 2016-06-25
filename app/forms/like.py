from lib.wtforms.form import Form
from lib.wtforms.fields.simple import HiddenField


class LikeForm(Form):
    key = HiddenField()
    csrf_token = HiddenField()
