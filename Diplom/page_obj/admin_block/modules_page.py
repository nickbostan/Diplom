
from selenium.webdriver.common.by import By

from Diplom.core.base_element import BaseElement
from Diplom.core.base_page import BasePage


class ModulesPage(BasePage, BaseElement):

    def __init__(self, driver):
        super().__init__(driver)
        self.LOGO = BaseElement(driver, (By.CLASS_NAME, "oxd-brand-banner"))
        self.MAIN_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "oxd-topbar-header-breadcrumb-level")
        )
        self.PAGE_TITLE = BaseElement(
            driver, (By.CLASS_NAME, "orangehrm-main-title")
        )
        self.MORE = BaseElement(driver, (By.XPATH, "//span[text()='More ']"))
        self.CONFIGURATION = BaseElement(driver, (By.XPATH, "//a[contains(text(), 'Configuration ')]"))
        self.MODULES = BaseElement(driver, (By.XPATH, "//a[contains(text(), 'Modules')]"))
        # Модули меню
        self.MENU_ADMIN = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/admin/viewAdminModule')]"))
        self.MENU_PIM = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/pim/viewPimModule')]"))
        self.MENU_LEAVE = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/leave/viewLeaveModule')]"))
        self.MENU_TIME = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/time/viewTimeModule')]"))
        self.MENU_RECRUITMENT = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/recruitment/viewRecruitmentModule')]"))
        self.MENU_MY_INFO = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/pim/viewMyDetails')]"))
        self.MENU_PERFORMANCE = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/performance/viewPerformanceModule')]"))
        self.MENU_DASHBOARD = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/dashboard/index')]"))
        self.MENU_DIRECTORY = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/directory/viewDirectory')]"))
        self.MENU_MAINTENANCE = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/maintenance/viewMaintenanceModule')]"))
        self.MENU_CLAIM = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/claim/viewClaimModule')]"))
        self.MENU_BUZZ = BaseElement(driver, (By.XPATH, "//a[contains(@href, '/buzz/viewBuzz')]"))
        # Чекбоксы отображения
        self.ADMIN_CHECK = BaseElement(driver, (By.XPATH, "//span[contains(@class, '--label-right')]"))
        self.PIM_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[2]"))
        self.LEAVE_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[3]"))
        self.TIME_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[4]"))
        self.RECRUITMENT_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[5]"))
        self.PERFORMANCE_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[6]"))
        self.DIRECTORY_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[7]"))
        self.MAINTENANCE_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[8]"))
        self.MOBILE_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[9]"))
        self.CLAIM_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[10]"))
        self.BUZZ_CHECK = BaseElement(driver, (By.XPATH, "(//span[contains(@class, '--label-right')])[11]"))
        # Кнопки
        self.SAVE_BUTTON = BaseElement(driver, (By.CSS_SELECTOR, "button[type='submit']"))



    def check_that_page_opened(self):
        self.LOGO.should_be_visible()
        self.MAIN_TITLE.should_be_visible()
        self.ADMIN_CHECK.is_displayed()
        self.PIM_CHECK.is_displayed()
        self.LEAVE_CHECK.should_be_visible()
        self.TIME_CHECK.should_be_visible()
        self.RECRUITMENT_CHECK.should_be_visible()
        self.PERFORMANCE_CHECK.should_be_visible()
        self.DIRECTORY_CHECK.should_be_visible()
        self.MAINTENANCE_CHECK.should_be_visible()
        self.CLAIM_CHECK.should_be_visible()
        self.BUZZ_CHECK.should_be_visible()
        self.SAVE_BUTTON.should_be_visible()
        self.PAGE_TITLE.should_be_visible()

        self.MAIN_TITLE.should_be_has_text("Configuration")
        self.PAGE_TITLE.should_be_has_text("Module Configuration")


    def all_modules_switch(self):
        self.CLAIM_CHECK.click()
        self.BUZZ_CHECK.click()
        self.LEAVE_CHECK.click()
        self.TIME_CHECK.click()
        self.RECRUITMENT_CHECK.click()
        self.PERFORMANCE_CHECK.click()
        self.DIRECTORY_CHECK.click()
        self.MAINTENANCE_CHECK.click()
        self.MOBILE_CHECK.click()

    def check_modules_off(self):
        self.MENU_LEAVE.should_be_not_visible()
        self.MENU_TIME.should_be_not_visible()
        self.MENU_BUZZ.should_be_not_visible()
        self.MENU_CLAIM.should_be_not_visible()
        self.MENU_RECRUITMENT.should_be_not_visible()
        self.MENU_PERFORMANCE.should_be_not_visible()
        self.MENU_DIRECTORY.should_be_not_visible()
        self.MENU_MAINTENANCE.should_be_not_visible()

