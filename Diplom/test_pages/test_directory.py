import pytest
import allure

from conftest import logger
from Diplom.page_obj.directory_page import DirectoryPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def directory_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return DirectoryPage(driver)


@allure.epic("Directory")
@allure.title("Открытие страницы Directory")
@pytest.mark.smoke
def test_directory_page(directory_page, driver):
    logger.info("=== Начало test_directory_page ===")
    with allure.step("Клик по меню Directory"):
        directory_page.MENU_DIRECTORY.click()
        logger.info("Меню Directory нажато")

    with allure.step("Проверка открытия страницы"):
        directory_page.check_that_page_opened()
        current_url = directory_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="directory_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )
        assert current_url == URLS.DIRECTORY
        logger.info("✓ URL страницы Directory корректен")

    logger.info("=== Конец test_directory_page ===")


@allure.epic("Directory")
@allure.title("Сворачивание/разворачивание панели фильтров")
def test_panel_filter(directory_page, driver):
    logger.info("=== Начало test_panel_filter ===")
    with allure.step("Открыть страницу Directory"):
        directory_page.MENU_DIRECTORY.click()
        logger.info("Меню Directory нажато")

    with allure.step("Свернуть панель фильтров"):
        directory_page.FILTER_PANNEL.click()
        logger.info("Панель фильтров свернута")

    with allure.step("Проверить, что поле Employee Name скрыто"):
        assert directory_page.EMPLOYEE_NAME.should_be_not_visible()
        logger.info("✓ Поле Employee Name не видно")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_collapsed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Развернуть панель фильтров"):
        directory_page.FILTER_PANNEL.click()
        logger.info("Панель фильтров развернута")

    with allure.step("Проверить, что поле Employee Name стало видимым"):
        directory_page.EMPLOYEE_NAME.should_be_visible()
        logger.info("✓ Поле Employee Name видно")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_expanded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_panel_filter ===")


@allure.epic("Directory")
@allure.title("Поиск по полям и сброс фильтров")
def test_search_fields_and_reset(directory_page, driver):
    logger.info("=== Начало test_search_fields_and_reset ===")
    with allure.step("Открыть страницу Directory"):
        directory_page.MENU_DIRECTORY.click()
        logger.info("Меню Directory нажато")

    with allure.step("Выбрать должность (Job Title)"):
        directory_page.JOB_TITLE_DROPDOWN.click()
        logger.info("Выпадающий список Job Title открыт")
        directory_page.FIRST_OPTION_DROPDOWN.click()
        logger.info("Выбран первый пункт в списке")

    with allure.step("Выбрать местоположение (Location)"):
        directory_page.LOCATION.click()
        logger.info("Выпадающий список Location открыт")
        directory_page.FIRST_OPTION_DROPDOWN.click()
        logger.info("Выбран первый пункт в списке")

    allure.attach(
        driver.get_screenshot_as_png(),
        name="filters_selected",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step("Нажать кнопку Search"):
        directory_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

    with allure.step("Проверить сообщение 'No Records'"):
        assert directory_page.check_message("No Records")
        logger.info("✓ Сообщение 'No Records' появилось")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="no_records_message",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить выбранное значение Job Title"):
        job_title = directory_page.JOB_TITLE_DROPDOWN.get_text()
        logger.info(f"Job Title после поиска: {job_title}")
        assert job_title == "Account Assistant"
        logger.info("✓ Job Title соответствует ожидаемому")

    with allure.step("Нажать кнопку Reset"):
        directory_page.RESET_BUTTON.click()
        logger.info("Кнопка Reset нажата")

    with allure.step("Проверить сброс Job Title на '-- Select --'"):
        new_job_title = directory_page.JOB_TITLE_DROPDOWN.get_text()
        logger.info(f"Job Title после сброса: {new_job_title}")
        assert new_job_title == "-- Select --"
        logger.info("✓ Job Title сброшен корректно")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_reset",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_search_fields_and_reset ===")