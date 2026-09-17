from helpers.usuario_helper import buscar_usuario_por_id


def test_buscar_usuario_por_id_com_sucesso(usuario_cadastrado):
    usuario_id = usuario_cadastrado["id"]
    usuario_original = usuario_cadastrado["dados"]

    response = buscar_usuario_por_id(usuario_id)

    assert response.status_code == 200

    body = response.json()

    assert body["_id"] == usuario_id
    assert body["nome"] == usuario_original["nome"]
    assert body["email"] == usuario_original["email"]
    assert body["administrador"] == usuario_original["administrador"]


def test_buscar_usuario_com_id_inexistente(id_usuario_inexistente):
    response = buscar_usuario_por_id(id_usuario_inexistente)

    assert response.status_code == 400

    body = response.json()

    assert body["message"] == "Usuário não encontrado"