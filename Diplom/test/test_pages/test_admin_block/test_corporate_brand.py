import time

import allure
import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)
from selenium.webdriver.support.wait import WebDriverWait

from conftest import logger
from Diplom.files import IMG_2, IMG_BIG, RES
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
        assert (
            current_url == URLS.CORP_BRANDING
        ), f"Ожидался {URLS.CORP_BRANDING}, получен {current_url}"
    logger.info("✓ Страница Corporate Branding открыта")


@allure.epic("Страница Corporate Branding")
@allure.title("Проверка сохранения цвета после установки и перезагрузки")
@pytest.mark.parametrize(
    "name, hex_color",
    [
        ("Чёрный", "#000000"),
        ("Белый", "#FFFFFF"),
        ("Красный", "#FF0000"),
        ("Зелёный", "#00FF00"),
        ("Синий", "#0000FF"),
        ("Жёлтый", "#FFFF00"),
        ("Пурпурный", "#FF00FF"),
        ("Бирюзовый", "#00FFFF"),
        ("Серый", "#808080"),
    ],
)
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
            message=f"Цвет не изменился на {hex_color} после перезагрузки",
        )
        selected_hex = fresh_picker.get_selected_color()
        assert (
            selected_hex == hex_color.upper()
        ), f"После перезагрузки цвет изменился: ожидался {hex_color}, получен {selected_hex}"

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
    picker = corp_branding_page.primary_gradient1_picker
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
        assert (
            selected_hex == default_color
        ), f"После сброса цвет не вернулся: ожидался {default_color}, получен {selected_hex}"

    logger.info("✓ Сброс к настройкам по умолчанию работает")


@allure.epic("Страница Corporate Branding")
@allure.title("Добавление изображений (логотип, баннеры)")
def test_add_images(corp_branding_page, resized_image, driver):
    logger.info("=== Начало test_add_images ===")

    with allure.step("Загрузить логотип (50x50)"):
        corp_branding_page.UPLOAD_LOGO.send_keys(resized_image(50, 50))
        logger.info("Логотип загружен")

    with allure.step("Загрузить баннер клиента (182x50)"):
        corp_branding_page.UPLOAD_CLIENT_BANNER.send_keys(resized_image(182, 50))
        logger.info("Баннер клиента загружен")

    with allure.step("Загрузить баннер логина (340x65)"):
        corp_branding_page.UPLOAD_LOGIN_BANNER.send_keys(resized_image(340, 65))
        logger.info("Баннер логина загружен")

    # Небольшая пауза для обработки файлов
    time.sleep(3)

    with allure.step("Нажать кнопку Publish"):
        corp_branding_page.PUBLISH_BUTTON.click()
        logger.info("Кнопка Publish нажата")

    with allure.step("Проверить сообщение об успешном сохранении"):
        assert corp_branding_page.check_message(
            "Saved"
        ), "Сообщение 'Saved' не появилось"
        logger.info("✓ Изменения сохранены")

    time.sleep(3)  # ожидание обновления страницы

    with allure.step("Проверить, что загруженные изображения отображаются"):
        corp_branding_page.CLIENT_LOGO.should_be_visible()
        logger.info("Логотип видим")
        corp_branding_page.CLIENT_BANNER.should_be_visible()
        logger.info("Баннер клиента видим")
        corp_branding_page.LOGIN_BANNER.should_be_visible()
        logger.info("Баннер логина видим")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="images_uploaded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_add_images ===")


@allure.epic("Страница Corporate Branding")
@allure.title("Восстановление настроек по умолчанию")
def test_reset_files(corp_branding_page, driver):

    logger.info("=== Начало test_reset_to_default ===")

    with allure.step("Нажать кнопку Reset to Default"):
        corp_branding_page.RESET_TO_DEFAULT.click()
        logger.info("Кнопка сброса нажата")

    time.sleep(3)

    with allure.step("Проверить, что логотип исчез"):
        assert corp_branding_page.CLIENT_LOGO.should_be_not_visible()
        logger.info("✓ Логотип скрыт")

    with allure.step("Проверить, что баннер клиента исчез"):
        assert corp_branding_page.CLIENT_BANNER.should_be_not_visible()
        logger.info("✓ Баннер клиента скрыт")

    allure.attach(
        driver.get_screenshot_as_png(),
        name="after_reset",
        attachment_type=allure.attachment_type.PNG,
    )

    logger.info("=== Конец test_reset_to_default ===")


@allure.epic("Страница Corporate Branding")
@allure.title("Ошибки при добавлении изображений")
@pytest.mark.parametrize(
    "file_1, file_2, file_3, expected_1, expected_2",
    [
        (IMG_2, IMG_BIG, RES, "Incorrect Dimensions", "Attachment Size Exceeded"),
        (RES, IMG_2, IMG_BIG, "Incorrect Dimensions", "Attachment Size Exceeded"),
        (IMG_BIG, RES, IMG_2, "Attachment Size Exceeded", "Incorrect Dimensions"),
    ],
)
def test_error_add_images(
    corp_branding_page, file_1, file_2, file_3, expected_1, expected_2, driver
):
    """В данном тесте должно было быть еще одно expected Only 'gif',
     'png', 'jpg', 'jpeg' type images are allowed!
    но почему-то в данном случае ошибку не бьет , хотя и не сохраняет"""
    logger.info(f"=== Начало test_error_add_images: {file_1}, {file_2}, {file_3} ===")

    with allure.step("Загрузить первый файл (логотип)"):
        corp_branding_page.UPLOAD_LOGO.send_keys(str(file_1))
        time.sleep(2)
        logger.info(f"Файл {file_1} загружен")

    with allure.step("Загрузить второй файл (баннер клиента)"):
        corp_branding_page.UPLOAD_CLIENT_BANNER.send_keys(str(file_2))
        time.sleep(2)
        logger.info(f"Файл {file_2} загружен")

    with allure.step("Загрузить третий файл (баннер логина)"):
        corp_branding_page.UPLOAD_LOGIN_BANNER.send_keys(str(file_3))
        time.sleep(2)
        logger.info(f"Файл {file_3} загружен")

    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"uploaded_files_{file_1.name}_{file_2.name}_{file_3.name}",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step(f"Проверить первую ожидаемую ошибку: '{expected_1}'"):
        assert corp_branding_page.check_that_error_is_visible(
            expected_1
        ), f"Ошибка '{expected_1}' не отобразилась"
        logger.info(f"✓ Ошибка '{expected_1}' видна")

    with allure.step(f"Проверить вторую ожидаемую ошибку: '{expected_2}'"):
        assert corp_branding_page.check_that_error_2_is_visible(
            expected_2
        ), f"Ошибка '{expected_2}' не отобразилась"
        logger.info(f"✓ Ошибка '{expected_2}' видна")

    allure.attach(
        driver.get_screenshot_as_png(),
        name="errors_displayed",
        attachment_type=allure.attachment_type.PNG,
    )

    logger.info("=== Конец test_error_add_images ===")
