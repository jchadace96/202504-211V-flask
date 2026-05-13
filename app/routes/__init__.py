from flask import Flask
from app.routes.post import post_bp
from app.routes.comment import comments_bp
from app.routes.base import base_bp
from app.routes.user import user_bp
from app.database import close_db_connection

def create_app():
    app = Flask(__name__)

    app.teardown_appcontext(close_db_connection)

    # Registrar Blueprints
    app.register_blueprint(base_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(user_bp)

    return app
