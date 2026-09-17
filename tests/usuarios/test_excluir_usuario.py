from helpers.usuario_helper import (
    buscar_usuario_por_id,
    excluir_usuario
)


def test_excluir_usuario_com_sucesso(usuario_cadastrado):
    usuario_id = usuario_cadastrado["id"]

    response = excluir_usuario(usuario_id)

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Registro excluído com sucesso"

    # Confirma que realmente deixou de existir
    response_busca = buscar_usuario_por_id(usuario_id)

    assert response_busca.status_code == 400
    assert response_busca.json()["message"] == "Usuário não encontrado"


def test_excluir_usuario_inexistente(id_usuario_inexistente):
    response = excluir_usuario(id_usuario_inexistente)

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Nenhum registro excluído"