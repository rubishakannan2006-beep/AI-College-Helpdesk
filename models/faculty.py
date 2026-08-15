from app import db

class Faculty(db.Model):
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    department = db.Column(db.String(128))
    subject = db.Column(db.String(128))
    email = db.Column(db.String(128))
    room = db.Column(db.String(64))
