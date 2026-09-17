import pytest

from helpers.produto_helper import (
    criar_produto,
    buscar_produto_por_id,
    excluir_produto
)


def test_criar_produto_com_sucesso(
    dados_produto,
    token_admin
):
    response = criar_produto(
        dados_produto,
        token_admin
    )

    assert response.status_code == 201

    body = response.json()

    assert body["message"] == "Cadastro realizado com sucesso"
    assert "_id" in body

    produto_id = body["_id"]

    # Confirma que o produto realmente foi persistido
    response_busca = buscar_produto_por_id(produto_id)

    assert response_busca.status_code == 200

    produto_criado = response_busca.json()

    assert produto_criado["_id"] == produto_id
    assert produto_criado["nome"] == dados_produto["nome"]
    assert produto_criado["preco"] == dados_produto["preco"]
    assert produto_criado["descricao"] == dados_produto["descricao"]
    assert produto_criado["quantidade"] == dados_produto["quantidade"]

    # Cleanup
    excluir_produto(produto_id, token_admin)


def test_criar_produto_com_nome_duplicado(
    dados_produto,
    token_admin
):
    primeira_response = criar_produto(
        dados_produto,
        token_admin
    )

    assert primeira_response.status_code == 201

    produto_id = primeira_response.json()["_id"]

    segunda_response = criar_produto(
        dados_produto,
        token_admin
    )

    assert segunda_response.status_code == 400

    body = segunda_response.json()

    assert body["message"] == "Já existe produto com esse nome"

    # Cleanup
    excluir_produto(produto_id, token_admin)


def test_criar_produto_sem_token(
    dados_produto
):
    response = criar_produto(
        dados_produto
    )

    assert response.status_code == 401

    body = response.json()

    assert "message" in body


def test_criar_produto_com_usuario_nao_admin(
    dados_produto,
    token_usuario_comum
):
    response = criar_produto(
        dados_produto,
        token_usuario_comum
    )

    assert response.status_code == 403

    body = response.json()

    assert "message" in body


def test_criar_produto_com_token_invalido(
    dados_produto
):
    response = criar_produto(
        dados_produto,
        "token-invalido"
    )

    assert response.status_code == 401

    body = response.json()

    assert "message" in body


@pytest.mark.parametrize(
    "campo_obrigatorio",
    [
        "nome",
        "preco",
        "descricao",
        "quantidade"
    ]
)
def test_criar_produto_sem_campo_obrigatorio(
    dados_produto,
    token_admin,
    campo_obrigatorio
):
    produto_invalido = dados_produto.copy()

    produto_invalido.pop(campo_obrigatorio)

    response = criar_produto(
        produto_invalido,
        token_admin
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "campo, valor_invalido",
    [
        ("nome", 123),
        ("preco", "cem"),
        ("descricao", 123),
        ("quantidade", "dez")
    ]
)
def test_criar_produto_com_tipo_invalido(
    dados_produto,
    token_admin,
    campo,
    valor_invalido
):
    produto_invalido = dados_produto.copy()

    produto_invalido[campo] = valor_invalido

    response = criar_produto(
        produto_invalido,
        token_admin
    )

    assert response.status_code == 400