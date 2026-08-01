import os
from flask import Flask
from flask_login import LoginManager

from config import Config
from app.models import db, User
from app.routes.auth import auth_bp
from app.routes.projects import projects_bp
from app.routes.documents import documents_bp
from app.routes.chat import chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure required directories exist
    instance_path = os.path.join(Config.BASE_DIR, "instance")
    os.makedirs(instance_path, exist_ok=True)
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.CHROMA_DB_PATH, exist_ok=True)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(documents_bp, url_prefix="/documents")
    app.register_blueprint(chat_bp, url_prefix="/chat")

    with app.app_context():
        db.create_all()

    return app