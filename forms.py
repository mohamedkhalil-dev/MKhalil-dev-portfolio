from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, DateTimeField


class AddProjectForm(FlaskForm):
    name = StringField('project name', validators=[DataRequired()])
    languages = StringField('languages used')
    overview = StringField('overview', validators=[DataRequired()])
    client = StringField('client name', validators=[DataRequired()])
    website = StringField('website')
    github_url = StringField('github url')
    rating = StringField('rating')
    date = DateField('date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    challenge = StringField('challenge')
    solution = StringField('solution')
    img_url = StringField('main image', validators=[DataRequired()])
    challenge_img_url = StringField('challenge image')
    submit = SubmitField("Add project")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in")
