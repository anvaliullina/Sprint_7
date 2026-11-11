"""Фикстуры: подготовка и очистка тестовых данных после каждого теста."""

import warnings

import allure
import pytest
import requests

from api.client import ScooterApi
from generators import generate_courier


@pytest.fixture
def api():
    """Отдельная сессия HTTP для каждого теста."""
    with requests.Session() as session:
        yield ScooterApi(session)


@pytest.fixture
def courier_cleanup(api):
    """Удалить курьеров, созданных в рамках теста, даже при ошибке assert."""
    couriers = []
    yield couriers
    for courier in couriers:
        if "login" not in courier or "password" not in courier:
            continue
        try:
            response = api.login_courier(
                {"login": courier["login"], "password": courier["password"]}
            )
            if response.status_code == 200:
                courier_id = response.json().get("id")
                if isinstance(courier_id, int):
                    deletion = api.delete_courier(courier_id)
                    if deletion.status_code != 200:
                        warnings.warn(
                            f"Не удалось удалить тестового курьера: {deletion.status_code}",
                            stacklevel=1,
                        )
        except (requests.RequestException, ValueError, TypeError) as exc:
            warnings.warn(f"Ошибка очистки тестового курьера: {exc}", stacklevel=1)


@pytest.fixture
def registered_courier(api, courier_cleanup):
    """Создать уникального курьера до теста, удалить после."""
    data = generate_courier()
    with allure.step("Подготовка: зарегистрировать нового курьера"):
        response = api.create_courier(data)
        assert response.status_code == 201, (
            f"Не удалось подготовить курьера: {response.status_code} {response.text}"
        )
        courier_cleanup.append(data)
    return data


@pytest.fixture
def order_cleanup(api):
    """Отменить тестовые заказы по их track после завершения проверки."""
    tracks = []
    yield tracks
    for track in tracks:
        try:
            response = api.cancel_order(track)
            if response.status_code != 200:
                warnings.warn(
                    f"Не удалось отменить тестовый заказ {track}: "
                    f"{response.status_code} {response.text[:200]}",
                    stacklevel=1,
                )
        except requests.RequestException as exc:
            warnings.warn(f"Ошибка отмены заказа {track}: {exc}", stacklevel=1)
