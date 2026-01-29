
import pytest
import allure

from conftest import logger
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


@pytest.mark.parametrize(
    "widget, expected_url",
    [
        ("ASSIGN_LEAVE_CARD", URLS.ASSIGN_LEAVE),
        ("LEAVE_LIST_CARD", URLS.LEAVE),
        ("TIMESHEETS_CARD", URLS.TIME),
        ("APPLY_LEAVE_CARD", URLS.APPLY_LEAVE),
        ("MY_LEAVE_CARD", URLS.MY_LEAVE),
        ("MY_TIMESHEET_CARD", URLS.MY_TIME),
        ("PUNCH_OUT", URLS.ATTENDANCE_PUNCH),
        ("SELF_REVIEW", URLS.PERFORMANCE),
        ("CANDIDATE_TO_INTERVIEW", URLS.RECRUITMENT_DASH),
    ],
)
def test_widget_links(dashboard_page, widget, expected_url, driver):
    """
    Тест перехода по ссылкам в виджетах
    """
    logger.info(f"=== Начало test_navigation_links: {widget} ===")

    with allure.step(f"Кликаем на ссылку '{widget}'"):
        logger.info(f"Переход по ссылке: {widget}")

        element = getattr(dashboard_page, widget)
        element.click()

        allure.attach(
            dashboard_page.driver.get_screenshot_as_png(),
            name=f"{widget}_page",
            attachment_type=allure.attachment_type.PNG
        )

    with allure.step(f"Проверяем переход на страницу {widget}"):
        current_url = dashboard_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        # Проверяем что URL содержит ожидаемый фрагмент
        assert expected_url in current_url, \
            f"URL не содержит '{expected_url}'. Фактический URL: {current_url}"
        logger.info(f"✓ URL содержит: {expected_url}")


    logger.info(f"=== Конец test_navigation_links: {widget} ===")


def test_config(dashboard_page):
    dashboard_page.CONFIG_EMPL_LEAVE.click()
    dashboard_page.SHOW_BUTTON.should_be_visible()
    dashboard_page.SHOW_BUTTON.click()
    dashboard_page.SAVE_BUTTON.click()
    dashboard_page.CONFIG_EMPL_LEAVE.click()
    assert not dashboard_page.SHOW_BUTTON.is_checked()
    dashboard_page.CANCEL_BUTTON.click()



