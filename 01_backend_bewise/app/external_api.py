from typing import Any

import httpx


J_SERVICE_URL = "https://jservice.io/api/random"


def fetch_questions(amount: int) -> list[dict[str, Any]]:
    response = httpx.get(J_SERVICE_URL, params={"count": amount}, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Unexpected response format from jservice.io")
    return data

