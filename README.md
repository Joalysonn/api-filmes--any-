# API Catálogo de Filmes

API REST simples, usada nos roteiros práticos da competência
**Elaborar um pipeline de CI/CD para cloud computing**.

Ela serve de exemplo para praticar versionamento, Integração Contínua (CI),
containers, docker-compose e Entrega/Implantação Contínua (CD) com GitLab CI.
O projeto de vocês deve ter um tema próprio: use esta API apenas como referência.

## Tecnologias

- Python 3.12 + Flask
- Flask-SQLAlchemy (SQLite no desenvolvimento local e nos testes, PostgreSQL no Docker/produção)
- pytest (testes automatizados) e flake8 (lint)
- Docker, docker-compose e GitLab CI/CD

## Rotas

| Método | Rota             | Descrição                                  |
|--------|------------------|--------------------------------------------|
| GET    | /health          | Healthcheck (confirma que a API está no ar) |
| GET    | /filmes          | Lista filmes (filtro opcional `?genero=`)   |
| GET    | /filmes/{id}     | Busca um filme pelo id                      |
| POST   | /filmes          | Cadastra um filme                           |
| PUT    | /filmes/{id}     | Atualiza um ou mais campos de um filme      |
| DELETE | /filmes/{id}     | Remove um filme                             |

Exemplo de corpo para `POST /filmes`:

```json
{ "titulo": "Central do Brasil", "ano": 1998, "genero": "Drama", "nota": 9.1 }
```

## Como rodar localmente (sem Docker)

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py                    # API em http://localhost:5000
```

## Testes e lint

```bash
pytest -v
flake8 .
```
