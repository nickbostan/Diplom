from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class AdminPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.SEARCH_FIELD = BaseElement(
            driver, (By.CSS_SELECTOR, "input[placeholder='Search']")
        )
        self.ADMIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module")
        )
        self.USER_DROPDOWN = BaseElement(
            driver, (By.CLASS_NAME, "oxd-userdropdown-tab")
        )
        self.DROPDOWN_MENU = BaseElement(driver, (By.CLASS_NAME, "oxd-dropdown-menu"))
        self.ABOUT_MENU_ITEM = BaseElement(driver, (By.XPATH, "//a[text()='About']"))
        self.SUPPORT_MENU_ITEM = BaseElement(
            driver, (By.XPATH, "//a[text()='Support']")
        )
        self.CHANGE_PASSWORD_MENU_ITEM = BaseElement(
            driver, (By.XPATH, "//a[text()='Change Password']")
        )
        self.LOGOUT_MENU_ITEM = BaseElement(driver, (By.XPATH, "//a[text()='Logout']"))
        self.SIDEBAR = BaseElement(driver, (By.CLASS_NAME, "oxd-sidepanel"))
        self.MENU_BUTTON = BaseElement(driver, (By.CLASS_NAME, "oxd-main-menu-button"))
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//span[text()='Admin']"))
        self.MENU_PIM = BaseElement(driver, (By.XPATH, "//span[text()='PIM']"))
        self.MENU_LEAVE = BaseElement(driver, (By.XPATH, "//span[text()='Leave']"))
        self.MENU_TIME = BaseElement(driver, (By.XPATH, "//span[text()='Time']"))
        self.MENU_RECRUITMENT = BaseElement(
            driver, (By.XPATH, "//span[text()='Recruitment']")
        )
        self.MENU_MY_INFO = BaseElement(driver, (By.XPATH, "//span[text()='My Info']"))
        self.MENU_PERFORMANCE = BaseElement(
            driver, (By.XPATH, "//span[text()='Performance']")
        )
        self.MENU_DASHBOARD = BaseElement(
            driver, (By.XPATH, "//span[text()='Dashboard']")
        )
        self.MENU_DIRECTORY = BaseElement(
            driver, (By.XPATH, "//span[text()='Directory']")
        )
        self.MENU_MAINTENANCE = BaseElement(
            driver, (By.XPATH, "//span[text()='Maintenance']")
        )
        self.MENU_CLAIM = BaseElement(driver, (By.XPATH, "//span[text()='Claim']"))
        self.MENU_BUZZ = BaseElement(driver, (By.XPATH, "//span[text()='Buzz']"))
        self.USERNAME_SEARCH = BaseElement(
            driver, (By.XPATH, "//label[text()='Username']/following::input[1]")
        )
        self.USER_ROLE_DROPDOWN = BaseElement(
            driver,
            (By.XPATH, '(//div[contains(@class, "oxd-select-text--active")])[1]'),
        )
        self.EMPLOYEE_NAME_SEARCH = BaseElement(
            driver, (By.CSS_SELECTOR, "input[placeholder='Type for hints...']")
        )
        self.STATUS_DROPDOWN = BaseElement(
            driver,
            (By.XPATH, '(//div[contains(@class, "oxd-select-text--active")])[2]'),
        )
        self.SEARCH_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.RESET_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='button']")
        )
        self.ADD_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[6]")
        )
        self.DELETE_SELECTED_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button.oxd-button--label-danger")
        )
        self.CHECKBOX_HEADER = BaseElement(
            driver, (By.CSS_SELECTOR, "input[wfd-id='id3']")
        )
        self.CHECKBOX_ADMIN = BaseElement(
            driver, (By.CSS_SELECTOR, "input[wfd-id='id4']")
        )
        self.CHECKBOX_FIRST_USER = BaseElement(
            driver, (By.CSS_SELECTOR, "input[wfd-id='id5']")
        )
        self.JOB = BaseElement(driver, (By.XPATH, "//span[text()='Job']"))
        self.USER_MANAGEMENT = BaseElement(driver, (By.XPATH, "//span[contains(text(), 'User Management')]"))
        self.ORGANIZATION = BaseElement(driver, (By.XPATH, "//span[text()='Organization ']"))
        self.QUALIFICATIONS = BaseElement(driver, (By.XPATH, "//span[text()='Qualifications ']"))
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))



    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.ADMIN_TITLE.should_be_visible()
        self.USER_DROPDOWN.should_be_visible()
        self.MENU_PIM.should_be_visible()
        self.MENU_DIRECTORY.should_be_visible()
        self.EMPLOYEE_NAME_SEARCH.should_be_visible()
        self.MENU_ADMIN.should_be_visible()
        self.SEARCH_FIELD.should_be_visible()
        self.ADD_BUTTON.should_be_visible()
        self.USER_MANAGEMENT.should_be_visible()
        self.QUALIFICATIONS.should_be_visible()
        self.MORE.should_be_visible()

        self.ADMIN_TITLE.should_be_has_text("Admin")

