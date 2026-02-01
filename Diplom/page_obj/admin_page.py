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
        self.PAGE_TITLE = BaseElement(driver, (By.CLASS_NAME, "oxd-table-filter-header-title"))
        # Личное меню
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
        # Основное меню
        self.SIDEBAR = BaseElement(driver, (By.CLASS_NAME, "oxd-main-menu-button"))
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
        # Фильтры поиска
        self.MAIN_FILTER = BaseElement(driver, (By.XPATH, "(//button[@type='button'][4]"))
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
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(
            driver, (By.CSS_SELECTOR, "button[type='submit']")
        )
        self.RESET_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'][5]"))
        self.ADD_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[6]")
        )
        # Действия с найденными карточками
        self.DEL_FIRST = BaseElement(driver, (By.XPATH, "(//button[@type='button'][7]"))
        self.REDACT_FIRST = BaseElement(driver, (By.XPATH, "(//button[@type='button'][8]"))
        self.DEL_SECOND = BaseElement(driver, (By.XPATH, "(//button[@type='button'][9]"))
        self.REDACT_SECOND = BaseElement(driver, (By.XPATH, "(//button[@type='button'][10]"))
        # Чекбоксы
        self.GENERAL_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])"))
        self.FIRST_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])[2]"))
        self.SECOND_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])[3]"))
        # Счетчик выбранных элементов
        self.COUNT = BaseElement(driver, (By.XPATH, "(//span[@class='oxd-text oxd-text--span'])[13]"))
        # Удаление выбранных элементов
        self.DELETE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--label-danger'])"))
        self.CANCEL = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--ghost'])[2]"))
        self.CONFIRMATION = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--label-danger'])[2]"))
        self.JOB = BaseElement(driver, (By.XPATH, "//span[text()='Job']"))
        self.USER_MANAGEMENT = BaseElement(driver, (By.XPATH, "//span[contains(text(), 'User Management')]"))
        self.ORGANIZATION = BaseElement(driver, (By.XPATH, "//span[text()='Organization ']"))
        self.QUALIFICATIONS = BaseElement(driver, (By.XPATH, "//span[text()='Qualifications ']"))
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))


    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.ADMIN_TITLE.should_be_visible()
        self.MAIN_FILTER.should_be_visible()
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
        self.GENERAL_CHECK.should_be_visible()
        self.FIRST_CHECK.should_be_visible()
        self.DEL_FIRST.should_be_visible()
        self.REDACT_FIRST.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.ADMIN_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_be_has_text("System Users")

