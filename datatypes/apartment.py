from app import db


class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), nullable=False)
