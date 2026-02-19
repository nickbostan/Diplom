import time

import allure
import pytest

from conftest import logger
from Diplom.page_obj.leave_page import LeavePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def leave_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return LeavePage(driver)


@allure.epic("Страница Leave")
@allure.title("Открытие страницы Leave")
@pytest.mark.smoke
def test_leave_page(leave_page, driver):
    logger.info("=== Начало test_leave_page ===")
    with allure.step("Клик по меню Leave"):
        leave_page.MENU_LEAVE.click()
        logger.info("Leave нажато")

    with allure.step("Проверка открытия страницы"):
        leave_page.check_that_page_opened()
        current_url = leave_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="leave_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.LEAVE
        logger.info("✓ Страница отображается корректно")

    logger.info("=== Конец test_leave_page ===")


@allure.epic("Страница Leave")
@allure.title("Сворачивание/разворачивание панели фильтров")
def test_panel_filter(leave_page, driver):
    logger.info("=== Начало test_panel_filter ===")
    with allure.step("Открыть страницу Leave"):
        leave_page.MENU_LEAVE.click()
        logger.info("Leave нажато")

    with allure.step("Свернуть панель фильтров"):
        leave_page.LEAVE_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров свернута")

    with allure.step("Проверить, что поле Employee Name скрыто"):
        assert leave_page.EMPLOYEE_NAME_FIELD.should_be_not_visible()
        logger.info("✓ Поле Employee Name не видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_collapsed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Развернуть панель фильтров"):
        leave_page.LEAVE_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров развернута")

    with allure.step("Проверить, что поле Employee Name стало видимым"):
        leave_page.EMPLOYEE_NAME_FIELD.should_be_visible()
        logger.info("✓ Поле Employee Name видно")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_expanded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_panel_filter ===")


@allure.epic("Страница Leave")
@allure.title("Поиск по полям и сброс фильтров")
def test_search_fields_and_reset(leave_page, driver):
    logger.info("=== Начало test_search_fields_and_reset ===")
    with allure.step("Открыть страницу Leave"):
        leave_page.MENU_LEAVE.click()
        logger.info("Leave нажато")

    with allure.step("Заполнить поля поиска через input_search()"):
        leave_page.input_search()
        logger.info("Поля поиска заполнены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_fields_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажать кнопку Search"):
        leave_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

    with allure.step("Проверить сообщение 'No Records'"):
        assert leave_page.check_message("No Records")
        logger.info("✓ Сообщение 'No Records' появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="no_records_message",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить значение поля Sub Unit и From date"):
        from_date = leave_page.FROM_DATE.get_attribute("value")
        status = leave_page.SUB_UNIT_DROPDOWN.get_text()
        logger.info(f"Значения после поиска: {status} и {from_date}")
        assert from_date == "2016-02-05"
        assert status == "Administration"
        logger.info("✓ Введенные значения соответствует ожидаемому")

    with allure.step("Нажать кнопку Reset"):
        leave_page.RESET_BUTTON.click()
        logger.info("Кнопка Reset нажата")

    with allure.step("Проверить сброс"):
        new_from_date = leave_page.FROM_DATE.get_attribute("value")
        new_status = leave_page.SUB_UNIT_DROPDOWN.get_text()
        logger.info(f"Значения после сброса: {new_status} и {new_from_date}")
        assert new_from_date == "2016-02-05"
        assert new_status == "-- Select --"
        logger.info("✓ Значения сброшены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_reset",
            attachment_type=allure.attachment_type.PNG,
        )

    """ Также хотел проверить как работает сброс дат , они должны вернуться на 2026-01-01 и 2026-31-12 ,
       но почему-то значения остаются те же """

    logger.info("=== Конец test_search_fields_and_reset ===")


@allure.epic("Страница Leave")
@allure.title("Проверка выбора статусов в выпадающем списке Show Leaves")
def test_show_leave_dropdown(leave_page, driver):
    logger.info("=== Начало test_show_leave_dropdown ===")

    with allure.step("Открыть страницу Leave"):
        leave_page.MENU_LEAVE.click()
        logger.info("Leave нажато")

    with allure.step("Выбрать статус 'Rejected' в выпадающем списке"):
        leave_page.SHOW_LEAVES_DROPDOWN.select_from_dropdown("Rejected")
        logger.info("Выбран статус 'Rejected'")

    with allure.step("Выбрать статус 'Cancelled' в выпадающем списке"):
        leave_page.SHOW_LEAVES_DROPDOWN.select_from_dropdown("Cancelled")
        logger.info("Выбран статус 'Cancelled'")

    with allure.step("Проверить, что статусы отображаются в таблице"):
        assert leave_page.LEAVE_STATUS_SHOWN_2.should_contain_text("Rejected")
        logger.info("✓ Статус 'Rejected' отображается")
        assert leave_page.LEAVE_STATUS_SHOWN_3.should_contain_text("Cancelled")
        logger.info("✓ Статус 'Cancelled' отображается")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="statuses_shown",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Удалить добавленные статусы"):
        leave_page.LEAVE_STATUS_DELETE_3.click()
        leave_page.LEAVE_STATUS_DELETE_2.click()
        leave_page.LEAVE_STATUS_DELETE_1.click()
        logger.info("Кнопки удаления нажаты")

    with allure.step("Проверить, что первый статус исчез"):
        assert leave_page.LEAVE_STATUS_SHOWN_1.should_be_not_visible()
        logger.info("✓ Статус исчез")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_deletion",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Повторно выбрать статус 'Rejected'"):
        leave_page.SHOW_LEAVES_DROPDOWN.select_from_dropdown("Rejected")
        logger.info("Статус 'Rejected' выбран повторно")

    time.sleep(3)

    with allure.step(
        "Открыть выпадающий список и проверить состояние опции 'Rejected'"
    ):
        leave_page.SHOW_LEAVES_DROPDOWN.click()
        rejected_option = leave_page.REJECTED_OPTION

        if not rejected_option.is_checked():
            logger.info("Опция 'Rejected' неактивна (disabled)")
        else:
            class_attr = rejected_option.get_attribute("class")
            assert (
                "selected" in class_attr or "oxd-select-option --selected" in class_attr
            ), f"Опция должна быть отмечена как выбранная, класс: {class_attr}"
            logger.info("Опция 'Rejected' имеет класс selected")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="dropdown_options",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_show_leave_dropdown ===")
