
from selenium.webdriver.common.by import By
from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage




class DirectoryPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.DIRECTORY_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-table-filter-header-title")
        )
        self.MENU_DIRECTORY = BaseElement(driver, (By.XPATH, "//span[text()='Directory']"))
        self.FILTER_PANNEL = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        self.EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, '//input[@placeholder="Type for hints..."]'))
        self.JOB_TITLE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.LOCATION = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.FIRST_OPTION_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-option'])[2]"))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='reset']"))
        self.FIRST_EMPLOYEE_CARD = BaseElement(driver,(By.CSS_SELECTOR, ".orangehrm-directory-card"))
        self.LAST_EMPLOYEE_CARD = BaseElement(driver,(By.CSS_SELECTOR, ".orangehrm-directory-card:last-of-type"))


    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.DIRECTORY_TITLE.should_be_visible()
        self.FILTER_PANNEL.should_be_visible()
        self.EMPLOYEE_NAME.should_be_visible()
        self.JOB_TITLE_DROPDOWN.should_be_visible()
        self.LOCATION.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.LAST_EMPLOYEE_CARD.should_be_visible()
        self.FIRST_EMPLOYEE_CARD.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.DIRECTORY_TITLE.should_be_has_text("Directory")
        self.PAGE_TITLE.should_be_has_text("Directory")

