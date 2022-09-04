"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# Add pets
shaun = User(first_name='Shaun', last_name="Watson")
mark = User(first_name='Mark', last_name="Melanson")
joshua = User(first_name='Joshua', last_name="Kyrlenko")
olga = User(first_name='Olga', last_name="Tipson")
demetri = User(first_name='Demetri', last_name="Martin")
svetlana = User(first_name='Svetlana', last_name="Kuznetsova")

# Add new objects to session, so they'll persist
db.session.add(shaun)
db.session.add(mark)
db.session.add(joshua)
db.session.add(olga)
db.session.add(demetri)
db.session.add(svetlana)

# Commit--otherwise, this never gets saved!
db.session.commit()

# add new posts
post1 = Post(title="Shaun's Post", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", user_id=1)
post2 = Post(title="Shaun's 2nd Post", content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum./n Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", user_id=1)
post3 = Post(title="Olga's Post", content="THERE JUST ISN'T MUCH HERE BECAUSE OLGA HAS DIFFICULTY WRITING IN ENGLISH. WIEUFNERIFEURFBEURYFBUEBYFUEBRFUERBFUREBFUERYFBUEYFYERFUBEURFBERFBEUBRYFEF.", user_id=4)
post4 = Post(title="Demetri's Post", content="Hi, my name is Demetri and I'm a comedian.", user_id=5)
post5 = Post(title="Demetri's 2nd Post", content="I'm still here. Idk what to really write since I'm new to this website", user_id=5)
post6 = Post(title="Svetlana's Post", content="MOTHER RUSSIA.", user_id=6)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)

db.session.commit()