import allure
import pytest
import pytest_check as check

from conftest import logger
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


@allure.epic("Страница логина")
@allure.title("Отображение страницы логина")
@pytest.mark.smoke
def test_check_all_elements(login_page, open_page, driver):
    logger.info("=== Начало test_check_all_elements ===")

    with allure.step("Проверяем открытие страницы логина"):
        login_page.check_that_page_opened()
        logger.info(f"Текущий URL: {login_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="login_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert login_page.driver.current_url == URLS.LOGIN
        logger.info("✓ Страница логина открыта корректно")

    logger.info("=== Конец test_check_all_elements ===")


@allure.epic("Страница логина")
@allure.feature("Авторизация")
@allure.title("Вход в систему")
@pytest.mark.smoke
def test_positive_login(login_page, dashboard_page, open_page, driver):
    logger.info("=== Начало test_positive_login ===")

    with allure.step("Логинимся с валидными данными"):
        logger.info("Логин с Admin/admin123")
        login_page.login("Admin", "admin123")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_login",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем дашборд"):
        dashboard_page.check_that_page_opened()
        current_url = dashboard_page.driver.current_url
        logger.info(f"URL после логина: {current_url}")

        assert current_url == URLS.DASHBOARD
        logger.info("✓ Успешный логин, открыта страница дашборда")

    logger.info("=== Конец test_positive_login ===")


@allure.epic("Страница логина")
@allure.feature("Авторизация")
@allure.title("Выход из системы")
def test_logout(login_page, dashboard_page, open_page, driver):
    logger.info("=== Начало test_logout ===")

    with allure.step("Заходим в систему"):
        login_page.login("Admin", "admin123")
        logger.info("✓ Пользователь авторизован")

    with allure.step("Проверяем дашборд"):
        dashboard_page.check_that_page_opened()
        check.equal(login_page.driver.current_url, URLS.DASHBOARD)
        logger.info(f"URL дашборда: {URLS.DASHBOARD}")

    with allure.step("Выполняем выход"):
        dashboard_page.click_logout()
        logger.info("✓ Выход выполнен")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_logout",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем страницу логина"):
        login_page.check_that_page_opened()
        check.equal(login_page.driver.current_url, URLS.LOGIN)
        logger.info("✓ Успешно вернулись на страницу логина")

    logger.info("=== Конец test_logout ===")


@pytest.mark.parametrize(
    "user, password, expect",
    [
        ("incorrectUser", "admin123", "Invalid credentials"),
        ("Admin", "incorrectPassword", "Invalid credentials"),
    ],
)
@allure.epic("Страница логина")
@allure.feature("Авторизация")
@allure.title("Ввод неверного имени пользователя")
def test_negative_username(login_page, open_page, user, password, expect, driver):
    logger.info(f"=== Начало test_negative_username: {user} ===")

    with allure.step(f"Логин с неверными данными: {user}"):
        logger.info(f"Попытка логина: {user}/{password}")
        login_page.login(user, password)

        allure.attach(
            login_page.driver.get_screenshot_as_png(),
            name=f"error_{user}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка ошибки"):
        login_page.check_that_error_is_visible(expect)
        actual_error = login_page.get_error_text()

        allure.attach(
            f"Ожидалось: {expect}\nПолучено: {actual_error}",
            name="error_validation",
            attachment_type=allure.attachment_type.TEXT,
        )

        logger.info(f"Ошибка на странице: '{actual_error}'")
        assert actual_error == expect
        logger.info(f"✓ Проверена ошибка: {expect}")

    logger.info(f"=== Конец test_negative_username: {user} ===")


@pytest.mark.parametrize(
    "user, password, expect",
    [
        ("", "admin123", "Required"),
        ("Admin", "", "Required"),
    ],
)
@allure.epic("Страница логина")
@allure.feature("Авторизация")
@allure.title("Пустые поля")
def test_negative_empty_fields(login_page, open_page, user, password, expect, driver):
    logger.info("=== Начало test_negative_empty_fields ===")

    with allure.step(f"Логин с пустым полем: {user or 'пусто'}/{password or 'пусто'}"):
        logger.info(f"Пустые поля: username='{user}', password='{password}'")
        login_page.login(user, password)

        allure.attach(
            login_page.driver.get_screenshot_as_png(),
            name=f"empty_field_{'username' if not user else 'password'}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка ошибки пустого поля"):
        login_page.check_that_empty_error_is_visible(expect)
        logger.info(f"✓ Проверена ошибка пустого поля: {expect}")

    logger.info("=== Конец test_negative_empty_fields ===")


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
@allure.epic("Страница логина")
@allure.feature("Переход по ссылкам")
@allure.title("Проверка перехода по ссылкам")
def test_social_links(login_page, link_element, expected_url, open_page, driver):
    logger.info(f"=== Начало test_social_links: {link_element} ===")

    with allure.step(f"Кликаем на ссылку {link_element}"):
        logger.info(f"Тестируем ссылку: {link_element}")
        original_url = driver.current_url
        original_window = driver.current_window_handle

        social_link = getattr(login_page, link_element)
        social_link.click()
        logger.info(f"✓ Нажата ссылка {link_element}")

    with allure.step("Проверяем новое окно"):
        new_url = login_page.switch_to_new_window(expected_windows=2)
        logger.info(f"Новый URL: {new_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"social_{link_element}",
            attachment_type=allure.attachment_type.PNG,
        )

        assert expected_url in new_url, f"URL {new_url} not contains {expected_url}"
        logger.info(f"✓ URL содержит: {expected_url}")

    with allure.step("Закрываем новое окно и возвращаемся"):
        driver.close()
        driver.switch_to.window(original_window)
        logger.info("✓ Вернулись в исходное окно")

        assert original_url == login_page.driver.current_url
        logger.info("✓ URL прежний")

    logger.info(f"=== Конец test_social_links: {link_element} ===")


@allure.epic("Страница логина")
@allure.feature("Авторизация")
@allure.title("Переход на ссылку восстановления пароля")
def test_forgot_password_link(login_page, open_page, driver):
    logger.info("=== Начало test_forgot_password_link ===")

    with allure.step("Кликаем на 'Forgot Password'"):
        logger.info("Тестируем ссылку восстановления пароля")
        login_page.FORGOT_PASSWORD_LINK.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="forgot_password_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем URL страницы восстановления"):
        current_url = login_page.driver.current_url
        logger.info(f"URL страницы восстановления: {current_url}")

        assert current_url == URLS.PASSWORD
        logger.info("✓ Страница восстановления пароля открыта корректно")

    logger.info("=== Конец test_forgot_password_link ===")
