from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e1cfafbd5b656ad9dc64d86a942691d4'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Blogger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.username}', '{self.email}', '{self.image_file}"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('blogger.id'),
                        nullable=False)

    def __repr__(self):
        return f"{self.title}', '{self.date_posted}"


posts = [{
    "author": "Masila David Mwendwa",
    "title": "Blog post 1",
    "content": "First post content",
    "date_posted": "October 6 2022"
}, {
    "author": "Titus Masila",
    "title": "Blog post 2",
    "content": "Second post content",
    "date_posted": "October 28 2022"
}]


@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Welcome, {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.email.data == "masila@flask.com" and form.password.data == "wossup":
        flash(f"Welcome back!", "success")
        return redirect(url_for('home'))
    else:
        flash(f"Login unsuccesful. Please check your login details", "danger")
    return render_template("login.html", title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)