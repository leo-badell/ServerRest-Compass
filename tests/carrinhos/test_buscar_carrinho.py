from helpers.carrinho_helper import buscar_carrinho_por_id


def test_buscar_carrinho_por_id_com_sucesso(
    carrinho_cadastrado
):
    carrinho_id = carrinho_cadastrado["id"]

    response = buscar_carrinho_por_id(
        carrinho_id
    )

    assert response.status_code == 200

    body = response.json()

    assert body["_id"] == carrinho_id
    assert "produtos" in body
    assert "precoTotal" in body
    assert "quantidadeTotal" in body
    assert "idUsuario" in body


def test_buscar_carrinho_com_id_inexistente(
    id_carrinho_inexistente
):
    response = buscar_carrinho_por_id(
        id_carrinho_inexistente
    )

    assert response.status_code == 400
    assert "message" in response.json()