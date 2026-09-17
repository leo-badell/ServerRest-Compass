from helpers.produto_helper import listar_produtos


def test_listar_produtos_com_sucesso():
    response = listar_produtos()

    assert response.status_code == 200

    body = response.json()

    assert "quantidade" in body
    assert "produtos" in body
    assert isinstance(body["produtos"], list)


def test_listar_produtos_filtrando_por_nome(
    produto_cadastrado
):
    produto = produto_cadastrado["dados"]

    response = listar_produtos(
        params={
            "nome": produto["nome"]
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["quantidade"] >= 1

    nomes = [
        produto_encontrado["nome"]
        for produto_encontrado in body["produtos"]
    ]

    assert produto["nome"] in nomes