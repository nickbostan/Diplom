
from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class LocalizationPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-level")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title")
        )
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/admin/viewAdminModule')]"))
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))
        self.CONFIGURATION = BaseElement(driver, (By.XPATH,"//a[contains(text(), 'Configuration')]"))
        self.LOCALIZATION = BaseElement(driver, (By.XPATH,"//a[contains(text(), 'Localization')]"))
        self.LANGUAGE = BaseElement(driver, (By.XPATH, "//div[@class='oxd-select-text oxd-select-text--active']"))
        self.DATE_FORMAT = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        # Кнопки
        self.SAVE_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))


    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.LANGUAGE.should_be_visible()
        self.DATE_FORMAT.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Configuration")
        self.PAGE_TITLE.should_be_has_text("Localization")
