from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class RecruitmentPage(BasePage):

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
        #Checkbox
        self.GENERAL_CHECKBOX = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[1]"))
        self.FIRST_CAND = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[2]"))
        self.SECOND_CAND = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[3]"))







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

    # def select_job(self, job):
       # self.select_from_dropdown(self.JOB_TITLE_DROPDOWN, job)

    # def select_status(self, status):
       # self.select_from_dropdown(self.STATUS_DROPDOWN, status)

    #def select_from_dropdown_general(self, dropdown_locator, option_text):
        #dropdown = get_element(dropdown_locator)
        #dropdown.click()

       # option = get_element(
          #  (By.XPATH, f"//div[contains(@class, 'oxd-select-text-input') and contains(text()='{option_text}')]")
       # )
       # option.click()
