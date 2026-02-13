import time

import pyautogui
import pytest
from faker import Faker

from Diplom.files import IMG_2, IMG_BIG
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


def test_buzz_page(buzz_page, driver):
    buzz_page.MENU_BUZZ.click()
    buzz_page.check_that_page_opened()
    assert buzz_page.driver.current_url == URLS.BUZZ


def test_post_text(buzz_page, driver, fake):

    post_text = fake.sentence()
    buzz_page.MENU_BUZZ.click()
    buzz_page.POST_WRITE_FIELD.fill(post_text)
    buzz_page.POST_BUTTON.click()
    assert buzz_page.check_message("Saved")
    text = buzz_page.FIRST_TEXT.get_text()
    assert text == post_text


def test_post_photo(buzz_page, driver, fake):

    post_text = fake.sentence()
    buzz_page.MENU_BUZZ.click()
    buzz_page.SHARE_PHOTOS.click()
    buzz_page.FIELD_POST_VIDEO_PHOTO.fill(post_text)
    buzz_page.ADD_PHOTO.send_keys(IMG_2)
    buzz_page.ADD_PHOTO.send_keys(IMG_2)
    buzz_page.ADD_PHOTO.send_keys(IMG_2)
    buzz_page.ADD_PHOTO.send_keys(IMG_2)
    buzz_page.ADD_PHOTO.send_keys(IMG_2)
    assert buzz_page.ADD_PHOTO.should_be_not_visible()
    buzz_page.REMOVE_PHOTO_BUTTON.click()
    assert buzz_page.ADD_PHOTO.should_be_visible()
    buzz_page.SHARE_PHOTO_VIDEO.click()
    assert buzz_page.check_message("Saved")
    time.sleep(3)
    buzz_page.IMAGE_BLOCK.is_displayed()
    src = buzz_page.IMAGE_BLOCK.get_attribute("src")
    assert "/buzz/photo/" in src


def test_post_video(buzz_page, driver, fake):

    post_text = fake.sentence()
    video = "https://www.youtube.com/watch?v=sDJO0EQP1Yo"
    buzz_page.MENU_BUZZ.click()
    buzz_page.SHARE_VIDEO.click()
    buzz_page.FIELD_POST_VIDEO_PHOTO.fill(post_text)
    time.sleep(2)
    buzz_page.VIDEO_URL.fill(video)
    time.sleep(2)
    assert buzz_page.VIDEO_BLOCK.is_displayed()
    time.sleep(3)
    buzz_page.SHARE_PHOTO_VIDEO.click()
    assert buzz_page.check_message("Saved")
    time.sleep(3)
    buzz_page.VIDEO_BLOCK.is_displayed()
    src = buzz_page.VIDEO_BLOCK.get_attribute("src")
    assert "sDJO0EQP1Yo" in src


def test_photo_post_errors(buzz_page, driver):

    buzz_page.MENU_BUZZ.click()
    buzz_page.SHARE_PHOTOS.click()
    buzz_page.ADD_PHOTO.send_keys(str(IMG_BIG))
    assert buzz_page.ALERTION.should_be_visible
    assert buzz_page.ALERTION.should_contain_text("images are allowed")
    buzz_page.REMOVE_ALERT_BUTTON.click()
    assert buzz_page.ALERTION.should_be_not_visible
    buzz_page.ADD_PHOTO.send_keys(str(IMG_BIG))
    assert buzz_page.ALERTION.should_be_visible
    assert buzz_page.ALERTION.should_contain_text("Maximum allowed file size is 2MB")


def test_video_post_errors(buzz_page, driver):

    buzz_page.MENU_BUZZ.click()
    buzz_page.SHARE_VIDEO.click()
    buzz_page.SHARE_PHOTO_VIDEO.click()
    assert buzz_page.ERROR_VIDEO.should_be_visible
    assert buzz_page.ERROR_VIDEO.should_contain_text("Required")
    buzz_page.VIDEO_URL.fill(URLS.BUZZ)
    time.sleep(4)
    assert buzz_page.ERROR_VIDEO.should_be_visible
    assert buzz_page.ERROR_VIDEO.should_contain_text("This URL is not a valid URL")
