import pytest

from Diplom.page_obj.maintenance_page import MaintenancePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def maintenance_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return MaintenancePage(driver)



def test_maintenance_page(maintenance_page, driver):
    maintenance_page.MENU_MAINTENANCE.click()
    maintenance_page.PASSWORD.fill("admin123")
    maintenance_page.CONFIRM_BUTTON.click()
    maintenance_page.check_that_page_opened()
    assert maintenance_page.driver.current_url == URLS.MAINTENANCE