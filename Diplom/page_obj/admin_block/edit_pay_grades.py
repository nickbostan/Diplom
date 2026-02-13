from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class EditPayGradePage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-card-container")
        )
        self.NAME = BaseElement(
            driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]")
        )
        self.ERROR_SALARY = BaseElement(
            driver,
            (By.XPATH, "(//span[contains(@class, 'oxd-input-field-error-message')])"),
        )
        self.CURRENCY = BaseElement(
            driver,
            (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])"),
        )
        self.A_CURRENCY = BaseElement(driver, (By.XPATH, "(//div[@role='option'])[3]"))
        self.CURRENCY_BHD = BaseElement(
            driver,
            (By.XPATH, "//div[@role='option']/span[contains(., 'Bahraini Dinar')]"),
        )
        self.MINIMUM_SALARY = BaseElement(
            driver, (By.XPATH, "//label[contains(text(), 'Minimum')]/following::input")
        )
        self.MAXIMUM_SALARY = BaseElement(
            driver, (By.XPATH, "//label[contains(text(), 'Maximum')]/following::input")
        )
        # Кнопки
        self.CANCEL_BUTTON = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[4]")
        )
        self.SAVE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='submit'])"))
        self.ADD_CURRENCY = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[5]")
        )
        self.CANCEL_CURRENCY = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[5]")
        )
        self.SAVE_CURRENCY = BaseElement(
            driver, (By.XPATH, "(//button[@type='submit'])[2]")
        )
        self.DELETE_CURRENCY = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[6]")
        )
        self.REDACT_CURRENCY = BaseElement(
            driver, (By.XPATH, "(//button[@type='button'])[7]")
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
        self.NAME.should_be_visible()
        self.ERROR_SALARY.should_be_not_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_contain_text("Edit Pay Grade")
