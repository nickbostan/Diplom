import time

import allure
import pytest

from conftest import logger
from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.pim_page import PIMPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def pim_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PIMPage(driver)


@allure.epic("Страница PIM")
@allure.title("Открытие страницы PIM")
@pytest.mark.smoke
def test_pim_page(pim_page, driver):
    logger.info("=== Начало test_pim_page ===")

    with allure.step("Клик по меню PIM"):
        pim_page.MENU_PIM.click()
        logger.info("PIM нажато")

    with allure.step("Проверка открытия страницы"):
        pim_page.check_that_page_opened()
        current_url = pim_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="pim_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.PIM, f"Ожидался {URLS.PIM}, получен {current_url}"
        logger.info("✓ Страница PIM открыта корректно")

    logger.info("=== Конец test_pim_page ===")


@allure.epic("Страница PIM")
@allure.title("Заполнение формы поиска")
def test_fill_search_form(pim_page, driver):
    logger.info("=== Начало test_fill_search_form ===")

    with allure.step("Переход в раздел PIM"):
        pim_page.MENU_PIM.click()
        logger.info("PIM нажато")

    with allure.step("Заполнение формы поиска"):
        pim_page.fill_search_form()
        logger.info("Форма поиска заполнена")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_form_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка значений dropdown"):
        status = pim_page.STATUS.get_text()
        job = pim_page.JOB_TITLE.get_text()
        sub_unit = pim_page.SUB_UNIT.get_text()
        bad_values_drop = ["-- Select --", ""]

        assert status not in bad_values_drop, f"Некорректное значение статуса: {status}"
        assert job not in bad_values_drop, f"Некорректное значение должности: {job}"
        assert (
            sub_unit not in bad_values_drop
        ), f"Некорректное значение подразделения: {sub_unit}"
        logger.info("✓ Выпадающие списки заполнены корректно")

    with allure.step("Проверка поля 'Employee Name'"):
        employee_name = pim_page.EMPLOYEE_NAME.get_attribute("value")
        assert employee_name != "", "Поле имени сотрудника пустое"
        assert (
            employee_name == "dfdfewr"
        ), f"Ожидалось 'dfdfewr', получено '{employee_name}'"
        logger.info(f"✓ Employee Name = '{employee_name}'")

    logger.info("=== Конец test_fill_search_form ===")


@allure.epic("Страница PIM")
@allure.title("Проверка кнопки Reset")
def test_reset_button(pim_page, driver):
    logger.info("=== Начало test_reset_button ===")

    with allure.step("Переход в раздел PIM"):
        pim_page.MENU_PIM.click()
        logger.info("PIM нажато")

    with allure.step("Заполнение формы поиска перед сбросом"):
        pim_page.fill_search_form()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="before_reset",
            attachment_type=allure.attachment_type.PNG,
        )

        logger.info("Форма заполнена")

    with allure.step("Нажатие кнопки Reset"):
        pim_page.RESET_BUTTON.click()
        logger.info("Кнопка Reset нажата")
        time.sleep(3)  # ожидание применения сброса

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_reset",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка значений выпадающих списков после сброса"):
        values_drop = ["-- Select --", ""]
        status = pim_page.STATUS.get_text()
        job = pim_page.JOB_TITLE.get_text()
        sub_unit = pim_page.SUB_UNIT.get_text()
        include = pim_page.INCLUDE.get_text()

        assert status in values_drop, f"Статус не сброшен: {status}"
        assert job in values_drop, f"Должность не сброшена: {job}"
        assert sub_unit in values_drop, f"Подразделение не сброшено: {sub_unit}"
        assert (
            include == "Current Employees Only"
        ), f"Поле Include не сброшено: {include}"
        logger.info("✓ Выпадающие списки сброшены корректно")

    with allure.step("Проверка текстовых полей после сброса"):
        employee_name = pim_page.EMPLOYEE_NAME.get_attribute("value")
        assert employee_name == "", f"Поле Employee Name не пусто: '{employee_name}'"
        employee_placeholder = pim_page.EMPLOYEE_NAME.get_attribute("placeholder")
        assert (
            employee_placeholder == "Type for hints..."
        ), f"Placeholder неверен: '{employee_placeholder}'"
        employee_id = pim_page.EMPLOYEE_ID.get_attribute("value")
        assert employee_id == "", f"Поле Employee ID не пусто: '{employee_id}'"
        supervisor = pim_page.SUPERVISOR_NAME.get_attribute("value")
        assert supervisor == "", f"Поле Supervisor Name не пусто: '{supervisor}'"
        logger.info("✓ Текстовые поля сброшены")

    logger.info("=== Конец test_reset_button ===")


@allure.epic("Страница PIM")
@allure.title("Удаление сотрудника из карточки")
def test_delete_in_card(pim_page, driver):
    logger.info("=== Начало test_delete_in_card ===")

    with allure.step("Переход в раздел PIM"):
        pim_page.MENU_PIM.click()
        logger.info("PIM нажато")

    with allure.step("Ввод ID сотрудника для поиска"):
        pim_page.EMPLOYEE_ID.fill("dfdf3433")
        logger.info("ID сотрудника введён")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="employee_id_entered",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Клик по кнопке удаления первого сотрудника"):
        pim_page.DEL_FIRST.click()
        logger.info("Кнопка удаления нажата")

    with allure.step("Подтверждение удаления в диалоге"):
        pim_page.CONFIRMATION.click()
        logger.info("Удаление подтверждено")

    with allure.step("Проверка сообщения об успешном удалении"):
        assert pim_page.check_message("Deleted"), "Сообщение 'Deleted' не появилось"
        logger.info("✓ Сообщение  появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="delete_success",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_delete_in_card ===")
