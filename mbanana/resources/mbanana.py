from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()
parser.add_argument('q', dest='query')


class MBanana(Resource):
    def __init__(self, w2v):
        self.w2v = w2v
        self.text = 'マジカルバナナやろうよ！'

    def get(self):
        args = parser.parse_args()

        if args['query'] in self.w2v:
            synonym = self.w2v.most_similar(args['query'])
            self.text = synonym[0][0]
        else:
            self.text = '君の勝ち！'

        return {
            'username': 'Banana',
            'text': self.text,
            'icon_emoji': ':banana:'
        }
