import pytest


from Diplom.page_obj.admin_page import AdminPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.secondary_pages.admin_add_user import AdminAddPage
from Diplom.urls import URLS


@pytest.fixture(scope="module")
def admin_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return AdminPage(driver)

@pytest.fixture()
def admin_add_page(driver):
    return AdminAddPage(driver)


def test_admin_page(admin_page, driver):
    admin_page.MENU_ADMIN.click()
    admin_page.check_that_page_opened()
    assert admin_page.driver.current_url == URLS.ADMIN




@pytest.mark.parametrize(
    "length",
    [5, 40]
)
def test_input_fields_valid_lengths(admin_page, admin_add_page, length):
    admin_page.MENU_ADMIN.click()
    admin_page.ADD_BUTTON.click()
    admin_add_page.INPUT_USERNAME.fill("x" * length)
    admin_add_page.INPUT_USERNAME.click()
    admin_add_page.USERNAME_ERROR.should_be_not_visible()

@pytest.mark.parametrize(
    "length,expected",
    [
        (4, "Should be at least 5 characters"),
        (41, "Should not exceed 40 characters"),
    ],
)
def test_input_fields_invalid_lengths(admin_page, admin_add_page, expected, length):
    admin_page.MENU_ADMIN.click()
    admin_page.ADD_BUTTON.click()
    admin_add_page.INPUT_USERNAME.fill("x" * length)
    admin_add_page.INPUT_USERNAME.click()
    admin_add_page.check_that_username_error_is_visible(expected)



