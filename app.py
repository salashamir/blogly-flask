"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ihaveasecret"

connect_db(app)
db.create_all()

@app.route('/')
def root_page():
    """Redirect to the users list"""
    return redirect('/users')

@app.route('/users')
def users_page():
    """Page with a list displaying all users in database"""
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    """Show form to add a new user to db"""
    return render_template('users/new-user.html')

@app.route('/users/new', methods=["POST"])
def new_user():
    """Get data from form submission and create new user in db"""
    created_user = User(first_name=request.form['first_name'], last_name=request.form['last_name'], image_url=request.form['image_url'] or None)

    db.session.add(created_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Display details of user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/user-details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Display a form allowing the person to edit user details"""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    """Deal with edit form submission and update the user info"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deal with form submission and delete the user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

