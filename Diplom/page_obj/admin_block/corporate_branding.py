from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage



class CorpBrandingPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb"))
        self.PAGE_TITLE = BaseElement(driver,(By.CLASS_NAME, "orangehrm-main-title"))
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//span[text()='Admin']"))
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))
        self.CORP_BRANDING = BaseElement(driver, (By.XPATH, "//a[text()='Corporate Branding ']"))
        self.PRIMARY_COLOR = BaseElement(driver,(By.CSS_SELECTOR, ".oxd-color-input-preview"))
        self.SECONDARY_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[2]"))
        self.PRIMARY_FONT_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[3]"))
        self.SECONDARY_FONT_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[4]"))
        self.PRIMARY_GRADIENT_COLOR1 = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[5]"))
        self.PRIMARY_GRADIENT_COLOR2 = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[6]"))
        self.HEX_INPUT = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-input oxd-input--active'])[2]"))
        # Добавление файлов
        self.CLIENT_LOGO = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-file-button'])"))
        self.CLIENT_BANNER = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-file-button'])[2]"))
        self.LOGIN_BANNER = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-file-button'])[3]"))
        # Кнопки
        self.PUBLISH_BUTTON = BaseElement(driver,(By.CSS_SELECTOR, "button[type='submit']"))
        self.RESET_TO_DEFAULT = BaseElement(driver,(By.XPATH, "(//button[@type='button'])[4]"))
        self.PREVIEW = BaseElement(driver,(By.XPATH, "(//button[@type='button'])[5]"))
        self.SOCIAL_MEDIA_CHECKBOX = BaseElement(driver,(By.CLASS_NAME, "oxd-switch-input"))

        # Сообщение об ошибке
        self.CLIENT_LOGO_ERROR = BaseElement(driver,(By.XPATH, "(//span[@class='oxd-input-field-error-message'])"))
        self.CLIENT_BANNER_ERROR = BaseElement(driver,(By.XPATH, "(//span[@class='oxd-input-field-error-message'])[2]"))
        self.LOGIN_BANNER_ERROR = BaseElement(driver,(By.XPATH, "(//span[@class='oxd-input-field-error-message'])[3]"))




    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.PRIMARY_COLOR.should_be_visible()
        self.SECONDARY_COLOR.should_be_visible()
        self.PRIMARY_FONT_COLOR.should_be_visible()
        self.SECONDARY_FONT_COLOR.should_be_visible()
        self.MENU_ADMIN.should_be_visible()
        self.PRIMARY_GRADIENT_COLOR1.should_be_visible()
        self.PRIMARY_GRADIENT_COLOR2.should_be_visible()
        self.CLIENT_LOGO.should_be_visible()
        self.CLIENT_BANNER.should_be_visible()
        self.LOGIN_BANNER.should_be_visible()
        self.PUBLISH_BUTTON.should_be_visible()
        self.RESET_TO_DEFAULT.should_be_visible()
        self.PREVIEW.should_be_visible()
        self.SOCIAL_MEDIA_CHECKBOX.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Admin")
        self.PAGE_TITLE.should_be_has_text("Corporate Branding")

        def set_color_by_index(self, driver, r, g, b, index=0):
            """
            Простая установка цвета для пикера по индексу
            """
            js = """
            var pickers = document.querySelectorAll('.oxd-color-input-preview');
            if (pickers[%s]) {
                pickers[%s].style.backgroundColor = 'rgb(%s, %s, %s)';
                return true;
            }
            return false;
            """ % (index, index, r, g, b)

            return driver.execute_script(js)
