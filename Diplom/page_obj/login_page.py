from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage
from Diplom.urls import URLS


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(
            driver, (By.CSS_SELECTOR, ".orangehrm-login-branding img")
        )
        self.LOGO_2 = BaseElement(driver, (By.CLASS_NAME, "orangehrm-login-logo"))
        self.LOGIN_TITLE = BaseElement(driver, (By.CLASS_NAME, "orangehrm-login-title"))
        self.PAGE_TITLE = BaseElement(driver, (By.TAG_NAME, "title"))
        self.LOGIN_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.INPUT_USER_NAME = BaseElement(driver, (By.NAME, "username"))
        self.INPUT_PASSWORD = BaseElement(driver, (By.NAME, "password"))
        self.FORGOT_PASSWORD_LINK = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-login-forgot-header")
        )
        self.LINKEDIN_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'linkedin.com')]")
        )
        self.FACEBOOK_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'facebook.com')]")
        )
        self.TWITTER_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'twitter.com')]")
        )
        self.YOUTUBE_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'youtube.com')]")
        )
        self.SITE_LINK = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, 'orangehrm.com')]")
        )
        self.ERROR = BaseElement(driver, (By.CLASS_NAME, "oxd-alert-content"))
        self.EMPTY_ERROR = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )

    def open_page(self):
        self.open(URLS.LOGIN)

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.LOGO_2.should_be_visible()
        self.LOGIN_TITLE.should_be_visible()
        self.LOGIN_BUTTON.should_be_visible()
        self.INPUT_USER_NAME.should_be_visible()
        self.INPUT_PASSWORD.should_be_visible()
        self.FORGOT_PASSWORD_LINK.should_be_visible()
        self.LINKEDIN_LINK.should_be_visible()
        self.FACEBOOK_LINK.should_be_visible()
        self.TWITTER_LINK.should_be_visible()
        self.YOUTUBE_LINK.should_be_visible()
        self.SITE_LINK.should_be_visible()

        self.LOGIN_TITLE.should_be_has_text("Login")

        self.ERROR.should_be_not_visible()
        self.EMPTY_ERROR.should_be_not_visible()

    def login(self, username, password):
        self.INPUT_USER_NAME.fill(username)
        self.INPUT_PASSWORD.fill(password)
        self.LOGIN_BUTTON.click()
        return self

    def check_that_error_is_visible(self, text):
        self.ERROR.should_be_visible()
        self.ERROR.should_be_has_text(text)
        return self

    def check_that_empty_error_is_visible(self, text):
        self.EMPTY_ERROR.should_be_visible()
        self.EMPTY_ERROR.should_be_has_text(text)
        return self

    def get_error_text(self):
        return self.ERROR.get_text()