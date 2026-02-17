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
    # Дополнительно можно проверить видимость ключевых элементов
    buzz_page.post_field.wait_for(state="visible")
    expect(buzz_page.post_field).to_be_visible()


@allure.epic("Buzz")
@allure.feature("Публикация текста")
@allure.title("Публикация текстового поста")
def test_post_text(buzz_page: BuzzPage, fake: Faker):
    logger.info("=== Начало test_post_text ===")

    post_text = fake.sentence()
    with allure.step("Открыть страницу Buzz"):
        buzz_page.open()

    with allure.step(f"Создать пост с текстом: {post_text}"):
        buzz_page.create_text_post(post_text)

    with allure.step("Проверить появление сообщения об успехе"):
        buzz_page.wait_for_success_message("Saved")

    with allure.step("Проверить текст первого поста"):
        first_text = buzz_page.get_first_post_text()
        assert (
            first_text == post_text
        ), f"Ожидался '{post_text}', получен '{first_text}'"
        logger.info("Текст поста совпадает")

    logger.info("=== Конец test_post_text ===")


@allure.epic("Buzz")
@allure.feature("Публикация фото")
@allure.title("Публикация нескольких фото и удаление")
def test_post_photo(buzz_page: BuzzPage, fake: Faker):
    logger.info("=== Начало test_post_photo ===")

    post_text = fake.sentence()
    with allure.step("Открыть страницу Buzz"):
        buzz_page.open()

    with allure.step("Открыть диалог добавления фото"):
        buzz_page.start_photo_upload()

    with allure.step("Ввести текст поста"):
        buzz_page.post_field.fill(
            post_text
        )  # поле то же, что и для текстового поста, но в диалоге
        logger.info(f"Текст: {post_text}")

    # Загружаем 5 раз один и тот же файл (имитация множественной загрузки)
    for i in range(5):
        with allure.step(f"Загрузить файл {i+1}"):
            buzz_page.upload_files([str(IMG_2)])

    with allure.step("Проверить, что кнопка добавления фото стала невидимой"):
        assert (
            not buzz_page.is_add_photo_visible()
        ), "Кнопка добавления фото должна быть скрыта"

    with allure.step("Удалить загруженные фото"):
        buzz_page.remove_photo()
        # После удаления кнопка должна снова стать видимой
        expect(buzz_page.add_photo_button).to_be_visible(timeout=5000)
        logger.info("Кнопка снова видима")

    with allure.step("Опубликовать пост"):
        buzz_page.click_share_in_dialog()

    with allure.step("Проверить сообщение об успехе"):
        buzz_page.wait_for_success_message("Saved")

    with allure.step("Проверить, что изображение отображается в посте"):
        # Небольшая пауза для загрузки страницы после публикации
        buzz_page.page.wait_for_timeout(3000)
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

    with allure.step("Открыть страницу Buzz"):
        buzz_page.open()

    with allure.step("Открыть диалог добавления видео"):
        buzz_page.start_video_upload()

    with allure.step("Ввести текст поста"):
        buzz_page.post_field.fill(post_text)
        logger.info(f"Текст поста: {post_text}")

    with allure.step(f"Ввести URL видео: {video_url}"):
        buzz_page.enter_video_url(video_url)

    with allure.step("Ожидать появления превью видео"):
        preview_src = buzz_page.wait_for_video_preview()
        logger.info(f"Превью видео: {preview_src}")

    with allure.step("Нажать Share"):
        buzz_page.click_share_in_dialog()

    with allure.step("Проверить сообщение об успехе"):
        buzz_page.wait_for_success_message("Saved")

    with allure.step("Проверить, что видео отображается в посте"):
        buzz_page.page.wait_for_timeout(3000)  # небольшая задержка для обновления ленты
        video_frame = buzz_page.page.locator(".orangehrm-buzz-post-body iframe").first
        src = video_frame.get_attribute("src")
        logger.info(f"SRC видео: {src}")
        assert video_id in src, f"ID видео {video_id} не найден в {src}"

    logger.info("=== Конец test_post_video ===")


@allure.epic("Buzz")
@allure.feature("Публикация фото")
@allure.title("Проверка ошибок при загрузке фото (неверный формат и размер)")
def test_photo_post_errors(buzz_page: BuzzPage):
    buzz_page.open()

    with allure.step("Открыть диалог добавления фото"):
        buzz_page.start_photo_upload()

    with allure.step("Загрузить файл другого формата"):
        buzz_page.upload_files(str(RES))

    with allure.step("Проверить появление алерта о неверном формате"):
        expect(buzz_page.alertion).to_be_visible(timeout=10000)
        expect(buzz_page.alertion).to_contain_text("images are allowed")

    with allure.step("Закрыть алерт"):
        buzz_page.close_alert()
        expect(buzz_page.alertion).not_to_be_visible()

    with allure.step("Повторно загрузить тот же файл"):
        buzz_page.upload_files(str(IMG_BIG))

    with allure.step("Проверить появление алерта о превышении размера"):
        expect(buzz_page.alertion).to_be_visible()
        expect(buzz_page.alertion).to_contain_text("Maximum allowed file size is 2MB")


@allure.epic("Buzz")
@allure.feature("Публикация видео")
@allure.title("Проверка ошибок при публикации видео (пустое поле и невалидный URL)")
def test_video_post_errors(buzz_page: BuzzPage):
    buzz_page.open()

    with allure.step("Открыть диалог добавления видео"):
        buzz_page.start_video_upload()

    with allure.step("Нажать Share без ввода данных"):
        buzz_page.click_share_in_dialog()

    with allure.step("Проверить появление ошибки 'Required'"):
        expect(buzz_page.error_video).to_be_visible()
        expect(buzz_page.error_video).to_contain_text("Required")

    with allure.step("Ввести невалидный URL (страница Buzz)"):
        buzz_page.enter_video_url(URLS.BUZZ)

    with allure.step("Дождаться появления ошибки о невалидном URL"):
        # После ввода URL ошибка 'Required' исчезает и появляется новая
        expect(buzz_page.error_video).to_contain_text(
            "This URL is not a valid URL", timeout=15000
        )
