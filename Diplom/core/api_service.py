import json
import re
import time
from typing import Any, Dict, List

import requests

from conftest import logger


class ApiService:
    """
    Сервис для работы с API OrangeHRM (CRUD сотрудников)
    """

    def __init__(self):
        self.base_url = "https://opensource-demo.orangehrmlive.com"
        self.session = requests.Session()
        self._login()

    def _login(self) -> bool:
        """Авторизация через веб-форму (получение сессионной куки) и CSRF-токена."""
        try:
            logger.info("🔐 Начинаем авторизацию в OrangeHRM...")

            # 1. Получаем страницу логина и CSRF-токен
            login_page_url = f"{self.base_url}/web/index.php/auth/login"
            response = self.session.get(login_page_url)
            if response.status_code != 200:
                logger.error(f"Ошибка получения страницы логина: {response.status_code}")
                return False

            # 2. Извлекаем CSRF-токен из страницы логина
            csrf_token = self._extract_csrf_token(response.text)
            if csrf_token:
                logger.info(f"CSRF токен получен: {csrf_token[:20]}...")
            else:
                logger.warning("CSRF токен не найден на странице логина")

            # 3. Отправляем POST-запрос на валидацию
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
                    "Referer": login_page_url,
                },
                allow_redirects=True,
            )

            # Проверяем успешность логина и наличие куки
            if auth_response.status_code == 200 and "orangehrm" in self.session.cookies:
                # После логина переходим на дашборд, чтобы получить актуальный CSRF-токен для API
                dashboard_url = f"{self.base_url}/web/index.php/dashboard/index"
                dashboard_response = self.session.get(dashboard_url)
                if dashboard_response.status_code == 200:
                    csrf_token = self._extract_csrf_token(dashboard_response.text)
                    if csrf_token:
                        # Сохраняем токен в заголовках для всех будущих запросов
                        self.session.headers.update({"X-CSRF-TOKEN": csrf_token})
                        logger.info(f"✅ CSRF-токен получен и сохранён: {csrf_token[:10]}...")
                        return True
                    else:
                        logger.warning("CSRF-токен не найден на дашборде")
                        return False  # без токена API не будет работать
                else:
                    logger.error("Не удалось загрузить дашборд после логина")
                    return False
            else:
                logger.error(f"Ошибка авторизации. Status: {auth_response.status_code}")
                return False

        except Exception as e:
            logger.error(f"❌ Исключение при авторизации: {e}")
            return False


    @staticmethod
    def _extract_csrf_token(html: str) -> str:
        patterns = [
            r'<meta name="csrf-token" content="([^"]+)"',
            r'<input type="hidden" name="_csrf" value="([^"]+)"',
            r"window\.csrfToken = '([^']+)'",
        ]
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                return match.group(1)
        return ""

    def _log_request(self, method: str, url: str, **kwargs):
        """Логирование деталей запроса"""
        logger.info(f"➡️  [{method}] {url}")
        if kwargs.get("params"):
            logger.info(f"📋 Параметры: {kwargs['params']}")
        if kwargs.get("json"):
            logger.info(f"📦 Тело запроса: {json.dumps(kwargs['json'], indent=2, ensure_ascii=False)}")

    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        logger.info(f"⬅️  Ответ: {response.status_code} {response.reason}")
        try:
            if response.text:
                if response.headers.get("content-type", "").startswith("application/json"):
                    logger.info(f"📄 Тело ответа: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
                else:
                    logger.info(f"📄 Тело ответа: {response.text[:500]}...")
        except Exception:
            logger.info(f"📄 Тело ответа: {response.text[:500]}...")

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Выполнение HTTP-запроса с логированием и обработкой ошибок"""
        self._log_request(method, url, **kwargs)
        try:
            response = self.session.request(method, url, **kwargs)
            self._log_response(response)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ HTTP ошибка: {e}")
            # Добавляем детали ответа, если есть
            if e.response is not None:
                try:
                    logger.error(f"Тело ошибки: {e.response.text[:500]}")
                except:
                    pass
            raise
        except Exception as e:
            logger.error(f"❌ Ошибка запроса: {e}")
            raise

    # ---------- Основные методы API ----------
    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST /employees – создание сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        timestamp = int(time.time())
        # Данные по умолчанию (если не переданы)
        data = {
            "firstName": f"Test{timestamp}",
            "lastName": f"User{timestamp}",
            "employeeId": f"EMP{timestamp % 10000:04d}",
        }
        data.update(employee_data)
        response = self._request("POST", url, json=data)
        return response.json()

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """GET /employees/{id}/personal-details – получение сотрудника по ID"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"
        response = self._request("GET", url)
        return response.json()

    def get_employees_list(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """GET /employees – список сотрудников с пагинацией"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"limit": limit, "offset": offset}
        response = self._request("GET", url, params=params)
        return response.json()

    def update_employee(self, employee_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT /employees/{id}/personal-details – обновление данных сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"
        response = self._request("PUT", url, json=update_data)
        return response.json()

    def delete_employee(self, employee_ids: List[str]) -> Dict[str, Any]:
        """DELETE /employees – удаление одного или нескольких сотрудников"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        data = {"ids": employee_ids}
        response = self._request("DELETE", url, json=data)
        return response.json()

    def search_employees(self, name: str = "", limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """GET /employees с фильтром по имени (поиск)"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name # type: ignore
        response = self._request("GET", url, params=params)
        return response.json()

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