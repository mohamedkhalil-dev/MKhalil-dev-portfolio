from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields import DateField, SelectMultipleField
from flask_ckeditor import CKEditorField


#
SKILLS = ['Python 3', 'Flask', 'Selenium Webdriver', 'Data Structures', 'Algorithms', 'Beautiful soup', 'Request',
          'WTForms', 'HTML5',
          'CSS', 'Bootstrap', 'Pandas', 'Numpy', 'Matplotlib', 'Rest', 'SQLite', 'Plotly', 'API',
          'Authentication', 'Adobe Photoshop', 'Adobe Illustrator', 'Adobe Indesign']


class AddProjectForm(FlaskForm):
    name = StringField('project name', validators=[DataRequired()])
    languages = SelectMultipleField('languages used', choices=SKILLS)
    overview = StringField('overview', validators=[DataRequired()])
    client = StringField('client name', validators=[DataRequired()])
    website = StringField('website')
    github_url = StringField('github url')
    rating = StringField('rating')
    date = DateField('date', format='%Y-%m-%d', validators=[DataRequired()])
    description = CKEditorField('description', validators=[DataRequired()])
    challenge = CKEditorField('challenge')
    solution = CKEditorField('solution')
    img_url = StringField('main image', validators=[DataRequired()])
    challenge_img_url = StringField('challenge image')
    submit = SubmitField("Add project")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in")
