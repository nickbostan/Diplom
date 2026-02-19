import time

import allure
import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)

from conftest import logger
from Diplom.page_obj.admin_block.modules_page import ModulesPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def modules_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return ModulesPage(driver)


@allure.epic("Страница модулей")
@allure.title("Открытие и проверка страницы модулей")
@pytest.mark.smoke
def test_modules_page(modules_page, driver):
    logger.info("=== Начало test_modules_page ===")
    with allure.step("Переход в админ панель и открытие модулей"):
        modules_page.MENU_ADMIN.click()
        try:
            modules_page.MORE.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        modules_page.CONFIGURATION.click()
        modules_page.MODULES.click()
        modules_page.check_that_page_opened()
        logger.info(f"Текущий URL: {modules_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="modules_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert modules_page.driver.current_url == URLS.MODULES
        logger.info("✓ Страница модулей открыта корректно")
    logger.info("=== Конец test_modules_page ===")


@allure.epic("Страница модулей")
@allure.feature("Выключение модулей")
@allure.title("Переключение всех модулей и проверка сохранения")
@pytest.mark.run(order=666)
def test_modules_switch(modules_page, driver):
    logger.info("=== Начало test_modules_switch ===")
    with allure.step("Открыть страницу модулей"):
        modules_page.MENU_ADMIN.click()
        try:
            modules_page.MORE.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        modules_page.CONFIGURATION.click()
        modules_page.MODULES.click()

    with allure.step("Переключить все модули и сохранить"):
        modules_page.check_that_page_opened()
        time.sleep(3)
        modules_page.all_modules_switch()
        modules_page.SAVE_BUTTON.click()
        assert modules_page.check_message("Saved")
        logger.info("✓ Сообщение  появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_save",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(4)

    with allure.step("Обновить страницу и проверить, что модули отключены"):
        driver.refresh()
        time.sleep(2)
        modules_page.check_modules_off()
        logger.info("✓ Все модули отключены")

    with allure.step("Снова переключить модули и сохранить"):
        modules_page.all_modules_switch()
        modules_page.SAVE_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_second_save",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_modules_switch ===")


@allure.epic("Страница модулей")
@allure.title("Проверка заблокированных переключателей Admin и PIM")
def test_check_disable_modules(modules_page, driver):
    logger.info("=== Начало test_check_disable_modules ===")
    with allure.step("Открыть страницу модулей"):
        modules_page.MENU_ADMIN.click()
        try:
            modules_page.MORE.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass
        modules_page.CONFIGURATION.click()
        modules_page.MODULES.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="modules_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить, что переключатель администратора заблокирован"):
        assert modules_page.ADMIN_CHECK.parent_has_class("--disabled")
        logger.info("✓ ADMIN_CHECK имеет класс --disabled")

    with allure.step("Проверить, что переключатель PIM заблокирован"):
        assert modules_page.PIM_CHECK.parent_has_class("--disabled")
        logger.info("✓ PIM_CHECK имеет класс --disabled")

    logger.info("=== Конец test_check_disable_modules ===")
