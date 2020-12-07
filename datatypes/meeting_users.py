from app import db


class MeetingUsers(db.Model):
    meeting = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
