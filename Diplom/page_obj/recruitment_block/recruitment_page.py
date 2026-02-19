import random
import re

from selenium.webdriver.common.by import By
from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


index_vacancy = random.randint(2, 7)
index_job = random.randint(2, 18)

class RecruitmentPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.RECRUITMENT_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver, (By.CLASS_NAME, "oxd-table-filter-header-title"))
        self.MENU_RECRUITMENT = BaseElement(
            driver, (By.XPATH, "//span[text()='Recruitment']")
        )
        self.RECRUITMENT_LIST_FILTER_PANEL = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        #Поля фильтрации
        self.JOB_TITLE_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[1]"))
        self.VACANCY_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[2]"))
        self.HIRING_MANAGER_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[3]"))
        self.STATUS_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text oxd-select-text--active'])[4]"))
        self.METHOD_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-text-input'])[5]"))
        self.CANDIDATE_NAME = BaseElement(driver, (By.CSS_SELECTOR, "input[placeholder='Type for hints...']"))
        self.KEYWORDS = BaseElement(driver, (By.XPATH, "(//input[@placeholder='Enter comma seperated words...'])"))
        self.FROM_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='From'])"))
        self.TO_DATE = BaseElement(driver, (By.XPATH, "(//input[@placeholder='To'])"))
        self.RANDOM_VACANCY = BaseElement(driver, (By.XPATH, f"(//div[@class='oxd-select-option'])[{index_vacancy}]"))
        self.RANDOM_JOB = BaseElement(driver, (By.XPATH, f"(//div[@class='oxd-select-option'])[{index_job}]"))
        self.FIRST_OPTION_DROPDOWN = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-select-option'])[2]"))
        self.FIRST_FOUND_CANDIDATE = BaseElement(driver, (By.XPATH, "//div[@class='oxd-autocomplete-option']"))
        # Кнопки
        self.SEARCH_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='reset']"))
        self.ADD_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[5]"))
        self.VIEW_FIRST_CAND = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[6]"))
        self.DEL_FIRST_CAND = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[7]"))
        self.VIEW_SECOND_CAND = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[8]"))
        self.DEL_SECOND_CAND = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[9]"))
        self.DOWNLOAD_RESUME_SECOND_CAND = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[10]"))
        self.DELETE_SELECTED = BaseElement(
            driver, (By.CLASS_NAME, "oxd-button--label-danger"))
        # Checkbox
        self.GENERAL_CHECKBOX = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[1]"))
        self.FIRST_CAND = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[2]"))
        self.SECOND_CAND = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[3]"))
        # Счетчик
        self.COUNT = BaseElement(driver, (By.XPATH,
                                          "(//span[contains(@class, 'oxd-text--span')])[13]"))
        # Ошибка
        self.ERROR = BaseElement(driver, (By.CLASS_NAME, "oxd-input-field-error-message"))







    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.RECRUITMENT_TITLE.should_be_visible()
        self.STATUS_DROPDOWN.should_be_visible()
        self.CANDIDATE_NAME.should_be_visible()
        self.DEL_FIRST_CAND.should_be_visible()
        self.HIRING_MANAGER_DROPDOWN.should_be_visible()
        self.MENU_RECRUITMENT.should_be_visible()
        self.SEARCH_BUTTON.should_be_visible()
        self.ADD_BUTTON.should_be_visible()
        self.RESET_BUTTON.should_be_visible()
        self.FIRST_CAND.should_be_visible()
        self.GENERAL_CHECKBOX.should_be_visible()
        self.FROM_DATE.should_be_visible()
        self.VIEW_SECOND_CAND.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.RECRUITMENT_TITLE.should_be_has_text("Recruitment")
        self.PAGE_TITLE.should_be_has_text("Candidates")



    def input_search(self):

        self.KEYWORDS.fill("bla bla")
        self.FROM_DATE.fill("2016-02-05")
        self.TO_DATE.fill("2025-25-08")
        self.JOB_TITLE_DROPDOWN.click()
        self.RANDOM_JOB.click()
        self.VACANCY_DROPDOWN.click()
        self.RANDOM_VACANCY.click()
        self.METHOD_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        self.HIRING_MANAGER_DROPDOWN.click()
        self.FIRST_OPTION_DROPDOWN.click()
        return self


    def get_records_count(self):
        text = self.COUNT.get_text()
        match = re.search(r'\((\d+)\)', text)
        return int(match.group(1)) if match else 0


    def check_that_error_is_visible(self, text):
        self.ERROR.should_be_visible()
        self.ERROR.should_contain_text(text)
        return self