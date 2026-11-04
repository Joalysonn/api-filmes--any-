FILME_VALIDO = {"titulo": "Cidade de Deus", "ano": 2002, "genero": "Drama"}


# ---------- GET /filmes ----------
def test_listar_filmes_vazio(client):
    resposta = client.get("/filmes")
    assert resposta.status_code == 200
    assert resposta.get_json() == []


def test_listar_filmes_com_itens(client, filme_criado):
    resposta = client.get("/filmes")
    dados = resposta.get_json()
    assert len(dados) == 1
    assert dados[0]["titulo"] == "Central do Brasil"


def test_listar_filmes_filtra_por_genero(client, filme_criado):
    client.post("/filmes", json={"titulo": "Bacurau", "ano": 2019,
                                 "genero": "Suspense"})
    resposta = client.get("/filmes?genero=suspense")
    dados = resposta.get_json()
    assert len(dados) == 1
    assert dados[0]["titulo"] == "Bacurau"


# ---------- GET /filmes/<id> ----------
def test_buscar_filme_existente(client, filme_criado):
    resposta = client.get(f"/filmes/{filme_criado['id']}")
    assert resposta.status_code == 200
    assert resposta.get_json()["titulo"] == "Central do Brasil"


def test_buscar_filme_inexistente_retorna_404(client):
    resposta = client.get("/filmes/999")
    assert resposta.status_code == 404
    assert "erro" in resposta.get_json()


def test_buscar_filme_id_invalido_retorna_404(client):
    resposta = client.get("/filmes/abc")
    assert resposta.status_code == 404


# ---------- POST /filmes ----------
def test_criar_filme_valido(client):
    resposta = client.post("/filmes", json=FILME_VALIDO)
    assert resposta.status_code == 201
    dados = resposta.get_json()
    assert dados["id"] is not None
    assert dados["titulo"] == "Cidade de Deus"
    assert dados["nota"] is None


def test_criar_filme_sem_campo_obrigatorio_retorna_400(client):
    resposta = client.post("/filmes", json={"titulo": "Sem ano"})
    assert resposta.status_code == 400
    assert "ano" in resposta.get_json()["erro"]


def test_criar_filme_com_nota_invalida_retorna_400(client):
    filme = {**FILME_VALIDO, "nota": 15}
    resposta = client.post("/filmes", json=filme)
    assert resposta.status_code == 400


def test_criar_filme_com_ano_texto_retorna_400(client):
    filme = {**FILME_VALIDO, "ano": "dois mil"}
    resposta = client.post("/filmes", json=filme)
    assert resposta.status_code == 400


def test_criar_filme_sem_json_retorna_400(client):
    resposta = client.post("/filmes", data="isso não é json")
    assert resposta.status_code == 400


# ---------- PUT /filmes/<id> ----------
def test_atualizar_filme(client, filme_criado):
    resposta = client.put(f"/filmes/{filme_criado['id']}", json={"nota": 10})
    assert resposta.status_code == 200
    assert resposta.get_json()["nota"] == 10


def test_atualizar_filme_persiste_alteracao(client, filme_criado):
    client.put(f"/filmes/{filme_criado['id']}", json={"genero": "Clássico"})
    resposta = client.get(f"/filmes/{filme_criado['id']}")
    assert resposta.get_json()["genero"] == "Clássico"


def test_atualizar_filme_inexistente_retorna_404(client):
    resposta = client.put("/filmes/999", json={"nota": 5})
    assert resposta.status_code == 404


def test_atualizar_filme_dados_invalidos_retorna_400(client, filme_criado):
    resposta = client.put(f"/filmes/{filme_criado['id']}", json={"titulo": ""})
    assert resposta.status_code == 400


# ---------- DELETE /filmes/<id> ----------
def test_remover_filme(client, filme_criado):
    resposta = client.delete(f"/filmes/{filme_criado['id']}")
    assert resposta.status_code == 204


def test_remover_filme_some_da_listagem(client, filme_criado):
    client.delete(f"/filmes/{filme_criado['id']}")
    resposta = client.get(f"/filmes/{filme_criado['id']}")
    assert resposta.status_code == 404


def test_remover_filme_inexistente_retorna_404(client):
    resposta = client.delete("/filmes/999")
    assert resposta.status_code == 404
