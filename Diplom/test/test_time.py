import time

import allure
import pytest

from conftest import logger
from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.time_page import TimePage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def time_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return TimePage(driver)


@allure.epic("Страница time")
@allure.title("Отображение страницы time")
@pytest.mark.smoke
def test_time_page(time_page, driver):
    logger.info("=== Начало test_time_page ===")

    with allure.step("Открыть вкладку Time"):
        logger.info("Кликаем на вкладку Time")
        time_page.MENU_TIME.click()

    with allure.step("Проверить открытие страницы Time"):
        logger.info("Проверяем открытие страницы Time")
        time_page.check_that_page_opened()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="time_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert time_page.driver.current_url == URLS.TIME
        logger.info("✓ Страница Time открыта корректно")

    logger.info("=== Конец test_time_page ===")


@allure.epic("Страница time")
@allure.feature("Поиск")
@allure.title("Проверка функции поиска")
def test_search_time(time_page, driver):
    logger.info("=== Начало test_search_time ===")

    with allure.step("Открыть  Time"):
        logger.info("Открываем  Time")
        time_page.MENU_TIME.click()

    with allure.step("Получить имя сотрудника для поиска"):
        employee = time_page.get_name_text()
        logger.info(f"Получено имя сотрудника для поиска: {employee}")

    with allure.step("Ввести имя сотрудника в поле поиска"):
        logger.info(f"Вводим имя сотрудника: {employee}")
        time_page.EMPLOYEE_NAME.fill(employee)

    with allure.step("Дождаться результатов поиска"):
        logger.info("Ждем появления результатов поиска")
        time.sleep(3)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_results",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Выбрать первого найденного сотрудника"):
        logger.info("Кликаем на первого найденного сотрудника")
        time_page.FIRST_FOUND_EMPLOYEE.click()

    with allure.step("Нажать кнопку View для просмотра"):
        logger.info("Нажимаем кнопку View")
        time_page.VIEW_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="view_button_clicked",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить переход на страницу timesheet"):
        current_url = time_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        assert (
            "viewTimesheet/employeeId" in current_url
        ), f"URL не содержит 'viewTimesheet/employeeId'. Текущий URL: {current_url}"

        logger.info("✓ Переход на страницу timesheet выполнен успешно")

    logger.info("=== Конец test_search_time ===")


@allure.epic("Страница time")
@allure.title("Проверка кнопки в таблице")
def test_view_button_table(time_page, driver):
    logger.info("=== Начало test_view_button_table ===")

    with allure.step("Открыть  Time"):
        logger.info("Открываем  Time")
        time_page.MENU_TIME.click()

    with allure.step("Нажать кнопку View в первой строке таблицы"):
        logger.info("Кликаем на первую кнопку View в таблице")
        time_page.VIEW_FIRST_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="timesheet_from_table",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить переход на страницу timesheet"):
        current_url = time_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        assert (
            "viewTimesheet/employeeId" in current_url
        ), f"URL не содержит 'viewTimesheet/employeeId'. Текущий URL: {current_url}"

        logger.info("✓ Переход на страницу таймшита из таблицы выполнен успешно")

    logger.info("=== Конец test_view_button_table ===")


@allure.epic("Страница time")
@allure.feature("Валидация ввода")
@allure.title("Проверка ошибок ввода")
def test_error(time_page, driver):
    logger.info("=== Начало test_error ===")

    with allure.step("Открыть  Time"):
        logger.info("Открываем Time")
        time_page.MENU_TIME.click()

    with allure.step("Проверка 1: Пустое поле"):
        logger.info("Пытаемся нажать View без ввода имени")
        time_page.VIEW_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="empty_field_error",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем видимость ошибки")
        time_page.ERROR.should_be_visible()

        logger.info("Проверяем текст ошибки 'Required'")
        assert time_page.ERROR.should_contain_text(
            "Required"
        ), "Не отображается ошибка 'Required' для пустого поля"

        logger.info("✓ Ошибка  отображается корректно")

    with allure.step("Проверка 2: Невалидное имя"):
        logger.info("Вводим невалидное имя: 'dddd'")
        time_page.EMPLOYEE_NAME.fill("dddd")

        logger.info("Нажимаем кнопку View")
        time_page.VIEW_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="invalid_name_error",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Проверяем текст ошибки 'Invalid'")
        assert time_page.ERROR.should_contain_text(
            "Invalid"
        ), "Не отображается ошибка 'Invalid' для невалидного имени"

        logger.info("✓ Ошибка  отображается корректно")

    logger.info("=== Конец test_error ===")
