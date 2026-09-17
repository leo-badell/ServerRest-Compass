import requests

from config import BASE_URL, TIMEOUT


def criar_carrinho(produtos, token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    payload = {
        "produtos": produtos
    }

    return requests.post(
        f"{BASE_URL}/carrinhos",
        json=payload,
        headers=headers,
        timeout=TIMEOUT
    )


def listar_carrinhos(params=None):
    return requests.get(
        f"{BASE_URL}/carrinhos",
        params=params,
        timeout=TIMEOUT
    )


def buscar_carrinho_por_id(carrinho_id):
    return requests.get(
        f"{BASE_URL}/carrinhos/{carrinho_id}",
        timeout=TIMEOUT
    )


def concluir_compra(token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    return requests.delete(
        f"{BASE_URL}/carrinhos/concluir-compra",
        headers=headers,
        timeout=TIMEOUT
    )


def cancelar_compra(token=None):
    headers = {}

    if token:
        headers["Authorization"] = token

    return requests.delete(
        f"{BASE_URL}/carrinhos/cancelar-compra",
        headers=headers,
        timeout=TIMEOUT
    )