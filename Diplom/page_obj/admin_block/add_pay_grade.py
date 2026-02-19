from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class AddPayGradePage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-card-container")
        )
        self.NAME = BaseElement(
            driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]")
        )
        self.ERROR_NAME = BaseElement(
            driver, (By.XPATH, "(//span[@class='oxd-input-field-error-message'])")
        )
        # Кнопки
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[4]")
        )
        self.SAVE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='submit'])"))

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.NAME.should_be_visible()
        self.ERROR_NAME.should_be_not_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_contain_text("Add Pay Grade")
