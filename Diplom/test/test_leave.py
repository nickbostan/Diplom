import pytest

from Diplom.page_obj.leave_page import LeavePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def leave_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return LeavePage(driver)



def test_leave_page(leave_page, driver):
    leave_page.MENU_LEAVE.click()
    leave_page.check_that_page_opened()
    assert leave_page.driver.current_url == URLS.LEAVE