from datetime import datetime
from extensions import db

class Notice(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(64))
    published_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
