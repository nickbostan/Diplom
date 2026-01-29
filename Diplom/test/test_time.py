import pytest

from Diplom.page_obj.time_page import TimePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def time_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return TimePage(driver)



def test_time_page(time_page, driver):
    time_page.MENU_TIME.click()
    time_page.check_that_page_opened()
    assert time_page.driver.current_url == URLS.TIME