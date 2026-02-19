
from selenium.webdriver.common.by import By
from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage

class LeavePage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.MENU_LEAVE = BaseElement(driver, (By.XPATH, "//span[text()='Leave']"))
        self.LEAVE_TITLE = BaseElement(driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver, (By.CLASS_NAME, "oxd-table-filter-header-title"))
        # Панель фильтров
        self.LEAVE_LIST_FILTER_PANEL = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        # Поля фильтрации
        self.EMPLOYEE_NAME_FIELD = BaseElement(driver, (By.XPATH, "//label[text()='Employee Name']/following::input[1]"))
        self.LEAVE_TYPE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.FROM_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[1]"))
        self.TO_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]"))
        self.SHOW_LEAVES_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.SUB_UNIT_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[3]"))
        self.PAST_EMPLOYEES_CHECKBOX = BaseElement(driver, (By.CLASS_NAME, "oxd-switch-input"))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_BUTTON = BaseElement(driver, (By.XPATH, "//button[@type='reset']"))
        self.SELECT_ALL_CHECKBOX = BaseElement(
            driver, (By.CLASS_NAME, "oxd-checkbox-input--active"))
        # Доп опции
        self.FIRST_OPTION_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[contains(@class, 'oxd-select-option')])[2]"))
        self.LEAVE_STATUS_SHOWN_1 = BaseElement(driver, (By.XPATH, "//span[contains(@class, 'oxd-multiselect-chips-selected')]"))
        self.LEAVE_STATUS_SHOWN_2 = BaseElement(driver,
                                                (By.XPATH, "(//span[contains(@class, 'oxd-multiselect-chips-selected')])[2]"))
        self.LEAVE_STATUS_SHOWN_3 = BaseElement(driver,
                                                (By.XPATH, "(//span[contains(@class, 'oxd-multiselect-chips-selected')])[3]"))
        self.LEAVE_STATUS_DELETE_1 = BaseElement(driver, (By.XPATH, "//i[@class='oxd-icon bi-x --clear']"))
        self.LEAVE_STATUS_DELETE_2 = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-icon bi-x --clear'])[2]"))
        self.LEAVE_STATUS_DELETE_3 = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-icon bi-x --clear'])[3]"))
        self.REJECTED_OPTION = BaseElement(driver, (By.XPATH,
                                                    "//div[contains(@class, 'oxd-select-option') and .//span[text()='Rejected']]"))





    def check_that_page_opened(self):
        self.LEAVE_TITLE.should_be_visible()
        self.LEAVE_LIST_FILTER_PANEL.should_be_visible()
        self.FROM_DATE.should_be_visible()
        self.SHOW_LEAVES_DROPDOWN.should_be_visible()
        self.SUB_UNIT_DROPDOWN.should_be_visible()
        self.PAST_EMPLOYEES_CHECKBOX.should_be_visible()
        self.SELECT_ALL_CHECKBOX.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.LEAVE_TITLE.should_be_has_text("Leave")
        self.PAGE_TITLE.should_be_has_text("Leave List")



    def input_search(self):
        self.FROM_DATE.fill("2016-02-05")
        self.TO_DATE.fill("2025-25-08")
        self.LEAVE_TYPE_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.SHOW_LEAVES_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.SUB_UNIT_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.PAST_EMPLOYEES_CHECKBOX.click()
        return self