import json
import re
import time
from typing import Any, Dict, List, Optional

import requests

from conftest import logger


class OrangeHRMService:
    """
    Сервис для работы с API OrangeHRM
    CRUD операции с сотрудниками
    """

    def __init__(self):
        self.base_url = "https://opensource-demo.orangehrmlive.com"
        self.session = requests.Session()
        self._login()

    def _login(self) -> bool:
        """Авторизация с использованием CSRF токена и сессионных кук"""
        try:
            logger.info("🔐 Начинаем авторизацию в OrangeHRM...")

            # 1. Получаем страницу логина и CSRF токен
            login_url = f"{self.base_url}/web/index.php/auth/login"
            response = self.session.get(login_url)

            if response.status_code != 200:
                logger.error(
                    f"Ошибка получения страницы логина: {response.status_code}"
                )
                return False

            # 2. Извлекаем CSRF токен
            csrf_token = self._extract_csrf_token(response.text)
            logger.info(
                f"Получен CSRF токен: {csrf_token[:20]}..."
                if csrf_token
                else "CSRF токен не найден"
            )

            # 3. Авторизация
            login_data = {
                "username": "Admin",
                "password": "admin123",
            }

            if csrf_token:
                login_data["_csrf"] = csrf_token

            auth_response = self.session.post(
                f"{self.base_url}/web/index.php/auth/validate",
                data=login_data,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": login_url,
                },
                allow_redirects=True,
            )

            # 4. Проверяем успешность авторизации
            if auth_response.status_code == 200:
                cookies = self.session.cookies.get_dict()

                if "orangehrm" in cookies:
                    logger.info(
                        f"✅ Авторизация успешна! Получена кука: orangehrm={cookies['orangehrm'][:10]}..."
                    )
                    logger.info(f"Все куки: {list(cookies.keys())}")
                    return True
                else:
                    logger.warning("Кука 'orangehrm' не найдена после авторизации")
                    return False
            else:
                logger.error(f"Ошибка авторизации. Status: {auth_response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Исключение при авторизации: {e}")
            return False

    def _extract_csrf_token(self, html: str) -> str:
        """Извлечение CSRF токена из HTML"""
        patterns = [
            r'<meta name="csrf-token" content="([^"]+)"',
            r'<input type="hidden" name="_csrf" value="([^"]+)"',
            r"window\.csrfToken = '([^']+)'",
            r'"csrfToken":"([^"]+)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return ""

    def _log_request(self, method: str, url: str, data: Any = None, params: Any = None):
        """Логирование запроса"""
        logger.info(f"➡️  [{method}] {url}")
        if params:
            logger.info(f"📋 Параметры: {params}")
        if data:
            logger.info(f"📦 Тело запроса: {json.dumps(data, indent=2)}")

    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        logger.info(f"⬅️  Ответ: {response.status_code} {response.reason}")
        try:
            if response.text:
                logger.info(f"📄 Тело ответа: {json.dumps(response.json(), indent=2)}")
        except:
            logger.info(f"📄 Тело ответа: {response.text[:500]}...")

    def _handle_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Обработка запроса с логированием"""
        self._log_request(method, url, kwargs.get("json"), kwargs.get("params"))

        try:
            response = getattr(self.session, method.lower())(url, **kwargs)
            self._log_response(response)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ HTTP ошибка: {e}")
            logger.error(f"Детали:  'response' in locals() else 'Нет ответа'")
            raise
        except Exception as e:
            logger.error(f"❌ Ошибка запроса: {e}")
            raise

    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST: Создание сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"

        # Стандартные данные с генерацией уникальных значений
        timestamp = int(time.time())
        data = {
            "firstName": employee_data.get("firstName", f"Test{timestamp}"),
            "lastName": employee_data.get("lastName", f"User{timestamp}"),
            "employeeId": employee_data.get(
                "employeeId", f"EMP{timestamp % 10000:04d}"
            ),
        }

        # Обновляем переданными данными
        data.update(employee_data)

        response = self._handle_request("POST", url, json=data)
        return response.json()

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """GET: Получение данных сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"

        response = self._handle_request("GET", url)
        return response.json()

    def get_employees_list(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """GET: Получение списка сотрудников"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"limit": limit, "offset": offset}

        response = self._handle_request("GET", url, params=params)
        return response.json()

    def update_employee(
        self, employee_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """PUT: Обновление данных сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"

        response = self._handle_request("PUT", url, json=update_data)
        return response.json()

    def delete_employee(self, employee_ids: List[str]) -> Dict[str, Any]:
        """DELETE: Удаление сотрудника/сотрудников"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        data = {"ids": employee_ids}

        response = self._handle_request("DELETE", url, json=data)
        return response.json()

    # noinspection PyTypeChecker
    def search_employees(
        self, name: str = "", limit: int = 10, offset: int = 0
    ) -> Dict[str, Any]:
        """Поиск сотрудников по имени"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"limit": limit, "offset": offset}

        if name:
            params["name"] = name

        response = self._handle_request("GET", url, params=params)
        return response.json()

    def get_employee_by_id(self, emp_id: str) -> Optional[Dict[str, Any]]:
        """Получить сотрудника по employeeId (не по ID в системе)"""
        # Ищем через API поиска
        result = self.search_employees(name=emp_id)

        if result.get("data"):
            for employee in result["data"]:
                if employee.get("employeeId") == emp_id:
                    return employee
        return None

    def cleanup_test_employees(self, name_prefix: str = "Test"):
        """Очистка тестовых сотрудников по префиксу имени"""
        try:
            # Получаем всех сотрудников
            all_employees = self.get_employees_list(limit=50)["data"]

            # Фильтруем тестовых сотрудников
            test_employees = [
                emp["empNumber"]
                for emp in all_employees
                if emp.get("firstName", "").startswith(name_prefix)
            ]

            if test_employees:
                logger.info(f"🧹 Удаление {len(test_employees)} тестовых сотрудников")
                return self.delete_employee(test_employees)

            return {"data": []}

        except Exception as e:
            logger.error(f"Ошибка при очистке тестовых сотрудников: {e}")
            return {"data": []}
