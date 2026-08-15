from flask import Blueprint, request, jsonify, current_app, session, render_template
from services.chatbot_engine import ChatbotEngine

chatbot_bp = Blueprint('chatbot', __name__)
engine = None


def init_engine():
    """Initialize the chatbot engine. Call this from the app factory within an app context."""
    global engine
    engine = ChatbotEngine()


@chatbot_bp.route('/chatbot')
def chatbot_ui():
    return render_template('chatbot.html')


@chatbot_bp.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json or {}
    question = data.get('question', '').strip()
    user_id = session.get('user_id')
    if not question:
        return jsonify({'error': 'Empty question'}), 400
    global engine
    if engine is None:
        init_engine()
    result = engine.answer(question)
    # Save chat
    from models.chat import ChatHistory, UnansweredQuestion
    from extensions import db
    chat = ChatHistory(user_id=user_id, question=question, answer=result.get('answer'), category=result.get('category'), confidence=result.get('confidence'))
    db.session.add(chat)
    # If low confidence, store unanswered
    if not result.get('matched'):
        ua = UnansweredQuestion(user_id=user_id, question=question)
        db.session.add(ua)
    db.session.commit()
    return jsonify(result)


@chatbot_bp.route('/api/faqs', methods=['GET'])
def api_faqs():
    from models.faq import FAQ
    faqs = FAQ.query.all()
    data = [{'id': f.id, 'question': f.question, 'answer': f.answer, 'category': f.category} for f in faqs]
    return jsonify(data)


@chatbot_bp.route('/api/notices', methods=['GET'])
def api_notices():
    from models.notice import Notice
    items = Notice.query.order_by(Notice.published_date.desc()).all()
    data = [{'id': i.id, 'title': i.title, 'description': i.description, 'published_date': str(i.published_date)} for i in items]
    return jsonify(data)


@chatbot_bp.route('/api/departments', methods=['GET'])
def api_departments():
    from models.department import Department
    items = Department.query.all()
    data = [{'id': i.id, 'name': i.name, 'description': i.description} for i in items]
    return jsonify(data)


@chatbot_bp.route('/api/faculty', methods=['GET'])
def api_faculty():
    from models.faculty import Faculty
    items = Faculty.query.all()
    data = [{'id': i.id, 'name': i.name, 'department': i.department, 'subject': i.subject} for i in items]
    return jsonify(data)


@chatbot_bp.route('/api/timetable', methods=['GET'])
def api_timetable():
    from models.timetable import Timetable
    items = Timetable.query.all()
    data = [{'id': i.id, 'department': i.department, 'day': i.day, 'subject': i.subject, 'start_time': i.start_time, 'end_time': i.end_time} for i in items]
    return jsonify(data)
