from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class BuzzPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.BUZZ_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-module"))
        self.PAGE_TITLE = BaseElement(driver,(By.CLASS_NAME, "orangehrm-buzz-newsfeed-title"))
        self.ANNIVERSARIES = BaseElement(driver, (By.CLASS_NAME, "orangehrm-buzz-anniversary-title"))
        self.MENU_BUZZ = BaseElement(driver, (By.XPATH, "//span[text()='Buzz']"))
        self.POST_WRITE_FIELD = BaseElement(driver, (By.CSS_SELECTOR, "textarea[placeholder='What\\'s on your mind?']"))
        self.POST_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))
        self.SHARE_PHOTOS = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[4]"))
        self.SHARE_VIDEO = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[5]"))
        # Фильтры сообщений ленты
        self.MOST_RECENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[6]"))
        self.MOST_LIKED = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[7]"))
        self.MOST_COMMENTED = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[8]"))
        # Активность с первым постом
        self.TO_DO = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[9]"))
        self.COMMENT = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[10]"))
        self.SHARE = BaseElement(driver, (By.XPATH, "(//button[@type='button'])[11]"))
        self.LIKE = BaseElement(driver, (By.ID, "heart"))
        self.COUNT_LIKES = BaseElement(driver, (By.XPATH, "(//p[@class='oxd-text oxd-text--p'])[6]"))
        self.COUNT_COMMENTS = BaseElement(driver, (By.XPATH, "(//p[@class='oxd-text oxd-text--p'])[7]"))
        self.COUNT_SHARES = BaseElement(driver, (By.XPATH, "(//p[@class='oxd-text oxd-text--p'])[8]"))


    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.BUZZ_TITLE.should_be_visible()
        self.POST_WRITE_FIELD.should_be_visible()
        self.MOST_RECENT.should_be_visible()
        self.MOST_LIKED.should_be_visible()
        self.MOST_COMMENTED.should_be_visible()
        self.MENU_BUZZ.should_be_visible()
        self.POST_BUTTON.should_be_visible()
        self.COUNT_LIKES.should_be_visible()
        self.PAGE_TITLE.should_be_visible()
        self.SHARE_PHOTOS.should_be_visible()

        self.BUZZ_TITLE.should_be_has_text("Buzz")
        self.PAGE_TITLE.should_be_has_text("Buzz Newsfeed")