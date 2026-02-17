import json
import time
from typing import Any, Dict, List

from playwright.sync_api import APIRequestContext
from selenium.common import TimeoutException

from conftest import logger


class OrangeHRMApiClient:
    """Клиент для работы с API OrangeHRM (CRUD сотрудников)"""

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def _log_request(self, method: str, url: str, **kwargs):
        logger.info(f"➡️  [{method}] {url}")
        if kwargs.get("params"):
            logger.info(f"📋 Параметры: {kwargs['params']}")
        if kwargs.get("data"):
            logger.info(
                f"📦 Тело запроса: {json.dumps(kwargs['data'], indent=2, ensure_ascii=False)}"
            )
        if kwargs.get("json"):
            logger.info(
                f"📦 Тело запроса: {json.dumps(kwargs['json'], indent=2, ensure_ascii=False)}"
            )

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"/web/index.php/api/v2{path}"
        self._log_request(method, url, **kwargs)
        response = self.request.fetch(method, url, **kwargs)  # type: ignore
        logger.info(f"⬅️  Ответ: {response.status} {response.status_text}")
        try:
            body = response.json()
            logger.info(
                f"📄 Тело ответа: {json.dumps(body, indent=2, ensure_ascii=False)}"
            )
        except TimeoutException:
            body = response.text()
            logger.info(f"📄 Тело ответа: {body[:500]}...")
        response.raise_for_status()  # type: ignore
        return body

    # ---------- Основные методы ----------
    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /pim/employees – создание сотрудника"""
        timestamp = int(time.time())
        data = {
            "firstName": f"Test{timestamp}",
            "lastName": f"User{timestamp}",
            "employeeId": f"EMP{timestamp % 10000:04d}",
        }
        data.update(employee_data)
        return self._request("POST", "/pim/employees", json=data)

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """GET /pim/employees/{id}/personal-details – получение сотрудника по ID"""
        return self._request("GET", f"/pim/employees/{employee_id}/personal-details")

    def get_employees_list(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """GET /pim/employees – список сотрудников с пагинацией"""
        return self._request(
            "GET", "/pim/employees", params={"limit": limit, "offset": offset}
        )

    def update_employee(
        self, employee_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """PUT /pim/employees/{id}/personal-details – обновление данных"""
        return self._request(
            "PUT", f"/pim/employees/{employee_id}/personal-details", json=update_data
        )

    def delete_employee(self, employee_ids: List[str]) -> Dict[str, Any]:
        """DELETE /pim/employees – удаление одного или нескольких сотрудников"""
        return self._request("DELETE", "/pim/employees", json={"ids": employee_ids})

    def search_employees(
        self, name: str = "", limit: int = 10, offset: int = 0
    ) -> Dict[str, Any]:
        """GET /pim/employees с фильтром по имени"""
        params = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name  # type: ignore
        return self._request("GET", "/pim/employees", params=params)

    def cleanup_test_employees(self, name_prefix: str = "Test") -> Dict[str, Any]:
        """Удаление тестовых сотрудников по префиксу имени"""
        try:
            employees = self.get_employees_list(limit=50).get("data", [])
            test_ids = [
                emp["empNumber"]
                for emp in employees
                if emp.get("firstName", "").startswith(name_prefix)
            ]
            if test_ids:
                logger.info(f"🧹 Удаление {len(test_ids)} тестовых сотрудников")
                return self.delete_employee(test_ids)
            return {"data": []}
        except Exception as e:
            logger.error(f"Ошибка при очистке тестовых сотрудников: {e}")
            return {"data": []}
