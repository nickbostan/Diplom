from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class ClaimPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.CLAIM_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver,(By.CLASS_NAME, "oxd-table-filter-header-title"))
        self.PAGE_TITLE_ASSIGN = BaseElement(driver, (By.CLASS_NAME, "orangehrm-main-title"))
        self.MENU_CLAIM = BaseElement(
            driver, (By.XPATH, "//span[text()='Claim']")
        )
        # Панель фильтров
        self.CLAIM_LIST_FILTER_PANEL = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        # Поля фильтрации
        self.EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, '//input[@placeholder="Type for hints..."]'))
        self.REFERENCE_ID = BaseElement(driver, (By.XPATH, '(//input[@placeholder="Type for hints..."])[2]'))
        self.FROM_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]"))
        self.TO_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]"))
        self.EVENT_NAME_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.STATUS_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.INCLUDE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[3]"))
        self.FIRST_OPTION_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-option'])[2]"))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[5]"))
        self.ASSIGN_CLAIM_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[6]"))
        # Действия в таблице
        self.VIEW_DETAILS_FIRST_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[7]"))
        self.VIEW_DETAILS_LAST_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[last()]"))







    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.CLAIM_TITLE.should_be_visible()
        self.EMPLOYEE_NAME.should_be_visible()
        self.REFERENCE_ID.should_be_visible()
        self.STATUS_DROPDOWN.should_be_visible()
        self.MENU_CLAIM.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.INCLUDE_DROPDOWN.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.ASSIGN_CLAIM_BUTTON.should_be_visible()
        self.VIEW_DETAILS_FIRST_BUTTON.should_be_visible()
        self.FROM_DATE.should_be_visible()
        self.VIEW_DETAILS_LAST_BUTTON.should_be_visible()
        self.CLAIM_LIST_FILTER_PANEL.should_be_visible()

        self.CLAIM_TITLE.should_be_has_text("Claim")
        self.PAGE_TITLE.should_be_has_text("Employee Claims")


    def input_search(self):
        self.REFERENCE_ID.fill("1234")
        self.FROM_DATE.fill("2016-02-05")
        self.TO_DATE.fill("2025-25-08")
        self.INCLUDE_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.STATUS_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.EVENT_NAME_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        return self