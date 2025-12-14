from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage

class PIMPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.PIM_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.SEARCH_FIELD = BaseElement(
            driver, (By.CSS_SELECTOR, "input[placeholder='Search']")
        )
        self.USER_DROPDOWN = BaseElement(
            driver, (By.CLASS_NAME, "oxd-userdropdown-tab")
        )
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//span[text()='Admin']"))
        self.MENU_BUZZ = BaseElement(driver, (By.XPATH, "//span[text()='Buzz']"))
        self.EMPLOYEE_PANEL = BaseElement(driver, (By.CLASS_NAME, "oxd-table-filter-header-options"))
        self.EMPLOYEE_NAME_FIELD = BaseElement(driver, (By.XPATH, "//label[text()='Employee Name']/following::input[1]"))
        self.EMPLOYEE_ID_FIELD = BaseElement(driver, (By.XPATH, "//label[text()='Employee Id']/following::input[1]"))
        self.EMPLOYMENT_STATUS_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.Full_Time_Permanent = BaseElement(driver, (By.XPATH, "//div[@role='option']/span[text()='Full-Time Permanent']"))
        self.Full_Time_Contract = BaseElement(driver, (By.XPATH, "//div[@role='option']/span[text()='Full-Time Contract']"))
        self.Part_Time_Permanent = BaseElement(driver, (By.XPATH, "//div[@role='option']/span[text()='Part-Time Permanent']"))
        self.Part_Time_Contract = BaseElement(driver, (By.XPATH, "//div[@role='option']/span[text()='Part-Time Contract']"))
        self.Freelance = BaseElement(driver, (By.XPATH, "//div[@role='option']/span[text()='Freelance']"))
        self.INCLUDE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
        self.RESET_BUTTON = (By.CSS_SELECTOR, "button[type='button']")
        self.ADD_BUTTON = (By.CSS_SELECTOR, "button.oxd-button--secondary")
        self.DELETE_SELECTED_BUTTON = (By.CLASS_NAME, "oxd-button--label-danger")
        self.SUPERVISOR_NAME_FIELD = BaseElement(driver, (By.XPATH, "//label[text()='Supervisor Name']/following::input[1]"))
        self.JOB_TITLE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[3]"))
        self.SUB_UNIT_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[4]"))
        self.INCLUDE_OPTIONS = {
            "Current Employees Only": (By.XPATH, "//div[@role='option']/span[text()='Current Employees Only']"),
            "Current and Past Employees": (By.XPATH, "//div[@role='option']/span[text()='Current and Past Employees']"),
            "Past Employees Only": (By.XPATH, "//div[@role='option']/span[text()='Past Employees Only']")}
        self.EMPLOYEE_TABLE = (By.CLASS_NAME, "oxd-table")
        self.TABLE_HEADERS = (By.CLASS_NAME, "oxd-table-header")
        self.TABLE_ROWS = (By.CLASS_NAME, "oxd-table-card")
        self.CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")
        self.ID_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][2]")
        self.FIRST_NAME_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][3]")
        self.LAST_NAME_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][4]")
        self.JOB_TITLE_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][5]")
        self.EMPLOYMENT_STATUS_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][6]")
        self.SUB_UNIT_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][7]")
        self.SUPERVISOR_COLUMN = (By.XPATH, "//div[contains(@class, 'oxd-table-cell')][8]")
        self.EDIT_BUTTONS = (By.CLASS_NAME, "bi-pencil-fill")
        self.DELETE_BUTTONS = (By.CLASS_NAME, "bi-trash")
        self.EMPLOYMENT_STATUS_OPTIONS = (By.CLASS_NAME, "oxd-select-dropdown")
        self.INCLUDE_OPTIONS = (By.CLASS_NAME, "oxd-select-dropdown")
        self.JOB_TITLE_OPTIONS = (By.CLASS_NAME, "oxd-select-dropdown")
        self.SUB_UNIT_OPTIONS = (By.CLASS_NAME, "oxd-select-dropdown")
        self.JOB_TITLE_OPTIONS = {
            "Account Assistant": (By.XPATH, "//div[@role='option']/span[text()='Account Assistant']"),
            "Chief Executive Officer": (By.XPATH, "//div[@role='option']/span[text()='Chief Executive Officer']"),
            "Chief Financial Officer": (By.XPATH, "//div[@role='option']/span[text()='Chief Financial Officer']"),
            "Content Specialist": (By.XPATH, "//div[@role='option']/span[text()='Content Specialist']"),
            "HR Manager": (By.XPATH, "//div[@role='option']/span[text()='HR Manager']"),
            "IT Manager": (By.XPATH, "//div[@role='option']/span[text()='IT Manager']"),
            "Network Administrator": (By.XPATH, "//div[@role='option']/span[text()='Network Administrator']"),
            "Sales Representative": (By.XPATH, "//div[@role='option']/span[text()='Sales Representative']"),
            "Senior Support Specialist": (By.XPATH, "//div[@role='option']/span[text()='Senior Support Specialist']"),
            "Support Specialist": (By.XPATH, "//div[@role='option']/span[text()='Support Specialist']")}
        self.SUB_UNIT_OPTIONS = {
            "Administration": (By.XPATH, "//div[@role='option']/span[text()='Administration']"),
            "Client Services": (By.XPATH, "//div[@role='option']/span[text()='Client Services']"),
            "Engineering": (By.XPATH, "//div[@role='option']/span[text()='Engineering']"),
            "Finance": (By.XPATH, "//div[@role='option']/span[text()='Finance']"),
            "Human Resources": (By.XPATH, "//div[@role='option']/span[text()='Human Resources']"),
            "Sales & Marketing": (By.XPATH, "//div[@role='option']/span[text()='Sales & Marketing']"),
            "Technical Support": (By.XPATH, "//div[@role='option']/span[text()='Technical Support']")}

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.PIM_TITLE.should_be_visible()
        self.USER_DROPDOWN.should_be_visible()
        self.MENU_ADMIN.should_be_visible()
        self.SEARCH_FIELD.should_be_visible()

        self.PIM_TITLE.should_be_has_text("PIM")