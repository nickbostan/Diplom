import time

import allure
import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)

from conftest import logger
from Diplom.page_obj.admin_block.localization import LocalizationPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def localization_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return LocalizationPage(driver)


@allure.epic("Страница локализации")
@allure.title("Открытие страницы локализации и проверка языка по умолчанию")
@pytest.mark.smoke
def test_localization_page(localization_page, driver):
    logger.info("=== Начало test_localization_page ===")
    with allure.step("Переход к разделу локализации"):
        localization_page.MENU_ADMIN.click()
        try:
            localization_page.MORE.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        localization_page.CONFIGURATION.click()
        localization_page.LOCALIZATION.click()
        localization_page.check_that_page_opened()
        logger.info("Страница локализации открыта")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="localization_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(2)

    with allure.step("Проверка URL страницы локализации"):
        current_url = localization_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")
        assert current_url == URLS.LOCALIZATION
        logger.info("✓ URL корректен")

    with allure.step("Проверка языка по умолчанию (English)"):
        localization_page.LANGUAGE.should_contain_text("English")
        logger.info("✓ Язык по умолчанию – English")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="default_english",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_localization_page ===")


@allure.epic("Страница локализации")
@allure.title("Выбор языка {language} и проверка текста заголовка")
@pytest.mark.parametrize(
    "language, expected",
    [
        ("Chine", "本地化"),
        ("Taiwan", "本土化"),
        ("Dutch", "Lokalisatie"),
        ("French", "Localisation"),
        ("German", "Lokalisierung"),
        ("Spanish", "Localizac"),
    ],
)
def test_language_selection(localization_page, driver, expected, language):
    logger.info(f"=== Начало test_language_selection для языка '{language}' ===")
    with allure.step("Переход к разделу локализации"):
        localization_page.MENU_ADMIN.click()
        try:
            localization_page.MORE.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        localization_page.CONFIGURATION.click()
        localization_page.LOCALIZATION.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"localization_page_before_{language}",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(2)

    with allure.step(f"Выбор языка '{language}' "):
        localization_page.LANGUAGE.select_from_dropdown(language)
        logger.info(f"✓ Язык '{language}' выбран")

    with allure.step("Сохранение настроек"):
        localization_page.SAVE_BUTTON.click()
        logger.info("Нажали сохранить")

    with allure.step("Проверка сообщения об успешном обновлении"):
        assert localization_page.check_message("Updated")
        logger.info("✓ Сообщение появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"after_save_{language}",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(5)

    with allure.step(f"Проверка заголовка страницы – ожидается '{expected}'"):
        assert localization_page.PAGE_TITLE.should_contain_text(expected)
        logger.info(f"✓ Заголовок содержит '{expected}'")

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"title_after_{language}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Возврат языка на English"):
        localization_page.LANGUAGE.should_be_visible()
        localization_page.LANGUAGE.select_from_dropdown("English")
        logger.info("Язык English выбран")

    with allure.step("Сохранение после возврата"):
        localization_page.SAVE_BUTTON.click()
        logger.info("Нажали сохранить")

    time.sleep(5)

    with allure.step("Проверка заголовка после возврата – 'Localization'"):
        assert localization_page.PAGE_TITLE.should_contain_text("Localization")
        logger.info("✓ Заголовок содержит 'Localization'")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="title_english",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info(f"=== Конец test_language_selection для языка '{language}' ===")
