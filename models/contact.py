from extensions import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(128))
    contact_name = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(128))
    location = db.Column(db.String(128))
