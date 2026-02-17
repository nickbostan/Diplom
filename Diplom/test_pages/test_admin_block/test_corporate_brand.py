import time

import pytest
import allure
from selenium.webdriver.support.wait import WebDriverWait

from conftest import logger
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from Diplom.page_obj.admin_block.corporate_branding import CorpBrandingPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def corp_branding_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    page = CorpBrandingPage(driver)
    page.MENU_ADMIN.click()
    try:
        page.MORE.click()
    except (NoSuchElementException, ElementNotInteractableException):
        pass
    page.CORP_BRANDING.click()
    page.check_that_page_opened()
    return page




@allure.epic("Страница Corporate Branding")
@allure.title("Открытие страницы Corporate Branding")
@pytest.mark.smoke
def test_check_branding_page(corp_branding_page, driver):
    logger.info("=== Начало test_open_page ===")
    with allure.step("Проверить отображение элементов'"):
        corp_branding_page.check_that_page_opened()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="branding_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить URL страницы"):
        current_url = corp_branding_page.driver.current_url
        assert current_url == URLS.CORP_BRANDING, \
            f"Ожидался {URLS.CORP_BRANDING}, получен {current_url}"
    logger.info("✓ Страница Corporate Branding открыта")


@allure.epic("Страница Corporate Branding")
@allure.title("Проверка сохранения цвета после установки и перезагрузки")
@pytest.mark.parametrize("name, hex_color", [
    ("Чёрный", "#000000"),
    ("Белый", "#FFFFFF"),
    ("Красный", "#FF0000"),
    ("Зелёный", "#00FF00"),
    ("Синий", "#0000FF"),
    ("Жёлтый", "#FFFF00"),
    ("Пурпурный", "#FF00FF"),
    ("Бирюзовый", "#00FFFF"),
    ("Серый", "#808080"),
])
def test_color_persistence_after_publish(corp_branding_page, name, hex_color, driver):
    logger.info(f"=== Начало test_color_persistence_after_publish: {name} ===")

    picker = corp_branding_page.primary_color_picker

    with allure.step(f"Выбрать цвет {name} ({hex_color})"):
        picker.select_color_by_hex(hex_color)

    with allure.step("Нажать Publish и дождаться подтверждения"):
        corp_branding_page.PUBLISH_BUTTON.click()
        assert corp_branding_page.check_message("Saved")

    with allure.step("Перезагрузить страницу и дождаться загрузки"):
        driver.refresh()
        corp_branding_page.check_that_page_opened()

    fresh_picker = corp_branding_page.primary_color_picker

    with allure.step("Проверить, что цвет сохранился"):
        # Ждём, пока цвет элемента не станет ожидаемым
        WebDriverWait(driver, 10).until(
            lambda d: fresh_picker.get_selected_color() == hex_color.upper(),
            message=f"Цвет не изменился на {hex_color} после перезагрузки"
        )
        selected_hex = fresh_picker.get_selected_color()
        assert selected_hex == hex_color.upper(), \
            f"После перезагрузки цвет изменился: ожидался {hex_color}, получен {selected_hex}"

    with allure.step("Проверить отсутствие ошибки"):
        assert not fresh_picker.has_error(), "Появилась ошибка при корректном HEX"

    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"color_{name}_after_reload",
        attachment_type=allure.attachment_type.PNG,
    )

    logger.info(f"✓ Цвет {name} успешно сохранился")


@allure.epic("Страница Corporate Branding")
@allure.title("Цвет применяется к превью темы")
def test_color_applies_to_theme_preview(corp_branding_page, driver):
    logger.info("=== Начало test_color_applies_to_theme_preview ===")
    picker = corp_branding_page.primary_color_picker
    test_hex = "#0000FF"

    with allure.step("Выбрать синий цвет"):
        picker.select_color_by_hex(test_hex)

    with allure.step("Нажать Publish"):
        corp_branding_page.PUBLISH_BUTTON.click()
        assert corp_branding_page.check_message("Saved")

    corp_branding_page.check_that_page_opened()

    with allure.step("Кликнуть вне области пикера (например, на заголовок)"):
        corp_branding_page.MAIN_TITLE.click()


    with allure.step("Проверить, что цвет применился к элементу превью"):
        theme_element = corp_branding_page.TOP_BAR
        bg_color = theme_element.get_element().value_of_css_property("background-color")
        bg_hex = picker._rgb_to_hex(bg_color)
        assert bg_hex == "#0000FF", f"Цвет не применился: получен {bg_color}"

    logger.info("✓ Цвет применился к превью")


@allure.epic("Страница Corporate Branding")
@allure.title("Ввод некорректного HEX")
@pytest.mark.parametrize("bad_hex", ["#GGGGGG", "123456", "#12345", "red"])
def test_invalid_input(corp_branding_page, bad_hex):
    logger.info(f"=== Начало test_invalid_hex: {bad_hex} ===")
    picker = corp_branding_page.primary_color_picker

    with allure.step(f"Попытаться ввести {bad_hex}"):
        picker.select_color_by_hex(bad_hex)

    with allure.step("Проверить появление ошибки"):
        assert picker.has_error(), f"Ошибка не появилась для неверного HEX '{bad_hex}'"

    logger.info(f"✓ Ошибка корректно отображается для {bad_hex}")


@allure.epic("Страница Corporate Branding")
@allure.title("Сброс к настройкам по умолчанию")
@allure.severity(allure.severity_level.NORMAL)
def test_reset_to_default(corp_branding_page):
    logger.info("=== Начало test_reset_to_default ===")
    picker = corp_branding_page.primary_gradient1_picker

    default_color = "#FF920B"

    with allure.step("Изменить цвет на другой"):
        picker.select_color_by_hex("#FF5733")

    with allure.step("Нажать Publish"):
        corp_branding_page.PUBLISH_BUTTON.click()
        assert corp_branding_page.check_message("Saved")
        corp_branding_page.check_that_page_opened()

    time.sleep(3)


    with allure.step("Нажать Reset to Default"):
        corp_branding_page.RESET_TO_DEFAULT.click()

    time.sleep(3)

    with allure.step("Проверить, что цвет вернулся к умолчанию"):
        selected_hex = picker.get_selected_color()
        assert selected_hex == default_color, \
            f"После сброса цвет не вернулся: ожидался {default_color}, получен {selected_hex}"

    logger.info("✓ Сброс к настройкам по умолчанию работает")
