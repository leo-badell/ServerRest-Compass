from uuid import uuid4


def gerar_usuario(administrador="false"):
    identificador = uuid4().hex[:8]

    return {
        "nome": f"Usuario Teste {identificador}",
        "email": f"qa_{identificador}@teste.com",
        "password": "teste123",
        "administrador": administrador
    }


def gerar_usuario_atualizado(administrador="false"):
    identificador = uuid4().hex[:8]

    return {
        "nome": f"Usuario Atualizado {identificador}",
        "email": f"qa_atualizado_{identificador}@teste.com",
        "password": "novaSenha123",
        "administrador": administrador
    }


def gerar_id_inexistente():
    return "0000000000000000"

def gerar_produto():
    from uuid import uuid4

    identificador = uuid4().hex[:8]

    return {
        "nome": f"Produto QA {identificador}",
        "preco": 100,
        "descricao": "Produto criado pelos testes automatizados",
        "quantidade": 10
    }

def gerar_id_produto_inexistente():
    return "0000000000000000"

def gerar_id_carrinho_inexistente():
    return "0000000000000000"


def gerar_item_carrinho(produto_id, quantidade=1):
    return {
        "idProduto": produto_id,
        "quantidade": quantidade
    }