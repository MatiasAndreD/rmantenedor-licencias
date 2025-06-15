import os
from flask import Flask, redirect, url_for, g
from flask_sqlalchemy import SQLAlchemy

from .config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()


def create_app():
    """Create and configure the Flask application."""
    env = os.getenv("FLASK_ENV", "development")
    config_class = ProductionConfig if env == "production" else DevelopmentConfig
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from .auth import auth_bp
    from .licencias import licencias_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(licencias_bp)

    @app.route('/')
    def index():
        from .auth import get_current_user

        user = get_current_user()
        if user and user.role == 'admin':
            return redirect(url_for('licencias.listar'))
        elif user and user.role == 'agente':
            return redirect(url_for('licencias.listar'))
        return redirect(url_for('licencias.listar'))

    return app
