from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage
from Diplom.urls import URLS


class PasswordPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.PASSWORD_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-forgot-password-title")
        )
        self.PAGE_TITLE = BaseElement(driver, (By.TAG_NAME, "title"))
        self.RESET_PASSWORD_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.INPUT_USER_NAME = BaseElement(driver, (By.NAME, "username"))
        self.EMPTY_ERROR = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='button']")
        )
        self.SITE_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'orangehrm.com')]")
        )

    def open_page(self):
        self.open(URLS.PASSWORD)

    def check_that_page_opened(self):
        self.PASSWORD_TITLE.should_be_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.INPUT_USER_NAME.should_be_visible()
        self.RESET_PASSWORD_BUTTON.should_be_visible()
        self.SITE_LINK.should_be_visible()

        self.PASSWORD_TITLE.should_be_has_text("Reset Password")

        self.EMPTY_ERROR.should_be_not_visible()

    def check_that_empty_error_is_visible(self, text):
        self.EMPTY_ERROR.should_be_visible()
        self.EMPTY_ERROR.should_be_has_text(text)
        return self

    def reset_password(self, username):
        self.INPUT_USER_NAME.fill(username)
        self.RESET_PASSWORD_BUTTON.click()
