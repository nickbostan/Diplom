import pytest

from Diplom.page_obj.pim_page import PIMPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def pim_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PIMPage(driver)



def test_pim_page(pim_page, driver):
    pim_page.MENU_PIM.click()
    pim_page.check_that_page_opened()
    assert pim_page.driver.current_url == URLS.PIM