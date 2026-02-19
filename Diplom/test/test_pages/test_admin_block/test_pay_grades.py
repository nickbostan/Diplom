import time

import allure
import pytest
from faker import Faker

from conftest import logger
from Diplom.page_obj.admin_block.add_pay_grade import AddPayGradePage
from Diplom.page_obj.admin_block.edit_pay_grades import EditPayGradePage
from Diplom.page_obj.admin_block.pay_grades import PayGradesPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture(scope="function")
def pay_grade(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PayGradesPage(driver)


@pytest.fixture()
def add_pay_grade(driver):
    return AddPayGradePage(driver)


@pytest.fixture()
def edit_pay_grade(driver):
    return EditPayGradePage(driver)


@allure.epic("Страница уровня зарплаты")
@allure.title("Проверка открытия страницы")
@pytest.mark.smoke
def test_pay_grade_page(pay_grade, driver):
    logger.info("=== Начало test_pay_grade_page ===")

    with allure.step("Открыть меню Admin"):
        logger.info("Кликаем на меню Admin")
        pay_grade.MENU_ADMIN.click()

    with allure.step("Раскрыть выпадающий список Job"):
        logger.info("Кликаем на выпадающий список Job")
        pay_grade.JOB_DROPDOWN.click()

    with allure.step("Выбрать пункт Pay Grades"):
        logger.info("Выбираем Pay Grades")
        pay_grade.PAY_GRADES.click()

    with allure.step("Проверить что страница открылась"):
        logger.info("Проверяем открытие страницы Pay Grades")
        pay_grade.check_that_page_opened()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="pay_grades_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert pay_grade.driver.current_url == URLS.PAY_GRADES
        logger.info("✓ Страница Pay Grades успешно открыта")

    logger.info("=== Конец test_pay_grade_page ===")


@pytest.mark.smoke
@allure.epic("Страница уровня зарплаты")
@allure.feature("Добавление уровня зарплаты")
@allure.title("Проверка простого добавления  и редактирования")
def test_add_pay_grade(add_pay_grade, driver, pay_grade, edit_pay_grade, fake):
    logger.info("=== Начало test_add_and_edit_pay_grade ===")

    with allure.step("Перейти на страницу Pay Grades"):
        logger.info("Открываем страницу Pay Grades")
        pay_grade.MENU_ADMIN.click()
        pay_grade.JOB_DROPDOWN.click()
        pay_grade.PAY_GRADES.click()

    with allure.step("Добавить новый уровень зарплаты"):
        logger.info("Кликаем на кнопку Add")
        pay_grade.ADD_BUTTON.click()
        add_pay_grade.check_that_page_opened()

        assert add_pay_grade.driver.current_url == URLS.ADD_PAY_GRADES
        logger.info("✓ Страница Add Pay Grades успешно открыта")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="add_pay_grade_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Заполнить данные Pay Grade"):
        grade_name = fake.name()
        logger.info(f"Заполняем имя Pay Grade: {grade_name}")
        add_pay_grade.NAME.fill(grade_name)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filled_pay_grade",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Сохранить Pay Grade"):
        logger.info("Сохраняем Pay Grade")
        add_pay_grade.SAVE_BUTTON.click()
        logger.info("✓ Pay Grade успешно сохранен")

    with allure.step("Редактировать Pay Grade"):
        logger.info("Редактируем Pay Grade")
        edit_pay_grade.check_that_page_opened()

        new_name = fake.name()
        logger.info(f"Изменяем имя на: {new_name}")
        edit_pay_grade.NAME.fill(new_name)
        edit_pay_grade.SAVE_BUTTON.click()
        logger.info("✓ Pay Grade успешно обновлен")

    with allure.step("Проверить отмену добавления валюты"):
        logger.info("Нажимаем на кнопаку добавления валюты")
        edit_pay_grade.ADD_CURRENCY.click()
        time.sleep(3)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="add_currency_form",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Отменяем добавление валюты")
        edit_pay_grade.CANCEL_CURRENCY.click()
        assert edit_pay_grade.SAVE_CURRENCY.should_be_not_visible()
        logger.info("✓ Добавление валюты отменено")

    with allure.step("Вернуться к списку Pay Grades"):
        logger.info("Возвращаемся к списку Pay Grades")
        edit_pay_grade.CANCEL_BUTTON.click()
        assert pay_grade.driver.current_url == URLS.PAY_GRADES
        logger.info("✓ Успешный возврат к списку")

    logger.info("=== Конец test_add_and_edit_pay_grade ===")


@allure.epic("Страница уровня зарплаты")
@allure.feature("Редактирование уровня зарплаты")
@allure.title("Проверка простого добавления  и редактирования валюты")
def test_add_currency(driver, pay_grade, edit_pay_grade):
    logger.info("=== Начало test_add_currency ===")

    with allure.step("Перейти к редактированию Pay Grade"):
        logger.info("Открываем Pay Grade для редактирования")
        pay_grade.MENU_ADMIN.click()
        pay_grade.JOB_DROPDOWN.click()
        pay_grade.PAY_GRADES.click()
        pay_grade.REDACT_SECOND.click()

        edit_pay_grade.check_that_page_opened()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="edit_pay_grade_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Добавить первую валюту (BHD)"):
        logger.info("Добавляем валюту BHD")
        edit_pay_grade.ADD_CURRENCY.click()
        time.sleep(4)

        edit_pay_grade.CURRENCY.click()
        edit_pay_grade.CURRENCY_BHD.click()

        logger.info("Заполняем данные зарплаты")
        edit_pay_grade.MINIMUM_SALARY.fill("100")
        edit_pay_grade.MAXIMUM_SALARY.fill("1000")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filled_currency_form",
            attachment_type=allure.attachment_type.PNG,
        )

        edit_pay_grade.SAVE_CURRENCY.click()
        time.sleep(2)
        assert edit_pay_grade.check_message("Saved")
        logger.info("✓ Валюта BHD успешно добавлена")

    with allure.step("Добавить вторую валюту"):
        logger.info("Добавляем дополнительную валюту")
        time.sleep(3)
        edit_pay_grade.ADD_CURRENCY.click()
        time.sleep(2)

        edit_pay_grade.CURRENCY.click()
        edit_pay_grade.A_CURRENCY.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="second_currency_selected",
            attachment_type=allure.attachment_type.PNG,
        )

        edit_pay_grade.SAVE_CURRENCY.click()
        assert edit_pay_grade.check_message("Saved")
        logger.info("✓ Вторая валюта успешно добавлена")

    logger.info("=== Конец test_add_currency ===")


@allure.epic("Страница уровня зарплаты")
@allure.feature("Удаление уровня зарплаты")
@allure.title("Проверка удаления уровня зарплаты")
def test_delete_grade(driver, pay_grade):
    logger.info("=== Начало test_delete_grade ===")

    with allure.step("Перейти на страницу Pay Grades"):
        logger.info("Открываем страницу Pay Grades")
        pay_grade.MENU_ADMIN.click()
        pay_grade.JOB_DROPDOWN.click()
        pay_grade.PAY_GRADES.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="pay_grades_before_delete",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Попытка удаления с отменой"):
        logger.info("Пытаемся удалить второй Pay Grade")
        pay_grade.DELETE_SECOND.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="delete_confirmation",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Отменяем удаление")
        pay_grade.NO_CANCEL.click()
        logger.info("✓ Удаление отменено")

    with allure.step("Удаление Pay Grade с подтверждением"):
        logger.info("Удаляем второй Pay Grade")
        pay_grade.DELETE_SECOND.click()
        pay_grade.YES_DELETE.click()

        assert pay_grade.check_message("Deleted")
        logger.info("✓ Pay Grade успешно удален")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="delete_success",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_delete_grade ===")


@allure.epic("Страница уровня зарплаты")
@allure.feature("Редактирование зарплаты")
@allure.title("Проверка ошибок ввода зарплаты")
def test_errors_salary(driver, pay_grade, edit_pay_grade):
    logger.info("=== Начало test_errors_salary ===")

    with allure.step("Перейти на страницу редактирования Pay Grade"):
        logger.info("Открываем страницу Pay Grades")
        pay_grade.MENU_ADMIN.click()
        pay_grade.JOB_DROPDOWN.click()
        pay_grade.PAY_GRADES.click()

        logger.info("Открываем первый Pay Grade для редактирования")
        pay_grade.REDACT_FIRST.click()
        edit_pay_grade.check_that_page_opened()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="edit_pay_grade_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Открыть форму добавления валюты"):
        logger.info("Открываем форму добавления валюты")
        edit_pay_grade.ADD_CURRENCY.click()
        time.sleep(2)

        logger.info("Выбираем валюту")
        edit_pay_grade.CURRENCY.click()
        edit_pay_grade.A_CURRENCY.click()

    with allure.step("Проверка 1: Maximum меньше Minimum"):
        logger.info("Заполняем Minimum=100, Maximum=10")
        edit_pay_grade.MINIMUM_SALARY.fill("100")
        edit_pay_grade.MAXIMUM_SALARY.fill("10")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="max_less_than_min",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем ошибку 'Should be higher than Minimum'")
        assert edit_pay_grade.ERROR_SALARY.should_contain_text(
            "Should be higher than Minimum"
        ), "Не отображается ошибка когда Maximum меньше Minimum"
        logger.info("✓ Ошибка корректно отображается")

    with allure.step("Установить корректное значение Maximum=1000"):
        logger.info("Меняем Maximum на 1000")
        edit_pay_grade.MAXIMUM_SALARY.fill("1000")

        logger.info("Проверяем что ошибка исчезла")
        assert (
            edit_pay_grade.ERROR_SALARY.should_be_not_visible()
        ), "Ошибка не исчезла после исправления"
        logger.info("✓ Ошибка исчезла после исправления")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_fixed_max_increased",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка 2: Minimum больше Maximum"):
        logger.info("Заполняем Minimum=10000 (больше Maximum=1000)")
        edit_pay_grade.MINIMUM_SALARY.fill("10000")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="min_greater_than_max",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем ошибку 'Should be lower than Maximum'")
        assert edit_pay_grade.ERROR_SALARY.should_contain_text(
            "Should be lower than Maximum"
        ), "Не отображается ошибка когда Minimum больше Maximum"
        logger.info("✓ Ошибка корректно отображается")

    with allure.step("Установить корректное значение Minimum=100"):
        logger.info("Исправляем Minimum на 100")
        edit_pay_grade.MINIMUM_SALARY.fill("100")

        logger.info("Проверяем что ошибка исчезла")
        assert (
            edit_pay_grade.ERROR_SALARY.should_be_not_visible()
        ), "Ошибка не исчезла после исправления"
        logger.info("✓ Ошибка исчезла после исправления")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_fixed_min_decreased",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка 3: Недопустимые символы в Maximum"):
        logger.info("Заполняем Maximum недопустимыми символами 'dddd'")
        edit_pay_grade.MAXIMUM_SALARY.fill("dddd")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="invalid_characters_in_max",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем ошибку 'Should be a valid number'")
        assert edit_pay_grade.ERROR_SALARY.should_contain_text(
            "Should be a valid number"
        ), "Не отображается ошибка при вводе недопустимых символов"
        logger.info("✓ Ошибка корректно отображается")

    with allure.step("Установить корректное значение Maximum=999999"):
        logger.info("Исправляем Maximum на 999999")
        edit_pay_grade.MAXIMUM_SALARY.fill("999999")

        logger.info("Проверяем что ошибка исчезла")
        assert (
            edit_pay_grade.ERROR_SALARY.should_be_not_visible()
        ), "Ошибка не исчезла после исправления"
        logger.info("✓ Ошибка исчезла после исправления")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_fixed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка 4: Недопустимые символы в Minimum"):
        logger.info("Заполняем Minimum недопустимыми символами 'dddd'")
        edit_pay_grade.MINIMUM_SALARY.fill("dddd")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="invalid_characters_in_max",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем ошибку 'Should be a valid number'")
        assert edit_pay_grade.ERROR_SALARY.should_contain_text(
            "Should be a valid number"
        ), "Не отображается ошибка при вводе недопустимых символов"
        logger.info("✓ Ошибка корректно отображается")

    logger.info("=== Конец test_errors_salary ===")


@allure.epic("Страница уровня зарплаты")
@allure.feature("Добавление зарплаты")
@allure.title("Полный workflow добавления Pay Grade с валютой")
def test_workflow_add_pay_grade(driver, pay_grade, edit_pay_grade, add_pay_grade, fake):
    logger.info("=== Начало test_workflow_add_pay_grade ===")

    with allure.step("Создать уникальное имя для Pay Grade"):
        grade = fake.name()
        logger.info(f"Сгенерировано имя Pay Grade: {grade}")

    with allure.step("Создать новый Pay Grade"):
        pay_grade.MENU_ADMIN.click()
        pay_grade.JOB_DROPDOWN.click()
        pay_grade.PAY_GRADES.click()
        pay_grade.ADD_BUTTON.click()

        add_pay_grade.NAME.fill(grade)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="new_pay_grade",
            attachment_type=allure.attachment_type.PNG,
        )

        add_pay_grade.SAVE_BUTTON.click()
        logger.info("✓ Новый Pay Grade создан")

    with allure.step("Добавить валюту Bahraini Dinar"):
        edit_pay_grade.ADD_CURRENCY.click()
        time.sleep(2)
        edit_pay_grade.CURRENCY.click()
        edit_pay_grade.CURRENCY_BHD.click()

        edit_pay_grade.MINIMUM_SALARY.fill("100")
        edit_pay_grade.MAXIMUM_SALARY.fill("1000")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="currency_bhd_filled",
            attachment_type=allure.attachment_type.PNG,
        )

        edit_pay_grade.SAVE_CURRENCY.click()
        assert edit_pay_grade.check_message("Saved")
        logger.info("✓ Валюта Bahraini Dinar добавлена")

    with allure.step("Сохранить изменения Pay Grade"):
        edit_pay_grade.SAVE_BUTTON.click()
        assert edit_pay_grade.check_message("Updated")
        logger.info("✓ Изменения Pay Grade сохранены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="pay_grade_updated",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Вернуться к списку и проверить отображение"):
        time.sleep(4)  # Ждем обновления
        edit_pay_grade.CANCEL_BUTTON.click()
        time.sleep(2)

        # Проверяем что созданный Pay Grade отображается
        assert grade in driver.page_source, f"Pay Grade '{grade}' не найден на странице"
        assert (
            "Bahraini Dinar" in driver.page_source
        ), "Валюта 'Bahraini Dinar' не найдена на странице"
        logger.info("✓ Созданный Pay Grade и валюта отображаются корректно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="final_pay_grades_list",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_workflow_add_pay_grade ===")
