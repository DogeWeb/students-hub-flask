from app import db


class NoteRating(db.Model):
    user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    note = db.Column(db.Integer, db.ForeignKey('note.id'), primary_key=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return u'NoteRating [user: %s ' \
               u'note: %s' \
               u'rating: %s]' % (self.user,
                                 self.note,
                                 self.rating)
