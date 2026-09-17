from helpers.carrinho_helper import (
    cancelar_compra,
    buscar_carrinho_por_id
)

from helpers.produto_helper import buscar_produto_por_id


def test_cancelar_compra_com_sucesso_e_repor_estoque(
    carrinho_cadastrado,
    produto_cadastrado,
    token_admin
):
    carrinho_id = carrinho_cadastrado["id"]
    produto_id = produto_cadastrado["id"]

    quantidade_original = produto_cadastrado["dados"]["quantidade"]

    response = cancelar_compra(
        token_admin
    )

    assert response.status_code == 200
    assert "message" in response.json()

    # Carrinho deve ter sido removido
    response_carrinho = buscar_carrinho_por_id(
        carrinho_id
    )

    assert response_carrinho.status_code == 400

    # Produto deve voltar à quantidade original
    response_produto = buscar_produto_por_id(
        produto_id
    )

    assert response_produto.status_code == 200

    produto = response_produto.json()

    assert produto["quantidade"] == quantidade_original


def test_cancelar_compra_sem_token():
    response = cancelar_compra()

    assert response.status_code == 401
    assert "message" in response.json()


def test_cancelar_compra_com_token_invalido():
    response = cancelar_compra(
        "token-invalido"
    )

    assert response.status_code == 401
    assert "message" in response.json()