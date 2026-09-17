from helpers.usuario_helper import criar_usuario, excluir_usuario


def test_criar_usuario_com_sucesso(dados_usuario):

    response = criar_usuario(dados_usuario)

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body

    usuario_id = body["_id"]

    excluir_usuario(usuario_id)


def test_criar_usuario_com_email_duplicado(dados_usuario):

    primeira_response = criar_usuario(dados_usuario)

    assert primeira_response.status_code == 201

    usuario_id = primeira_response.json()["_id"]

    segunda_response = criar_usuario(dados_usuario)

    assert segunda_response.status_code == 400

    body = segunda_response.json()

    assert body["message"] == "Este email já está sendo usado"

    excluir_usuario(usuario_id)