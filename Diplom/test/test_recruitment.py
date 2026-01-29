import pytest

from Diplom.page_obj.recruitment_page import RecruitmentPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def recruitment_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return RecruitmentPage(driver)



def test_recruitment_page(recruitment_page, driver):
    recruitment_page.MENU_RECRUITMENT.click()
    recruitment_page.check_that_page_opened()
    assert recruitment_page.driver.current_url == URLS.RECRUITMENT

