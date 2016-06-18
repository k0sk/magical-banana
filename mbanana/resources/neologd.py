from mbanana import db


class NEologd(db.Model):
    __tablename__ = 'neologd'
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.Text, unique=True, nullable=False)
    pron = db.Column(db.Text, index=True, nullable=False)

    def __repr__(self):
        return '<NEologd id=%i word=%s pron=%s>' %
        (self.id, self.word, self.pron)

    def init():
        db.create_all()
