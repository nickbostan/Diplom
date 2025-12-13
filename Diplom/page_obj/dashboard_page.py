from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class DashboardPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.SEARCH_FIELD = BaseElement(
            driver, (By.CSS_SELECTOR, "input[placeholder='Search']")
        )
        self.DASHBOARD_TITLE = BaseElement(
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
        self.MENU_CLAIM = BaseElement(driver, (By.XPATH, "//span[text()='Claim']"))
        self.MENU_MAINTENANCE = BaseElement(
            driver, (By.XPATH, "//span[text()='Maintenance']")
        )
        self.MENU_BUZZ = BaseElement(driver, (By.XPATH, "//span[text()='Buzz']"))
        self.QUICK_LAUNCH = BaseElement(
            driver, (By.XPATH, "//p[text()='Quick Launch']")
        )
        self.TIME_AT_WORK_WIDGET = BaseElement(
            driver, (By.XPATH, "//p[text()='Time at Work']")
        )
        self.MY_ACTIONS_WIDGET = BaseElement(
            driver, (By.XPATH, "//p[text()='My Actions']")
        )
        self.ASSIGN_LEAVE_CARD = BaseElement(
            driver, (By.XPATH, "//p[text()='Assign Leave']")
        )
        self.LEAVE_LIST_CARD = BaseElement(
            driver, (By.XPATH, "//p[text()='Leave List']")
        )
        self.TIMESHEETS_CARD = BaseElement(
            driver, (By.XPATH, "//p[text()='Timesheets']")
        )
        self.APPLY_LEAVE_CARD = BaseElement(
            driver, (By.XPATH, "//p[text()='Apply Leave']")
        )
        self.MY_LEAVE_CARD = BaseElement(driver, (By.XPATH, "//p[text()='My Leave']"))
        self.MY_TIMESHEET_CARD = BaseElement(
            driver, (By.XPATH, "//p[text()='My Timesheet']")
        )
        self.CONFIG_EMPL_LEAVE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-leave-card-icon")
        )
        self.SAVE_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.CANCEL_BUTTON = BaseElement(driver, (By.CLASS_NAME, "oxd-button--ghost"))
        self.SHOW_BUTTON = BaseElement(driver, (By.CLASS_NAME, "--label-right"))

    def click_logout(self):
        self.USER_DROPDOWN.click()
        self.LOGOUT_MENU_ITEM.click()

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.DASHBOARD_TITLE.should_be_visible()
        self.USER_DROPDOWN.should_be_visible()
        self.MENU_PIM.should_be_visible()
        self.MENU_DIRECTORY.should_be_visible()
        self.QUICK_LAUNCH.should_be_visible()
        self.MENU_ADMIN.should_be_visible()
        self.SEARCH_FIELD.should_be_visible()
        self.MY_TIMESHEET_CARD.should_be_visible()

        self.DASHBOARD_TITLE.should_be_has_text("Dashboard")
