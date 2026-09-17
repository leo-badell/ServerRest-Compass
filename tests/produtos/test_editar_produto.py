import pytest

from helpers.produto_helper import (
    criar_produto,
    editar_produto,
    buscar_produto_por_id,
    excluir_produto
)


def test_editar_produto_com_sucesso(
    produto_cadastrado,
    dados_produto_atualizado,
    token_admin
):
    produto_id = produto_cadastrado["id"]

    response = editar_produto(
        produto_id,
        dados_produto_atualizado,
        token_admin
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Registro alterado com sucesso"

    # Confirma persistência da alteração
    response_busca = buscar_produto_por_id(
        produto_id
    )

    assert response_busca.status_code == 200

    produto_atualizado = response_busca.json()

    assert produto_atualizado["nome"] == dados_produto_atualizado["nome"]
    assert produto_atualizado["preco"] == dados_produto_atualizado["preco"]
    assert (
        produto_atualizado["descricao"]
        == dados_produto_atualizado["descricao"]
    )
    assert (
        produto_atualizado["quantidade"]
        == dados_produto_atualizado["quantidade"]
    )

def test_editar_produto_com_nome_ja_existente(
    produto_cadastrado,
    dados_produto,
    token_admin
):
    # Cria um segundo produto
    response_segundo = criar_produto(
        dados_produto,
        token_admin
    )

    assert response_segundo.status_code == 201

    segundo_id = response_segundo.json()["_id"]

    # Tenta colocar no segundo produto o nome do primeiro
    dados_edicao = dados_produto.copy()

    dados_edicao["nome"] = produto_cadastrado["dados"]["nome"]

    response = editar_produto(
        segundo_id,
        dados_edicao,
        token_admin
    )

    assert response.status_code == 400

    assert (
        response.json()["message"]
        == "Já existe produto com esse nome"
    )

    excluir_produto(
        segundo_id,
        token_admin
    )

def test_editar_produto_sem_token(
    produto_cadastrado,
    dados_produto_atualizado
):
    response = editar_produto(
        produto_cadastrado["id"],
        dados_produto_atualizado
    )

    assert response.status_code == 401
    assert "message" in response.json()

def test_editar_produto_com_usuario_nao_admin(
    produto_cadastrado,
    dados_produto_atualizado,
    token_usuario_comum
):
    response = editar_produto(
        produto_cadastrado["id"],
        dados_produto_atualizado,
        token_usuario_comum
    )

    assert response.status_code == 403
    assert "message" in response.json()

@pytest.mark.parametrize(
    "campo_obrigatorio",
    [
        "nome",
        "preco",
        "descricao",
        "quantidade"
    ]
)
def test_editar_produto_sem_campo_obrigatorio(
    produto_cadastrado,
    dados_produto_atualizado,
    token_admin,
    campo_obrigatorio
):
    produto_invalido = dados_produto_atualizado.copy()

    produto_invalido.pop(campo_obrigatorio)

    response = editar_produto(
        produto_cadastrado["id"],
        produto_invalido,
        token_admin
    )

    assert response.status_code == 400

def test_editar_produto_com_token_invalido(
    produto_cadastrado,
    dados_produto_atualizado
):
    response = editar_produto(
        produto_cadastrado["id"],
        dados_produto_atualizado,
        "token-invalido"
    )

    assert response.status_code == 401
    assert "message" in response.json()

@pytest.mark.parametrize(
    "campo, valor_invalido",
    [
        ("nome", 123),
        ("preco", "cem"),
        ("descricao", 123),
        ("quantidade", "dez")
    ]
)
def test_editar_produto_com_tipo_invalido(
    produto_cadastrado,
    dados_produto_atualizado,
    token_admin,
    campo,
    valor_invalido
):
    produto_invalido = dados_produto_atualizado.copy()

    produto_invalido[campo] = valor_invalido

    response = editar_produto(
        produto_cadastrado["id"],
        produto_invalido,
        token_admin
    )

    assert response.status_code == 400