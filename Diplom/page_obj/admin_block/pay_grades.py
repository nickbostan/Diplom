from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class PayGradesPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-level")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-header-container")
        )
        self.JOB_DROPDOWN = BaseElement(driver, (By.XPATH, "//span[text()='Job ']"))
        self.MENU_ADMIN = BaseElement(
            driver, (By.XPATH, "//a[contains(@href, '/admin/viewAdminModule')]")
        )
        self.PAY_GRADES = BaseElement(driver, (By.XPATH, "//a[text()='Pay Grades']"))
        # Кнопки
        self.ADD_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[4]")
        )
        self.DELETE_FIRST = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[5]")
        )
        self.REDACT_FIRST = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[6]")
        )
        self.DELETE_SECOND = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[7]")
        )
        self.REDACT_SECOND = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[8]")
        )
        # Действия в всплывающем окне удаления
        self.NO_CANCEL = BaseElement(
            driver,
            (
                By.XPATH,
                "//button[@type='button' and contains(@class, 'orangehrm-button-margin')]",
            ),
        )
        self.YES_DELETE = BaseElement(
            driver,
            (
                By.XPATH,
                "//button[@type='button' and contains(@class, 'oxd-button--label-danger')]",
            ),
        )

    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.DELETE_FIRST.should_be_visible()
        self.REDACT_FIRST.should_be_visible()
        self.DELETE_SECOND.should_be_visible()
        self.REDACT_SECOND.should_be_visible()
        self.ADD_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Job")
        self.PAGE_TITLE.should_contain_text("Pay Grades")
