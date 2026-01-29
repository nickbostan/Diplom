import pytest

from Diplom.page_obj.buzz_page import BuzzPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def buzz_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return BuzzPage(driver)



def test_buzz_page(buzz_page, driver):
    buzz_page.MENU_BUZZ.click()
    buzz_page.check_that_page_opened()
    assert buzz_page.driver.current_url == URLS.BUZZ