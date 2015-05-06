from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class NewsForm(Form):

    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    

class UpdatesForm(Form):

    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    

class UserForm(Form):

    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])


class ProjectForm(Form):

    # want to select user from a list
    # user will be PI on project
    # do I even need this?  User will be logged in, can default to that user
    
    name = StringField('name', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])

