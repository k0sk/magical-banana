from mbanana import db


class NEologd(db.Model):
    __tablename__ = 'neologd'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text, nullable=False)
    pron = db.Column(db.Text, index=True, nullable=False)

    def __repr__(self):
        return '<NEologd id=%i word=%s pron=%s>' % \
            (self.id, self.word, self.pron)

    def init():
        db.create_all()

    def import_entries():
        """Imports entries from the NEologd dictionary.

        Imports entries, specifically nouns and its pronounciation properties,
        from the NEologd dictionary.
        """
        import glob

        exclude_parts = frozenset(['組織', '記号', '代名詞'])
        imported_words = set()

        for filename in glob.glob('lib/mecab-ipadic-neologd/seed/*.csv'):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    entry = line.strip().split(',')

                    if entry[-3] not in imported_words and \
                            len(entry[-3]) <= 10:
                        imported_words.add(entry[-3])

                        if '名詞' in entry and \
                                not exclude_parts.intersection(set(entry)):
                            db.session.add(NEologd(word=entry[-3],
                                                   pron=entry[-2]))
                            db.session.commit()
