import time

import allure
import pytest

from conftest import logger
from Diplom.core.api_service import ApiService


# ---------- Фикстуры ----------
@pytest.fixture(scope="module")
def orangehrm_service():
    """Фикстура для сервиса OrangeHRM (инициализация один раз на модуль)"""
    logger.info("Инициализация OrangeHRM сервиса...")
    service = ApiService()
    # Проверка доступности
    try:
        resp = service.get_employees_list(limit=1)
        logger.info(f"Сервис доступен. Всего сотрудников: {resp.get('meta', {}).get('total', 'неизвестно')}")
    except Exception as e:
        logger.error(f"Сервис недоступен: {e}")
        pytest.skip(f"Не удалось инициализировать OrangeHRM сервис: {e}")
    yield service
    # Очистка после всех тестов
    try:
        service.cleanup_test_employees("Test")
    except Exception as e:
        logger.warning(f"Очистка не удалась: {e}")
    logger.info("Очистка после тестов завершена")


@pytest.fixture
def test_employee_data():
    """Генерация уникальных данных для нового сотрудника"""
    timestamp = int(time.time())
    return {
        "firstName": f"TestUser{timestamp}",
        "lastName": f"LastName{timestamp}",
        "employeeId": f"AUTO{timestamp % 10000:04d}",
        "gender": "1",
    }


@pytest.fixture
def created_employee(orangehrm_service, test_employee_data):
    """Фикстура, создающая сотрудника и возвращающая его данные, затем удаляющая"""
    with allure.step("Создание тестового сотрудника"):
        response = orangehrm_service.create_employee(test_employee_data)
        employee = response["data"]
        employee_id = employee["empNumber"]
        logger.info(f"✅ Создан сотрудник ID: {employee_id}")
        yield {"id": employee_id, "data": employee, "test_data": test_employee_data}
    # Удаление после теста
    with allure.step("Удаление тестового сотрудника"):
        try:
            orangehrm_service.delete_employee([employee_id])
            logger.info(f"✅ Сотрудник {employee_id} удалён")
        except Exception as e:
            logger.warning(f"Не удалось удалить сотрудника {employee_id}: {e}")


# ---------- Тесты CRUD ----------
@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Создание сотрудника")
def test_create_employee(orangehrm_service, test_employee_data):
    """POST /employees – проверка создания сотрудника"""
    with allure.step("Отправка POST-запроса"):
        response = orangehrm_service.create_employee(test_employee_data)
    with allure.step("Проверка ответа"):
        assert response is not None, "Ответ отсутствует"
        assert "data" in response, "Нет поля 'data'"
        employee = response["data"]
        assert employee["firstName"] == test_employee_data["firstName"]
        assert employee["lastName"] == test_employee_data["lastName"]
        assert employee.get("employeeId") == test_employee_data["employeeId"]
    # Удаление созданного сотрудника (вручную, т.к. фикстура не используется)
    employee_id = employee["empNumber"]
    orangehrm_service.delete_employee([employee_id])
    allure.attach(str(employee), name="created_employee", attachment_type=allure.attachment_type.JSON)


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Получение сотрудника")
def test_get_employee(orangehrm_service, created_employee):
    """GET /employees/{id} – получение данных сотрудника"""
    employee_id = created_employee["id"]
    with allure.step(f"Запрос GET для ID {employee_id}"):
        response = orangehrm_service.get_employee(employee_id)
    with allure.step("Проверка соответствия данных"):
        assert response["data"]["empNumber"] == employee_id
        assert response["data"]["firstName"] == created_employee["test_data"]["firstName"]
        assert response["data"]["lastName"] == created_employee["test_data"]["lastName"]


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Обновление сотрудника")
def test_update_employee(orangehrm_service, created_employee):
    """PUT /employees/{id} – обновление данных сотрудника"""
    employee_id = created_employee["id"]
    update_data = {
        "firstName": "UpdatedFirstName",
        "lastName": "UpdatedLastName",
        "middleName": "MiddleName",
        "gender": "2",
    }
    with allure.step(f"Отправка PUT-запроса для ID {employee_id}"):
        response = orangehrm_service.update_employee(employee_id, update_data)
    with allure.step("Проверка обновлённых полей"):
        updated = response["data"]
        assert updated["firstName"] == update_data["firstName"]
        assert updated["lastName"] == update_data["lastName"]
        assert updated["middleName"] == update_data["middleName"]
        assert updated["gender"] == update_data["gender"]


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Удаление сотрудника")
def test_delete_employee(orangehrm_service):
    """DELETE /employees – удаление сотрудника"""
    # Сначала создадим временного сотрудника
    with allure.step("Создание временного сотрудника для удаления"):
        timestamp = int(time.time())
        temp_data = {
            "firstName": f"TempToDelete{timestamp}",
            "lastName": "ForDeletion",
            "employeeId": f"TEMP{timestamp % 10000:04d}",
        }
        create_resp = orangehrm_service.create_employee(temp_data)
        employee_id = create_resp["data"]["empNumber"]
    with allure.step("Удаление сотрудника"):
        delete_resp = orangehrm_service.delete_employee([employee_id])
        assert delete_resp is not None, "Ответ на DELETE отсутствует"
    with allure.step("Проверка, что сотрудник действительно удалён"):
        try:
            orangehrm_service.get_employee(employee_id)
            pytest.fail("Сотрудник всё ещё доступен после удаления")
        except Exception as e:
            # Ожидаем 404 или подобную ошибку
            assert "404" in str(e) or "Not Found" in str(e), f"Неожиданная ошибка: {e}"


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Список сотрудников")
def test_get_employees_list(orangehrm_service):
    """GET /employees – получение списка с пагинацией"""
    with allure.step("Запрос первой страницы (limit=5, offset=0)"):
        response = orangehrm_service.get_employees_list(limit=5)
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
@allure.title("Создание сотрудника с пустыми обязательными полями")
@pytest.mark.parametrize("data, description", [
    ({"firstName": "", "lastName": ""}, "Пустые имя и фамилия"),
    ({"firstName": "Test", "lastName": ""}, "Отсутствует фамилия"),
    ({"firstName": "", "lastName": "User"}, "Отсутствует имя"),
])
def test_create_employee_invalid_data(orangehrm_service, data, description):
    """Попытка создания сотрудника с некорректными данными"""
    with allure.step(f"Тест: {description}"):
        try:
            orangehrm_service.create_employee(data)
            # Если запрос прошёл без ошибки – проверяем, не вернул ли сервер ошибку в теле
            pytest.fail("Сервер не вернул ошибку на некорректные данные")
        except Exception as e:
            # Ожидаем исключение (HTTP 400 или 422)
            assert any(code in str(e) for code in ["400", "422"]), f"Неверный код ошибки: {e}"


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Негативные сценарии")
@allure.title("Получение несуществующего сотрудника")
@pytest.mark.parametrize("employee_id", ["999999", "invalid_id", "0", "-1"])
def test_get_nonexistent_employee(orangehrm_service, employee_id):
    """GET для несуществующего ID должен возвращать 404"""
    with allure.step(f"Запрос с ID = {employee_id}"):
        try:
            orangehrm_service.get_employee(employee_id)
            pytest.fail(f"Сервер вернул данные для несуществующего ID {employee_id}")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e), f"Ожидалась 404, получено: {e}"


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Негативные сценарии")
@allure.title("Обновление несуществующего сотрудника")
def test_update_nonexistent_employee(orangehrm_service):
    """PUT для несуществующего ID должен возвращать 404"""
    fake_id = "888888"
    update_data = {"firstName": "Updated", "lastName": "Name"}
    with allure.step(f"Обновление ID {fake_id}"):
        try:
            orangehrm_service.update_employee(fake_id, update_data)
            pytest.fail("Обновление несуществующего сотрудника прошло без ошибки")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e), f"Ожидалась 404, получено: {e}"


# ---------- Интеграционные тесты ----------
@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@allure.title("Полный цикл CRUD")
def test_complete_crud_flow(orangehrm_service):
    """Последовательное выполнение всех операций с одним сотрудником"""
    timestamp = int(time.time())
    employee_data = {
        "firstName": f"CrudTest{timestamp}",
        "lastName": f"Flow{timestamp}",
        "employeeId": f"CRUD{timestamp % 10000:04d}",
    }
    # CREATE
    with allure.step("1. Создание сотрудника"):
        create_resp = orangehrm_service.create_employee(employee_data)
        emp_id = create_resp["data"]["empNumber"]
        assert create_resp["data"]["firstName"] == employee_data["firstName"]
    # READ
    with allure.step("2. Получение созданного сотрудника"):
        get_resp = orangehrm_service.get_employee(emp_id)
        assert get_resp["data"]["empNumber"] == emp_id
    # UPDATE
    with allure.step("3. Обновление данных"):
        update_data = {"firstName": "UpdatedCrud", "lastName": "UpdatedFlow"}
        update_resp = orangehrm_service.update_employee(emp_id, update_data)
        assert update_resp["data"]["firstName"] == "UpdatedCrud"
    # DELETE
    with allure.step("4. Удаление сотрудника"):
        orangehrm_service.delete_employee([emp_id])
    # VERIFY DELETION
    with allure.step("5. Проверка удаления"):
        try:
            orangehrm_service.get_employee(emp_id)
            pytest.fail("Сотрудник не был удалён")
        except Exception as e:
            assert "404" in str(e) or "Not Found" in str(e)


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@allure.title("Поиск сотрудников по имени")
def test_search_employees(orangehrm_service, created_employee):
    """Поиск созданного сотрудника по имени"""
    name = created_employee["test_data"]["firstName"]
    with allure.step(f"Поиск по имени '{name}'"):
        result = orangehrm_service.search_employees(name=name, limit=10)
    found = any(emp["empNumber"] == created_employee["id"] for emp in result.get("data", []))
    assert found, f"Сотрудник с именем {name} не найден"


@allure.epic("OrangeHRM API")
@allure.feature("Employees")
@allure.story("Интеграционные сценарии")
@allure.title("Пагинация списка сотрудников")
def test_employee_pagination(orangehrm_service):
    """Проверка, что страницы не пересекаются"""
    page1 = orangehrm_service.get_employees_list(limit=5, offset=0)["data"]
    page2 = orangehrm_service.get_employees_list(limit=5, offset=5)["data"]
    ids1 = {emp["empNumber"] for emp in page1}
    ids2 = {emp["empNumber"] for emp in page2}
    assert ids1.isdisjoint(ids2), "Страницы пересекаются (одинаковые ID)"
    logger.info(f"Пагинация работает: первая страница {len(page1)}, вторая {len(page2)}")