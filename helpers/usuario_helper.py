import requests

from config import BASE_URL, TIMEOUT


def criar_usuario(usuario):
    return requests.post(
        f"{BASE_URL}/usuarios",
        json=usuario,
        timeout=TIMEOUT
    )


def listar_usuarios(params=None):
    return requests.get(
        f"{BASE_URL}/usuarios",
        params=params,
        timeout=TIMEOUT
    )


def buscar_usuario_por_id(usuario_id):
    return requests.get(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=TIMEOUT
    )


def editar_usuario(usuario_id, novos_dados):
    return requests.put(
        f"{BASE_URL}/usuarios/{usuario_id}",
        json=novos_dados,
        timeout=TIMEOUT
    )


def excluir_usuario(usuario_id):
    return requests.delete(
        f"{BASE_URL}/usuarios/{usuario_id}",
        timeout=TIMEOUT
    )