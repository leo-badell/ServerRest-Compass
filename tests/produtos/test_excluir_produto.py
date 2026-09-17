from helpers.produto_helper import (
    excluir_produto,
    buscar_produto_por_id
)


def test_excluir_produto_com_sucesso(
    produto_cadastrado,
    token_admin
):
    produto_id = produto_cadastrado["id"]

    response = excluir_produto(
        produto_id,
        token_admin
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Registro excluído com sucesso"

    # Confirma que realmente foi excluído
    response_busca = buscar_produto_por_id(
        produto_id
    )

    assert response_busca.status_code == 400
    assert (
        response_busca.json()["message"]
        == "Produto não encontrado"
    )

def test_excluir_produto_sem_token(
    produto_cadastrado
):
    response = excluir_produto(
        produto_cadastrado["id"]
    )

    assert response.status_code == 401
    assert "message" in response.json()

def test_excluir_produto_com_usuario_nao_admin(
    produto_cadastrado,
    token_usuario_comum
):
    response = excluir_produto(
        produto_cadastrado["id"],
        token_usuario_comum
    )

    assert response.status_code == 403
    assert "message" in response.json()

def test_excluir_produto_inexistente(
    id_produto_inexistente,
    token_admin
):
    response = excluir_produto(
        id_produto_inexistente,
        token_admin
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Nenhum registro excluído"