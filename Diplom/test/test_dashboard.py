import pytest

from Diplom.page_obj.dashboard_page import DashboardPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture()
def dashboard_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return DashboardPage(driver)


def test_dashboard_page(dashboard_page, driver):
    dashboard_page.check_that_page_opened()
    assert dashboard_page.driver.current_url == URLS.DASHBOARD


def test_config(dashboard_page):
    dashboard_page.CONFIG_EMPL_LEAVE.click()
    dashboard_page.SHOW_BUTTON.click()
    dashboard_page.SAVE_BUTTON.click()
    dashboard_page.CONFIG_EMPL_LEAVE.click()
    assert not dashboard_page.SHOW_BUTTON.is_checked()
    dashboard_page.CANCEL_BUTTON.click()
