from helpers.produto_helper import buscar_produto_por_id


def test_buscar_produto_por_id_com_sucesso(
    produto_cadastrado
):
    produto_id = produto_cadastrado["id"]
    produto_original = produto_cadastrado["dados"]

    response = buscar_produto_por_id(produto_id)

    assert response.status_code == 200

    body = response.json()

    assert body["_id"] == produto_id
    assert body["nome"] == produto_original["nome"]
    assert body["preco"] == produto_original["preco"]
    assert body["descricao"] == produto_original["descricao"]
    assert body["quantidade"] == produto_original["quantidade"]


def test_buscar_produto_com_id_inexistente(
    id_produto_inexistente
):
    response = buscar_produto_por_id(
        id_produto_inexistente
    )

    assert response.status_code == 400

    body = response.json()

    assert body["message"] == "Produto não encontrado"