def test_health_retorna_200(client):
    resposta = client.get("/health")
    assert resposta.status_code == 200


def test_health_retorna_status_ok(client):
    resposta = client.get("/health")
    assert resposta.get_json() == {"status": "ok"}


def test_health_retorna_json(client):
    resposta = client.get("/health")
    assert resposta.content_type == "application/json"
