from extensions import db

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(128))
    semester = db.Column(db.String(32))
    day = db.Column(db.String(16))
    subject = db.Column(db.String(128))
    faculty = db.Column(db.String(128))
    room = db.Column(db.String(64))
    start_time = db.Column(db.String(16))
    end_time = db.Column(db.String(16))
