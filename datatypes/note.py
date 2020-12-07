from app import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    description = db.Column(db.String(250))
    upload_date = db.Column(db.Date, nullable=False)
    file = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return u'Note [id: %s ' \
               u'author: %s ' \
               u'subject: %s ' \
               u'description: %s ' \
               u'upload_date: %s ' \
               u'file: %s]' % (self.id,
                               self.author,
                               self.subject,
                               self.description,
                               self.upload_date,
                               self.file)
