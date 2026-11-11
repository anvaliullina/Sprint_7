"""Новые, независимые тестовые данные для каждого прогона."""

from datetime import date, timedelta
from uuid import uuid4


def generate_courier() -> dict:
    """Сгенерировать уникальные логин, пароль и имя курьера."""
    unique = uuid4().hex[:16]
    return {
        "login": f"qa_{unique}",
        "password": f"pass_{uuid4().hex[:14]}",
        "firstName": f"Courier_{unique[:8]}",
    }


def generate_order(colors=None) -> dict:
    """Сгенерировать корректный заказ; None означает отсутствие поля color."""
    payload = {
        "firstName": "Тестовый",
        "lastName": "Покупатель",
        "address": "Москва, улица Тестовая, 5",
        "metroStation": 4,
        "phone": "+7 999 123 45 67",
        "rentTime": 3,
        "deliveryDate": (date.today() + timedelta(days=5)).isoformat(),
        "comment": "Автоматизированный тест Sprint_7",
    }
    if colors is not None:
        payload["color"] = colors
    return payload
