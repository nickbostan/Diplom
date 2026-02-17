from selenium.webdriver.common.by import By
from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage
from Diplom.page_obj.admin_block.color_pick import ColorPicker


class CorpBrandingPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.TOP_BAR = BaseElement(driver, (By.CLASS_NAME, "oxd-topbar-header"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb"))
        self.PAGE_TITLE = BaseElement(driver,(By.CLASS_NAME, "orangehrm-main-title"))
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//span[text()='Admin']"))
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))
        self.CORP_BRANDING = BaseElement(driver, (By.XPATH, "//a[text()='Corporate Branding ']"))
        self.PRIMARY_COLOR = BaseElement(driver,(By.XPATH, "//div[@class='oxd-color-input-preview']"))
        self.SECONDARY_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[2]"))
        self.PRIMARY_FONT_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[3]"))
        self.SECONDARY_FONT_COLOR = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[4]"))
        self.PRIMARY_GRADIENT_COLOR1 = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[5]"))
        self.PRIMARY_GRADIENT_COLOR2 = BaseElement(driver,(By.XPATH, "(//div[@class='oxd-color-input-preview'])[6]"))
        self.HEX_INPUT = BaseElement(driver, (By.XPATH, "(//div[@class='oxd-input oxd-input--active'])[2]"))
        self.PICKER_PANEL_LOCATOR = BaseElement(driver, (By.CSS_SELECTOR, "div.oxd-color-picker"))
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
        self.ERROR = BaseElement(driver, (By.CLASS_NAME, "oxd-input-field-error-message"))




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


    def check_that_error_is_visible(self, text):
        self.ERROR.should_be_visible()
        self.ERROR.should_be_has_text(text)
        return self


    @property
    def primary_color_picker(self):
        return ColorPicker(self.driver, self.PRIMARY_COLOR.selector)

    @property
    def secondary_color_picker(self):
        return ColorPicker(self.driver, self.SECONDARY_COLOR.selector)

    @property
    def primary_font_color_picker(self):
        return ColorPicker(self.driver, self.PRIMARY_FONT_COLOR.selector)

    @property
    def secondary_font_color_picker(self):
        return ColorPicker(self.driver, self.SECONDARY_FONT_COLOR.selector)

    @property
    def primary_gradient1_picker(self):
        return ColorPicker(self.driver, self.PRIMARY_GRADIENT_COLOR1.selector)

    @property
    def primary_gradient2_picker(self):
        return ColorPicker(self.driver, self.PRIMARY_GRADIENT_COLOR2.selector)



