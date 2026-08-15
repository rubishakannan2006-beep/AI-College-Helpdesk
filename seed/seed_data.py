import os
import sys
from datetime import date

# Ensure project root is on sys.path so imports like `from app import create_app` work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import create_app, db
from models.user import User
from models.faq import FAQ
from models.department import Department
from models.faculty import Faculty
from models.notice import Notice
from models.timetable import Timetable
from models.contact import Contact

def seed():
    app = create_app()
    from extensions import db
    with app.app_context():
        db.create_all()
        # Default admin
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@college.edu')
        admin_pwd = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if not User.query.filter_by(email=admin_email).first():
            admin = User(name='Administrator', email=admin_email, role='ADMIN')
            admin.set_password(admin_pwd)
            db.session.add(admin)

        # Sample departments
        deps = ['Computer Science','Mechanical','Civil','Electronics']
        for d in deps:
            if not Department.query.filter_by(name=d).first():
                db.session.add(Department(name=d, description=f'{d} dept'))

        # Sample FAQ (30 minimal entries)
        sample_faqs = [
            ('What is the library timing?','The library is open from 9:00 AM to 5:00 PM.','Library'),
            ('How to apply for admission?','Visit the admissions office or apply online via the college website.','Admission'),
            ('What are the exam dates?','Exam dates are published on the academic calendar and notices.','Examination'),
            ('How can I pay fees?','Fees can be paid online or at the accounts office.','Fees'),
            ('What is the attendance policy?','Students must maintain 75% attendance to be eligible for exams.','Attendance'),
        ]
        # Duplicate variations to reach ~30
        for i, (q,a,c) in enumerate(sample_faqs*6):
            if i>29: break
            if not FAQ.query.filter_by(question=q).first():
                db.session.add(FAQ(question=q, answer=a, category=c))

        # Notices
        if not Notice.query.first():
            db.session.add(Notice(title='Welcome Back', description='Semester begins next week', category='General', published_date=date.today()))

        # Faculty
        if not Faculty.query.first():
            db.session.add(Faculty(name='Dr. A. Kumar', department='Computer Science', subject='AI', email='akumar@college.edu', room='CS101'))

        # Contacts
        if not Contact.query.first():
            db.session.add(Contact(department='Admin', contact_name='Office', phone='0123456789', email='office@college.edu'))

        db.session.commit()
        print('Seed data inserted')

if __name__ == '__main__':
    seed()
