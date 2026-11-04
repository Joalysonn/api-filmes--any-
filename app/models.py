"""Modelos do banco de dados."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Filme(db.Model):
    __tablename__ = "filmes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(50), nullable=False)
    nota = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "ano": self.ano,
            "genero": self.genero,
            "nota": self.nota,
        }
