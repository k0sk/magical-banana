from flask import Flask
from flask_restful import Resource, Api
from gensim.models import Word2Vec
from mbanana.resources.mbanana import MBanana

app = Flask(__name__)
api = Api(app)

w2v = Word2Vec.load('mbanana/w2v/jawiki.model')

api.add_resource(MBanana, '/api/mbanana/', resource_class_args=[w2v])
