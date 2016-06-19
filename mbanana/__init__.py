from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object('mbanana.config')
CORS(app)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from gensim.models import Word2Vec
w2v = Word2Vec.load('mbanana/w2v/jawiki.model')

from mbanana.api.mbanana import MBanana
api = Api(app)
api.add_resource(MBanana, '/api/', resource_class_args=[w2v])
