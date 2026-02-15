from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class AddJobTitlePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.JOB_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title")
        )
        self.JOB_TITLE_FIELD = BaseElement(
            driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]")
        )
        self.JOB_DESCRIPTION = BaseElement(
            driver, (By.XPATH, "(//textarea[@placeholder='Type description here'])")
        )
        self.JOB_SPECIFICATION = BaseElement(
            driver, (By.XPATH, "//input[@type='file']")
        )
        self.NOTE = BaseElement(
            driver, (By.XPATH, "(//textarea[@placeholder='Add note'])")
        )
        # Кнопки
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[4]")
        )
        self.SAVE_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        # Сообщение об ошибке
        self.ERROR = BaseElement(
            driver, (By.XPATH, "(//span[@type='oxd-input-field-error-message'])")
        )

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.JOB_TITLE.should_be_visible()
        self.JOB_TITLE_FIELD.should_be_visible()
        self.JOB_DESCRIPTION.should_be_visible()
        self.NOTE.should_be_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.JOB_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_be_has_text("Add Job Title")
