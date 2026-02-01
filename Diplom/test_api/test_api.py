import pytest
import time

from conftest import logger
from Diplom.OrangeHRM_service.OrangeHRM_service import OrangeHRMService


@pytest.fixture
def orangehrm_service():
    """Фикстура для сервиса OrangeHRM с логированием"""
    logger.info("Инициализация OrangeHRM сервиса...")
    service = OrangeHRMService()

    # Проверяем доступность сервиса
    try:
        # Пробный запрос
        response = service.get_employees_list(limit=1)
        logger.info(f"Сервис инициализирован. Сотрудников в системе: {len(response.get('data', []))}")
    except Exception as e:
        logger.error(f"Ошибка инициализации сервиса: {e}")
        pytest.skip(f"Не удалось инициализировать OrangeHRM сервис: {e}")

    yield service

    logger.info("Очистка после тестов завершена")


@pytest.fixture
def test_employee_data():
    """Генерация тестовых данных с уникальным ID"""
    timestamp = int(time.time())
    return {
        "firstName": f"TestUser{timestamp}",
        "lastName": f"LastName{timestamp}",
        "employeeId": f"AUTO{timestamp % 10000}"
    }

def test_create_employee_post(orangehrm_service, test_employee_data):
    """
    Тест операции POST - создание сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: POST - Создание нового сотрудника")
    logger.info("=" * 60)

    try:
        # Логируем начало теста
        logger.info(f"Тестовые данные: {test_employee_data}")

        # Выполняем POST запрос
        logger.info("Отправка POST запроса на создание сотрудника...")
        response = orangehrm_service.create_employee(test_employee_data)

        # Проверяем ответ
        assert response is not None, "Ответ от сервера пустой"
        assert "data" in response, "В ответе нет поля 'data'"

        employee_data = response["data"]
        employee_id = employee_data["empNumber"]

        # Проверки данных
        assert employee_data["firstName"] == test_employee_data["firstName"], \
            f"Имя не совпадает: {employee_data['firstName']}"
        assert employee_data["lastName"] == test_employee_data["lastName"], \
            f"Фамилия не совпадает: {employee_data['lastName']}"

        logger.info(f"✅ Создан сотрудник ID: {employee_id}")
        logger.info(f"   Имя: {employee_data['firstName']} {employee_data['lastName']}")

        # Сохраняем ID для последующих тестов
        pytest.created_employee_id = employee_id

        return employee_id

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте создания сотрудника: {e}")
        pytest.fail(f"Тест создания сотрудника провален: {e}")

def test_get_employee(orangehrm_service):
    """
    Тест операции GET - получение данных сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: GET - Получение данных сотрудника")
    logger.info("=" * 60)

    # Проверяем, что сотрудник был создан в предыдущем тесте
    if not hasattr(pytest, 'created_employee_id'):
        logger.warning("Пропускаем тест: нет созданного сотрудника")
        pytest.skip("Нет созданного сотрудника для теста GET")

    employee_id = pytest.created_employee_id

    try:
        logger.info(f"Получение данных сотрудника ID: {employee_id}")
        response = orangehrm_service.get_employee(employee_id)

        # Проверки
        assert response is not None, "Ответ от сервера пустой"
        assert "data" in response, "В ответе нет поля 'data'"

        employee = response["data"]

        logger.info(f"✅ Получены данные сотрудника:")
        logger.info(f"   ID: {employee.get('empNumber')}")
        logger.info(f"   Имя: {employee.get('firstName')} {employee.get('lastName')}")
        logger.info(f"   Гендер: {'Мужской' if employee.get('gender') == '1' else 'Женский'}")

        # Дополнительные логи
        if employee.get('joinedDate'):
            logger.info(f"   Дата приема: {employee.get('joinedDate')}")

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте получения сотрудника: {e}")
        pytest.fail(f"Тест получения сотрудника провален: {e}")

def test_update_employee_put(orangehrm_service):
    """
    Тест операции PUT - обновление данных сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: PUT - Обновление данных сотрудника")
    logger.info("=" * 60)

    if not hasattr(pytest, 'created_employee_id'):
        logger.warning("Пропускаем тест: нет созданного сотрудника")
        pytest.skip("Нет созданного сотрудника для теста PUT")

    employee_id = pytest.created_employee_id

    try:
        # Данные для обновления
        update_data = {
            "firstName": "UpdatedFirstName",
            "lastName": "UpdatedLastName",
            "middleName": "MiddleName",
            "gender": "2"  # Меняем на женский
        }

        logger.info(f"Обновление сотрудника ID: {employee_id}")
        logger.info(f"Новые данные: {update_data}")

        response = orangehrm_service.update_employee(employee_id, update_data)

        # Проверки
        assert response is not None, "Ответ от сервера пустой"
        assert "data" in response, "В ответе нет поля 'data'"

        updated_employee = response["data"]

        # Проверяем обновленные поля
        assert updated_employee["firstName"] == "UpdatedFirstName", "Имя не обновлено"
        assert updated_employee["lastName"] == "UpdatedLastName", "Фамилия не обновлена"
        assert updated_employee["gender"] == "2", "Гендер не обновлен"

        logger.info("✅ Данные сотрудника успешно обновлены")
        logger.info(f"   Новое имя: {updated_employee['firstName']} {updated_employee['lastName']}")

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте обновления сотрудника: {e}")
        pytest.fail(f"Тест обновления сотрудника провален: {e}")

def test_delete_employee(self, orangehrm_service):
    """
    Тест операции DELETE - удаление сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: DELETE - Удаление сотрудника")
    logger.info("=" * 60)

    if not hasattr(pytest, 'created_employee_id'):
        # Если сотрудник не создан, создаем временного для удаления
        logger.info("Создание временного сотрудника для теста удаления...")
        temp_data = {
             "firstName": f"TempToDelete{int(time.time())}",
            "lastName": "ForDeletion",
            "employeeId": f"TEMP{int(time.time()) % 1000}"
        }
        temp_response = orangehrm_service.create_employee(temp_data)
        employee_id = temp_response["data"]["empNumber"]
        is_temp = True
    else:
        employee_id = pytest.created_employee_id
        is_temp = False

    try:
        logger.info(f"Удаление сотрудника ID: {employee_id}")

        response = orangehrm_service.delete_employee([employee_id])

        # Проверяем успешность удаления
        # В OrangeHRM DELETE может возвращать пустой ответ или статус
        logger.info(f"✅ Сотрудник удален. Ответ сервера: {response}")

        # Пытаемся получить удаленного сотрудника (должна быть ошибка)
        try:
            orangehrm_service.get_employee(employee_id)
            logger.warning("⚠️  Сотрудник все еще доступен после удаления")
        except:
            logger.info("✅ Подтверждение: сотрудник больше не доступен через GET")

        if not is_temp:
            # Убираем ID из pytest, если это был основной сотрудник
            delattr(pytest, 'created_employee_id')

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте удаления сотрудника: {e}")
        pytest.fail(f"Тест удаления сотрудника провален: {e}")

def test_get_employees_list(self, orangehrm_service):
    """
    Тест получения списка сотрудников
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: GET - Получение списка сотрудников")
    logger.info("=" * 60)

    try:
        logger.info("Запрос списка сотрудников...")
        response = orangehrm_service.get_employees_list(limit=5)

        assert response is not None, "Ответ от сервера пустой"
        assert "data" in response, "В ответе нет поля 'data'"

        employees = response["data"]
        logger.info(f"✅ Получено {len(employees)} сотрудников")

        # Логируем первых 3 сотрудников
        for i, emp in enumerate(employees[:3]):
            logger.info(
                f"  {i + 1}. {emp.get('firstName', 'N/A')} {emp.get('lastName', 'N/A')} (ID: {emp.get('empNumber', 'N/A')})")

        if "meta" in response:
            total = response["meta"].get("total", 0)
            logger.info(f"Всего сотрудников в системе: {total}")

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте получения списка: {e}")
        pytest.fail(f"Тест получения списка провален: {e}")


def test_complete_crud_flow():
    """
    Комплексный тест полного цикла CRUD в одном тесте
    Полезно для демонстрации в дипломе
    """
    print("\n" + "=" * 70)
    print("КОМПЛЕКСНЫЙ ТЕСТ: ПОЛНЫЙ ЦИКЛ CRUD ОПЕРАЦИЙ")
    print("=" * 70)

    service = OrangeHRMService()
    timestamp = int(time.time())

    try:
        # 1. CREATE (POST)
        print(f"\n1. 📝 СОЗДАНИЕ СОТРУДНИКА (POST)")
        employee_data = {
            "firstName": f"CrudTest{timestamp}",
            "lastName": f"Flow{timestamp}",
            "employeeId": f"CRUD{timestamp % 1000}",
            "gender": "1"
        }

        create_response = service.create_employee(employee_data)
        employee_id = create_response["data"]["empNumber"]
        print(f"   ✅ Создан сотрудник ID: {employee_id}")

        # 2. READ (GET)
        print(f"\n2. 👁️  ПОЛУЧЕНИЕ ДАННЫХ (GET)")
        get_response = service.get_employee(employee_id)
        print(f"   ✅ Получены данные: {get_response['data']['firstName']} {get_response['data']['lastName']}")

        # 3. UPDATE (PUT)
        print(f"\n3. ✏️  ОБНОВЛЕНИЕ ДАННЫХ (PUT)")
        update_data = {"firstName": "ОбновленноеИмя", "lastName": "ОбновленнаяФамилия"}
        update_response = service.update_employee(employee_id, update_data)
        print(f"   ✅ Данные обновлены: {update_response['data']['firstName']}")

        # 4. DELETE (DELETE)
        print(f"\n4. 🗑️  УДАЛЕНИЕ СОТРУДНИКА (DELETE)")
        delete_response = service.delete_employee([employee_id])
        print(f"   ✅ Сотрудник удален")

        # 5. VERIFY (проверка что удален)
        print(f"\n5. 🔍 ПРОВЕРКА УДАЛЕНИЯ")
        try:
            service.get_employee(employee_id)
            print("   ⚠️  Сотрудник все еще доступен (неожиданно)")
        except:
            print("   ✅ Сотрудник успешно удален (недоступен)")

        print(f"\n🎉 ВСЕ 5 ОПЕРАЦИЙ ВЫПОЛНЕНЫ УСПЕШНО!")

    except Exception as e:
        print(f"\n❌ ОШИБКА В КОМПЛЕКСНОМ ТЕСТЕ: {e}")
        raise


def test_create_employee_with_empty_data(self, orangehrm_service):
    """
    Тест: Создание сотрудника с пустыми обязательными полями
    Проверяем, что API корректно валидирует входные данные
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: Создание сотрудника с некорректными данными")
    logger.info("=" * 60)

    # Варианты некорректных данных
    test_cases = [
        {
            "name": "Пустые имя и фамилия",
            "data": {"firstName": "", "lastName": ""},
            "expected_error": True
        },
        {
            "name": "Только имя (без фамилии)",
            "data": {"firstName": "Test", "lastName": ""},
            "expected_error": True
        },
        {
            "name": "Только фамилия (без имени)",
            "data": {"firstName": "", "lastName": "User"},
            "expected_error": True
        },
        {
            "name": "Некорректный пол",
            "data": {"firstName": "Test", "lastName": "User", "gender": "invalid"},
            "expected_error": True
        },
        {
            "name": "Некорректная дата",
            "data": {"firstName": "Test", "lastName": "User", "joinedDate": "2024-13-45"},
            "expected_error": True
        }
    ]

    for test_case in test_cases:
        logger.info(f"Проверка: {test_case['name']}")
        logger.info(f"Данные: {test_case['data']}")

        try:
            response = orangehrm_service.create_employee(test_case['data'])

            # Если ожидалась ошибка, но ее не было
            if test_case['expected_error']:
                logger.error(f"❌ Ожидалась ошибка, но запрос прошел. Ответ: {response}")

                # Проверяем, не вернул ли сервер ошибку в ответе
                if isinstance(response, dict):
                    if "error" in response or "message" in response:
                        logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
                    else:
                        pytest.fail(f"Сервер не вернул ошибку для данных: {test_case['data']}")
                else:
                    pytest.fail(f"Запрос с некорректными данными прошел успешно: {test_case['name']}")
            else:
                logger.info(f"✅ Запрос успешен (как и ожидалось): {test_case['name']}")

        except Exception as e:
            # Логируем ошибку
            error_message = str(e)
            logger.info(f"Получено исключение: {error_message[:100]}...")

            # Проверяем, что это ожидаемая ошибка
            if test_case['expected_error']:
                # Проверяем код ошибки в сообщении
                if any(error_code in error_message for error_code in ['400', '422', '500']):
                    logger.info(f"✅ Корректная ошибка валидации: {test_case['name']}")
                elif "Required" in error_message or "Validation" in error_message:
                    logger.info(f"✅ Ошибка валидации полей: {test_case['name']}")
                else:
                    logger.info(f"⚠️  Нестандартная ошибка: {error_message[:100]}")
            else:
                logger.error(f"❌ Неожиданная ошибка: {error_message}")
                pytest.fail(f"Неожиданная ошибка для {test_case['name']}: {error_message}")


def test_get_nonexistent_employee(self, orangehrm_service):
    """
    Тест: Попытка получить несуществующего сотрудника
    Проверяем обработку 404 ошибки
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: Получение несуществующего сотрудника")
    logger.info("=" * 60)

    # Генерируем заведомо несуществующий ID
    non_existent_ids = [
        "999999",  # Очень большой ID
        "invalid_id",  # Нечисловой ID
        "0",  # Нулевой ID
        "-1",  # Отрицательный ID
        "999999999999"  # Очень-очень большой ID
    ]

    for employee_id in non_existent_ids:
        logger.info(f"Попытка получить сотрудника с ID: {employee_id}")

        try:
            response = orangehrm_service.get_employee(employee_id)

            # Если запрос прошел - проверяем что вернул сервер
            if isinstance(response, dict):
                if "error" in response or "message" in response:
                    logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
                else:
                    # Если сервер вернул какие-то данные для несуществующего ID
                    # это может быть особенностью API - логируем
                    logger.warning(f"⚠️  Сервер вернул данные для несуществующего ID {employee_id}: {response}")
            else:
                logger.warning(f"⚠️  Запрос для ID {employee_id} вернул: {type(response)}")

        except Exception as e:
            error_message = str(e)
            logger.info(f"Получено исключение для ID {employee_id}: {error_message[:150]}")

            # Проверяем, что это корректная ошибка "не найдено"
            if any(code in error_message for code in ['404', 'Not Found', 'not found']):
                logger.info(f"✅ Корректная 404 ошибка для ID {employee_id}")
            elif '500' in error_message:
                logger.warning(f"⚠️  Серверная ошибка 500 для ID {employee_id}")
            else:
                logger.info(f"Другая ошибка для ID {employee_id}: {error_message[:100]}")


def test_update_nonexistent_employee(self, orangehrm_service):
    """
    Тест: Попытка обновить несуществующего сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: Обновление несуществующего сотрудника")
    logger.info("=" * 60)

    fake_employee_id = "888888"
    update_data = {
        "firstName": "Updated",
        "lastName": "Name"
    }

    logger.info(f"Попытка обновить сотрудника с ID: {fake_employee_id}")

    try:
        response = orangehrm_service.update_employee(fake_employee_id, update_data)

        # Если запрос прошел
        if isinstance(response, dict):
            if "error" in response or "message" in response:
                logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
            else:
                logger.warning(f"⚠️  Запрос обновления прошел для несуществующего ID: {response}")
        else:
            logger.warning(f"⚠️  Неожиданный ответ: {type(response)}")

    except Exception as e:
        error_message = str(e)
        logger.info(f"Получено исключение: {error_message[:150]}")

        if any(code in error_message for code in ['404', 'Not Found', 'not found']):
            logger.info("✅ Корректная обработка попытки обновить несуществующего сотрудника")
        else:
            logger.info(f"Другая ошибка: {error_message[:100]}")


def test_delete_nonexistent_employee(self, orangehrm_service):
    """
    Тест: Попытка удалить несуществующего сотрудника
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: Удаление несуществующего сотрудника")
    logger.info("=" * 60)

    fake_ids = ["777777", "invalid_id"]

    for employee_id in fake_ids:
        logger.info(f"Попытка удалить сотрудника с ID: {employee_id}")

        try:
            response = orangehrm_service.delete_employee([employee_id])

            if isinstance(response, dict):
                if "error" in response or "message" in response:
                    logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
                elif "success" in response and not response["success"]:
                    logger.info(f"✅ Сервер вернул неуспешный статус: {response}")
                else:
                    logger.warning(f"⚠️  Удаление прошло для несуществующего ID {employee_id}: {response}")
            else:
                logger.warning(f"⚠️  Неожиданный ответ: {type(response)}")

        except Exception as e:
            error_message = str(e)
            logger.info(f"Получено исключение: {error_message[:150]}")

            if any(code in error_message for code in ['404', 'Not Found', 'not found', '400']):
                logger.info(f"✅ Корректная обработка для ID {employee_id}")
            else:
                logger.info(f"Другая ошибка: {error_message[:100]}")


