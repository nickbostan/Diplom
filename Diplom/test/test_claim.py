import pytest

from Diplom.page_obj.claim_page import ClaimPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def claim_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return ClaimPage(driver)



def test_claim_page(claim_page, driver):
    claim_page.MENU_CLAIM.click()
    claim_page.check_that_page_opened()
    assert claim_page.driver.current_url == URLS.CLAIM
