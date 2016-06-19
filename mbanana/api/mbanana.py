from flask_restful import Resource, reqparse
from mbanana.models.neologd import NEologd
import re
import random
import MeCab

parser = reqparse.RequestParser()
parser.add_argument('q', dest='query')
parser.add_argument('text')


class MBanana(Resource):
    def __init__(self, w2v):
        self.w2v = w2v
        self.username = 'Mr. Magical B.'
        self.text = ''
        self.icon_emoji = ':banana:'

    def get(self):
        args = parser.parse_args()
        self._generate_response(args['query'])

        return {
            'username': self.username,
            'text': self.text,
            'icon_emoji': self.icon_emoji
        }

    def post(self):
        args = parser.parse_args()
        self._generate_response(args['text'])

        return {
            'username': self.username,
            'text': self.text,
            'icon_emoji': self.icon_emoji
            }

    def _generate_response(self, query):
        pat = r'といったら|と言ったら|といえば|と言えば'
        mat = re.search(pat, query)

        if mat is None:
            nouns = self._extract_nouns(query)
        else:
            nouns = self._extract_nouns(query[mat.end():])

        ans_cand = []
        if nouns:
            picked = random.choice(list(nouns.keys()))
            ans_cand += self._get_synonyms(picked)
            ans_cand += self._get_same_pron(picked)

        if ans_cand:
            self.text += '%sといったら%s' % (picked, random.choice(ans_cand))
        else:
            self.text = '君の勝ち！'

    def _extract_nouns(self, query):
        """Extracts nouns from a given query based on Morphological Analysis.

        Returns:
            A dict mapping nouns to its pronounciation. Both nouns and
            pronounciations are represented as string.
        """
        mt = MeCab.Tagger('-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd')
        res = mt.parse(query)

        pat = r'\t|-'
        mat = [re.split(pat, line) for line in res.splitlines()]

        return {s[0]: s[1] for s in mat if '名詞' in s}

    def _get_synonyms(self, word):
        """Get the three most similar words to a given word from the W2V model.

        Returns:
            A list of nouns. Each noun is represented as a string.
        """
        if word in self.w2v:
            sims = self.w2v.most_similar(word, topn=3)
            return [s[0] for s in sims]

        return []

    def _get_same_pron(self, word):
        """Retrieves words that have the same pronounciation as a given word.

        Returns:
            A list of nouns.
        """
        entries = NEologd.query.filter_by(pron=word)
        return [e.word for e in entries]
