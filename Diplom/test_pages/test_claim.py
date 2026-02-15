import pytest
import allure

from conftest import logger
from Diplom.page_obj.claim_page import ClaimPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def claim_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return ClaimPage(driver)


@allure.epic("Страница Claims")
@allure.title("Открытие страницы Claims")
@pytest.mark.smoke
def test_claim_page(claim_page, driver):
    logger.info("=== Начало test_claim_page ===")
    with allure.step("Клик по меню Claims"):
        claim_page.MENU_CLAIM.click()
        logger.info("Claims нажато")

    with allure.step("Проверка открытия страницы"):
        claim_page.check_that_page_opened()
        current_url = claim_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="claim_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.CLAIM
        logger.info("✓ Страница открыта")

    logger.info("=== Конец test_claim_page ===")


@allure.epic("Страница Claims")
@allure.title("Проверка кнопки Assign Claim")
def test_assign_button(claim_page, driver):
    logger.info("=== Начало test_assign_button ===")
    with allure.step("Переход в раздел Claims"):
        claim_page.MENU_CLAIM.click()
        logger.info("Claims нажато")

    with allure.step("Клик по кнопке Assign Claim"):
        claim_page.ASSIGN_CLAIM_BUTTON.click()
        logger.info("Кнопка Assign Claim нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_assign_click",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка URL и заголовка"):
        current_url = claim_page.driver.current_url
        logger.info(f"URL после клика: {current_url}")
        assert "assignClaim" in current_url
        logger.info("✓ URL содержит 'assignClaim'")

        assert claim_page.PAGE_TITLE_ASSIGN.should_contain_text("Create Claim Request")
        logger.info("✓ Заголовок страницы верный")

    logger.info("=== Конец test_assign_button ===")


@allure.epic("Страница Claims")
@allure.title("Проверка сворачивания/разворачивания панели фильтров")
def test_panel_filter(claim_page, driver):
    logger.info("=== Начало test_panel_filter ===")
    with allure.step("Открыть страницу Claims"):
        claim_page.MENU_CLAIM.click()
        logger.info("Claims нажато")

    with allure.step("Свернуть панель фильтров"):
        claim_page.CLAIM_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров свернута")

    with allure.step("Проверить, что поле Employee Name скрыто"):
        assert claim_page.EMPLOYEE_NAME.should_be_not_visible()
        logger.info("✓ Поле Employee Name не видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_collapsed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Развернуть панель фильтров"):
        claim_page.CLAIM_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров развернута")

    with allure.step("Проверить, что поле Employee Name стало видимым"):
        claim_page.EMPLOYEE_NAME.should_be_visible()
        logger.info("✓ Поле Employee Name видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_expanded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_panel_filter ===")


@allure.epic("Страница Claims")
@allure.title("Поиск по полям и сброс фильтров")
def test_search_fields_and_reset(claim_page, driver):
    logger.info("=== Начало test_search_fields_and_reset ===")
    with allure.step("Открыть страницу Claims"):
        claim_page.MENU_CLAIM.click()
        logger.info("Claims нажато")

    with allure.step("Заполнить поля поиска через метод input_search()"):
        claim_page.input_search()
        logger.info("Поля поиска заполнены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_fields_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить значения полей после ввода"):
        ids = claim_page.REFERENCE_ID.get_attribute('value')
        status = claim_page.STATUS_DROPDOWN.get_text()
        to_date = claim_page.TO_DATE.get_attribute('value')
        logger.info(f"Reference ID: {ids}, Status: {status}, To Date: {to_date}")

        assert ids == "1234"
        assert status == "Initiated"
        assert to_date == "2025-25-08"
        logger.info("✓ Значения полей соответствуют введённым")

    with allure.step("Нажать кнопку Search"):
        claim_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

    with allure.step("Проверить сообщение 'No Records'"):
        assert claim_page.check_message("No Records")
        logger.info("✓ Сообщение  появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="no_records_message",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажать кнопку Reset"):
        claim_page.RESET_BUTTON.click()
        logger.info("Кнопка Reset нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_reset",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить значения полей после сброса"):
        new_id = claim_page.REFERENCE_ID.get_attribute('value')
        new_status = claim_page.STATUS_DROPDOWN.get_text()
        new_date = claim_page.TO_DATE.get_attribute('value')
        logger.info(f"После сброса: Reference ID: {new_id}, Status: {new_status}, To Date: {new_date}")

        assert new_id == "1234"  # поле Reference Id остается статичным даже после reset
        assert new_status == "-- Select --"
        assert new_date == ""
        logger.info("✓ Поля сброшены корректно (Reference ID не изменился)")
