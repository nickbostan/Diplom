import random

from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage

index_vacancy = random.randint(2, 7)


class CandidateAddPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver, (By.CLASS_NAME, "orangehrm-main-title"))
        self.MENU_RECRUITMENT = BaseElement(
            driver, (By.XPATH, "//span[text()='Recruitment']")
        )
        #Поля заполнения
        self.FIRST_NAME = BaseElement(driver, (By.NAME, "firstName"))
        self.MIDDLE_NAME = BaseElement(driver, (By.NAME, "middleName"))
        self.LAST_NAME = BaseElement(driver, (By.NAME, "lastName"))
        self.VACANCY_DROPDOWN = BaseElement(driver, (By.XPATH, "//div[@class='oxd-select-text oxd-select-text--active']"))
        self.RANDOM_VACANCY = BaseElement(driver, (By.XPATH, f"(//div[@class='oxd-select-option'])[{index_vacancy}]"))
        self.EMAIL = BaseElement(driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[2]"))
        self.CONTACT_NUMBER = BaseElement(driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[3]"))
        self.RESUME = BaseElement(driver, (By.XPATH, "//input[@type='file']"))
        self.KEYWORDS = BaseElement(driver, (By.XPATH, "(//input[@placeholder='Enter comma seperated words...'])"))
        self.DATE_OF_APPLICATION = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])"))
        self.NOTES = BaseElement(driver, (By.CLASS_NAME, "oxd-textarea"))
        # Кнопки
        self.KEEP_DATA_CHECKBOX = BaseElement(driver, (By.CLASS_NAME, "--label-right"))
        self.SAVE_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.CANCEL_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        # Ошибка
        self.ERROR = BaseElement(driver, (By.CLASS_NAME, "oxd-input-field-error-message"))




    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.MIDDLE_NAME.should_be_visible()
        self.FIRST_NAME.should_be_visible()
        self.LAST_NAME.should_be_visible()
        self.EMAIL.should_be_visible()
        self.KEYWORDS.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.CONTACT_NUMBER.should_be_visible()
        self.CANCEL_BUTTON.should_be_visible()
        self.NOTES.should_be_visible()
        self.VACANCY_DROPDOWN.should_be_visible()
        self.KEEP_DATA_CHECKBOX.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Recruitment")
        self.PAGE_TITLE.should_be_has_text("Add Candidate")


    def add_candidate(self, email, first_name, middle_name, last_name, number, kwords, notes, date):
        self.FIRST_NAME.fill(first_name)
        self.MIDDLE_NAME.fill(middle_name)
        self.LAST_NAME.fill(last_name)
        self.VACANCY_DROPDOWN.click()
        self.RANDOM_VACANCY.click()
        self.CONTACT_NUMBER.fill(number)
        self.KEEP_DATA_CHECKBOX.click()
        self.DATE_OF_APPLICATION.fill(date)
        self.KEYWORDS.fill(kwords)
        self.NOTES.fill(notes)
        self.EMAIL.fill(email)
        return self


    def check_that_error_is_visible(self, text):
        self.ERROR.should_be_visible()
        self.ERROR.should_contain_text(text)
        return self
