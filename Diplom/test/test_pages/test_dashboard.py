import allure
import pytest

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


@allure.epic("Страница dashboard")
@allure.title("Проверка отображения страницы dashboard")
def test_dashboard_page(dashboard_page, driver):
    logger.info("=== Начало test_dashboard_page ===")

    with allure.step("Проверяем открытие главной страницы Dashboard"):
        dashboard_page.check_that_page_opened()
        logger.info(f"Текущий URL: {dashboard_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="dashboard_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert dashboard_page.driver.current_url == URLS.DASHBOARD
        logger.info("✓ Главная страница Dashboard открыта корректно")

    logger.info("=== Конец test_dashboard_page ===")


@pytest.mark.parametrize(
    "widget, expected_url",
    [
        ("ASSIGN_LEAVE_CARD", URLS.ASSIGN_LEAVE),
        ("LEAVE_LIST_CARD", URLS.LEAVE),
        ("TIMESHEETS_CARD", URLS.TIME),
        ("APPLY_LEAVE_CARD", URLS.APPLY_LEAVE),
        ("MY_LEAVE_CARD", URLS.MY_LEAVE),
        ("MY_TIMESHEET_CARD", URLS.MY_TIME),
        ("PUNCH_OUT", (URLS.ATTENDANCE_PUNCH, URLS.PERFORMANCE)),
        ("SELF_REVIEW", (URLS.PERFORMANCE_DASH, URLS.PERFORMANCE)),
        ("CANDIDATE_TO_INTERVIEW", URLS.RECRUITMENT_DASH),
    ],
)
@allure.epic("Страница dashboard")
@allure.feature("Ссылки виджетов")
@allure.title("Проверка перехода по ссылкам виджетов")
def test_widget_links(dashboard_page, widget, expected_url, driver):
    logger.info(f"=== Начало test_navigation_links: {widget} ===")

    with allure.step(f"Кликаем на ссылку '{widget}'"):
        logger.info(f"Переход по ссылке: {widget}")

        element = getattr(dashboard_page, widget)
        element.click()

        allure.attach(
            dashboard_page.driver.get_screenshot_as_png(),
            name=f"{widget}_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step(f"Проверяем переход на страницу {widget}"):
        current_url = dashboard_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        if isinstance(expected_url, tuple):
            url_matched = any(url in current_url for url in expected_url)
            error_msg = f"URL не содержит ни один из: {expected_url}. Фактический: {current_url}"
        else:
            url_matched = expected_url in current_url
            error_msg = f"URL не содержит '{expected_url}'. Фактический: {current_url}"

        assert url_matched, error_msg

        logger.info("✓ Переход выполнен успешно")

    logger.info(f"=== Конец test_navigation_links: {widget} ===")


@allure.epic("Страница dashboard")
@allure.feature("Чекбокс")
@allure.title("Проверка выбора чекбокса")
def test_config(dashboard_page, driver):
    logger.info("=== Начало test_config ===")

    with allure.step("Открываем настройки отпусков сотрудников"):
        logger.info("Кликаем на кнопку конфигурации отпусков")
        dashboard_page.CONFIG_EMPL_LEAVE.click()

    with allure.step("Проверяем и нажимаем кнопку 'Показать'"):
        logger.info("Проверяем видимость кнопки 'Показать'")
        dashboard_page.SHOW_BUTTON.should_be_visible()
        logger.info("Кликаем на кнопку 'Показать'")
        dashboard_page.SHOW_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="show_button_clicked",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Сохраняем настройки"):
        logger.info("Сохраняем изменения через кнопку 'Сохранить'")
        dashboard_page.SAVE_BUTTON.click()

    with allure.step("Повторно открываем настройки для проверки"):
        logger.info("Повторно открываем конфигурацию отпусков")
        dashboard_page.CONFIG_EMPL_LEAVE.click()

        allure.attach(
            dashboard_page.driver.get_screenshot_as_png(),
            name="config_reopened",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверяем состояние кнопки 'Показать'"):
        logger.info("Проверяем, что кнопка 'Показать'  отмечена")
        is_checked = dashboard_page.SHOW_BUTTON.is_checked()

        assert (
            not is_checked
        ), "Кнопка 'Показать' должна быть  отмечена после сохранения"
        logger.info("✓ Кнопка 'Показать' корректно  отмечена")

    with allure.step("Выходим из окна"):
        logger.info("Выход из окна через кнопку 'Отмена'")
        dashboard_page.CANCEL_BUTTON.click()
        logger.info("✓ Вернулись на страницу dashboard")

    logger.info("=== Конец test_config ===")


@pytest.mark.parametrize(
    "link_element, expected_url",
    [
        ("DOWN_LINK", "orangehrm.com"),
        ("UPGRADE_LINK", "orangehrm.com/open-source/upgrade-to-advanced"),
        ("HELP_LINK", "starterhelp.orangehrm"),
    ],
)
@allure.epic("Страница dashboard")
@allure.feature("Переход по ссылкам")
@allure.title("Проверка перехода по ссылкам")
def test_links(dashboard_page, link_element, expected_url, driver):
    logger.info(f"=== Начало test_social_links: {link_element} ===")

    with allure.step(f"Кликаем на ссылку {link_element}"):
        logger.info(f"Тестируем ссылку: {link_element}")
        original_url = driver.current_url
        original_window = driver.current_window_handle

        social_link = getattr(dashboard_page, link_element)
        social_link.click()
        logger.info(f"✓ Нажата ссылка {link_element}")

    with allure.step("Проверяем новое окно"):
        new_url = dashboard_page.switch_to_new_window(expected_windows=2)
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

        assert original_url == dashboard_page.driver.current_url
        logger.info("✓ URL прежний")

    logger.info(f"=== Конец test_social_links: {link_element} ===")


@allure.epic("Страница dashboard")
@allure.feature("Поиск")
@allure.title("Проверка поискового запроса")
def test_search(dashboard_page, driver):
    logger.info("=== Начало test_search ===")
    with allure.step("Проверяем видимость поля поиска и заполняем форму"):
        dashboard_page.SEARCH_FIELD.should_be_visible()
        dashboard_page.SEARCH_FIELD.fill("admin")
        logger.info(" Поле поиска актино и совершен ввод")

        assert dashboard_page.MENU_PIM.should_be_not_visible()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="dashboard_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Очищаем поле поиска"):
        dashboard_page.SEARCH_FIELD.fill("")
        logger.info(" Поле поиска очищено")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="dashboard_page",
            attachment_type=allure.attachment_type.PNG,
        )

        dashboard_page.MENU_PIM.should_be_visible()
        logger.info("Все значения меню снова отображаются")

    logger.info("=== Конец test_search ===")
