from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class AdminAddPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.USER_ROLE = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[1]"))
        self.STATUS = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[2]"))
        self.INPUT_EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, "//input[@placeholder='Type for hints...']"))
        self.INPUT_USERNAME = BaseElement(driver, (By.XPATH, "(//input[contains(@class, 'oxd-input oxd-input--active')])[2]"))
        self.ROLE_ESS = BaseElement(driver, (By.XPATH,"//div[@class='oxd-select-text-input' and text()='ESS']"))
        self.ROLE_ADMIN = BaseElement(driver, (By.XPATH, "//div[@class='oxd-select-text-input' and text()='Enabled']"))
        self.ROLE_ESS = BaseElement(driver, (By.XPATH, "//div[@class='oxd-select-text-input' and text()='Disabled']"))
        self.INPUT_PASSWORD = BaseElement(driver, (By.XPATH, "//input[@type='password'][1]"))
        self.INPUT_CONF_PASSWORD = BaseElement(driver, (By.XPATH, "//input[@type='password'][2]"))
        self.SAVE_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='button']")
        )
        self.USERNAME_ERROR = BaseElement(driver, (By.CLASS_NAME, "oxd-input-field-error-message"))
        self.PASSWORD_ERROR = BaseElement(driver, (By.XPATH, "(//span[@class='oxd-input-field-error-message'])[2]"))

    def check_that_page_opened(self):
        self.INPUT_EMPLOYEE_NAME.should_be_visible()
        self.INPUT_CONF_PASSWORD.should_be_visible()
        self.ROLE_ADMIN.should_be_visible()
        self.STATUS.should_be_visible()
        self.USER_ROLE.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()

    def check_that_username_error_is_visible(self, text):
        self.USERNAME_ERROR.should_be_visible()
        self.USERNAME_ERROR.should_be_has_text(text)
        return self

    def check_that_password_error_is_visible(self, expected):
        self.PASSWORD_ERROR.should_be_visible()
        self.PASSWORD_ERROR.should_be_has_text(expected)
        return self







