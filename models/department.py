from app import db

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    hod = db.Column(db.String(128))
    location = db.Column(db.String(128))
    contact = db.Column(db.String(64))
