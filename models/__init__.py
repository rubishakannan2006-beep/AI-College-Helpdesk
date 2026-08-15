from app import db

__all__ = [
    'User', 'FAQ', 'ChatHistory', 'UnansweredQuestion', 'Notice', 'Department', 'Faculty', 'Timetable', 'Contact'
]

from .user import User
from .faq import FAQ
from .chat import ChatHistory, UnansweredQuestion
from .notice import Notice
from .department import Department
from .faculty import Faculty
from .timetable import Timetable
from .contact import Contact
