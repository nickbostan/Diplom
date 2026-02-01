import pytest
import pytest_check as check
import allure

from conftest import logger
from selenium.webdriver.common.by import By
from Diplom.page_obj.password_reset_page import PasswordPage
from Diplom.urls import URLS


@pytest.fixture()
def password_page(driver):
    return PasswordPage(driver)


@pytest.fixture()
def open_page(password_page):
    password_page.open_page()

@allure.epic("Страница восстановления пароля")
@allure.title("Проверка отображения страницы восстановления пароля")
@pytest.mark.smoke
def test_check_all_elements(password_page, open_page, driver):
    logger.info("=== Начало test_check_all_elements ===")

    with allure.step("Проверяем страницу"):
        password_page.check_that_page_opened()
        allure.attach(driver.get_screenshot_as_png(), name="page", attachment_type=allure.attachment_type.PNG)
        assert password_page.driver.current_url == URLS.PASSWORD
        logger.info("✓ Страница открыта")

    logger.info("=== Конец test_check_all_elements ===")

@allure.epic("Страница восстановления пароля")
@allure.title("Отмена восстановления")
def test_cancel(password_page, open_page, driver):
    logger.info("=== Начало test_cancel ===")

    with allure.step("Нажимаем Cancel"):
        password_page.CANCEL_BUTTON.click()
        allure.attach(driver.get_screenshot_as_png(), name="cancel", attachment_type=allure.attachment_type.PNG)
        assert password_page.driver.current_url == URLS.LOGIN
        logger.info("✓ Возврат на страницу логина")

    logger.info("=== Конец test_cancel ===")

@allure.epic("Страница восстановления пароля")
@allure.feature("Сброс пароля")
@allure.title("Сброс и восстановление пароля")
def test_reset(password_page, open_page, driver):
    logger.info("=== Начало test_reset ===")

    with allure.step("Сбрасываем пароль"):
        password_page.reset_password("Admin")
        allure.attach(driver.get_screenshot_as_png(), name="reset", attachment_type=allure.attachment_type.PNG)

        success_message = password_page.driver.find_element(
            By.CSS_SELECTOR, "h6.orangehrm-forgot-password-title"
        )

        check.is_in("sent successfully", success_message.text)
        check.is_true(success_message.is_displayed())
        check.is_in("auth/sendPasswordReset", password_page.driver.current_url)
        logger.info("✓ Пароль сброшен")

    logger.info("=== Конец test_reset ===")

@allure.epic("Страница восстановления пароля")
@allure.feature("Сброс пароля")
@allure.title("Пустые поля")
def test_negative_empty_fields(password_page, open_page, driver):
    logger.info("=== Начало test_negative_empty_fields ===")

    with allure.step("Пустое поле"):
        password_page.reset_password("")
        allure.attach(driver.get_screenshot_as_png(), name="empty", attachment_type=allure.attachment_type.PNG)
        assert password_page.check_that_empty_error_is_visible("Required")
        logger.info("✓ Ошибка отображается")

    logger.info("=== Конец test_negative_empty_fields ===")



