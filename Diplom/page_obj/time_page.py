from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class TimePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.TIME_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title"))
        self.MENU_TIME = BaseElement(driver, (By.XPATH, "//span[text()='Time']"))
        self.EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, '//input[@placeholder="Type for hints..."]'))
        self.VIEW_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.VIEW_FIRST_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        self.VIEW_LAST_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[last()]"))


    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.TIME_TITLE.should_be_visible()
        self.EMPLOYEE_NAME.should_be_visible()
        self.VIEW_BUTTON.should_be_visible()
        self.VIEW_FIRST_BUTTON.should_be_visible()
        self.VIEW_LAST_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.TIME_TITLE.should_be_has_text("Time")
        self.PAGE_TITLE.should_be_has_text("Select Employee")
