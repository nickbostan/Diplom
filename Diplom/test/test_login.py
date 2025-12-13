import pytest
import pytest_check as check

from Diplom.page_obj.dashboard_page import DashboardPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture()
def dashboard_page(driver):
    return DashboardPage(driver)


@pytest.fixture()
def open_page(login_page):
    login_page.open_page()


@pytest.mark.smoke
def test_check_all_elements(login_page, open_page, driver):
    login_page.check_that_page_opened()
    assert login_page.driver.current_url == URLS.LOGIN


@pytest.mark.smoke
def test_positive_login(login_page, dashboard_page, open_page):
    login_page.login("Admin", "admin123")
    dashboard_page.check_that_page_opened()


def test_logout(login_page, dashboard_page, open_page, driver):
    login_page.login("Admin", "admin123")
    dashboard_page.check_that_page_opened()
    check.equal(login_page.driver.current_url, URLS.DASHBOARD)
    dashboard_page.click_logout()
    login_page.check_that_page_opened()
    check.equal(login_page.driver.current_url, URLS.LOGIN)


@pytest.mark.parametrize(
    "user, password, expect",
    [
        ("incorrectUser", "admin123", "Invalid credentials"),
        ("Admin", "incorrectPassword", "Invalid credentials"),
    ],
)
def test_negative_username(login_page, open_page, user, password, expect):
    login_page.login(user, password)
    login_page.check_that_error_is_visible(expect)


@pytest.mark.parametrize(
    "user, password, expect",
    [
        ("", "admin123", "Required"),
        ("Admin", "", "Required"),
    ],
)
def test_negative_empty_fields(login_page, open_page, user, password, expect):
    login_page.login(user, password)
    login_page.check_that_empty_error_is_visible(expect)


@pytest.mark.parametrize(
    "link_element,expected_url",
    [
        ("LINKEDIN_LINK", "linkedin.com"),
        ("FACEBOOK_LINK", "facebook.com"),
        ("TWITTER_LINK", "x.com"),
        ("YOUTUBE_LINK", "youtube.com"),
        ("SITE_LINK", "orangehrm.com"),
    ],
)
def test_social_links(login_page, link_element, expected_url, open_page, driver):
    original_url = driver.current_url
    original_window = driver.current_window_handle
    social_link = getattr(login_page, link_element)
    social_link.click()
    new_url = login_page.switch_to_new_window(expected_windows=2)
    assert expected_url in new_url, f"URL {new_url} not contains {expected_url}"
    driver.close()
    driver.switch_to.window(original_window)
    assert original_url == login_page.driver.current_url


def test_forgot_password_link(login_page, open_page, driver):
    login_page.FORGOT_PASSWORD_LINK.click()
    assert login_page.driver.current_url == URLS.PASSWORD


@pytest.mark.parametrize(
    "length,expected",
    [
        (50, "accept"),
        (100, "accept"),
        (255, "accept"),
        (256, "cut off"),
        (500, "cut off"),
        (1000, "cut off"),
    ],
)
def test_input_fields_lengths(login_page, open_page, length, expected):
    login_page.INPUT_PASSWORD.fill("x" * length)

    actual_value = login_page.INPUT_PASSWORD.get_attribute("value")
    actual_length = len(actual_value)

    if expected == "accept":
        check.equal(
            actual_length, length, f"Expected {length}, granted {actual_length}"
        )
    elif expected == "cut off":
        check.less_equal(
            actual_length, length, f"Entered much more then possible: {actual_length}"
        )

    login_page.INPUT_USER_NAME.fill("x" * length)

    actual_value = login_page.INPUT_USER_NAME.get_attribute("value")
    actual_length = len(actual_value)

    if expected == "accept":
        check.equal(
            actual_length, length, f"Expected {length}, granted {actual_length}"
        )
    elif expected == "cut off":
        check.less_equal(
            actual_length, length, f"Entered much more then possible: {actual_length}"
        )
