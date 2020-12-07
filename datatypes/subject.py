from app import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return u'Subject [id: %s ' \
               u'course: %s ' \
               u'name: %s]' % (self.id,
                               self.course,
                               self.name)

