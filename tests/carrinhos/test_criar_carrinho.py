from helpers.carrinho_helper import (
    criar_carrinho,
    cancelar_compra
)

from fixtures.data_factory import gerar_item_carrinho


def test_criar_carrinho_com_sucesso(
    produto_cadastrado,
    token_admin
):
    produtos = [
        gerar_item_carrinho(
            produto_cadastrado["id"],
            quantidade=1
        )
    ]

    response = criar_carrinho(
        produtos,
        token_admin
    )

    assert response.status_code == 201

    body = response.json()

    assert "message" in body
    assert "_id" in body

    # Cleanup
    cancelar_compra(token_admin)


def test_criar_carrinho_sem_token(
    item_carrinho
):
    response = criar_carrinho(
        [item_carrinho]
    )

    assert response.status_code == 401
    assert "message" in response.json()


def test_criar_carrinho_com_token_invalido(
    item_carrinho
):
    response = criar_carrinho(
        [item_carrinho],
        "token-invalido"
    )

    assert response.status_code == 401
    assert "message" in response.json()

def test_criar_segundo_carrinho_para_mesmo_usuario(
    produto_cadastrado,
    token_admin
):
    produtos = [
        gerar_item_carrinho(
            produto_cadastrado["id"],
            quantidade=1
        )
    ]

    primeira_response = criar_carrinho(
        produtos,
        token_admin
    )

    assert primeira_response.status_code == 201

    segunda_response = criar_carrinho(
        produtos,
        token_admin
    )

    assert segunda_response.status_code == 400
    assert "message" in segunda_response.json()

    cancelar_compra(token_admin)

def test_criar_carrinho_com_produto_duplicado(
    produto_cadastrado,
    token_admin
):
    produto = gerar_item_carrinho(
        produto_cadastrado["id"],
        quantidade=1
    )

    produtos = [
        produto,
        produto.copy()
    ]

    response = criar_carrinho(
        produtos,
        token_admin
    )

    assert response.status_code == 400
    assert "message" in response.json()

def test_criar_carrinho_com_produto_inexistente(
    token_admin
):
    produtos = [
        gerar_item_carrinho(
            "0000000000000000",
            quantidade=1
        )
    ]

    response = criar_carrinho(
        produtos,
        token_admin
    )

    assert response.status_code == 400
    assert "message" in response.json()

def test_criar_carrinho_com_estoque_insuficiente(
    produto_cadastrado,
    token_admin
):
    produtos = [
        gerar_item_carrinho(
            produto_cadastrado["id"],
            quantidade=11
        )
    ]

    response = criar_carrinho(
        produtos,
        token_admin
    )

    assert response.status_code == 400
    assert "message" in response.json()

