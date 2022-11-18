from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, DateTimeField


class AddProjectForm(FlaskForm):
    name = StringField('project name', validators=[DataRequired()])
    languages = StringField('languages used')
    overview = StringField('overview', validators=[DataRequired()])
    client = StringField('client name', validators=[DataRequired()])
    website = StringField('website')
    github_url = StringField('github url')
    rating = StringField('rating', validators=[DataRequired()])
    date = DateField('date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    challenge = StringField('challenge', validators=[DataRequired()])
    solution = StringField('solution', validators=[DataRequired()])
    img_url = StringField('main image', validators=[DataRequired()])
    challenge_img_url = StringField('challenge image', validators=[DataRequired()])
    submit = SubmitField("Add project")