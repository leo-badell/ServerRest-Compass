from helpers.usuario_helper import (
    buscar_usuario_por_id,
    editar_usuario
)


def test_editar_usuario_com_sucesso(
    usuario_cadastrado,
    dados_usuario_atualizado
):
    usuario_id = usuario_cadastrado["id"]

    response = editar_usuario(
        usuario_id,
        dados_usuario_atualizado
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Registro alterado com sucesso"

    # Confirma pela própria API que a alteração persistiu
    response_busca = buscar_usuario_por_id(usuario_id)

    assert response_busca.status_code == 200

    usuario_atualizado = response_busca.json()

    assert usuario_atualizado["nome"] == dados_usuario_atualizado["nome"]
    assert usuario_atualizado["email"] == dados_usuario_atualizado["email"]
    assert (
        usuario_atualizado["administrador"]
        == dados_usuario_atualizado["administrador"]
    )


def test_editar_usuario_com_email_ja_existente(
    usuario_cadastrado,
    dados_usuario
):
    # Cria um segundo usuário
    from helpers.usuario_helper import criar_usuario, excluir_usuario

    segundo_response = criar_usuario(dados_usuario)

    assert segundo_response.status_code == 201

    segundo_id = segundo_response.json()["_id"]

    dados_edicao = usuario_cadastrado["dados"].copy()

    # Tentamos editar o segundo usuário usando o email do primeiro
    response = editar_usuario(
        segundo_id,
        dados_edicao
    )

    assert response.status_code == 400

    body = response.json()

    assert body["message"] == "Este email já está sendo usado"

    excluir_usuario(segundo_id)