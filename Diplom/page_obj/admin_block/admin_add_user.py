import time

from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class AdminAddPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.SEARCH_FIELD = BaseElement(
            driver, (By.CSS_SELECTOR, "input[placeholder='Search']")
        )
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module")
        )
        self.PAGE_TITLE = BaseElement(driver, (By.CLASS_NAME, "orangehrm-main-title"))
        self.USER_ROLE = BaseElement(
            driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]")
        )
        self.ROLE_ADMIN = BaseElement(
            driver, (By.XPATH, f".//*[contains(text(), 'Admin')]")
        )
        self.ROLE_ESS = BaseElement(
            driver, (By.XPATH, f".//*[contains(text(), 'ESS')]")
        )
        self.STATUS = BaseElement(
            driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]")
        )
        self.STATUS_ENABLED = BaseElement(
            driver, (By.XPATH, f".//*[contains(text(), 'Enabled')]")
        )
        self.STATUS_DISABLED = BaseElement(
            driver, (By.XPATH, f".//*[contains(text(), 'Disabled')]")
        )
        self.INPUT_EMPLOYEE_NAME = BaseElement(
            driver, (By.XPATH, "//input[@placeholder='Type for hints...']")
        )
        self.MAIN_NAME = BaseElement(
            driver, (By.XPATH, "//p[@class='oxd-userdropdown-name']")
        )
        self.FIRST_FOUND_EMPLOYEE = BaseElement(
            driver, (By.XPATH, "//div[@class='oxd-autocomplete-option']")
        )
        self.INPUT_USERNAME = BaseElement(
            driver,
            (By.XPATH, "(//input[contains(@class, 'oxd-input oxd-input--active')])[2]"),
        )
        self.INPUT_PASSWORD = BaseElement(
            driver, (By.XPATH, "//input[@type='password']")
        )
        self.TABLE = BaseElement(
            driver, (By.XPATH, "//div[@row-decorator()='oxd-table-decorator-card']")
        )
        self.INPUT_CONF_PASSWORD = BaseElement(
            driver, (By.XPATH, "(//input[@type='password'])[2]")
        )
        # Кнопки
        self.SAVE_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[4]")
        )
        # Ошибки
        self.ERROR_LENGTH_PASS = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )
        self.ERROR_WEAK_PASS = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )
        self.ERROR_MATCH_PASS = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )
        self.USERNAME_ERROR = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )
        self.EMPTY_ERROR = BaseElement(
            driver, (By.CLASS_NAME, "oxd-input-field-error-message")
        )

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.PAGE_TITLE.should_be_visible()
        self.INPUT_CONF_PASSWORD.should_be_visible()
        self.STATUS.should_be_visible()
        self.USER_ROLE.should_be_visible()
        self.INPUT_PASSWORD.should_be_visible()
        self.INPUT_USERNAME.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.USERNAME_ERROR.should_be_not_visible()

        self.MAIN_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_be_has_text("Add User")

    def check_that_username_error_is_visible(self, text):
        self.USERNAME_ERROR.should_be_visible()
        self.USERNAME_ERROR.should_be_has_text(text)
        return self

    def check_that_weak_password_error_is_visible(self, text):
        self.ERROR_WEAK_PASS.should_be_visible()
        self.ERROR_WEAK_PASS.should_be_has_text(text)
        return self

    def check_that_length_password_error_is_visible(self, text):
        self.ERROR_LENGTH_PASS.should_be_visible()
        self.ERROR_LENGTH_PASS.should_be_has_text(text)
        return self

    def check_that_match_password_error_is_visible(self):
        self.ERROR_MATCH_PASS.should_be_visible()
        self.ERROR_MATCH_PASS.should_be_has_text("Passwords do not match")
        return self

    def check_that_empty_error_is_visible(self, text):
        self.EMPTY_ERROR.should_be_visible()
        self.EMPTY_ERROR.should_be_has_text(text)
        return self

    def get_name_text(self):
        return self.MAIN_NAME.get_text()

    def add_user(self, username, password, name):
        self.STATUS.click()
        self.STATUS_ENABLED.click()
        self.USER_ROLE.click()
        self.ROLE_ESS.click()
        self.INPUT_EMPLOYEE_NAME.fill(name)
        time.sleep(3)
        self.FIRST_FOUND_EMPLOYEE.click()
        self.INPUT_USERNAME.fill(username)
        self.INPUT_PASSWORD.fill(password)
        self.INPUT_CONF_PASSWORD.fill(password)
        return self
