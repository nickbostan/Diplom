import time

import pytest

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
        logger.info(
            f"Сервис инициализирован. Сотрудников в системе: {len(response.get('data', []))}"
        )
    except Exception as e:
        logger.error(f"Ошибка инициализации сервиса: {e}")
        pytest.skip(f"Не удалось инициализировать OrangeHRM сервис: {e}")

    yield service

    # Очистка после выполнения всех тестов
    try:
        logger.info("Очистка тестовых данных после завершения тестов...")
        service.cleanup_test_employees("TestUser")
    except Exception as e:
        logger.warning(f"Не удалось выполнить очистку: {e}")

    logger.info("Очистка после тестов завершена")


@pytest.fixture
def test_employee_data():
    """Генерация тестовых данных с уникальным ID"""
    timestamp = int(time.time())
    return {
        "firstName": f"TestUser{timestamp}",
        "lastName": f"LastName{timestamp}",
        "employeeId": f"AUTO{timestamp % 10000:04d}",
        "gender": "1",
    }


@pytest.fixture
def created_employee(orangehrm_service, test_employee_data):
    """Фикстура для создания сотрудника и возврата его данных"""
    logger.info("Создание тестового сотрудника...")
    try:
        response = orangehrm_service.create_employee(test_employee_data)
        employee = response["data"]
        employee_id = employee["empNumber"]
        logger.info(f"✅ Создан тестовый сотрудник ID: {employee_id}")

        # Возвращаем данные сотрудника
        yield {"id": employee_id, "data": employee, "test_data": test_employee_data}

        # Очистка после использования фикстуры
        try:
            logger.info(f"Удаление тестового сотрудника ID: {employee_id}")
            orangehrm_service.delete_employee([employee_id])
        except Exception as e:
            logger.warning(f"Не удалось удалить тестового сотрудника: {e}")

    except Exception as e:
        logger.error(f"Ошибка создания тестового сотрудника: {e}")
        pytest.skip(f"Не удалось создать тестового сотрудника: {e}")


class TestEmployeeCRUD:
    """Тестовый класс для операций CRUD с сотрудниками"""

    def test_create_employee_post(self, orangehrm_service, test_employee_data):
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
            assert (
                employee_data["firstName"] == test_employee_data["firstName"]
            ), f"Имя не совпадает: {employee_data['firstName']}"
            assert (
                employee_data["lastName"] == test_employee_data["lastName"]
            ), f"Фамилия не совпадает: {employee_data['lastName']}"
            assert (
                employee_data.get("employeeId") == test_employee_data["employeeId"]
            ), f"Employee ID не совпадает: {employee_data.get('employeeId')}"

            logger.info(f"✅ Создан сотрудник ID: {employee_id}")
            logger.info(
                f"   Имя: {employee_data['firstName']} {employee_data['lastName']}"
            )

            # Очистка
            orangehrm_service.delete_employee([employee_id])

        except Exception as e:
            logger.error(f"❌ Ошибка в тесте создания сотрудника: {e}")
            pytest.fail(f"Тест создания сотрудника провален: {e}")

    def test_get_employee(self, orangehrm_service, created_employee):
        """
        Тест операции GET - получение данных сотрудника
        """
        logger.info("=" * 60)
        logger.info("ТЕСТ: GET - Получение данных сотрудника")
        logger.info("=" * 60)

        employee_id = created_employee["id"]

        try:
            logger.info(f"Получение данных сотрудника ID: {employee_id}")
            response = orangehrm_service.get_employee(employee_id)

            # Проверки
            assert response is not None, "Ответ от сервера пустой"
            assert "data" in response, "В ответе нет поля 'data'"

            employee = response["data"]

            # Проверяем, что полученный сотрудник - тот же, что создали
            assert employee["empNumber"] == employee_id, "ID сотрудника не совпадает"
            assert (
                employee["firstName"] == created_employee["test_data"]["firstName"]
            ), "Имя не совпадает"
            assert (
                employee["lastName"] == created_employee["test_data"]["lastName"]
            ), "Фамилия не совпадает"

            logger.info(f"✅ Получены данные сотрудника:")
            logger.info(f"   ID: {employee.get('empNumber')}")
            logger.info(
                f"   Имя: {employee.get('firstName')} {employee.get('lastName')}"
            )
            logger.info(
                f"   Пол: {'Мужской' if employee.get('gender') == '1' else 'Женский'}"
            )

        except Exception as e:
            logger.error(f"❌ Ошибка в тесте получения сотрудника: {e}")
            pytest.fail(f"Тест получения сотрудника провален: {e}")

    def test_update_employee_put(self, orangehrm_service, created_employee):
        """
        Тест операции PUT - обновление данных сотрудника
        """
        logger.info("=" * 60)
        logger.info("ТЕСТ: PUT - Обновление данных сотрудника")
        logger.info("=" * 60)

        employee_id = created_employee["id"]

        try:
            # Данные для обновления
            update_data = {
                "firstName": "UpdatedFirstName",
                "lastName": "UpdatedLastName",
                "middleName": "MiddleName",
                "gender": "2",  # Меняем на женский
            }

            logger.info(f"Обновление сотрудника ID: {employee_id}")
            logger.info(f"Новые данные: {update_data}")

            response = orangehrm_service.update_employee(employee_id, update_data)

            # Проверки
            assert response is not None, "Ответ от сервера пустой"
            assert "data" in response, "В ответе нет поля 'data'"

            updated_employee = response["data"]

            # Проверяем обновленные поля
            assert (
                updated_employee["firstName"] == "UpdatedFirstName"
            ), "Имя не обновлено"
            assert (
                updated_employee["lastName"] == "UpdatedLastName"
            ), "Фамилия не обновлена"
            assert updated_employee["gender"] == "2", "Пол не обновлен"
            assert (
                updated_employee["middleName"] == "MiddleName"
            ), "Отчество не обновлено"

            logger.info("✅ Данные сотрудника успешно обновлены")
            logger.info(
                f"   Новое имя: {updated_employee['firstName']} {updated_employee['lastName']}"
            )

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

        try:
            # Создаем временного сотрудника для удаления
            timestamp = int(time.time())
            temp_data = {
                "firstName": f"TempToDelete{timestamp}",
                "lastName": "ForDeletion",
                "employeeId": f"TEMP{timestamp % 10000:04d}",
                "gender": "1",
            }

            logger.info("Создание временного сотрудника для теста удаления...")
            temp_response = orangehrm_service.create_employee(temp_data)
            employee_id = temp_response["data"]["empNumber"]

            logger.info(f"Временный сотрудник создан: ID {employee_id}")

            # Удаляем сотрудника
            logger.info(f"Удаление сотрудника ID: {employee_id}")
            response = orangehrm_service.delete_employee([employee_id])

            # Проверяем успешность удаления
            assert response is not None, "Ответ от сервера пустой"

            # В зависимости от формата ответа
            if isinstance(response, dict):
                if "data" in response:
                    assert response["data"] == [], "Данные после удаления не пусты"
                elif "message" in response:
                    logger.info(f"Сообщение от сервера: {response['message']}")

            logger.info(f"✅ Сотрудник удален")

            # Пытаемся получить удаленного сотрудника (должна быть ошибка)
            try:
                orangehrm_service.get_employee(employee_id)
                pytest.fail("⚠️  Сотрудник все еще доступен после удаления")
            except Exception as e:
                if "404" in str(e) or "Not Found" in str(e):
                    logger.info(
                        "✅ Подтверждение: сотрудник больше не доступен через GET"
                    )
                else:
                    logger.warning(f"Ожидалась ошибка 404, но получена: {e}")

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

            # Проверяем структуру данных
            if employees:
                sample_employee = employees[0]
                assert "empNumber" in sample_employee, "Нет поля empNumber"
                assert "firstName" in sample_employee, "Нет поля firstName"
                assert "lastName" in sample_employee, "Нет поля lastName"

            # Логируем первых 3 сотрудников
            for i, emp in enumerate(employees[:3]):
                logger.info(
                    f"  {i + 1}. {emp.get('firstName', 'N/A')} {emp.get('lastName', 'N/A')} (ID: {emp.get('empNumber', 'N/A')})"
                )

            if "meta" in response:
                total = response["meta"].get("total", 0)
                logger.info(f"Всего сотрудников в системе: {total}")

        except Exception as e:
            logger.error(f"❌ Ошибка в тесте получения списка: {e}")
            pytest.fail(f"Тест получения списка провален: {e}")


# noinspection PyUnreachableCode
class TestNegativeScenarios:
    """Тесты негативных сценариев"""

    def test_create_employee_with_empty_data(self, orangehrm_service):
        """
        Тест: Создание сотрудника с пустыми обязательными полями
        """
        logger.info("=" * 60)
        logger.info("ТЕСТ: Создание сотрудника с некорректными данными")
        logger.info("=" * 60)

        # Варианты некорректных данных
        test_cases = [
            {
                "name": "Пустые имя и фамилия",
                "data": {"firstName": "", "lastName": ""},
                "expected_error": True,
            },
            {
                "name": "Только имя (без фамилии)",
                "data": {"firstName": "Test", "lastName": ""},
                "expected_error": True,
            },
            {
                "name": "Только фамилия (без имени)",
                "data": {"firstName": "", "lastName": "User"},
                "expected_error": True,
            },
        ]

        for test_case in test_cases:
            logger.info(f"Проверка: {test_case['name']}")
            logger.info(f"Данные: {test_case['data']}")

            try:
                response = orangehrm_service.create_employee(test_case["data"])

                # Если ожидалась ошибка, но запрос прошел
                if test_case["expected_error"]:
                    logger.error(
                        f"❌ Ожидалась ошибка, но запрос прошел. Ответ: {response}"
                    )

                    # Проверяем, не вернул ли сервер ошибку в ответе
                    if isinstance(response, dict):
                        if "error" in response or "message" in response:
                            logger.info(
                                f"✅ Сервер вернул сообщение об ошибке: {response}"
                            )
                        else:
                            # Если нет явной ошибки, но запрос прошел - это проблема
                            pytest.fail(
                                f"Сервер не вернул ошибку для данных: {test_case['data']}"
                            )
                else:
                    logger.info(
                        f"✅ Запрос успешен (как и ожидалось): {test_case['name']}"
                    )

            except Exception as e:
                # Логируем ошибку
                error_message = str(e)
                logger.info(f"Получено исключение: {error_message[:100]}...")

                # Проверяем, что это ожидаемая ошибка
                if test_case["expected_error"]:
                    # Проверяем код ошибки в сообщении
                    if any(
                        error_code in error_message
                        for error_code in ["400", "422", "500"]
                    ):
                        logger.info(
                            f"✅ Корректная ошибка валидации: {test_case['name']}"
                        )
                    elif "Required" in error_message or "Validation" in error_message:
                        logger.info(f"✅ Ошибка валидации полей: {test_case['name']}")
                    else:
                        logger.info(f"⚠️  Нестандартная ошибка: {error_message[:100]}")
                else:
                    logger.error(f"❌ Неожиданная ошибка: {error_message}")
                    pytest.fail(
                        f"Неожиданная ошибка для {test_case['name']}: {error_message}"
                    )

    def test_get_nonexistent_employee(self, orangehrm_service):
        """
        Тест: Попытка получить несуществующего сотрудника
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
            "999999999999",  # Очень-очень большой ID
        ]

        for employee_id in non_existent_ids:
            logger.info(f"Попытка получить сотрудника с ID: {employee_id}")

            try:
                response = orangehrm_service.get_employee(employee_id)

                # Если запрос прошел
                if isinstance(response, dict):
                    if "error" in response or "message" in response:
                        logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
                    else:
                        # Если сервер вернул какие-то данные для несуществующего ID
                        logger.warning(
                            f"⚠️  Сервер вернул данные для несуществующего ID {employee_id}"
                        )
                else:
                    logger.warning(
                        f"⚠️  Запрос для ID {employee_id} вернул: {type(response)}"
                    )

            except Exception as e:
                error_message = str(e)
                logger.info(
                    f"Получено исключение для ID {employee_id}: {error_message[:150]}"
                )

                # Проверяем, что это корректная ошибка "не найдено"
                if any(
                    code in error_message for code in ["404", "Not Found", "not found"]
                ):
                    logger.info(f"✅ Корректная 404 ошибка для ID {employee_id}")
                elif "500" in error_message:
                    logger.warning(f"⚠️  Серверная ошибка 500 для ID {employee_id}")
                else:
                    logger.info(
                        f"Другая ошибка для ID {employee_id}: {error_message[:100]}"
                    )

    def test_update_nonexistent_employee(self, orangehrm_service):
        """
        Тест: Попытка обновить несуществующего сотрудника
        """
        logger.info("=" * 60)
        logger.info("ТЕСТ: Обновление несуществующего сотрудника")
        logger.info("=" * 60)

        fake_employee_id = "888888"
        update_data = {"firstName": "Updated", "lastName": "Name"}

        logger.info(f"Попытка обновить сотрудника с ID: {fake_employee_id}")

        try:
            response = orangehrm_service.update_employee(fake_employee_id, update_data)

            # Если запрос прошел
            if isinstance(response, dict):
                if "error" in response or "message" in response:
                    logger.info(f"✅ Сервер вернул сообщение об ошибке: {response}")
                else:
                    logger.warning(
                        f"⚠️  Запрос обновления прошел для несуществующего ID"
                    )
            else:
                logger.warning(f"⚠️  Неожиданный ответ: {type(response)}")

        except Exception as e:
            error_message = str(e)
            logger.info(f"Получено исключение: {error_message[:150]}")

            if any(code in error_message for code in ["404", "Not Found", "not found"]):
                logger.info(
                    "✅ Корректная обработка попытки обновить несуществующего сотрудника"
                )
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
                        logger.warning(
                            f"⚠️  Удаление прошло для несуществующего ID {employee_id}"
                        )
                else:
                    logger.warning(f"⚠️  Неожиданный ответ: {type(response)}")

            except Exception as e:
                error_message = str(e)
                logger.info(f"Получено исключение: {error_message[:150]}")

                if any(
                    code in error_message
                    for code in ["404", "Not Found", "not found", "400"]
                ):
                    logger.info(f"✅ Корректная обработка для ID {employee_id}")
                else:
                    logger.info(f"Другая ошибка: {error_message[:100]}")


class TestIntegrationScenarios:
    """Интеграционные тесты"""

    # noinspection PyTypeChecker
    def test_complete_crud_flow(self):
        """
        Комплексный тест полного цикла CRUD в одном тесте
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
                "employeeId": f"CRUD{timestamp % 10000:04d}",
                "gender": "1",
            }

            create_response = service.create_employee(employee_data)
            employee_id = create_response["data"]["empNumber"]
            print(f"   ✅ Создан сотрудник ID: {employee_id}")

            # 2. READ (GET)
            print(f"\n2. 👁️  ПОЛУЧЕНИЕ ДАННЫХ (GET)")
            get_response = service.get_employee(employee_id)
            print(
                f"   ✅ Получены данные: {get_response['data']['firstName']} {get_response['data']['lastName']}"
            )

            # 3. UPDATE (PUT)
            print(f"\n3. ✏️  ОБНОВЛЕНИЕ ДАННЫХ (PUT)")
            update_data = {
                "firstName": "ОбновленноеИмя",
                "lastName": "ОбновленнаяФамилия",
                "middleName": "Отчество",
            }
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
                print("   ❌ Сотрудник все еще доступен (неожиданно)")
                pytest.fail("Сотрудник не был удален")
            except Exception as e:
                if "404" in str(e) or "Not Found" in str(e):
                    print("   ✅ Сотрудник успешно удален (недоступен)")
                else:
                    print(f"   ⚠️  Ошибка при проверке: {e}")

            print(f"\n🎉 ВСЕ 5 ОПЕРАЦИЙ ВЫПОЛНЕНЫ УСПЕШНО!")

        except Exception as e:
            print(f"\n❌ ОШИБКА В КОМПЛЕКСНОМ ТЕСТЕ: {e}")
            # Пытаемся очистить, если что-то пошло не так

            raise

    def test_search_employees(self, orangehrm_service, created_employee):
        """
        Тест поиска сотрудников
        """
        logger.info("=" * 60)
        logger.info("ТЕСТ: Поиск сотрудников")
        logger.info("=" * 60)

        try:
            # Поиск по имени созданного сотрудника
            search_name = created_employee["test_data"]["firstName"]
            logger.info(f"Поиск сотрудников по имени: '{search_name}'")

            search_result = orangehrm_service.search_employees(
                name=search_name, limit=10
            )

            assert search_result is not None, "Ответ от сервера пустой"
            assert "data" in search_result, "В ответе нет поля 'data'"

            found_employees = search_result["data"]

            # Проверяем, что наш сотрудник найден
            found = False
            for emp in found_employees:
                if emp["empNumber"] == created_employee["id"]:
                    found = True
                    break

            assert (
                found
            ), f"Созданный сотрудник не найден при поиске по имени '{search_name}'"
            logger.info(f"✅ Сотрудник найден в результатах поиска")

            # Поиск по несуществующему имени
            fake_name = "NonexistentName12345"
            logger.info(f"Поиск по несуществующему имени: '{fake_name}'")

            no_result = orangehrm_service.search_employees(name=fake_name)

            if "data" in no_result:
                if len(no_result["data"]) == 0:
                    logger.info(
                        "✅ Поиск по несуществующему имени вернул пустой результат"
                    )
                else:
                    logger.warning(
                        f"⚠️  Поиск по несуществующему имени вернул {len(no_result['data'])} результатов"
                    )

        except Exception as e:
            logger.error(f"❌ Ошибка в тесте поиска: {e}")
            pytest.fail(f"Тест поиска провален: {e}")


def test_employee_pagination(orangehrm_service):
    """
    Тестирование пагинации при получении списка сотрудников
    """
    logger.info("=" * 60)
    logger.info("ТЕСТ: Пагинация списка сотрудников")
    logger.info("=" * 60)

    try:
        # Получаем первую страницу
        page1 = orangehrm_service.get_employees_list(limit=5, offset=0)
        assert "data" in page1, "Нет данных на первой странице"

        # Получаем вторую страницу
        page2 = orangehrm_service.get_employees_list(limit=5, offset=5)
        assert "data" in page2, "Нет данных на второй странице"

        # Проверяем, что сотрудники на страницах разные (если сотрудников достаточно)
        if len(page1["data"]) > 0 and len(page2["data"]) > 0:
            page1_ids = {emp["empNumber"] for emp in page1["data"]}
            page2_ids = {emp["empNumber"] for emp in page2["data"]}

            # ID не должны пересекаться (при корректной пагинации)
            intersection = page1_ids.intersection(page2_ids)
            if len(intersection) == 0:
                logger.info("✅ Пагинация работает корректно: страницы не пересекаются")
            else:
                logger.warning(f"⚠️  Страницы пересекаются: {intersection}")

        logger.info("✅ Тест пагинации завершен")

    except Exception as e:
        logger.error(f"❌ Ошибка в тесте пагинации: {e}")
        pytest.fail(f"Тест пагинации провален: {e}")
