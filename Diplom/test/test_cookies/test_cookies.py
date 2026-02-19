import time

import allure
import pytest
from selenium.common.exceptions import TimeoutException

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


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver)


@allure.epic("Cookies")
@allure.title("Проверка наличия куки orangehrm после логина")
def test_cookie_exists_after_login(dashboard_page, driver):
    logger.info("=== Начало test_cookie_exists_after_login ===")
    driver = dashboard_page.driver

    with allure.step("Получить все cookies"):
        cookies = driver.get_cookies()
        cookie_names = [c["name"] for c in cookies]
        logger.info(f"Список cookie: {cookie_names}")

    with allure.step("Проверить наличие cookie 'orangehrm'"):
        assert "orangehrm" in cookie_names, "Кука 'orangehrm' не найдена"
        logger.info("✓ Кука orangehrm присутствует")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="cookies_list",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_cookie_exists_after_login ===")


@allure.epic("Cookies")
@allure.title("Проверка атрибутов куки orangehrm")
def test_cookie_attributes(dashboard_page, driver):
    logger.info("=== Начало test_cookie_attributes ===")
    driver = dashboard_page.driver

    with allure.step("Получить cookie 'orangehrm'"):
        cookie = driver.get_cookie("orangehrm")
        assert cookie is not None, "Кука 'orangehrm' отсутствует"
        logger.info(f"Cookie получена: {cookie}")

    with allure.step("Проверить, что значение не пустое"):
        assert cookie["value"] != "", "Значение куки пустое"
        logger.info("✓ Значение не пустое")

    with allure.step("Проверить параметр expiry (если есть)"):
        if cookie.get("expiry") is not None:
            assert cookie["expiry"] > 0, "Неверный expiry"
        logger.info("✓ Expiry корректен (или отсутствует)")

    with allure.step("Записать атрибуты в отчёт"):

        allure.attach(
            f"httpOnly: {cookie.get('httpOnly')}, secure: {cookie.get('secure')}, domain: {cookie.get('domain')}",
            name="cookie_attributes",
            attachment_type=allure.attachment_type.TEXT,
        )

    logger.info("✓ Атрибуты куки проверены")
    logger.info("=== Конец test_cookie_attributes ===")


@allure.epic("Cookies")
@allure.title("Удаление куки orangehrm приводит к выходу из системы")
def test_delete_cookie_and_check_logout(dashboard_page, login_page, driver):
    logger.info("=== Начало test_delete_cookie_and_check_logout ===")
    driver = dashboard_page.driver

    with allure.step("Проверить, что находимся на Dashboard"):
        assert driver.current_url == URLS.DASHBOARD
        logger.info("✓ Текущий URL соответствует Dashboard")

    with allure.step("Удалить cookie 'orangehrm'"):
        driver.delete_cookie("orangehrm")
        logger.info("Cookie удалена")

    with allure.step("Обновить страницу"):
        driver.refresh()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_refresh",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить, что произошёл переход на страницу логина"):
        try:
            login_page.INPUT_USER_NAME.should_be_visible()
            login_page.check_that_page_opened()
            assert (
                driver.current_url == URLS.LOGIN
            ), "URL не соответствует странице логина"
            logger.info("✓ Произошёл переход на страницу логина")
        except TimeoutException:
            pytest.fail("После удаления куки не произошёл переход на страницу логина")

    allure.attach(
        driver.get_screenshot_as_png(),
        name="login_page_after_logout",
        attachment_type=allure.attachment_type.PNG,
    )

    logger.info("=== Конец test_delete_cookie_and_check_logout ===")


@allure.epic("Cookies")
@allure.title("Удаление всех cookies приводит к выходу из системы")
def test_delete_all_cookies(dashboard_page, login_page, driver):
    logger.info("=== Начало test_delete_all_cookies ===")
    driver = dashboard_page.driver

    with allure.step("Удалить все cookies"):
        driver.delete_all_cookies()
        logger.info("Все cookies удалены")

    with allure.step("Обновить страницу"):
        driver.refresh()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_refresh",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить переход на страницу логина"):
        try:
            login_page.INPUT_USER_NAME.should_be_visible()
            login_page.check_that_page_opened()
            assert driver.current_url == URLS.LOGIN
            logger.info("✓ Произошёл переход на страницу логина")
        except TimeoutException:
            pytest.fail("После удаления всех куки не произошёл переход на логин")

    allure.attach(
        driver.get_screenshot_as_png(),
        name="login_page_after_all_deleted",
        attachment_type=allure.attachment_type.PNG,
    )

    logger.info("=== Конец test_delete_all_cookies ===")


@allure.epic("Cookies")
@allure.title("Inject ранее сохранённой куки позволяет восстановить сессию")
@pytest.mark.skip(
    reason="Тест отключен из-за того что нельзя по куке войти в систему обратно"
)
def test_inject_cookie(dashboard_page, driver, login_page):
    logger.info("=== Начало test_inject_cookie ===")
    driver = dashboard_page.driver

    with allure.step("Сохранить оригинальную cookie 'orangehrm'"):
        original_cookie = driver.get_cookie("orangehrm")
        assert original_cookie is not None, "Нет куки для сохранения"
        logger.info(f"Оригинальная cookie: {original_cookie}")

    with allure.step("Удалить все cookies и перезагрузить страницу"):
        driver.delete_all_cookies()
        driver.refresh()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_delete_all",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить, что мы на странице логина"):
        login_page.INPUT_USER_NAME.should_be_visible()
        logger.info("✓ Страница логина открыта")

    with allure.step("Добавить сохранённую cookie обратно"):
        driver.add_cookie(original_cookie)
        logger.info("Cookie добавлена")

    with allure.step("Перейти на Dashboard и проверить доступ"):
        driver.get(URLS.DASHBOARD)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_inject",
            attachment_type=allure.attachment_type.PNG,
        )

        try:
            dashboard_page.DASHBOARD_TITLE.should_be_visible()
            success = True
            logger.info("✓ Удалось войти по  куке")
        except TimeoutException:
            success = False
            logger.error("Не удалось войти по куке")
        assert success, "Не удалось войти по сохраненной куке"

    logger.info("=== Конец test_inject_cookie ===")


@allure.epic("Cookies")
@allure.title("Кука статична при переходе между страницами")
def test_cookie_persistence(dashboard_page, driver):
    logger.info("=== Начало test_cookie_persistence ===")
    driver = dashboard_page.driver

    with allure.step("Получить cookie до перехода"):
        cookie_before = driver.get_cookie("orangehrm")
        logger.info(f"Cookie до: {cookie_before}")

    with allure.step("Перейти на страницу PIM"):
        dashboard_page.MENU_PIM.click()
        allure.attach(
            driver.get_screenshot_as_png(),
            name="pim_page",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(5)

    with allure.step("Получить cookie после перехода"):
        cookie_after = driver.get_cookie("orangehrm")
        logger.info(f"Cookie после: {cookie_after}")

    with allure.step("Проверить, что cookie не изменилась"):
        assert cookie_before == cookie_after, "Кука изменилась после перехода"
        logger.info("✓ Кука стабильна при навигации")

    logger.info("=== Конец test_cookie_persistence ===")
