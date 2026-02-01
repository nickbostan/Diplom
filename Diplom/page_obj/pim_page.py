from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class PIMPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-text oxd-text--h5 oxd-table-filter-title")
        )
        self.MENU_PIM = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/pim/viewPimModule')]"))
        self.MAIN_FILTER = BaseElement(driver, (By.XPATH, "(//button[@type='button'][4]"))
        self.EMPLOYEE_NAME = BaseElement(driver, (By.XPATH, "(//input[@placeholder='Type for hints...'])"))
        self.EMPLOYEE_ID = BaseElement(driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]"))
        self.STATUS = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[1]"))
        self.INCLUDE = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[2]"))
        self.JOB_TITLE = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[3]"))
        self.SUB_UNIT = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[4]"))
        self.SUPERVISOR_NAME = BaseElement(driver, (By.XPATH, "(//input[@placeholder='Type for hints...'])[2]"))
        # Кнопки
        self.RESET_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='reset']"))
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.ADD_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'][5]"))
        # Действия с найденными карточками
        self.DEL_FIRST = BaseElement(driver, (By.XPATH, "(//button[@type='button'][6]"))
        self.REDACT_FIRST = BaseElement(driver, (By.XPATH, "(//button[@type='button'][7]"))
        self.DEL_SECOND = BaseElement(driver, (By.XPATH, "(//button[@type='button'][8]"))
        self.REDACT_SECOND = BaseElement(driver, (By.XPATH, "(//button[@type='button'][9]"))
        # Чекбоксы
        self.GENERAL_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])"))
        self.FIRST_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])[2]"))
        self.SECOND_CHECK = BaseElement(driver, (By.XPATH, "(//span[@class='--label-right'])[3]"))
        # Счетчик выбранных элемнетов
        self.COUNT = BaseElement(driver, (By.XPATH, "(//span[@class='oxd-text oxd-text--span'])[13]"))
        # Удаление выбранных элементов
        self.DELETE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--label-danger'])"))
        self.CANCEL = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--ghost'])[2]"))
        self.CONFIRMATION = BaseElement(driver, (By.XPATH, "(//button[@class='oxd-button--label-danger'])[2]"))
        # Сортировка таблицы
        self.SORT_ID = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])"))
        self.SORT_FIRST_NAME = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[2]"))
        self.SORT_LAST_NAME = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[3]"))
        self.SORT_JOB_TITLE = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[4]"))
        self.SORT_STATUS = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[5]"))
        self.SORT_SUB_UNIT = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[6]"))
        self.SORT_SUPERVISOR = BaseElement(driver, (By.XPATH, "(//i[@class='oxd-table-header-sort-icon'])[7]"))
        # Тип сортировки
        self.SORT_BY_ASCENDING = BaseElement(driver, (By.XPATH, "//span[@text()='Ascending']"))
        self.SORT_BY_DESCENDING = BaseElement(driver, (By.XPATH, "//span[@text()='Descending']"))
        # Сообщение об успешном выполнении
        self.SUCCESS = BaseElement(driver, (By.CSS_SELECTOR, ".oxd-toast.oxd-toast--success"))






    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.EMPLOYEE_NAME.should_be_visible()
        self.MAIN_FILTER.should_be_visible()
        self.EMPLOYEE_ID.should_be_visible()
        self.STATUS.should_be_visible()
        self.INCLUDE.should_be_visible()
        self.SUPERVISOR_NAME.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.ADD_BUTTON.should_be_visible()
        self.COUNT.should_be_visible()
        self.DEL_FIRST.should_be_visible()
        self.REDACT_FIRST.should_be_visible()
        self.GENERAL_CHECK.should_be_visible()
        self.SORT_SUPERVISOR.should_be_visible()
        self.SORT_FIRST_NAME.should_be_visible()
        self.SORT_BY_ASCENDING.should_be_not_visible()
        self.DELETE_BUTTON.should_be_not_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("PIM")
        self.PAGE_TITLE.should_be_has_text("Employee Information")
