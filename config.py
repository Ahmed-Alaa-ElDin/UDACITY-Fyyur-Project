import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:aaass123@localhost:5432/fyyur'

# basedir.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
