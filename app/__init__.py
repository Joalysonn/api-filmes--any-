"""Fábrica da aplicação Flask (application factory)."""
import os

from flask import Flask

from app.models import db
from app.routes import bp


def create_app(config=None):
    """Cria e configura a aplicação.

    `config` permite sobrescrever configurações (usado nos testes).
    """
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///filmes.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.ensure_ascii = False

    if config:
        app.config.update(config)

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
