import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///databases/neologd.db'
SECRET_KEY = os.environ['DB_SECRET_KEY']
SQLALCHEMY_TRACK_MODIFICATIONS = False
