import time

import allure
import pytest
from faker import Faker
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from conftest import logger
from Diplom.files import IMG_2
from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.my_info_page import MyInfoPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def my_info_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return MyInfoPage(driver)


@pytest.fixture
def fake():
    return Faker()


@allure.epic("Страница My Info")
@allure.title("Открытие страницы My Info")
@pytest.mark.smoke
def test_my_info_page(my_info_page, driver):
    logger.info("=== Начало test_my_info_page ===")
    with allure.step("Клик по меню My Info"):
        my_info_page.MENU_MY_INFO.click()
        logger.info("My Info нажато")

    with allure.step("Проверка открытия страницы"):
        my_info_page.check_that_page_opened()
        current_url = my_info_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="my_info_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.MYINFO
        logger.info("✓ Страница My info открыта корректно")

    logger.info("=== Конец test_my_info_page ===")


@allure.epic("Страница My Info")
@allure.title("Загрузка вложения в разделе My Info")
def test_upload_attach(my_info_page, driver):
    logger.info("=== Начало test_upload_attach ===")
    with allure.step("Открыть страницу My Info"):
        my_info_page.MENU_MY_INFO.click()
        logger.info("My Info нажато")

    with allure.step("Нажать кнопку добавления вложения"):
        my_info_page.ADD_ATTACHMENT.click()
        logger.info("Кнопка ADD_ATTACHMENT нажата")

    with allure.step("Загрузить файл"):
        my_info_page.UPLOAD_ATTACH.send_keys(str(IMG_2))
        logger.info(f"Файл {IMG_2} выбран для загрузки")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="file_selected",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(3)

    with allure.step("Сохранить вложение"):
        my_info_page.SAVE_ATTACH.click()
        logger.info("Кнопка SAVE_ATTACH нажата")

    with allure.step("Проверить сообщение об успешном сохранении"):
        assert my_info_page.check_message("Saved")
        logger.info("✓ Сообщение 'Saved' появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="upload_success",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_upload_attach ===")


@allure.epic("Страница My Info")
@allure.feature("Удаление вложения")
@allure.title("Проверка удаления attachment")
def test_delete_attach(my_info_page, driver):
    logger.info("=== Начало test_delete_attach ===")

    with allure.step("Открыть страницу My Info"):
        my_info_page.MENU_MY_INFO.click()
        logger.info("My Info нажато")

    with allure.step("Попытка удаления с отменой"):
        logger.info("Пытаемся удалить первое приложение")
        my_info_page.DELETE_ATTACHMENT.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="delete_confirmation",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Отменяем удаление")
        my_info_page.NO_CANCEL.click()
        logger.info("✓ Удаление отменено")

    with allure.step("Удаление attachment с подтверждением"):
        logger.info("Удаляем первое приложение")
        my_info_page.DELETE_ATTACHMENT.click()
        my_info_page.YES_DELETE.click()

        assert my_info_page.check_message("Deleted")
        logger.info("✓ Pay Grade успешно удален")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="delete_success",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_delete_attach ===")


@allure.epic("Страница  My Info")
@allure.title("Скачивание файла")
def test_download_attachment(my_info_page, driver, tmp_path):
    logger.info("=== Начало test_download_attachment ===")

    with allure.step("Открыть страницу My Info"):
        my_info_page.MENU_MY_INFO.click()
        logger.info("My Info нажато")

    time.sleep(3)

    with allure.step("Нажать кнопку скачивания"):
        my_info_page.DOWNLOAD_ATTACH.click()
        logger.info("Кнопка скачивания нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="download_clicked",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step(
        "Обработать всплывающее окно подтверждения, если оно все же всплыло"
    ):
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            logger.info(f"Текст подтверждения: {alert_text}")
            alert.accept()
            logger.info("Подтверждение принято")
        except Exception as e:
            logger.warning(
                f"Окно подтверждения не появилось или не удалось обработать: {e}"
            )

    with allure.step("Проверить, что файл скачался"):

        downloaded_file = my_info_page.wait_for_file_download(tmp_path, timeout=30)
        assert (
            downloaded_file is not None
        ), "Файл не был скачан в течение ожидаемого времени"
        logger.info(f"Файл скачан: {downloaded_file}")

        allure.attach.file(
            str(downloaded_file),
            name="downloaded_file",
            attachment_type=allure.attachment_type.TEXT,
        )

        file_size = downloaded_file.stat().st_size
        logger.info(f"Размер файла: {file_size} байт")
        assert file_size > 0, "Скачанный файл пуст"

    logger.info("=== Конец test_download_attachment ===")


@allure.epic("Страница My Info")
@allure.title("Заполнение основных полей")
def test_main_fields(my_info_page, driver, fake):
    logger.info("=== Начало test_main_fields ===")
    with allure.step("Открыть страницу My Info"):
        my_info_page.MENU_MY_INFO.click()
        logger.info("My Info нажато")

    time.sleep(3)

    with allure.step("Генерация тестовых данных"):
        first_name = fake.first_name()
        middle_name = fake.first_name()
        last_name = fake.last_name()
        ids = fake.random_number(digits=6)
        other_id = fake.passport_number()
        drivers_license = fake.license_plate()
        license_expire = fake.date(pattern="%Y-%d-%m")
        date_birth = fake.date_of_birth(minimum_age=21, maximum_age=50).strftime(
            "%Y-%d-%m"
        )
        logger.info("Сгенерированы случайные данные")

    with allure.step("Заполнить все поля через update_info"):
        my_info_page.update_info(
            first_name,
            middle_name,
            last_name,
            ids,
            other_id,
            drivers_license,
            license_expire,
            date_birth,
        )
        logger.info("Все поля заполнены")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="fields_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Сохранить изменения"):
        my_info_page.SAVE_BUTTON.click()
        logger.info("Кнопка SAVE_BUTTON нажата")

    with allure.step("Проверить сообщение об успешном сохранении"):
        assert my_info_page.check_message("Saved")
        logger.info("✓ Сообщение  появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="save_success",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_main_fields ===")
