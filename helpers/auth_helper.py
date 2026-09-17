import requests

from config import BASE_URL, TIMEOUT


def realizar_login(email, password):
    payload = {
        "email": email,
        "password": password
    }

    return requests.post(
        f"{BASE_URL}/login",
        json=payload,
        timeout=TIMEOUT
    )