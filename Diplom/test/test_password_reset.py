import pytest
import pytest_check as check
from selenium.webdriver.common.by import By

from Diplom.page_obj.password_reset_page import PasswordPage
from Diplom.urls import URLS


@pytest.fixture()
def password_page(driver):
    return PasswordPage(driver)


@pytest.fixture()
def open_page(password_page):
    password_page.open_page()


@pytest.mark.smoke
def test_check_all_elements(password_page, open_page, driver):
    password_page.check_that_page_opened()
    assert password_page.driver.current_url == URLS.PASSWORD


def test_cancel(password_page, open_page, driver):
    password_page.CANCEL_BUTTON.click()
    assert password_page.driver.current_url == URLS.LOGIN


def test_reset(password_page, open_page, driver):
    password_page.reset_password("Admin")
    success_message = password_page.driver.find_element(
        By.CSS_SELECTOR, "h6.orangehrm-forgot-password-title"
    )
    check.is_in("sent successfully", success_message.text)
    check.is_true(success_message.is_displayed())
    check.is_in("auth/sendPasswordReset", password_page.driver.current_url)


def test_negative_empty_fields(password_page, open_page):
    password_page.reset_password("")
    password_page.check_that_empty_error_is_visible("Required")



