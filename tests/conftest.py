"""Fixtures compartilhadas pelos testes."""
import pytest

from app import create_app
from app.models import db


@pytest.fixture
def app():
    # Cada teste usa um banco SQLite em memória, limpo e isolado.
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def filme_criado(client):
    """Cria um filme e devolve o JSON retornado pela API."""
    resposta = client.post("/filmes", json={
        "titulo": "Central do Brasil",
        "ano": 1998,
        "genero": "Drama",
        "nota": 9.1,
    })
    return resposta.get_json()
