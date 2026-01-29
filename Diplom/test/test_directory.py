import pytest

from Diplom.page_obj.directory_page import DirectoryPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def directory_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return DirectoryPage(driver)



def test_directory_page(directory_page, driver):
    directory_page.MENU_DIRECTORY.click()
    directory_page.check_that_page_opened()
    assert directory_page.driver.current_url == URLS.DIRECTORY