import pytest
import allure

from conftest import logger
from Diplom.page_obj.maintenance_page import MaintenancePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def maintenance_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return MaintenancePage(driver)


@allure.epic("Страница Maintenance")
@allure.title("Доступ к странице Maintenance с паролем")
@pytest.mark.smoke
def test_maintenance_page(maintenance_page, driver):
    logger.info("=== Начало test_maintenance_page ===")
    with allure.step("Клик по меню Maintenance"):
        maintenance_page.MENU_MAINTENANCE.click()
        logger.info("Maintenance нажато")

    with allure.step("Ввод пароля администратора"):
        maintenance_page.PASSWORD.fill("admin123")
        logger.info("Пароль введён")

    with allure.step("Подтверждение пароля"):
        maintenance_page.CONFIRM_BUTTON.click()
        logger.info("Кнопка Confirm нажата")

    with allure.step("Проверка открытия страницы Maintenance"):
        maintenance_page.check_that_page_opened()
        current_url = maintenance_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="maintenance_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.MAINTENANCE
        logger.info("✓ Страница открыта корректно")

    logger.info("=== Конец test_maintenance_page ===")