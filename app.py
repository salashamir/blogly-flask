"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "ihaveasecret"

connect_db(app)
db.create_all()

# error handling route
@app.errorhandler(404)
def page_404(e):
    "Display our 404 template"
    return render_template('404-not-found.html'), 404

# root
@app.route('/')
def root_page():
    """Root route will show list of posts with most recent first"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(6).all()
    return render_template('/posts/home.html', posts=posts)

# USER ROUTES
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
    flash('New user added!')

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


# POST ROUTES
@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Show post details page"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post-details.html', post=post)

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """Display a form to create a new post for one user"""
    user = User.query.get_or_404(user_id)
    return render_template('posts/new-post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
    """Deal with submitted form to create a new post"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'], content=request.form['content'], user_id=user_id)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post {new_post.title} added.")

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deal with post deletion"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash("Post deleted")

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """Form to edit post"""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def submit_edit(post_id):
    """Form to edit post"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash("Post edited.")

    return redirect(f'/posts/{post_id}')

