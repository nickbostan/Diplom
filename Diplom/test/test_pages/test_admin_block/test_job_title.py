import allure
import pytest

from conftest import logger
from Diplom.page_obj.admin_block.add_job_title import AddJobTitlePage
from Diplom.page_obj.admin_block.job_title import JobTitlePage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def job_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return JobTitlePage(driver)


@pytest.fixture()
def job_add_page(driver):
    return AddJobTitlePage(driver)


@allure.epic("Страница Job Titles")
@allure.title("Открытие страницы Job Titles")
@pytest.mark.smoke
def test_job_page(job_page, driver):
    logger.info("=== Начало test_job_page ===")
    with allure.step("Перейти в раздел Admin"):
        job_page.MENU_ADMIN.click()
        logger.info("Admin нажато")

    with allure.step("Перейти в подраздел Job"):
        job_page.ADMIN_JOB.click()
        logger.info("Подраздел Job открыт")

    with allure.step("Перейти в Job Titles"):
        job_page.ADMIN_JOB_TITLES.click()
        logger.info("Страница Job Titles открыта")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="job_titles_page",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить открытие страницы"):
        job_page.check_that_page_opened()
        current_url = job_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")
        assert current_url == URLS.JOB_TITLE
        logger.info("✓ Страница Job Titles открыта")

    logger.info("=== Конец test_job_page ===")


@allure.epic("Страница Job Titles")
@allure.title("Переход на страницу добавления новой должности")
def test_add_job_page(job_add_page, job_page, driver):
    logger.info("=== Начало test_add_job_page ===")
    with allure.step("Перейти в раздел Admin"):
        job_page.MENU_ADMIN.click()
        logger.info("Admin нажато")

    with allure.step("Перейти в подраздел Job"):
        job_page.ADMIN_JOB.click()
        logger.info("Подраздел Job открыт")

    with allure.step("Перейти в Job Titles"):
        job_page.ADMIN_JOB_TITLES.click()
        logger.info("Страница Job Titles открыта")

    with allure.step("Нажать кнопку Add"):
        job_page.ADD_BUTTON.click()
        logger.info("Кнопка Add нажата")

    with allure.step("Проверить открытие страницы добавления"):
        job_add_page.check_that_page_opened()
        current_url = job_add_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")
        assert current_url == URLS.ADD_JOB_TITLE
        logger.info("✓ Страница добавления должности открыта")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="add_job_title_page",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_add_job_page ===")
