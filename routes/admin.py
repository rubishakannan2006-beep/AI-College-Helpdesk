from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from models.user import User
from models.faq import FAQ
from models.chat import UnansweredQuestion

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(fn):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'ADMIN':
            flash('Admin login required', 'danger')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper


@admin_bp.route('/login')
def admin_login():
    return redirect(url_for('auth.login'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='STUDENT').count()
    total_faqs = FAQ.query.count()
    total_questions = 0
    unanswered = UnansweredQuestion.query.filter_by(status='pending').count()
    return render_template('admin/dashboard.html', total_students=total_students, total_faqs=total_faqs, unanswered=unanswered)


@admin_bp.route('/faqs')
@admin_required
def faqs():
    q = request.args.get('q')
    if q:
        faqs = FAQ.query.filter(FAQ.question.ilike(f'%{q}%') | FAQ.answer.ilike(f'%{q}%')).all()
    else:
        faqs = FAQ.query.all()
    return render_template('admin/faqs.html', faqs=faqs)


@admin_bp.route('/unanswered')
@admin_required
def unanswered():
    items = UnansweredQuestion.query.filter_by(status='pending').all()
    return render_template('admin/unanswered.html', items=items)


@admin_bp.route('/api/faqs', methods=['POST'])
@admin_required
def api_add_faq():
    from app import db
    data = request.form
    faq = FAQ(question=data.get('question'), answer=data.get('answer'), category=data.get('category'), keywords=data.get('keywords'))
    db.session.add(faq)
    db.session.commit()
    return redirect(url_for('admin.faqs'))
