from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class PerformancePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.PERFORMANCE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver,(By.CLASS_NAME, "oxd-table-filter-header-title"))
        self.MENU_PERFORMANCE = BaseElement(
            driver, (By.XPATH, "//span[text()='Performance']")
        )
        self.PERFORMANCE_LIST_FILTER_PANEL = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        #Поля фильтрации
        self.JOB_TITLE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.SUB_UNIT_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.INCLUDE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[3]"))
        self.STATUS_DROPDOWN = BaseElement(driver,
                                           (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[4]"))
        self.EMPLOYEE_NAME = BaseElement(driver, (By.CSS_SELECTOR, "input[placeholder='Type for hints...']"))
        self.FROM_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]"))
        self.TO_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]"))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='reset']"))




    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.PERFORMANCE_TITLE.should_be_visible()
        self.STATUS_DROPDOWN.should_be_visible()
        self.EMPLOYEE_NAME.should_be_visible()
        self.JOB_TITLE_DROPDOWN.should_be_visible()
        self.STATUS_DROPDOWN.should_be_visible()
        self.MENU_PERFORMANCE.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.PERFORMANCE_TITLE.should_be_has_text("Performance")
        self.PAGE_TITLE.should_be_has_text("Employee Reviews")
