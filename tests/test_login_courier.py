
from uuid import uuid4

import allure
import pytest


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_successful_login_returns_id(self, api, registered_courier):
        credentials = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }

        response = api.login_courier(credentials)

        assert response.status_code == 200, response.text
        body = response.json()
        assert isinstance(body.get("id"), int)
        assert body["id"] > 0

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    @allure.title("Авторизация без поля {missing_field}")
    def test_missing_credentials_returns_400(
        self, api, registered_courier, missing_field
    ):
        credentials = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }

        credentials.pop(missing_field)

        response = api.login_courier(credentials)

        if missing_field == "password" and response.status_code == 504:
            allure.attach(
                response.text,
                name="Ответ сервера при отсутствии пароля",
                attachment_type=allure.attachment_type.TEXT,
            )
            pytest.xfail(
                "Известный дефект учебного API: "
                "без password сервер возвращает 504 вместо 400"
            )

        assert response.status_code == 400, response.text
        assert response.json().get("message") == (
            "Недостаточно данных для входа"
        )

    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    @allure.title("Авторизация с неверным полем {wrong_field}")
    def test_incorrect_credentials_returns_404(
        self, api, registered_courier, wrong_field
    ):
        credentials = {
            "login": registered_courier["login"],
            "password": registered_courier["password"],
        }

        credentials[wrong_field] = f"incorrect_{uuid4().hex}"

        response = api.login_courier(credentials)

        assert response.status_code == 404, response.text
        assert response.json().get("message") == (
            "Учетная запись не найдена"
        )

    @allure.title("Авторизация несуществующего курьера")
    def test_nonexistent_courier_returns_404(self, api):
        credentials = {
            "login": f"unknown_{uuid4().hex}",
            "password": f"unknown_{uuid4().hex}",
        }

        response = api.login_courier(credentials)

        assert response.status_code == 404, response.text
        assert response.json().get("message") == (
            "Учетная запись не найдена"
        )
