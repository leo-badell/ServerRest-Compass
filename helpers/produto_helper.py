import requests

from config import BASE_URL, TIMEOUT


def criar_produto(produto, token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    return requests.post(
        f"{BASE_URL}/produtos",
        json=produto,
        headers=headers,
        timeout=TIMEOUT
    )


def listar_produtos(params=None):
    return requests.get(
        f"{BASE_URL}/produtos",
        params=params,
        timeout=TIMEOUT
    )


def buscar_produto_por_id(produto_id):
    return requests.get(
        f"{BASE_URL}/produtos/{produto_id}",
        timeout=TIMEOUT
    )


def editar_produto(produto_id, produto, token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    return requests.put(
        f"{BASE_URL}/produtos/{produto_id}",
        json=produto,
        headers=headers,
        timeout=TIMEOUT
    )


def excluir_produto(produto_id, token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    return requests.delete(
        f"{BASE_URL}/produtos/{produto_id}",
        headers=headers,
        timeout=TIMEOUT
    )