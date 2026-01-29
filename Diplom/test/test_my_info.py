import pytest

from Diplom.page_obj.my_info_page import MyInfoPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def my_info_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return MyInfoPage(driver)



def test_my_info_page(my_info_page, driver):
    my_info_page.MENU_MY_INFO.click()
    my_info_page.check_that_page_opened()
    assert my_info_page.driver.current_url == URLS.MYINFO