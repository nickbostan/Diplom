import allure
from playwright.sync_api import Page, expect

from conftest import logger


class BuzzPage:
    def __init__(self, page: Page):
        self.page = page
        # Основные элементы (уже были)
        self.menu_buzz = page.locator("//span[text()='Buzz']")
        self.post_field = page.locator(
            "textarea[placeholder*='on your mind']"
        )  # поле для текстового поста
        self.post_button = page.locator(
            "button[type='submit']"
        )  # кнопка отправки поста
        self.share_photos_btn = page.locator("(//button[@type='button'])[4]")
        self.share_video_btn = page.locator("(//button[@type='button'])[5]")
        self.video_url_input = page.locator("textarea[placeholder*='Paste Video URL']")
        self.share_photo_video_btn = page.locator("(//button[@type='submit'])[2]")
        self.alert_message = page.locator(".oxd-toast")  # тост об успехе
        self.alertion = page.locator(".oxd-alert-content")  # алерт для ошибок фото
        self.error_video = page.locator(
            ".oxd-input-field-error-message"
        )  # ошибка видео
        self.remove_alert_btn = page.locator(
            ".orangehrm-photo-input-remove"
        )  # кнопка закрытия алерта
        self.first_post_text = page.locator(
            "(//p[contains(@class,'post-body-text')])[1]"
        )
        self.file_input = page.locator("input[type='file']")  # скрытый input для файлов

        # Новые локаторы для тестов публикации
        self.image_block = page.locator(
            ".orangehrm-buzz-post-body img"
        ).first  # первое изображение в посте
        self.remove_photo_button = page.locator(
            ".orangehrm-photo-input-remove"
        )  # кнопка удаления фото (та же, что и для алерта)
        self.add_photo_button = page.locator(
            "(//button[@type='button'])[4]"
        )  # кнопка добавления фото (share_photos_btn)

    @allure.step("Открыть страницу Buzz")
    def open(self):
        self.menu_buzz.click()
        self.page.wait_for_url("**/buzz/viewBuzz**")
        logger.info("Страница Buzz открыта")

    @allure.step("Создать текстовый пост: {text}")
    def create_text_post(self, text: str):
        self.post_field.fill(text)
        logger.info(f"Введён текст: {text}")
        self.post_button.click()
        logger.info("Кнопка отправки нажата")

    @allure.step("Получить текст первого поста")
    def get_first_post_text(self) -> str:
        return self.first_post_text.text_content()

    @allure.step("Ожидать сообщение об успехе: {expected_text}")
    def wait_for_success_message(
        self, expected_text: str = "Saved", timeout: int = 10000
    ):
        expect(self.alert_message).to_contain_text(expected_text, timeout=timeout)
        logger.info(f"Сообщение '{expected_text}' появилось")

    @allure.step("Начать добавление фото")
    def start_photo_upload(self):
        self.share_photos_btn.click()

    @allure.step("Начать добавление видео")
    def start_video_upload(self):
        self.share_video_btn.click()

    @allure.step("Загрузить файл(ы): {file_paths}")
    def upload_files(self, file_paths):
        with self.page.expect_file_chooser() as fc_info:
            self.file_input.click()
        file_chooser = fc_info.value
        file_chooser.set_files(file_paths)
        logger.info(f"Загружено файлов: {len(file_paths)}")

    @allure.step("Ввести URL видео: {url}")
    def enter_video_url(self, url: str):
        self.video_url_input.fill(url)

    @allure.step("Нажать кнопку Share (в диалоге)")
    def click_share_in_dialog(self):
        self.share_photo_video_btn.click()

    @allure.step("Закрыть алерт")
    def close_alert(self):
        self.remove_alert_btn.click()
        expect(self.alertion).not_to_be_visible()

    @property
    def url(self) -> str:
        return self.page.url

    # Новые методы для теста с фото
    @allure.step("Проверить видимость кнопки добавления фото")
    def is_add_photo_visible(self) -> bool:
        return self.add_photo_button.is_visible()

    @allure.step("Удалить загруженное фото")
    def remove_photo(self):
        self.remove_photo_button.click()

    @allure.step("Получить src первого изображения в посте")
    def get_first_image_src(self) -> str:
        return self.image_block.get_attribute("src")

    @allure.step("Ожидать появления блока с превью видео")
    def wait_for_video_preview(self, timeout: int = 15000):
        video_block = self.page.locator(".orangehrm-buzz-post-body iframe").first
        expect(video_block).to_be_visible(timeout=timeout)
        return video_block.get_attribute("src")
