from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.faq import FAQ
from app import db
from flask import current_app
from .nlp_processor import preprocess

class ChatbotEngine:
    def __init__(self):
        self.reload()

    def reload(self):
        faqs = FAQ.query.all()
        self.questions = [f.question for f in faqs]
        self.answers = [f.answer for f in faqs]
        self.categories = [f.category for f in faqs]
        self.vectorizer = TfidfVectorizer()
        if self.questions:
            corpus = [preprocess(q) for q in self.questions]
            self.tfidf = self.vectorizer.fit_transform(corpus)
        else:
            self.tfidf = None

    def answer(self, question):
        qproc = preprocess(question)
        if self.tfidf is None:
            return {'answer': "No FAQs available.", 'category': None, 'confidence': 0.0, 'matched': False, 'suggestions': []}
        qvec = self.vectorizer.transform([qproc])
        sims = cosine_similarity(qvec, self.tfidf)[0]
        best_idx = sims.argmax()
        best_score = float(sims[best_idx])
        threshold = current_app.config.get('CHAT_CONFIDENCE_THRESHOLD', 0.35)
        matched = best_score >= threshold
        suggestions = []
        # top 3 suggestions
        top_idxs = sims.argsort()[::-1][:3]
        for i in top_idxs:
            suggestions.append(self.questions[i])
        return {
            'answer': self.answers[best_idx] if matched else "Sorry, I couldn't find an accurate answer to your question.",
            'category': self.categories[best_idx] if matched else None,
            'confidence': best_score,
            'matched': bool(matched),
            'suggestions': suggestions
        }
