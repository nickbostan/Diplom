import allure
import pytest

from conftest import logger
from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.performance_page import PerformancePage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def performance_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PerformancePage(driver)


@allure.epic("Страница Performance")
@allure.title("Открытие страницы Performance")
@pytest.mark.smoke
def test_performance_page(performance_page, driver):
    logger.info("=== Начало test_performance_page ===")
    with allure.step("Клик по меню Performance"):
        performance_page.MENU_PERFORMANCE.click()
        logger.info("Performance нажато")

    with allure.step("Проверка открытия страницы"):
        performance_page.check_that_page_opened()
        current_url = performance_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="performance_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.PERFORMANCE
        logger.info("✓ Страница Performance открыта")

    logger.info("=== Конец test_performance_page ===")


@allure.epic("Страница Performance")
@allure.title("Тестирование панели фильтров")
def test_panel_filter(performance_page, driver):
    logger.info("=== Начало test_panel_filter ===")
    with allure.step("Открыть страницу Performance"):
        performance_page.MENU_PERFORMANCE.click()
        logger.info("Performance нажато")

    with allure.step("Свернуть панель фильтров"):
        performance_page.PERFORMANCE_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров свернута")

    with allure.step("Проверить, что поле Employee Name скрыто"):
        assert performance_page.EMPLOYEE_NAME.should_be_not_visible()
        logger.info("✓ Поле Employee Name не видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_collapsed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Развернуть панель фильтров"):
        performance_page.PERFORMANCE_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров развернута")

    with allure.step("Проверить, что поле Employee Name стало видимым"):
        performance_page.EMPLOYEE_NAME.should_be_visible()
        logger.info("✓ Поле Employee Name видно")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_expanded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_panel_filter ===")


@allure.epic("Страница Performance")
@allure.title("Поиск по полям и сброс фильтров")
def test_search_fields_and_reset(performance_page, driver):
    logger.info("=== Начало test_search_fields_and_reset ===")
    with allure.step("Открыть страницу Performance"):
        performance_page.MENU_PERFORMANCE.click()
        logger.info("Performance нажато")

    with allure.step("Заполнить поля поиска через input_search()"):
        performance_page.input_search()
        logger.info("Поля поиска заполнены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_fields_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажать кнопку Search"):
        performance_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

    with allure.step("Проверить сообщение 'No Records'"):
        assert performance_page.check_message("No Records")
        logger.info("✓ Сообщение 'No Records' появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="no_records_message",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить значения полей после поиска"):
        from_date = performance_page.FROM_DATE.get_attribute("value")
        status = performance_page.STATUS_DROPDOWN.get_text()
        logger.info(f"From Date: {from_date}, Status: {status}")

        assert from_date == "2016-02-05"
        assert status == "Activated"
        logger.info("✓ Значения полей соответствуют ожидаемым")

    with allure.step("Нажать кнопку Reset"):
        performance_page.RESET_BUTTON.click()
        logger.info("Кнопка Reset нажата")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_reset",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить значения полей после сброса"):
        new_from_date = performance_page.FROM_DATE.get_attribute("value")
        new_status = performance_page.STATUS_DROPDOWN.get_text()
        logger.info(f"После сброса: From Date: {new_from_date}, Status: {new_status}")

        assert new_status == "-- Select --"
        assert (
            new_from_date == "2026-01-01"
        )  # После reset ставиться дата на начало текущего года
        logger.info("✓ Поля сброшены корректно (дата по умолчанию установлена)")

    logger.info("=== Конец test_search_fields_and_reset ===")
