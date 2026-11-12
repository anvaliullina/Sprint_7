"""Проверка получения списка заказов."""

import allure


@allure.feature("Список заказов")
class TestGetOrders:
    @allure.title("GET /api/v1/orders возвращает список заказов")
    def test_get_orders_returns_list(self, api):
        response = api.get_orders()

        assert response.status_code == 200, response.text[:300]
        body = response.json()
        assert isinstance(body, dict)
        assert "orders" in body
        assert isinstance(body["orders"], list)
