from helpers.usuario_helper import listar_usuarios


def test_listar_usuarios_com_sucesso():
    response = listar_usuarios()

    assert response.status_code == 200

    body = response.json()

    assert "quantidade" in body
    assert "usuarios" in body
    assert isinstance(body["usuarios"], list)


def test_listar_usuarios_filtrando_por_email(usuario_cadastrado):
    usuario = usuario_cadastrado["dados"]

    response = listar_usuarios(
        params={
            "email": usuario["email"]
        }
    )

    assert response.status_code == 200

    body = response.json()

    assert body["quantidade"] >= 1
    assert len(body["usuarios"]) >= 1

    emails = [
        usuario_encontrado["email"]
        for usuario_encontrado in body["usuarios"]
    ]

    assert usuario["email"] in emails