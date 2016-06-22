from lib.wtforms.form import Form
from lib.wtforms.fields.core import StringField
from lib.wtforms.fields.simple import TextAreaField, HiddenField
from lib.wtforms import validators


class PostForm(Form):
    title = StringField('Title',
                        [validators.length(max=50, message='Titles must not exceed 50 chars.'),
                         validators.required(message='Please enter a title.')])
    subject = StringField('Subject',
                          [validators.length(max=100, message='Subject must not exceed 100 chars.')])
    content = TextAreaField('Content',
                            [validators.length(max=1800, message='Content must not exceed 1,800 chars.'),
                             validators.required(message='Please enter some content for the post.')])
    csrf_token = HiddenField()


class PostEditForm(Form):
    title = StringField('Title',
                        [validators.length(max=50, message='Titles must not exceed 50 chars.'),
                         validators.required(message='Please enter a title.')])
    subject = StringField('Subject',
                          [validators.length(max=100, message='Subject must not exceed 100 chars.')])
    content = TextAreaField('Content',
                            [validators.length(max=1800, message='Content must not exceed 1,800 chars.'),
                             validators.required(message='Please enter some content for the post.')])
    key = HiddenField()
    csrf_token = HiddenField()
