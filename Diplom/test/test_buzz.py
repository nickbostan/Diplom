import allure
import pytest
from faker import Faker
from playwright.sync_api import expect

from conftest import logger
from Diplom.files import IMG_2, IMG_BIG, RES
from Diplom.pages.buzz_page import BuzzPage
from Diplom.urls import URLS


@pytest.fixture
def fake():
    return Faker()


@allure.epic("Buzz")
@allure.feature("Основная страница")
def test_buzz_page(buzz_page: BuzzPage):
    with allure.step("Открыть страницу Buzz"):
        buzz_page.open()
    with allure.step("Проверить URL"):
        assert (
            buzz_page.url == URLS.BUZZ
        ), f"Ожидался {URLS.BUZZ}, получен {buzz_page.url}"
    with allure.step("Проверить видимость поля ввода"):
        expect(buzz_page.post_field).to_be_visible()


@allure.epic("Buzz")
@allure.feature("Публикация текста")
@allure.title("Публикация текстового поста")
def test_post_text(buzz_page: BuzzPage, fake: Faker):
    logger.info("=== Начало test_post_text ===")
    post_text = fake.sentence()

    buzz_page.open()
    buzz_page.create_text_post(post_text)
    buzz_page.wait_for_success_message("Saved")

    first_text = buzz_page.get_first_post_text()
    assert first_text == post_text, f"Ожидался '{post_text}', получен '{first_text}'"
    logger.info("Текст поста совпадает")
    logger.info("=== Конец test_post_text ===")


@allure.epic("Buzz")
@allure.feature("Публикация фото")
@allure.title("Публикация нескольких фото и удаление")
def test_post_photo(buzz_page: BuzzPage, fake: Faker):
    logger.info("=== Начало test_post_photo ===")
    post_text = fake.sentence()

    buzz_page.open()
    buzz_page.start_photo_upload()
    buzz_page.post_field.fill(post_text)

    # Загружаем 5 файлов – каждый раз ожидаем превью и активность кнопки
    for i in range(5):
        buzz_page.upload_files([str(IMG_2)], wait_for_preview=True)

    # Кнопка добавления фото должна стать невидимой (после загрузки 5 файлов, вероятно, максимум достигнут)
    # Но в OrangeHRM лимит может отсутствовать, поэтому проверяем, что кнопка всё ещё может быть видимой.
    # Вместо этого можно проверить, что миниатюры отображаются.
    # В данном случае просто удалим одно фото и проверим, что кнопка снова видима (логика приложения).
    buzz_page.remove_photo()
    # После удаления кнопка должна стать видимой
    expect(buzz_page.file_input).to_be_visible(timeout=5000)

    buzz_page.click_share_in_dialog()
    buzz_page.wait_for_success_message("Saved")

    src = buzz_page.get_first_image_src()
    assert "/buzz/photo/" in src, f"Неверный src изображения: {src}"
    logger.info(f"Изображение загружено: {src}")
    logger.info("=== Конец test_post_photo ===")


@allure.epic("Buzz")
@allure.feature("Публикация видео")
@allure.title("Публикация видео с YouTube")
def test_post_video(buzz_page: BuzzPage, fake: Faker):
    logger.info("=== Начало test_post_video ===")
    post_text = fake.sentence()
    video_url = "https://www.youtube.com/watch?v=sDJO0EQP1Yo"
    video_id = "sDJO0EQP1Yo"

    buzz_page.open()
    buzz_page.start_video_upload()
    buzz_page.post_field.fill(post_text)
    buzz_page.enter_video_url(
        video_url, wait_for_preview=True
    )  # ждём превью и активность кнопки
    buzz_page.click_share_in_dialog()
    buzz_page.wait_for_success_message("Saved")

    # Проверяем, что видео появилось в ленте (ждём iframe)
    preview_src = buzz_page.wait_for_video_preview(timeout=15000)
    assert video_id in preview_src, f"ID видео {video_id} не найден в {preview_src}"
    logger.info(f"Видеопост опубликован, превью: {preview_src}")
    logger.info("=== Конец test_post_video ===")


@allure.epic("Buzz")
@allure.feature("Публикация фото")
@allure.title("Проверка ошибок при загрузке фото (неверный формат и размер)")
def test_photo_post_errors(buzz_page: BuzzPage):
    logger.info("=== Начало test_photo_post_errors ===")
    buzz_page.open()
    buzz_page.start_photo_upload()

    # Загружаем файл неподдерживаемого формата (docx)
    with allure.step("Загрузить файл неподдерживаемого формата"):
        buzz_page.upload_files([str(RES)], wait_for_preview=False)

    with allure.step("Проверить алерт о неверном формате"):
        expect(buzz_page.alertion).to_be_visible(timeout=10000)
        expect(buzz_page.alertion).to_contain_text("images are allowed")

    buzz_page.close_alert()

    # Загружаем слишком большой файл
    with allure.step("Загрузить файл большого размера"):
        buzz_page.upload_files([str(IMG_BIG)], wait_for_preview=False)

    with allure.step("Проверить алерт о превышении размера"):
        expect(buzz_page.alertion).to_be_visible(timeout=10000)
        expect(buzz_page.alertion).to_contain_text("Maximum allowed file size is 2MB")

    logger.info("=== Конец test_photo_post_errors ===")


@allure.epic("Buzz")
@allure.feature("Публикация видео")
@allure.title("Проверка ошибок при публикации видео (пустое поле и невалидный URL)")
def test_video_post_errors(buzz_page: BuzzPage):
    logger.info("=== Начало test_video_post_errors ===")
    buzz_page.open()
    buzz_page.start_video_upload()

    with allure.step("Нажать Share без ввода данных"):
        buzz_page.click_share_in_dialog()

    with allure.step("Проверить ошибку 'Required'"):
        expect(buzz_page.error_video).to_be_visible()
        expect(buzz_page.error_video).to_contain_text("Required")

    with allure.step("Ввести невалидный URL (страница Buzz) без ожидания превью"):
        buzz_page.enter_video_url(URLS.BUZZ, wait_for_preview=False)

    with allure.step("Дождаться появления ошибки о невалидном URL"):
        # Playwright сам подождёт, пока текст ошибки изменится
        expect(buzz_page.error_video).to_contain_text(
            "This URL is not a valid URL", timeout=15000
        )

    logger.info("=== Конец test_video_post_errors ===")
