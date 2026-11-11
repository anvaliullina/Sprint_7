"""Параметризованная проверка создания заказа с разными цветами."""

import allure
import pytest

from generators import generate_order


@allure.feature("Создание заказа")
class TestCreateOrder:
    @pytest.mark.parametrize(
        "colors",
        [
            pytest.param(["BLACK"], id="black"),
            pytest.param(["GREY"], id="grey"),
            pytest.param(["BLACK", "GREY"], id="both_colors"),
            pytest.param([], id="empty_color_array"),
            pytest.param(None, id="without_color_field"),
        ],
    )
    @allure.title("Заказ создаётся с цветами: {param_id}")
    def test_create_order_with_colors_returns_track(self, api, order_cleanup, colors):
        payload = generate_order(colors)
        response = api.create_order(payload)

        assert response.status_code == 201, response.text
        body = response.json()
        assert isinstance(body, dict)
        assert isinstance(body.get("track"), int) and body["track"] > 0
        order_cleanup.append(body["track"])
