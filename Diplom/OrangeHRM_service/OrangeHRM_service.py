import requests
import json
import time

from typing import Dict, Any, List


class OrangeHRMService:
    """
    Простой сервис для работы с API OrangeHRM
    Только основные CRUD операции с логированием
    """

    def __init__(self):
        self.base_url = "https://opensource-demo.orangehrmlive.com"
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Настройка сессии с авторизацией"""
        try:
            # 1. Получаем CSRF токен
            login_page = self.session.get(f"{self.base_url}/web/index.php/auth/login")

            # 2. Авторизация
            auth_data = {
                "username": "Admin",
                "password": "admin123",
                "_csrf": self._extract_csrf_token(login_page.text)
            }

            auth_response = self.session.post(
                f"{self.base_url}/web/index.php/auth/validate",
                data=auth_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            if auth_response.status_code == 200:
                print("[INFO] Авторизация в OrangeHRM успешна")
            else:
                print(f"[WARN] Статус авторизации: {auth_response.status_code}")

        except Exception as e:
            print(f"[ERROR] Ошибка настройки сессии: {e}")

    def _extract_csrf_token(self, html: str) -> str:
        """Извлечение CSRF токена из HTML"""
        # Простой парсинг - в реальном проекте нужно адаптировать
        if '_csrf' in html:
            start = html.find('_csrf') + 8
            end = html.find('"', start)
            return html[start:end]
        return ""

    def _log_request(self, method: str, url: str, data: Dict = None):
        """Логирование запроса"""
        print(f"[API] {method} {url}")
        if data:
            print(f"[API] Data: {json.dumps(data, indent=2)[:200]}...")

    def _log_response(self, response: requests.Response):
        """Логирование ответа"""
        status = "✅" if response.status_code < 400 else "❌"
        print(f"[API] {status} Status: {response.status_code}")

        if response.status_code >= 400:
            print(f"[API] Error: {response.text[:200]}")

    # ============ CRUD МЕТОДЫ ============

    def create_employee(self, employee_data: Dict[str, Any]) -> Dict[str, Any]:
        """POST: Создание сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"

        # Стандартные данные
        data = {
            "firstName": employee_data.get("firstName", f"Test{int(time.time())}"),
            "lastName": employee_data.get("lastName", f"User{int(time.time())}"),
            "employeeId": employee_data.get("employeeId", f"EMP{int(time.time()) % 1000}")
        }

        self._log_request("POST", url, data)

        try:
            response = self.session.post(url, json=data)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка создания: {e}")
            raise

    def get_employee(self, employee_id: str) -> Dict[str, Any]:
        """GET: Получение данных сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"

        self._log_request("GET", url)

        try:
            response = self.session.get(url)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка получения: {e}")
            raise

    def get_employees_list(self, limit: int = 10) -> Dict[str, Any]:
        """GET: Получение списка сотрудников"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"limit": limit, "offset": 0}

        self._log_request("GET", url, params)

        try:
            response = self.session.get(url, params=params)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка получения списка: {e}")
            raise

    def update_employee(self, employee_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT: Обновление данных сотрудника"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees/{employee_id}/personal-details"

        self._log_request("PUT", url, update_data)

        try:
            response = self.session.put(url, json=update_data)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка обновления: {e}")
            raise

    def delete_employee(self, employee_ids: List[str]) -> Dict[str, Any]:
        """DELETE: Удаление сотрудника/сотрудников"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        data = {"ids": employee_ids}

        self._log_request("DELETE", url, data)

        try:
            response = self.session.delete(url, json=data)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка удаления: {e}")
            raise

    def search_employees(self, name: str = "") -> Dict[str, Any]:
        """Поиск сотрудников по имени"""
        url = f"{self.base_url}/web/index.php/api/v2/pim/employees"
        params = {"name": name} if name else {}

        self._log_request("GET", url, params)

        try:
            response = self.session.get(url, params=params)
            self._log_response(response)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] Ошибка поиска: {e}")
            raise