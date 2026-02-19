import time

import allure
import pytest
from faker import Faker
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import logger
from Diplom.files import IMG_2, IMG_BIG, RES
from Diplom.page_obj.buzz_page import BuzzPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture(scope="function")
def buzz_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return BuzzPage(driver)


@allure.epic("Страница Buzz")
@allure.title("Открытие страницы Buzz")
def test_buzz_page(buzz_page, driver):
    logger.info("=== Начало test_buzz_page ===")

    with allure.step("Клик по меню Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Buzz нажато")

    with allure.step("Проверка открытия страницы Buzz"):
        buzz_page.check_that_page_opened()
        current_url = buzz_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="buzz_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.BUZZ, f"Ожидался {URLS.BUZZ}, получен {current_url}"
        logger.info("✓ Страница Buzz открыта корректно")

    logger.info("=== Конец test_buzz_page ===")


@allure.epic("Страница Buzz")
@allure.title("Публикация текстового поста")
def test_post_text(buzz_page, driver, fake):
    logger.info("=== Начало test_post_text ===")

    post_text = fake.sentence()

    with allure.step("Клик по меню Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Buzz нажато")

    with allure.step(f"Ввод текста поста: {post_text}"):
        buzz_page.POST_WRITE_FIELD.fill(post_text)
        logger.info("Текст введён")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="post_text_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажатие кнопки публикации"):
        buzz_page.POST_BUTTON.click()
        logger.info("Кнопка 'Post' нажата")

    with allure.step("Проверка сообщения об успешном сохранении"):
        assert buzz_page.check_message("Saved"), "Сообщение 'Saved' не появилось"
        logger.info("✓ Пост опубликован")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="post_text_success",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка текста первого поста"):
        first_text = buzz_page.FIRST_TEXT.get_text()
        assert (
            first_text == post_text
        ), f"Ожидался '{post_text}', получен '{first_text}'"
        logger.info("✓ Текст поста совпадает")

    logger.info("=== Конец test_post_text ===")


@allure.epic("Страница Buzz")
@allure.title("Публикация нескольких фото и удаление")
@pytest.mark.skip(reason="Тест отключен из-за резкого закрытия окна диалога")
def test_post_photo(buzz_page, driver, fake):
    logger.info("=== Начало test_post_photo ===")

    post_text = fake.sentence()

    with allure.step("Клик по меню Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Buzz нажато")

    with allure.step("Открытие диалога добавления фото"):
        buzz_page.SHARE_PHOTOS.click()
        logger.info("Кнопка 'Share Photos' нажата")

    with allure.step(f"Ввод текста поста: {post_text}"):
        buzz_page.FIELD_POST_VIDEO_PHOTO.fill(post_text)
        logger.info("Текст введён")

    for i in range(5):
        with allure.step(f"Загрузка файла {i+1}"):
            buzz_page.ADD_PHOTO.send_keys(str(IMG_2))
            time.sleep(2)
            logger.info(f"Файл {i+1} загружен")

    with allure.step("Проверка, что кнопка добавления фото скрыта"):
        assert (
            buzz_page.ADD_PHOTO.should_be_not_visible()
        ), "Кнопка добавления фото не скрыта"
        logger.info("✓ Кнопка добавления фото скрыта")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_5_uploads",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Удаление загруженных фото"):
        buzz_page.REMOVE_PHOTO_BUTTON.click()
        logger.info("Кнопка удаления фото нажата")

    with allure.step("Проверка, что кнопка добавления фото снова видима"):
        assert (
            buzz_page.ADD_PHOTO.should_be_visible()
        ), "Кнопка добавления фото не появилась после удаления"
        logger.info("✓ Кнопка добавления фото снова видима")

    with allure.step("Публикация поста"):
        buzz_page.SHARE_PHOTO_VIDEO.click()
        logger.info("Кнопка 'Share' нажата")

    with allure.step("Проверка сообщения об успешном сохранении"):
        assert buzz_page.check_message("Saved"), "Сообщение 'Saved' не появилось"
        logger.info("✓ Пост с фото опубликован")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="photo_post_success",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Ожидание появления изображения в ленте"):
        time.sleep(3)
        logger.info("Пауза 3 секунды для загрузки")

    with allure.step("Проверка отображения изображения в посте"):
        assert buzz_page.IMAGE_BLOCK.is_displayed(), "Блок изображения не виден"
        src = buzz_page.IMAGE_BLOCK.get_attribute("src")
        assert "/buzz/photo/" in src, f"Неверный src изображения: {src}"
        logger.info(f"✓ Изображение загружено, src: {src}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="final_post_with_image",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_post_photo ===")


@allure.epic("Страница Buzz")
@allure.feature("Публикация видео")
@allure.title("Публикация видео с YouTube")
@pytest.mark.skip(reason="Тест отключен из-за резкого закрытия окна диалога")
def test_post_video(buzz_page, driver, fake):
    post_text = fake.sentence()
    video_url = "https://www.youtube.com/watch?v=sDJO0EQP1Yo"
    video_id = "sDJO0EQP1Yo"

    with allure.step("Переход в раздел Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Перешли в Buzz")

    with allure.step("Открытие диалога добавления видео"):
        buzz_page.SHARE_VIDEO.click()
        logger.info("Клик по кнопке 'Share Video'")

    with allure.step("Ожидание появления поля для текста"):
        try:
            text_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    buzz_page.FIELD_POST_VIDEO_PHOTO.selector
                )
            )
            text_field.send_keys(post_text)
            logger.info(f"Введён текст поста: {post_text}")
        except TimeoutException:
            logger.error("Поле для текста не появилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="timeout_text_field",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Ввод URL видео"):
        try:
            url_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(buzz_page.VIDEO_URL.selector)
            )
            url_input.send_keys(video_url)
            logger.info(f"Введён URL видео: {video_url}")
        except TimeoutException:
            logger.error("Поле для URL не появилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="timeout_url_field",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Ожидание появления блока с превью видео"):
        try:
            video_block = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(buzz_page.VIDEO_BLOCK.selector)
            )
            logger.info("Превью видео отобразилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="video_preview",
                attachment_type=allure.attachment_type.PNG,
            )
        except TimeoutException:
            logger.error("Превью видео не появилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="no_preview",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Нажатие кнопки 'Share'"):
        buzz_page.SHARE_PHOTO_VIDEO.click()
        logger.info("Клик по кнопке Share")

    with allure.step("Ожидание сообщения об успешном сохранении"):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(text(),'Saved')]")
                )
            )
            logger.info("Сообщение 'Saved' появилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="success_message",
                attachment_type=allure.attachment_type.PNG,
            )
        except TimeoutException:
            logger.error("Сообщение 'Saved' не появилось")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="no_success",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Проверка, что видео отображается в посте"):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(buzz_page.VIDEO_BLOCK.selector)
            )
            video_block = buzz_page.VIDEO_BLOCK
            assert video_block.is_displayed(), "Блок видео не виден после публикации"
            src = video_block.get_attribute("src")
            logger.info(f"Атрибут src видео: {src}")
            assert video_id in src, f"ID видео {video_id} не найден в {src}"
            allure.attach(
                driver.get_screenshot_as_png(),
                name="final_post",
                attachment_type=allure.attachment_type.PNG,
            )
        except TimeoutException:
            logger.error("Блок видео не появился после публикации")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="post_failed",
                attachment_type=allure.attachment_type.PNG,
            )


@allure.epic("Страница Buzz")
@allure.feature("Публикация фото")
@allure.title("Проверка ошибок при загрузке фото (неверный формат и размер)")
@pytest.mark.skip(reason="Тест отключен из-за резкого закрытия окна диалога")
def test_photo_post_errors(buzz_page, driver):
    with allure.step("Переход в раздел Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Открыт раздел Buzz")

    with allure.step("Открытие диалога добавления фото"):
        buzz_page.SHARE_PHOTOS.click()
        logger.info("Клик по кнопке 'Share Photos'")

    # Первая загрузка – проверка на неверный формат
    with allure.step("Загрузка файла другого формата"):
        buzz_page.ADD_PHOTO.send_keys(str(RES))
        logger.info(f"Файл отправлен: {RES.name}")

    with allure.step("Ожидание появления алерта о неверном формате"):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(buzz_page.ALERTION.selector)
            )
            # Проверка текста алерта
            alert_text = buzz_page.ALERTION.get_text()
            assert (
                "images are allowed" in alert_text
            ), f"Текст алерта '{alert_text}' не содержит 'images are allowed'"
            logger.info("Алерт о неверном формате отобразился корректно")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="format_alert",
                attachment_type=allure.attachment_type.PNG,
            )

        except TimeoutException:
            logger.error("Алерт о неверном формате не появился")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="format_alert_missing",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Закрытие алерта"):
        buzz_page.REMOVE_ALERT_BUTTON.click()
        logger.info("Клик по кнопке закрытия алерта")

    with allure.step("Ожидание исчезновения алерта"):
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located(buzz_page.ALERTION.selector)
            )
            logger.info("Алерт исчез")
        except TimeoutException:
            logger.error("Алерт не исчез после закрытия")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="alert_still_visible",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    # Вторая загрузка – проверка на превышение размера
    with allure.step("Загрузка большого файла"):
        buzz_page.ADD_PHOTO.send_keys(str(IMG_BIG))
        logger.info("Файл отправлен повторно")

    with allure.step("Ожидание появления алерта о превышении размера"):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(buzz_page.ALERTION.selector)
            )
            alert_text = buzz_page.ALERTION.get_text()
            assert (
                "Maximum allowed file size is 2MB" in alert_text
            ), f"Текст алерта '{alert_text}' не содержит информацию о размере"
            logger.info("Алерт о превышении размера отобразился корректно")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="size_alert",
                attachment_type=allure.attachment_type.PNG,
            )

        except TimeoutException:
            logger.error("Алерт о размере не появился")

            allure.attach(
                driver.get_screenshot_as_png(),
                name="size_alert_missing",
                attachment_type=allure.attachment_type.PNG,
            )

            raise


@allure.epic("Страница Buzz")
@allure.feature("Публикация видео")
@allure.title("Проверка ошибок при публикации видео (пустое поле и невалидный URL)")
@pytest.mark.skip(reason="Тест отключен из-за резкого закрытия окна диалога")
def test_video_post_errors(buzz_page, driver):
    with allure.step("Переход в раздел Buzz"):
        buzz_page.MENU_BUZZ.click()
        logger.info("Открыт раздел Buzz")

    with allure.step("Открытие диалога добавления видео"):
        buzz_page.SHARE_VIDEO.click()
        logger.info("Клик по кнопке 'Share Video'")

    with allure.step("Нажатие кнопки 'Share' без ввода данных"):
        buzz_page.FIELD_POST_VIDEO_PHOTO.click()
        buzz_page.SHARE_PHOTO_VIDEO.click()

        logger.info("Клик по кнопке Share (без данных)")

    with allure.step("Проверить, что диалог ещё открыт после ввода URL"):
        try:
            WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located(buzz_page.VIDEO_URL.selector)
            )
        except TimeoutException:
            logger.warning("Диалог закрылся, открываем заново")
            buzz_page.SHARE_VIDEO.click()
            # Повторно вводим URL (можно сохранить значение)
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(buzz_page.VIDEO_URL.selector)
            ).send_keys(URLS.BUZZ)
            buzz_page.SHARE_PHOTO_VIDEO.click()

    with allure.step("Ожидание появления ошибки 'Required'"):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(buzz_page.ERROR_VIDEO.selector)
            )
            error_text = buzz_page.ERROR_VIDEO.get_text()
            assert (
                "Required" in error_text
            ), f"Текст ошибки '{error_text}' не содержит 'Required'"
            logger.info("Ошибка 'Required' отобразилась")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="required_error",
                attachment_type=allure.attachment_type.PNG,
            )
        except TimeoutException:
            logger.error("Ошибка 'Required' не появилась")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="required_error_missing",
                attachment_type=allure.attachment_type.PNG,
            )
            raise

    with allure.step("Ввод невалидного URL (страница Buzz)"):
        buzz_page.VIDEO_URL.fill(URLS.BUZZ)
        logger.info(f"Введён URL: {URLS.BUZZ}")

    # После ввода URL ошибка может исчезнуть, а затем появиться новая
    # Ждём появления ошибки о невалидном URL
    with allure.step("Ожидание появления ошибки о невалидном URL"):
        try:
            # Сначала ждём, что ошибка 'Required' исчезнет (необязательно)
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located(buzz_page.ERROR_VIDEO.selector)
            )
            logger.info("Ошибка 'Required' исчезла")
        except TimeoutException:
            logger.warning("Ошибка 'Required' не исчезла после ввода URL, продолжаем")

        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(buzz_page.ERROR_VIDEO.selector)
            )
            error_text = buzz_page.ERROR_VIDEO.get_text()
            assert (
                "This URL is not a valid URL" in error_text
            ), f"Текст ошибки '{error_text}' не содержит 'This URL is not a valid URL'"
            logger.info("Ошибка о невалидном URL отобразилась")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="invalid_url_error",
                attachment_type=allure.attachment_type.PNG,
            )
        except TimeoutException:
            logger.error("Ошибка о невалидном URL не появилась")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="invalid_url_error_missing",
                attachment_type=allure.attachment_type.PNG,
            )
            raise
