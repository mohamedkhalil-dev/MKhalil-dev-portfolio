# Phase-1
# 1-TODO select and download website template
# 2-TODO adjust template in "static" & "templates" forlders and relocating the files in new folder locations
# 3-TODO import flask and render the pages with route decorator
# 4-TODO creating a header and footer html files including it using flask(ninja) instead of duplicating their codes in each file
# 5-TODO customizing the fonts/bg colors and adding new pics to the template
# 7-TODO Rendering portfolio projects using JINJA2 inside html files
# 8-TODO Creating env variables to store passwords
# 9-TODO using the .gitignore while comitting the files to git and uploading to github
# 10-TODO Deploying to heruku

# Phase-2
# 11-TODO Adding a login feature with Authentication and hashing password
# 11-TODO Adding an Add-Project feature from the website itself
# 12-TODO Activating blog pages
# 11-TODO Adding an Add-blog feature from the website itself


from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
import random
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from forms import AddProjectForm, LoginForm
from dotenv import load_dotenv
import requests

response = requests.get(url='https://api.github.com/users/Tic-Tac-Toe/starred')

load_dotenv()

QUOTES = [
    "Programming isn't about what you know; it's about what you can figure out. - Chris Pine",
    "The only way to learn a new programming language is by writing programs in it. - Dennis Ritchie",
    "The most damaging phrase in the language is.. it's always been done this way - Grace Hopper",
    "Don't write better error messages, write code that doesn't need them. - Jason C. McDonald"
]
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)
# 11-TODO Adding a login feature with flask-login
login_manager = LoginManager()
login_manager.init_app(app=app)

# 6-TODO Adding sqlalchemy db for portfolio projects
##Connecting to db
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///projects.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Creating github api function
def get_github_repo_stars_count(link):
    """
        split github url, grab project name then use the github api to get the project's stats
        return stars int type
    """
    headers = {
        'USERNAME': os.getenv('GITHUB_TOKEN')
    }
    project_name = link.split('https://github.com/mohamedkhalil-dev/')[1]
    response = requests.get(url='https://api.github.com/users/mohamedkhalil-dev/repos', headers=headers)
    data = response.json()
    for repos in data:
        if repos["name"] == project_name:
            stars_count = repos["stargazers_count"]
            return stars_count


##Creating db for portfolio projects
class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    languages = db.Column(db.String(50))
    overview = db.Column(db.String(250), nullable=False)
    client = db.Column(db.String(50))
    website = db.Column(db.String(100))
    github_url = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String)
    date = db.Column(db.DateTime)
    description = db.Column(db.Text, nullable=False)
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    img_url = db.Column(db.String(250), nullable=False)
    challenge_img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Skill(UserMixin, db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    name = db.Column(db.String(50))


# app.app_context().push()


# with app.app_context():
#     db.create_all()


# new_project = Projects(
#     name="Phone new",
#     overview="this is an overview",
#     rating=9,
#     date=datetime(year=2002, month=11, day=3),
#     github_url="https://github.com/mohamedkhalil-dev",
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     img_url="https://scoutlife.org/wp-content/uploads/2007/02/morsecode-1.jpg",
#     challenge_img_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKVxQ78Og8XPDvmao18jrzMsnnaNGkZwh1iQ&usqp=CAU"
# )
# with app.app_context():
#     db.session.add(new_project)


# new_skill = Skill(
#     category='1',
#     name='11'
# )
# with app.app_context():
#     db.session.add(new_skill)
# with app.app_context():
#     db.session.commit()

# SKILLS_list = {
#                 'Back-end': ['Python 3', 'Flask', 'Selenium Webdriver','Data Structures', 'Algorithms','Beautiful soup', 'Request', 'WTForms',  'Pandas', 'Numpy', 'Matplotlib', 'Rest', 'SQLite', 'Plotly', 'API','Authentication'],
#                 'Front-end': ['HTML5', 'CSS', 'Bootstrap'],
#                 'Graphic design': ['Adobe Photoshop', 'Adobe Illustrator', 'Adobe Indesign']
#               }


# with app.app_context():
#     db.session.add(new_project)
# with app.app_context():
#     db.session.add(new_user)
# with app.app_context():
#     db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/')
def home():
    all_skills = Skill.query.all()
    all_projects = Projects.query.all()
    random_quote = random.choice(QUOTES)
    return render_template('index.html', skills=all_skills, projects=all_projects, quote=random_quote)


@app.route('/add-project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = AddProjectForm()
    if form.validate_on_submit():
        new_project = Projects(
            name=form.name.data,
            client=form.client.data,
            overview=form.overview.data,
            rating=form.rating.data,
            website=form.website.data,
            languages=form.languages.data[0],
            date=form.date.data,
            description=form.description.data,
            challenge=form.challenge.data,
            solution=form.solution.data,
            github_url=form.github_url.data,
            img_url=form.img_url.data,
            challenge_img_url=form.challenge_img_url.data,
        )

        db.session.add(new_project)
        db.session.commit()

    return render_template('add-project.html', form=form, logged_in=current_user.is_authenticated)


@app.route("/delete/<int:project_id>")
@login_required
def delete_project(project_id):
    project_to_delete = Projects.query.get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/edit-project/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Projects.query.get(project_id)
    edit_form = AddProjectForm(
        name=project.name,
        client=project.client,
        overview=project.overview,
        rating=project.rating,
        website=project.website,
        languages=project.languages,
        date=project.date,
        description=project.description,
        challenge=project.challenge,
        solution=project.solution,
        github_url=project.github_url,
        img_url=project.img_url,
        challenge_img_url=project.challenge_img_url,
    )
    if edit_form.validate_on_submit():
        project.name = edit_form.name.data
        project.client = edit_form.client.data
        project.overview = edit_form.overview.data
        project.rating = edit_form.rating.data
        project.website = edit_form.website.data
        project.languages = edit_form.languages.data[0]
        project.date = edit_form.date.data
        project.description = edit_form.description.data
        project.challenge = edit_form.challenge.data
        project.solution = edit_form.solution.data
        project.github_url = edit_form.github_url.data
        project.img_url = edit_form.img_url.data
        project.challenge_img_url = edit_form.challenge_img_url.data

        db.session.commit()
        return redirect(url_for("show_project", project_id=project.id))

    return render_template("add-project.html", form=edit_form, logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    """"
    if user is logged-in > will be directed to home-screen
    // if user is logged-out > will be directed to login-screen
    """
    # redirecting user to home if logged-in
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    else:
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data

            user_to_check = User.query.filter_by(email=email).first()

            if user_to_check and form.password.data == ADMIN_PASSWORD:
                login_user(user_to_check)
                return redirect(url_for("add_project"))

            elif not user_to_check:
                flash("This email is not registered")
                return redirect(url_for("login"))
            else:
                flash("This password is incorrect")
                return redirect(url_for("login"))

        return render_template("admin.html", form=form, logged_in=current_user.is_authenticated)


@app.route('/about')
def about():
    all_skills = Skill.query.all()
    return render_template('about-us.html', skills=all_skills)


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/portfolio')
def portfolio():
    all_projects = Projects.query.all()
    return render_template('portfolio.html', projects=all_projects)


@app.route('/project-details/<int:project_id>', methods=["GET", "Post"])
def show_project(project_id):
    requested_project = Projects.query.get(project_id)
    project_github_url = requested_project.github_url

    github_stars = get_github_repo_stars_count(project_github_url)
    print(github_stars)
    return render_template('portfolio-details.html', project=requested_project, github_stars=github_stars)


# @app.route('/portfolio-details')
# def portfolio_details():
#     return (render_template('portfolio-details.html'))

@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/single-blog')
def single_blog():
    return render_template('single-blog.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
