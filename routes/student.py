from flask import Blueprint, render_template, session, redirect, url_for

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'STUDENT':
        return redirect(url_for('auth.login'))
    return render_template('student_dashboard.html')


@student_bp.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('chatbot.html')


@student_bp.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('chat_history.html')
