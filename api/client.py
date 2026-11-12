"""Методы взаимодействия с HTTP API Яндекс Самокат."""

import os

import allure
import requests


DEFAULT_BASE_URL = "https://qa-scooter.praktikum-services.ru"


class ScooterApi:
    """Одна точка входа для HTTP-запросов тестов."""

    def __init__(self, session: requests.Session):
        self.session = session
        self.base_url = os.environ.get("SCOOTER_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.timeout = (10, 45)  # время соединения и чтения ответа, секунды

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    @allure.step("POST /api/v1/courier — создать курьера")
    def create_courier(self, payload: dict) -> requests.Response:
        return self.session.post(
            self._url("/api/v1/courier"), json=payload, timeout=self.timeout
        )

    @allure.step("POST /api/v1/courier/login — авторизовать курьера")
    def login_courier(self, payload: dict) -> requests.Response:
        return self.session.post(
            self._url("/api/v1/courier/login"), json=payload, timeout=self.timeout
        )

    @allure.step("DELETE /api/v1/courier/{courier_id} — удалить курьера")
    def delete_courier(self, courier_id: int) -> requests.Response:
        return self.session.delete(
            self._url(f"/api/v1/courier/{courier_id}"), timeout=self.timeout
        )

    @allure.step("POST /api/v1/orders — создать заказ")
    def create_order(self, payload: dict) -> requests.Response:
        return self.session.post(
            self._url("/api/v1/orders"), json=payload, timeout=self.timeout
        )

    @allure.step("GET /api/v1/orders — получить список заказов")
    def get_orders(self) -> requests.Response:
        # Параметр limit ограничивает размер ответа с общего учебного сервера.
        return self.session.get(
            self._url("/api/v1/orders"),
            params={"limit": 10, "page": 0},
            timeout=(10, 90),
        )

    @allure.step("PUT /api/v1/orders/cancel — отменить созданный тестовый заказ")
    def cancel_order(self, track: int) -> requests.Response:
        return self.session.put(
            self._url("/api/v1/orders/cancel"),
            params={"track": track},
            timeout=self.timeout,
        )
