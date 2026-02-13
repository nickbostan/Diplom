import pytest

from Diplom.page_obj.admin_block.add_job_title import AddJobTitlePage
from Diplom.page_obj.admin_block.job_title import JobTitlePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def job_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return JobTitlePage(driver)


@pytest.fixture()
def job_add_page(driver):
    return AddJobTitlePage(driver)


@pytest.mark.smoke
def test_job_page(job_page, driver):
    job_page.MENU_ADMIN.click()
    job_page.ADMIN_JOB.click()
    job_page.ADMIN_JOB_TITLES.click()
    job_page.check_that_page_opened()
    assert job_page.driver.current_url == URLS.JOB_TITLE
