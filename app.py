import sys
from flask import Flask, flash

# When running `python app.py` the module's __name__ is '__main__', but
# other modules import this file as 'app'. Ensure both names point to the
# same module object so extensions (like SQLAlchemy) are not created twice.
if __name__ == '__main__':
    sys.modules.setdefault('app', sys.modules['__main__'])
from flask_migrate import Migrate
from config import Config

from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.chatbot import chatbot_bp
    from routes.student import student_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    # Initialize chatbot engine (needs app context)
    from routes import chatbot as chatbot_module
    with app.app_context():
        try:
            chatbot_module.init_engine()
        except Exception:
            # If engine initialization fails, continue; it will be lazy-loaded on first use
            pass

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
