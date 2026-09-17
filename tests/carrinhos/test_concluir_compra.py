from helpers.carrinho_helper import (
    concluir_compra,
    buscar_carrinho_por_id
)


def test_concluir_compra_com_sucesso(
    carrinho_cadastrado,
    token_admin
):
    carrinho_id = carrinho_cadastrado["id"]

    response = concluir_compra(
        token_admin
    )

    assert response.status_code == 200
    assert "message" in response.json()

    # Carrinho deve deixar de existir
    response_busca = buscar_carrinho_por_id(
        carrinho_id
    )

    assert response_busca.status_code == 400


def test_concluir_compra_sem_token():
    response = concluir_compra()

    assert response.status_code == 401
    assert "message" in response.json()


def test_concluir_compra_com_token_invalido():
    response = concluir_compra(
        "token-invalido"
    )

    assert response.status_code == 401
    assert "message" in response.json()