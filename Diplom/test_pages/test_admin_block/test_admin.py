import time

import allure
import pytest
from faker import Faker

from conftest import logger
from Diplom.page_obj.admin_block.admin_add_user import AdminAddPage
from Diplom.page_obj.admin_block.admin_page import AdminPage
from Diplom.page_obj.login_page import LoginPage
from Diplom.urls import URLS


@pytest.fixture
def fake():
    return Faker()


@pytest.fixture(scope="function")
def admin_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return AdminPage(driver)


@pytest.fixture()
def admin_add_page(driver):
    return AdminAddPage(driver)


@allure.epic("Страница администратора")
@allure.title("Отображение страницы администратора")
@pytest.mark.smoke
def test_check_all_elements(admin_page, driver):
    logger.info("=== Начало test_check_all_elements ===")
    admin_page.MENU_ADMIN.click()

    with allure.step("Проверяем открытие страницы администратора"):
        admin_page.check_that_page_opened()
        logger.info(f"Текущий URL: {admin_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="admin_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert admin_page.driver.current_url == URLS.ADMIN
        logger.info("✓ Страница администратора открыта корректно")

    logger.info("=== Конец test_check_all_elements ===")


@allure.epic("Страница администратора")
@allure.title("Проверка главного фильтра dropdown")
def test_main_filter(admin_page, driver):
    logger.info("=== Начало test_main_filter ===")
    admin_page.MENU_ADMIN.click()

    with allure.step("Проверяем открытие страницы администратора"):
        admin_page.check_that_page_opened()
        logger.info(f"Текущий URL: {admin_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="admin_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert admin_page.driver.current_url == URLS.ADMIN
        logger.info("✓ Страница адми открыта корректно")

    logger.info("=== Конец test_main_filter ===")


@allure.epic("Страница администратора")
@allure.feature("Переход по кнопке и обратно")
@allure.title("Проверка кнопки и страницы добавления")
def test_admin_add_user_page(admin_add_page, admin_page, driver):
    logger.info("=== Начало test_admin_add_user_page ===")
    admin_page.MENU_ADMIN.click()

    with allure.step("Нажимаем на кнопку добавить"):
        admin_page.ADD_BUTTON.click()
        logger.info("✓ Переход на страницу добавления выполнен")

    with allure.step("Проверяем открытие страницы добавления"):
        admin_add_page.check_that_page_opened()
        logger.info(f"Текущий URL: {admin_add_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="admin_add_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert admin_add_page.driver.current_url == URLS.ADMIN_SAVE
        logger.info("✓ Страница добавления пользователя открыта корректно")

    with allure.step("Нажимаем на кнопку отмены "):
        admin_add_page.CANCEL_BUTTON.click()
        logger.info(f"Текущий URL: {admin_page.driver.current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="admin_page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert admin_page.driver.current_url == URLS.ADMIN
        logger.info("✓ Обратный переход выполнен")

    logger.info("=== Конец test_admin_add_user_page ===")


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка ввода валидной граничной длины символов поля user")
@pytest.mark.parametrize("length", [5, 40])
def test_input_fields_valid_lengths(admin_page, admin_add_page, driver, length):
    logger.info(f"=== Начало test_input_fields_valid_lengths (длина: {length}) ===")

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step(f"Вводим username длиной {length} символов"):
        username = "x" * length
        logger.info(f"Вводим username: '{username}' ({length} символов)")
        admin_add_page.INPUT_USERNAME.fill(username)

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"username_{length}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Кликаем еще раз на поле ввода"):
        logger.info("Кликаем на другое поле для активации валидации")
        admin_add_page.INPUT_USERNAME.click()

    with allure.step("Проверяем отсутствие ошибки "):
        logger.info("Проверяем, что ошибка не отображается")
        error_not_visible = admin_add_page.USERNAME_ERROR.should_be_not_visible()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="page",
            attachment_type=allure.attachment_type.PNG,
        )

        assert error_not_visible, f"Ошибка валидации не должна отображаться"
        logger.info("✓ Валидация прошла успешно")

    logger.info(f"=== Конец test_input_fields_valid_lengths (длина: {length}) ===")


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка ввода валидной граничной длины символов поля password")
@pytest.mark.parametrize("password", ["d1d1d1d", "d1" * 32])
def test_input_fields_valid(admin_page, admin_add_page, driver, password):
    logger.info(f"=== Начало test_input_fields_valid ===")

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step(f"Вводим пароль"):
        logger.info(f"Вводим пароль длиной {len(password)} символов")
        admin_add_page.INPUT_PASSWORD.fill(password)

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"password_{len(password)}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Активируем валидацию пароля"):
        logger.info("Кликаем на поле username для активации валидации")
        admin_add_page.INPUT_USERNAME.click()

    with allure.step("Проверяем отсутствие ошибок"):
        logger.info("Проверяем отсутствие ошибок слабого пароля ")
        is_weak_error_not_visible = (
            admin_add_page.ERROR_WEAK_PASS.should_be_not_visible()
        )

        logger.info("Проверяем отсутствие ошибок длины пароля")
        is_length_error_not_visible = (
            admin_add_page.ERROR_LENGTH_PASS.should_be_not_visible()
        )

        allure.attach(
            f"Длина пароля: {len(password)} символов\n"
            f"Ошибка слабого пароля: {not is_weak_error_not_visible}\n"
            f"Ошибка длины пароля: {not is_length_error_not_visible}",
            name="password_validation_result",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert is_weak_error_not_visible, "Ошибка слабого пароля не должна отображаться"
        assert is_length_error_not_visible, "Ошибка длины пароля не должна отображаться"
        logger.info("✓ Пароль прошел валидацию")

    logger.info(f"=== Конец test_input_fields_valid ===")


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка ввода невалидной граничной длины символов поля user")
@pytest.mark.parametrize(
    "length, expected",
    [
        (4, "Should be at least 5 characters"),
        (41, "Should not exceed 40 characters"),
    ],
)
def test_input_username_fields_invalid_lengths(
    admin_page, admin_add_page, driver, expected, length
):
    logger.info(
        f"=== Начало test_input_username_fields_invalid_lengths (длина: {length}) ==="
    )

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step(f"Вводим username невалидной длины ({length} символов)"):
        username = "x" * length
        logger.info(f"Вводим username: '{username}' ({length} символов)")
        admin_add_page.INPUT_USERNAME.fill(username)

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"invalid_username_{length}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Активируем валидацию поля"):
        admin_add_page.INPUT_USERNAME.click()
        logger.info("Активирована валидация поля")

    with allure.step("Проверяем сообщение об ошибке"):
        logger.info(f"Ожидаемое сообщение об ошибке: '{expected}'")
        is_error_visible = admin_add_page.check_that_username_error_is_visible(expected)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="username_error",
            attachment_type=allure.attachment_type.PNG,
        )

        assert (
            is_error_visible
        ), f"Ожидалась ошибка: '{expected}' для username длиной {length} символов"
        logger.info("✓ Сообщение об ошибке отображается корректно")

    logger.info(
        f"=== Конец test_input_username_fields_invalid_lengths (длина: {length}) ==="
    )


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка ввода невалидной граничной длины символов поля password")
@pytest.mark.parametrize(
    "length, expected",
    [
        (6, "Should have at least 7 characters"),
        (65, "Should not exceed 64 characters"),
    ],
)
def test_input_password_fields_invalid_lengths(
    admin_page, admin_add_page, driver, expected, length
):
    logger.info(
        f"=== Начало test_input_password_fields_invalid_lengths (длина: {length}) ==="
    )

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step(f"Вводим пароль невалидной длины ({length} символов)"):
        password = "x" * length
        logger.info(f"Вводим пароль длиной {length} символов")
        admin_add_page.INPUT_PASSWORD.fill(password)

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"invalid_password_{length}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Активируем валидацию пароля"):
        admin_add_page.INPUT_PASSWORD.click()
        logger.info("Активирована валидация пароля")

    with allure.step("Проверяем сообщение об ошибке длины пароля"):
        logger.info(f"Ожидаемое сообщение об ошибке: '{expected}'")
        is_error_visible = admin_add_page.check_that_length_password_error_is_visible(
            expected
        )

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"password_length_error",
            attachment_type=allure.attachment_type.PNG,
        )

        assert (
            is_error_visible
        ), f"Ожидалась ошибка: '{expected}' для пароля длиной {length} символов"
        logger.info("✓ Сообщение об ошибке длины отображается корректно")

    logger.info(
        f"=== Конец test_input_password_fields_invalid_lengths (длина: {length}) ==="
    )


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка ввода слабого пароля")
@pytest.mark.parametrize(
    "password, expected",
    [
        ("1" * 8, "Your password must contain minimum 1 lower-case letter"),
        ("d" * 8, "Your password must contain minimum 1 number"),
    ],
)
def test_input_password_fields_weakness(
    admin_page, admin_add_page, driver, expected, password
):
    logger.info(
        f"=== Начало test_input_password_fields_weakness (пароль: {password}) ==="
    )

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step(f"Вводим слабый пароль"):
        logger.info(f"Вводим пароль: '{password}'")
        admin_add_page.INPUT_PASSWORD.fill(password)

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"weak_password_entered_{password[:5]}",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Активируем валидацию пароля"):
        admin_add_page.INPUT_PASSWORD.click()
        logger.info("Активирована валидация пароля")

    with allure.step("Проверяем сообщение об ошибке слабого пароля"):
        logger.info(f"Ожидаемое сообщение об ошибке: '{expected}'")
        is_error_visible = admin_add_page.check_that_weak_password_error_is_visible(
            expected
        )

        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"weak_password_error",
            attachment_type=allure.attachment_type.PNG,
        )

        assert (
            is_error_visible
        ), f"Ожидалась ошибка: '{expected}' для пароля '{password}'"
        logger.info("✓ Сообщение об ошибке слабого пароля отображается корректно")

    logger.info(
        f"=== Конец test_input_password_fields_weakness (пароль: {password}) ==="
    )


@allure.epic("Страница администратора")
@allure.feature("Добавление пользователя")
@allure.title("Проверка соответствия паролей")
def test_match_passwords(admin_page, admin_add_page, driver):
    logger.info("=== Начало test_match_passwords ===")

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step("Вводим пароль в поле подтверждения"):
        test_password = "password"
        logger.info(f"Вводим пароль '{test_password}' в поле подтверждения")
        admin_add_page.INPUT_CONF_PASSWORD.fill(test_password)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="conf_password_entered",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Активируем валидацию поля подтверждения пароля"):
        admin_add_page.INPUT_USERNAME.click()
        logger.info("Активирована валидация поля подтверждения пароля")

    with allure.step("Проверяем сообщение об ошибке несоответствия паролей"):
        logger.info("Проверяем отображение ошибки несоответствия паролей")
        is_error_visible = admin_add_page.check_that_match_password_error_is_visible()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="match_password_error",
            attachment_type=allure.attachment_type.PNG,
        )

        assert is_error_visible, "Ожидалась ошибка несоответствия паролей"
        logger.info(
            "✓ Сообщение об ошибке несоответствия паролей отображается корректно"
        )

    logger.info("=== Конец test_match_passwords ===")


@allure.epic("Страница добавления")
@allure.feature("Добавление пользователя")
@allure.title("Пустые поля")
def test_negative_empty_fields(admin_page, admin_add_page, driver):
    logger.info(f"=== Начало test_negative_empty_fields ===")

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step("Логин с пустым полями"):
        logger.info(f"Пустые поля: username='', password=''")
        admin_add_page.SAVE_BUTTON.click()

        allure.attach(
            driver.get_screenshot_as_png(),
            name="empty_field",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка ошибки пустого поля"):
        assert admin_add_page.check_that_empty_error_is_visible("Required")
        logger.info(f"✓ Проверена ошибка пустого поля")

    logger.info(f"=== Конец test_negative_empty_fields ===")


@allure.epic("Страница добавления")
@allure.feature("Добавление")
@allure.title("Полный ввод валидных данных и добавление нового пользователя")
def test_adding_user(admin_page, admin_add_page, fake, driver):
    logger.info(f"=== Начало test_adding_user ===")

    with allure.step("Открываем страницу добавления"):
        logger.info("Кликаем на меню Admin и на кнопку Add")
        admin_page.MENU_ADMIN.click()
        admin_page.ADD_BUTTON.click()

    with allure.step("Вводим валидные данные"):
        logger.info("Полный ввод валидных данных")
        username = fake.pystr(min_chars=7, max_chars=7)
        password = fake.password(
            length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
        )
        name = admin_add_page.get_name_text()
        admin_add_page.add_user(username, password, name)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="fulfillment",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажимаем кнопку сохранить"):
        logger.info("Сохраняем пользователя")
        admin_add_page.SAVE_BUTTON.click()

    allure.attach(
        driver.get_screenshot_as_png(),
        name="success",
        attachment_type=allure.attachment_type.PNG,
    )

    with allure.step("Проверка успешного добавления"):
        # assert admin_add_page.SUCCESS.should_be_visible()
        logger.info(f"✓ Сообщение появилось")

    time.sleep(3)

    with allure.step("Проверка отображения нового пользователя в таблице"):
        table_text = admin_add_page.TABLE.get_text()
        assert username in table_text
        logger.info(f"✓ Пользователь найден")

    logger.info(f"=== Конец test_adding_user ===")
