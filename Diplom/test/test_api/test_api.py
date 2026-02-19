import time

import allure
import pytest

from conftest import logger
from Diplom.core.api_service import ApiService


@pytest.fixture(scope="module")
def api_client():
    """Фикстура, возвращающая клиент API с уже авторизованным контекстом."""
    return ApiService()


@pytest.fixture
def employee_data():
    timestamp = int(time.time())
    return {
        "firstName": f"TestUser{timestamp}",
        "lastName": f"LastName{timestamp}",
        "employeeId": f"AUTO{timestamp % 10000:04d}",
        "gender": "1",
    }


@pytest.fixture
def created_employee(api_client, employee_data):
    with allure.step("Создание тестового сотрудника"):
        response = api_client.create_employee(employee_data)
        employee = response["data"]
        employee_id = employee["empNumber"]
        logger.info(f"✅ Создан сотрудник ID: {employee_id}")
        yield {"id": employee_id, "data": employee, "test_data": employee_data}
    with allure.step("Удаление тестового сотрудника"):
        try:
            api_client.delete_employee([employee_id])
            logger.info(f"✅ Сотрудник {employee_id} удалён")
        except Exception as e:
            logger.warning(f"Не удалось удалить сотрудника {employee_id}: {e}")


# ---------- Тесты CRUD ----------
@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Создание сотрудника")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_create_employee(api_client, employee_data):
    with allure.step("Отправка POST-запроса"):
        response = api_client.create_employee(employee_data)
    with allure.step("Проверка ответа"):
        assert response is not None
        assert "data" in response
        employee = response["data"]
        assert employee["firstName"] == employee_data["firstName"]
        assert employee["lastName"] == employee_data["lastName"]
        assert employee.get("employeeId") == employee_data["employeeId"]
    # Очистка
    api_client.delete_employee([employee["empNumber"]])


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Получение сотрудника")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_get_employee(api_client, created_employee):
    employee_id = created_employee["id"]
    with allure.step(f"Запрос GET для ID {employee_id}"):
        response = api_client.get_employee(employee_id)
    with allure.step("Проверка данных"):
        assert response["data"]["empNumber"] == employee_id
        assert (
            response["data"]["firstName"] == created_employee["test_data"]["firstName"]
        )
        assert response["data"]["lastName"] == created_employee["test_data"]["lastName"]


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Обновление сотрудника")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_update_employee(api_client, created_employee):
    employee_id = created_employee["id"]
    update_data = {
        "firstName": "UpdatedFirstName",
        "lastName": "UpdatedLastName",
        "middleName": "MiddleName",
        "gender": "2",
    }
    with allure.step(f"PUT для ID {employee_id}"):
        response = api_client.update_employee(employee_id, update_data)
    with allure.step("Проверка обновлённых полей"):
        updated = response["data"]
        assert updated["firstName"] == update_data["firstName"]
        assert updated["lastName"] == update_data["lastName"]
        assert updated["middleName"] == update_data["middleName"]
        assert updated["gender"] == update_data["gender"]


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Удаление сотрудника")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_delete_employee(api_client):
    with allure.step("Создание временного сотрудника"):
        timestamp = int(time.time())
        temp_data = {
            "firstName": f"TempToDelete{timestamp}",
            "lastName": "ForDeletion",
            "employeeId": f"TEMP{timestamp % 10000:04d}",
        }
        create_resp = api_client.create_employee(temp_data)
        employee_id = create_resp["data"]["empNumber"]
    with allure.step("Удаление сотрудника"):
        delete_resp = api_client.delete_employee([employee_id])
        assert delete_resp is not None
    with allure.step("Проверка удаления"):
        try:
            api_client.get_employee(employee_id)
            pytest.fail("Сотрудник всё ещё доступен")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e)


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Список сотрудников")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_get_employees_list(api_client):
    with allure.step("Запрос списка (limit=5)"):
        response = api_client.get_employees_list(limit=5)
    with allure.step("Проверка структуры"):
        assert "data" in response
        assert isinstance(response["data"], list)
        logger.info(f"Получено {len(response['data'])} сотрудников")
        if response["data"]:
            sample = response["data"][0]
            assert "empNumber" in sample
            assert "firstName" in sample
            assert "lastName" in sample


# ---------- Негативные сценарии ----------
@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Негативные сценарии")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
@pytest.mark.parametrize(
    "data, description",
    [
        ({"firstName": "", "lastName": ""}, "Пустые имя и фамилия"),
        ({"firstName": "Test", "lastName": ""}, "Отсутствует фамилия"),
        ({"firstName": "", "lastName": "User"}, "Отсутствует имя"),
    ],
)
def test_create_employee_invalid_data(api_client, data, description):
    with allure.step(f"Тест: {description}"):
        try:
            api_client.create_employee(data)
            pytest.fail("Сервер не вернул ошибку на некорректные данные")
        except Exception as e:
            # Ожидаем 400 или 422
            assert any(
                code in str(e) for code in ["400", "422"]
            ), f"Неверный код ошибки: {e}"


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Негативные сценарии")
@pytest.mark.parametrize("employee_id", ["999999", "invalid_id", "0", "-1"])
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_get_nonexistent_employee(api_client, employee_id):
    with allure.step(f"Запрос с ID = {employee_id}"):
        try:
            api_client.get_employee(employee_id)
            pytest.fail("Сервер вернул данные для несуществующего ID")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e)


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Негативные сценарии")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_update_nonexistent_employee(api_client):
    fake_id = "888888"
    update_data = {"firstName": "Updated", "lastName": "Name"}
    with allure.step(f"Обновление ID {fake_id}"):
        try:
            api_client.update_employee(fake_id, update_data)
            pytest.fail("Обновление несуществующего сотрудника прошло без ошибки")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e)


# ---------- Интеграционные тесты ----------
@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_complete_crud_flow(api_client):
    timestamp = int(time.time())
    employee_data = {
        "firstName": f"CrudTest{timestamp}",
        "lastName": f"Flow{timestamp}",
        "employeeId": f"CRUD{timestamp % 10000:04d}",
    }
    with allure.step("1. Создание сотрудника"):
        create_resp = api_client.create_employee(employee_data)
        emp_id = create_resp["data"]["empNumber"]
        assert create_resp["data"]["firstName"] == employee_data["firstName"]
    with allure.step("2. Получение сотрудника"):
        get_resp = api_client.get_employee(emp_id)
        assert get_resp["data"]["empNumber"] == emp_id
    with allure.step("3. Обновление данных"):
        update_data = {"firstName": "UpdatedCrud", "lastName": "UpdatedFlow"}
        update_resp = api_client.update_employee(emp_id, update_data)
        assert update_resp["data"]["firstName"] == "UpdatedCrud"
    with allure.step("4. Удаление сотрудника"):
        api_client.delete_employee([emp_id])
    with allure.step("5. Проверка удаления"):
        try:
            api_client.get_employee(emp_id)
            pytest.fail("Сотрудник не был удалён")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e)


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_search_employees(api_client, created_employee):
    name = created_employee["test_data"]["firstName"]
    with allure.step(f"Поиск по имени '{name}'"):
        result = api_client.search_employees(name=name, limit=10)
    found = any(
        emp["empNumber"] == created_employee["id"] for emp in result.get("data", [])
    )
    assert found


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@pytest.mark.skip(reason="Тест отключен из-за явного отсутствия CSRF токена")
def test_employee_pagination(api_client):
    page1 = api_client.get_employees_list(limit=5, offset=0)["data"]
    page2 = api_client.get_employees_list(limit=5, offset=5)["data"]
    ids1 = {emp["empNumber"] for emp in page1}
    ids2 = {emp["empNumber"] for emp in page2}
    assert ids1.isdisjoint(ids2), "Страницы пересекаются"
