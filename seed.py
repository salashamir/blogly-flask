"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
shaun = User(first_name='Shaun', last_name="Watson")
mark = User(first_name='Mark', last_name="Melanson")
joshua = User(first_name='Joshua', last_name="Kyrlenko")
olga = User(first_name='Olga', last_name="Tipson")

# Add new objects to session, so they'll persist
db.session.add(shaun)
db.session.add(mark)
db.session.add(joshua)
db.session.add(olga)

# Commit--otherwise, this never gets saved!
db.session.commit()