from helpers.carrinho_helper import listar_carrinhos


def test_listar_carrinhos_com_sucesso():
    response = listar_carrinhos()

    assert response.status_code == 200

    body = response.json()

    assert "quantidade" in body
    assert "carrinhos" in body
    assert isinstance(body["carrinhos"], list)


def test_listar_carrinhos_filtrando_por_id(
    carrinho_cadastrado
):
    carrinho_id = carrinho_cadastrado["id"]

    response = listar_carrinhos(
        params={
            "_id": carrinho_id
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["quantidade"] >= 1

    ids = [
        carrinho["_id"]
        for carrinho in body["carrinhos"]
    ]

    assert carrinho_id in ids