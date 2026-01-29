import pytest

from Diplom.page_obj.performance_page import PerformancePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def performance_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PerformancePage(driver)



def test_performance_page(performance_page, driver):
    performance_page.MENU_PERFORMANCE.click()
    performance_page.check_that_page_opened()
    assert performance_page.driver.current_url == URLS.PERFORMANCE