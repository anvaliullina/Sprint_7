
"""Позитивные и негативные проверки создания курьера."""

import allure
import pytest

from generators import generate_courier


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьер успешно создаётся, ответ 201 и ok=true")
    def test_create_courier_success(self, api, courier_cleanup):
        courier = generate_courier()

        courier_cleanup.append(courier)
        response = api.create_courier(courier)

        assert response.status_code == 201, response.text
        assert response.json() == {"ok": True}

    @allure.title("Повторное создание курьера с тем же логином запрещено")
    def test_duplicate_courier_returns_409(self, api, registered_courier):
        response = api.create_courier(registered_courier)

        assert response.status_code == 409, response.text
        assert response.json().get("message", "").startswith(
            "Этот логин уже используется"
        )

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Без обязательного поля {missing_field} курьера создать нельзя")
    def test_missing_required_field_returns_400(
        self, api, missing_field
    ):
        courier = generate_courier()
        courier.pop(missing_field)

        response = api.create_courier(courier)

        assert response.status_code == 400, response.text
        assert response.json().get("message") == (
            "Недостаточно данных для создания учетной записи"
        )

    @pytest.mark.parametrize("empty_field", ["login", "password"])
    @allure.title("С пустым обязательным полем {empty_field} курьера создать нельзя")
    def test_empty_required_field_returns_400(
        self, api, empty_field
    ):
        courier = generate_courier()
        courier[empty_field] = ""

        response = api.create_courier(courier)

        assert response.status_code == 400, response.text
        assert response.json().get("message") == (
            "Недостаточно данных для создания учетной записи"
        )
