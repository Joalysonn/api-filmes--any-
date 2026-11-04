"""Rotas da API Catálogo de Filmes."""
from flask import Blueprint, jsonify, request

from app.models import Filme, db

bp = Blueprint("api", __name__)

CAMPOS_OBRIGATORIOS = ("titulo", "ano", "genero")


def validar_filme(dados, parcial=False):
    """Retorna uma mensagem de erro ou None se os dados forem válidos.

    parcial=True permite atualizar apenas alguns campos (PUT parcial).
    """
    if not isinstance(dados, dict):
        return "Corpo da requisição deve ser um JSON válido"

    if not parcial:
        faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in dados]
        if faltando:
            return f"Campos obrigatórios ausentes: {', '.join(faltando)}"

    if "titulo" in dados:
        titulo = dados["titulo"]
        if not isinstance(titulo, str) or not titulo.strip():
            return "O campo 'titulo' deve ser um texto não vazio"

    if "ano" in dados:
        ano = dados["ano"]
        if not isinstance(ano, int) or isinstance(ano, bool):
            return "O campo 'ano' deve ser um número inteiro"
        if ano < 1888 or ano > 2100:
            return "O campo 'ano' deve estar entre 1888 e 2100"

    if "genero" in dados:
        genero = dados["genero"]
        if not isinstance(genero, str) or not genero.strip():
            return "O campo 'genero' deve ser um texto não vazio"

    if dados.get("nota") is not None:
        nota = dados["nota"]
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            return "O campo 'nota' deve ser numérico"
        if nota < 0 or nota > 10:
            return "O campo 'nota' deve estar entre 0 e 10"

    return None


@bp.get("/health")
def health():
    """Healthcheck: confirma que a aplicação está no ar."""
    return jsonify({"status": "ok"}), 200


@bp.get("/filmes")
def listar_filmes():
    """Lista os filmes. Aceita filtro opcional ?genero=Drama."""
    consulta = Filme.query
    genero = request.args.get("genero")
    if genero:
        consulta = consulta.filter(Filme.genero.ilike(genero))
    filmes = consulta.order_by(Filme.id).all()
    return jsonify([f.to_dict() for f in filmes]), 200


@bp.get("/filmes/<int:filme_id>")
def buscar_filme(filme_id):
    filme = db.session.get(Filme, filme_id)
    if filme is None:
        return jsonify({"erro": "Filme não encontrado"}), 404
    return jsonify(filme.to_dict()), 200


@bp.post("/filmes")
def criar_filme():
    dados = request.get_json(silent=True)
    erro = validar_filme(dados)
    if erro:
        return jsonify({"erro": erro}), 400

    filme = Filme(
        titulo=dados["titulo"].strip(),
        ano=dados["ano"],
        genero=dados["genero"].strip(),
        nota=dados.get("nota"),
    )
    db.session.add(filme)
    db.session.commit()
    return jsonify(filme.to_dict()), 201


@bp.put("/filmes/<int:filme_id>")
def atualizar_filme(filme_id):
    filme = db.session.get(Filme, filme_id)
    if filme is None:
        return jsonify({"erro": "Filme não encontrado"}), 404

    dados = request.get_json(silent=True)
    erro = validar_filme(dados, parcial=True)
    if erro:
        return jsonify({"erro": erro}), 400
    if not dados:
        return jsonify({"erro": "Nenhum campo enviado para atualização"}), 400

    for campo in ("titulo", "ano", "genero", "nota"):
        if campo in dados:
            valor = dados[campo]
            setattr(filme, campo, valor.strip() if isinstance(valor, str) else valor)

    db.session.commit()
    return jsonify(filme.to_dict()), 200


@bp.delete("/filmes/<int:filme_id>")
def remover_filme(filme_id):
    filme = db.session.get(Filme, filme_id)
    if filme is None:
        return jsonify({"erro": "Filme não encontrado"}), 404
    db.session.delete(filme)
    db.session.commit()
    return "", 204
