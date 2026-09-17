from helpers.auth_helper import realizar_login


def test_login_com_sucesso(usuario_cadastrado):
    usuario = usuario_cadastrado["dados"]

    response = realizar_login(
        usuario["email"],
        usuario["password"]
    )

    assert response.status_code == 200

    body = response.json()

    assert body["message"] == "Login realizado com sucesso"
    assert "authorization" in body
    assert body["authorization"]

def test_login_com_senha_invalida(usuario_cadastrado):
    usuario = usuario_cadastrado["dados"]

    response = realizar_login(
        usuario["email"],
        "senha_incorreta"
    )

    assert response.status_code == 401

    body = response.json()

    assert body["message"] == "Email e/ou senha inválidos"