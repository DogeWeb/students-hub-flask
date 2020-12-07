from app import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(256), nullable=False)
