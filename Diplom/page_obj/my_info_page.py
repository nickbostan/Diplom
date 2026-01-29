from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class MyInfoPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MY_INFO_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title")
        )
        self.MENU_MY_INFO = BaseElement(driver, (By.XPATH, "//span[text()='My Info']"))
        #Вкладки
        self.PERSONAL_DETAILS = BaseElement(driver, (By.XPATH, "//a[text()='Personal Details']"))
        self.CONTACT_DETAILS = BaseElement(driver, (By.XPATH, "//a[text()='Contact Details']"))
        self.EMERGENCY_CONTACTS = BaseElement(driver, (By.XPATH, "//a[text()='Emergency Contacts']"))
        self.DEPENDENTS = BaseElement(driver, (By.XPATH, "//a[text()='Dependents']"))
        self.IMMIGRATION = BaseElement(driver, (By.XPATH, "//a[text()='Immigration']"))
        self.JOB = BaseElement(driver, (By.XPATH, "//a[text()='Job']"))
        self.SALARY = BaseElement(driver, (By.XPATH, "//a[text()='Salary']"))
        self.REPORT_TO = BaseElement(driver, (By.XPATH, "//a[text()='Report-to']"))
        self.QUALIFICATIONS = BaseElement(driver, (By.XPATH, "//a[text()='Qualifications']"))
        self.MEMBERSHIPS = BaseElement(driver, (By.XPATH, "//a[text()='Memberships']"))
        #Личная информация
        self.FIRST_NAME = BaseElement(driver, (By.NAME, "firstName"))
        self.MIDDLE_NAME = BaseElement(driver, (By.NAME, "middleName"))
        self.LAST_NAME = BaseElement(driver, (By.NAME, "lastName"))
        self.NICKNAME = BaseElement(driver, (By.XPATH, "(//input[@class='oxd-input oxd-input--active'])[5]"))
        self.ID = BaseElement(
            driver, (By.XPATH, "(//input[contains(@class,'oxd-input--active')])[5]"))
        self.OTHER_ID = BaseElement(
            driver, (By.XPATH, "(//input[contains(@class,'oxd-input--active')])[6]"))
        self.DRIVER_LICENSE = BaseElement(
            driver, (By.XPATH, "(//input[contains(@class,'oxd-input--active')])[7]"))
        self.LICENSE_EXPIRE = BaseElement(driver, (By.CSS_SELECTOR, "input[placeholder='yyyy-dd-mm']"))
        self.SIN_NUMBER = BaseElement(
            driver, (By.XPATH, "(//input[contains(@class,'oxd-input--active')])[9]"))
        self.NATIONALITY = BaseElement(driver, (By.CLASS_NAME, "oxd-select-text-input"))
        self.MARITAL_STATUS = BaseElement(driver, (By.XPATH, "(//input[@class='oxd-select-text-input'])[2]"))
        self.DATE_OF_BIRTH = BaseElement(driver, (By.XPATH, "(//input[@placeholder='yyyy-dd-mm'])[2]"))
        self.MALE = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'oxd-radio-input')])[1]"))
        self.FEMALE = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'oxd-radio-input')])[2]"))
        # Кнопки
        self.SAVE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='submit'])[2]"))
        self.ADD_ATTACHMENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        # Если был выбран чекбокс то нумерация следующих кнопок будет 6,7 и 8 соответственно
        self.REDACTION_ATTACHMENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[5]"))
        self.DELETE_ATTACHMENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[6]"))
        self.UPLOAD_ATTACHMENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[7]"))
        self.HIDDEN_DELETE_BUTTON = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[5]"))
        # Чекбоксы
        self.GENERAL_CHECKBOX = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[3]"))
        self.FIRST_ATTACH = BaseElement(
            driver, (By.XPATH, "(//span[contains(@class,'--label-right')])[4]"))



    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MY_INFO_TITLE.should_be_visible()
        self.MENU_MY_INFO.should_be_visible()
        self.NATIONALITY.should_be_visible()
        self.LICENSE_EXPIRE.should_be_visible()
        self.ID.should_be_visible()
        self.FIRST_NAME.should_be_visible()
        self.CONTACT_DETAILS.should_be_visible()
        self.IMMIGRATION.should_be_visible()
        self.MALE.should_be_visible()
        self.GENERAL_CHECKBOX.should_be_visible()
        self.DATE_OF_BIRTH.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.DRIVER_LICENSE.should_be_visible()

        self.MY_INFO_TITLE.should_be_has_text("Personal Details")