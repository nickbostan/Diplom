#import re

import pytest
#import pytest_check as check
#import allure

#from conftest import logger
from Diplom.page_obj.admin_block.corporate_branding import CorpBrandingPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def corp_branding_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return CorpBrandingPage(driver)



def test_corp_branding_page(corp_branding_page, driver):
    corp_branding_page.MENU_ADMIN.click()
    try:
        corp_branding_page.CORP_BRANDING.click()
    except:
        corp_branding_page.MORE.click()
        corp_branding_page.CORP_BRANDING.click()
    corp_branding_page.check_that_page_opened()
    assert corp_branding_page.driver.current_url == URLS.CORP_BRANDING


#Incorrect Dimensions
#Attachment Size Exceeded


def test_color_change(corp_branding_page, driver):
    corp_branding_page.MENU_ADMIN.click()

    try:
        corp_branding_page.CORP_BRANDING.click()
    except:
        corp_branding_page.MORE.click()
        corp_branding_page.CORP_BRANDING.click()

    # Получаем WebElement из BaseElement
    # Вариант 1: Если есть метод get_element()
    web_element = corp_branding_page.PRIMARY_COLOR.get_element()

    # Вариант 2: Если есть свойство element
    # web_element = corp_branding_page.PRIMARY_COLOR.element

    # Вариант 3: Если нужно найти элемент заново
    # web_element = driver.find_element(*corp_branding_page.PRIMARY_COLOR.locator)

    # Теперь используем web_element
    actual_color = driver.execute_script(
        "return window.getComputedStyle(arguments[0]).backgroundColor;",
        web_element
    )

    assert "rgb(255, 123, 29)" in actual_color, \
        f"Ожидался rgb(255, 123, 29), получено: {actual_color}"

#def test_custom_color(corp_branding_page, driver):
    #set_color_by_index(driver, 255, 63, 29, 0)
    #set_color_by_index(driver, 0, 255, 0, 1)


def test_all_colors_simple(driver):
    """
    Простой тест всех основных цветов для первого пикера
    """
    colors = [
        ("Черный", 0, 0, 0),
        ("Белый", 255, 255, 255),
        ("Красный", 255, 0, 0),
        ("Зеленый", 0, 255, 0),
        ("Синий", 0, 0, 255),
        ("Желтый", 255, 255, 0),
        ("Пурпурный", 255, 0, 255),
        ("Бирюзовый", 0, 255, 255),
        ("Серый", 128, 128, 128),
    ]

    print("Тестируем цвета для первого пикера:")
    print("-" * 40)

    for name, r, g, b in colors:
        print(f"{name}: ", end="")

        #if set_color_by_index(driver, r, g, b, 0):
        #    print(f"✓ Установлен RGB({r}, {g}, {b})")
       # else:
       #     print("✗ Ошибка")

    print("-" * 40)
    print("Тест завершен")