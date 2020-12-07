from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.Integer, db.ForeignKey('university.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return u'Course [id: %s ' \
               u'university: %s ' \
               u'name: %s]' % (self.id,
                               self.university,
                               self.name)
