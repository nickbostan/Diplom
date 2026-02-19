from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class MaintenancePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAINTENANCE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title")
        )
        self.MENU_MAINTENANCE = BaseElement(driver, (By.XPATH, "//span[text()='Maintenance']"))
        # Страница подтверждения
        self.PASSWORD = BaseElement(driver, (By.NAME, "password"))
        self.CONFIRM_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.CANCEL_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='button']"))
        # Основная страница
        self.PAST_EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, '//input[@placeholder="Type for hints..."]'))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAINTENANCE_TITLE.should_be_visible()
        self.MENU_MAINTENANCE.should_be_visible()
        self.PAST_EMPLOYEE_NAME.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAINTENANCE_TITLE.should_be_has_text("Maintenance")
        self.PAGE_TITLE.should_be_has_text("Purge Employee Records")
