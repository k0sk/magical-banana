from flask_restful import Resource, reqparse
import re
import random
import MeCab

parser = reqparse.RequestParser()
parser.add_argument('q', dest='query')


class MBanana(Resource):
    def __init__(self, w2v):
        self.w2v = w2v
        self.text = ''
        self.ans_cand = []

    def get(self):
        args = parser.parse_args()
        self._generate_response(args['query'])

        return {
            'username': 'Banana',
            'text': self.text,
            'icon_emoji': ':banana:'
        }

    def _generate_response(self, query):
        pat = r'といったら|と言ったら|といえば|と言えば'
        mat = re.search(pat, query)

        if mat is None:
            self.text = 'マジカルバナナやろうよ！'
            nouns = self._extract_nouns(query)
        else:
            nouns = self._extract_nouns(query[mat.end():])

        if nouns:
            picked = random.choice(nouns)
            self._get_synonyms(picked)

        if self.ans_cand:
            self.text += '%sといったら%s' % (picked, random.choice(self.ans_cand))
        else:
            self.text = '君の勝ち！'

    def _extract_nouns(self, query):
        mt = MeCab.Tagger('-Ochasen')
        res = mt.parse(query)

        pat = r'\t|-'
        mat = [re.split(pat, line) for line in res.splitlines()]

        return [s[0] for s in mat if '名詞' in s]

    def _get_synonyms(self, word):
        if word in self.w2v:
            sims = self.w2v.most_similar(word, topn=3)
            self.ans_cand += [s[0] for s in sims]
