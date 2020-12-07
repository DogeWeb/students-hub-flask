from app import db


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.Integer, db.ForeignKey('user.id'))
    subject = db.Column(db.Integer, db.ForeignKey('subject.id'))
    datetime = db.Column(db.DateTime, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    link = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return u'Meeting [id: %s ' \
               u'host: %s ' \
               u'subject: %s ' \
               u'datetime: %s ' \
               u'creation_date: %s ' \
               u'link: %s ' \
               u'description: %s]' % (self.id,
                                      self.host,
                                      self.subject,
                                      self.datetime,
                                      self.creation_date,
                                      self.link,
                                      self.description)
