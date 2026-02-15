import time

import pytest

from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.pim_page import PIMPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def pim_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return PIMPage(driver)


@pytest.mark.smoke
def test_pim_page(pim_page, driver):
    pim_page.MENU_PIM.click()
    pim_page.check_that_page_opened()
    assert pim_page.driver.current_url == URLS.PIM


def test_fill_search_form(pim_page, driver):
    pim_page.MENU_PIM.click()
    pim_page.fill_search_form()
    status = pim_page.STATUS.get_text()
    job = pim_page.JOB_TITLE.get_text()
    sub_unit = pim_page.SUB_UNIT.get_text()
    bad_values_drop = ["-- Select --", ""]
    assert status not in bad_values_drop
    assert job not in bad_values_drop
    assert sub_unit not in bad_values_drop

    employee_name = pim_page.EMPLOYEE_NAME.get_attribute("value")
    assert employee_name != ""
    assert employee_name == "dfdfewr"


def test_reset_button(pim_page, driver):
    pim_page.MENU_PIM.click()
    pim_page.fill_search_form()
    pim_page.RESET_BUTTON.click()
    time.sleep(3)
    values_drop = ["-- Select --", ""]
    status = pim_page.STATUS.get_text()
    job = pim_page.JOB_TITLE.get_text()
    sub_unit = pim_page.SUB_UNIT.get_text()
    include = pim_page.INCLUDE.get_text()
    assert status in values_drop
    assert job in values_drop
    assert sub_unit in values_drop
    # Тут проверка на точное совпадения , так как оно стоит по дефолту
    assert include == "Current Employees Only"

    employee_name = pim_page.EMPLOYEE_NAME.get_attribute("value")
    assert employee_name == ""
    employee_placeholder = pim_page.EMPLOYEE_NAME.get_attribute("placeholder")
    assert employee_placeholder == "Type for hints..."

    employee_id = pim_page.EMPLOYEE_ID.get_attribute("value")
    assert employee_id == ""
    supervisor = pim_page.SUPERVISOR_NAME.get_attribute("value")
    assert supervisor == ""


def test_delete_in_card(pim_page, driver):
    pim_page.MENU_PIM.click()
    # first_id = pim_page.FIRST_ID.text

    pim_page.DEL_FIRST.click()
    pim_page.CONFIRMATION.click()
    assert pim_page.SUCCESS_SAVED_TOAST.should_be_visible()
    assert pim_page.SUCCESS_SAVED_TOAST.should_be_has_text("Successfully Deleted")
