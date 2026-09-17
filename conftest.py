import pytest
from fixtures.data_factory import (
    gerar_usuario,
    gerar_usuario_atualizado,
    gerar_id_inexistente,
    gerar_produto,
    gerar_id_produto_inexistente
)

from helpers.auth_helper import realizar_login

from helpers.usuario_helper import (
    criar_usuario,
    excluir_usuario
)

from helpers.produto_helper import (
    criar_produto,
    excluir_produto
)

from fixtures.data_factory import (
    gerar_item_carrinho,
    gerar_id_carrinho_inexistente
)

from helpers.carrinho_helper import (
    criar_carrinho,
    cancelar_compra
)


# ============================================================
# FIXTURES DE USUÁRIOS
# ============================================================

@pytest.fixture
def dados_usuario():
    return gerar_usuario()


@pytest.fixture
def dados_usuario_atualizado():
    return gerar_usuario_atualizado()


@pytest.fixture
def id_usuario_inexistente():
    return gerar_id_inexistente()


@pytest.fixture
def usuario_cadastrado():
    usuario = gerar_usuario()

    response = criar_usuario(usuario)

    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "dados": usuario,
        "id": usuario_id
    }

    # Cleanup
    excluir_usuario(usuario_id)


# ============================================================
# FIXTURES DE PRODUTOS
# ============================================================

@pytest.fixture
def dados_produto():
    return gerar_produto()

@pytest.fixture
def dados_produto_atualizado():
    return gerar_produto()


@pytest.fixture
def id_produto_inexistente():
    return gerar_id_produto_inexistente()


@pytest.fixture
def produto_cadastrado(token_admin):
    produto = gerar_produto()

    response = criar_produto(
        produto,
        token_admin
    )

    assert response.status_code == 201

    produto_id = response.json()["_id"]

    yield {
        "dados": produto,
        "id": produto_id
    }

    # Cleanup
    excluir_produto(
        produto_id,
        token_admin
    )

# ============================================================
# FIXTURES DE AUTENTICAÇÃO - ADMIN
# ============================================================

@pytest.fixture
def usuario_admin():
    usuario = gerar_usuario(administrador="true")

    response = criar_usuario(usuario)

    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "dados": usuario,
        "id": usuario_id
    }

    # Cleanup
    excluir_usuario(usuario_id)


@pytest.fixture
def token_admin(usuario_admin):
    usuario = usuario_admin["dados"]

    response = realizar_login(
        usuario["email"],
        usuario["password"]
    )

    assert response.status_code == 200

    return response.json()["authorization"]


# ============================================================
# FIXTURES DE AUTENTICAÇÃO - USUÁRIO COMUM
# ============================================================

@pytest.fixture
def usuario_comum():
    usuario = gerar_usuario(administrador="false")

    response = criar_usuario(usuario)

    assert response.status_code == 201

    usuario_id = response.json()["_id"]

    yield {
        "dados": usuario,
        "id": usuario_id
    }

    # Cleanup
    excluir_usuario(usuario_id)


@pytest.fixture
def token_usuario_comum(usuario_comum):
    usuario = usuario_comum["dados"]

    response = realizar_login(
        usuario["email"],
        usuario["password"]
    )

    assert response.status_code == 200

    return response.json()["authorization"]

# ============================================================
# FIXTURES DE CARRINHOS
# ============================================================

@pytest.fixture
def id_carrinho_inexistente():
    return gerar_id_carrinho_inexistente()


@pytest.fixture
def item_carrinho(produto_cadastrado):
    return gerar_item_carrinho(
        produto_cadastrado["id"],
        quantidade=1
    )


@pytest.fixture
def carrinho_cadastrado(
    produto_cadastrado,
    token_admin
):
    produtos = [
        gerar_item_carrinho(
            produto_cadastrado["id"],
            quantidade=1
        )
    ]

    response = criar_carrinho(
        produtos,
        token_admin
    )

    assert response.status_code == 201

    carrinho_id = response.json()["_id"]

    yield {
        "id": carrinho_id,
        "produtos": produtos
    }

    # Cleanup:
    # cancelar-compra remove eventual carrinho
    # e devolve os produtos ao estoque.
    cancelar_compra(token_admin)