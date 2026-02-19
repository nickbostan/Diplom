import time

import allure
import pytest
from faker import Faker

from conftest import logger
from Diplom.files import BIG_FILE, IMG_2, RES
from Diplom.page_obj.login_page import LoginPage
from Diplom.page_obj.recruitment_block.add_candidate_page import CandidateAddPage
from Diplom.page_obj.recruitment_block.recruitment_page import RecruitmentPage
from Diplom.urls import URLS


@pytest.fixture(scope="function")
def recruitment_page(driver):
    login_page = LoginPage(driver)
    login_page.open_page()
    login_page.login("Admin", "admin123")

    return RecruitmentPage(driver)


@pytest.fixture()
def add_candidates(driver):
    return CandidateAddPage(driver)


@pytest.fixture
def fake():
    return Faker()


# Блок статичных данных для тестов
fakes = Faker()
TEST_NAME = fakes.first_name()
TEST_LAST = fakes.last_name()
TEST_MAIL = fakes.email()


@allure.epic("Страница Recruitment")
@allure.title("Открытие страницы Recruitment")
@pytest.mark.smoke
def test_recruitment_page(recruitment_page, driver):
    logger.info("=== Начало test_recruitment_page ===")
    with allure.step("Клик по меню Recruitment"):
        recruitment_page.MENU_RECRUITMENT.click()
        logger.info("Recruitment нажато")

    with allure.step("Проверка открытия страницы"):
        recruitment_page.check_that_page_opened()
        current_url = recruitment_page.driver.current_url
        logger.info(f"Текущий URL: {current_url}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="recruitment_page_opened",
            attachment_type=allure.attachment_type.PNG,
        )

        assert current_url == URLS.RECRUITMENT
        logger.info("✓ Страница Recruitment открылась")

    logger.info("=== Конец test_recruitment_page ===")


@allure.epic("Страница Recruitment")
@allure.title("Переход на страницу добавления кандидата и возврат назад")
def test_add_button(add_candidates, recruitment_page, driver):
    logger.info("=== Начало test_add_button ===")
    with allure.step("Открыть страницу Recruitment"):
        recruitment_page.MENU_RECRUITMENT.click()
        logger.info("Recruitment нажато")

    with allure.step("Нажать кнопку Add"):
        recruitment_page.ADD_BUTTON.click()
        logger.info("Кнопка Add нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_add_click",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка открытия страницы добавления кандидата"):
        add_candidates.check_that_page_opened()
        current_url = add_candidates.driver.current_url
        logger.info(f"URL страницы добавления: {current_url}")
        assert current_url == URLS.RECRUITMENT_ADD
        logger.info("✓ Страница добавления кандидата открыта корректно")

    with allure.step("Нажать кнопку Cancel"):
        add_candidates.CANCEL_BUTTON.click()
        logger.info("Кнопка Cancel нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_cancel_click",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверка возврата на страницу Recruitment"):
        recruitment_page.check_that_page_opened()
        current_url = recruitment_page.driver.current_url
        logger.info(f"URL после отмены: {current_url}")
        assert current_url == URLS.RECRUITMENT
        logger.info("✓ Возврат на страницу Recruitment выполнен")

    logger.info("=== Конец test_add_button ===")


@allure.epic("Страница Recruitment")
@allure.title("Простое добавление кандидата")
def test_simple_add(add_candidates, recruitment_page, fake, driver):
    logger.info("=== Начало test_simple_add ===")
    with allure.step("Открыть страницу Recruitment и нажать Add"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        logger.info("Переход на форму добавления кандидата")

    with allure.step("Генерация тестовых данных"):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.safe_email()
        logger.info(f"Данные: {first_name} {last_name}, {email}")

    with allure.step("Заполнение обязательных полей"):
        add_candidates.FIRST_NAME.fill(first_name)
        add_candidates.LAST_NAME.fill(last_name)
        add_candidates.EMAIL.fill(email)
        logger.info("Поля заполнены")

    with allure.step("Сохранить кандидата"):
        add_candidates.SAVE_BUTTON.click()
        logger.info("Кнопка Save нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="after_save_simple",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Проверить сообщение об успехе"):
        assert add_candidates.check_message("Saved")
        logger.info("✓ Сообщение появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="save_success_simple",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_simple_add ===")


@allure.epic("Страница Recruitment")
@allure.title("Полный цикл добавления кандидата")
def test_add_candidate_workflow(add_candidates, recruitment_page, fake, driver):
    logger.info("=== Начало test_add_candidate_workflow ===")
    with allure.step("Открыть страницу Recruitment и нажать Add"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        logger.info("Переход на форму добавления кандидата")

    with allure.step("Генерация тестовых данных"):
        email = fake.safe_email()
        first_name = fake.first_name()
        middle_name = fake.first_name()
        last_name = fake.last_name()
        phone = fake.numerify("(###) ###-####")
        keywords = fake.words(nb=3)
        notes = fake.sentences(nb=4)
        date = fake.date(pattern="%Y-%d-%m")
        logger.info(
            f"Данные: {first_name} {middle_name} {last_name}, {email}, {phone}, дата {date}"
        )

    with allure.step("Заполнить все поля кандидата (метод add_candidate)"):
        add_candidates.add_candidate(
            email, first_name, middle_name, last_name, phone, keywords, notes, date
        )
        logger.info("Основные поля заполнены")

    with allure.step("Загрузить резюме"):
        add_candidates.RESUME.send_keys(str(RES))
        logger.info(f"Файл резюме загружен: {RES}")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="resume_uploaded",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Сохранить кандидата"):
        add_candidates.SAVE_BUTTON.click()
        logger.info("Кнопка Save нажата")

    with allure.step("Проверить сообщение об успехе"):
        assert add_candidates.check_message("Saved")
        logger.info("✓ Сообщение  появилось")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="save_success_full",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_add_candidate_workflow ===")


@allure.epic("Страница Recruitment")
@allure.title("Сворачивание/разворачивание панели фильтров")
def test_panel_filter(recruitment_page, driver):
    logger.info("=== Начало test_panel_filter ===")
    with allure.step("Открыть страницу Recruitment"):
        recruitment_page.MENU_RECRUITMENT.click()
        logger.info("Recruitment нажато")

    with allure.step("Свернуть панель фильтров"):
        recruitment_page.RECRUITMENT_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров свернута")

    with allure.step("Проверить, что поле Candidate Name скрыто"):
        assert recruitment_page.CANDIDATE_NAME.should_be_not_visible()
        logger.info("✓ Поле Candidate Name не видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_collapsed",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Развернуть панель фильтров"):
        recruitment_page.RECRUITMENT_LIST_FILTER_PANEL.click()
        logger.info("Панель фильтров развернута")

    with allure.step("Проверить, что поле Candidate Name стало видимым"):
        recruitment_page.CANDIDATE_NAME.should_be_visible()
        logger.info("✓ Поле Candidate Name видно")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="filter_panel_expanded",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_panel_filter ===")


@allure.epic("Страница Recruitment")
@allure.title("Проверка поиска и отображения количества записей")
def test_search_button_and_count(recruitment_page, driver):
    logger.info("=== Начало test_search_button_and_count ===")
    with allure.step("Открыть страницу Recruitment"):
        recruitment_page.MENU_RECRUITMENT.click()
        logger.info("Recruitment нажато")

    with allure.step("Нажать кнопку Search"):
        recruitment_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_clicked",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(3)

    with allure.step("Получить количество записей и текст счётчика"):
        count = recruitment_page.get_records_count()
        text = recruitment_page.COUNT.get_text()
        logger.info(f"Количество записей: {count}, текст счётчика: '{text}'")

    with allure.step("Проверить соответствие количества и текста"):
        if count > 0:
            assert count > 0 and "Records Found" in text
            logger.info(f"✓ Найдено {count} записей, текст содержит 'Records Found'")
        else:
            assert "No records" in text
            logger.info("✓ Нет записей, текст содержит 'No records'")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_results",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_search_button_and_count ===")


@allure.epic("Страница Recruitment")
@allure.title("Поиск созданного кандидата по имени")
def test_search_fields(add_candidates, recruitment_page, fake, driver):
    logger.info("=== Начало test_search_fields ===")
    with allure.step("Создать нового кандидата"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.safe_email()
        add_candidates.FIRST_NAME.fill(first_name)
        add_candidates.LAST_NAME.fill(last_name)
        add_candidates.EMAIL.fill(email)
        add_candidates.SAVE_BUTTON.click()
        logger.info(f"Кандидат {first_name} {last_name} создан")
        assert add_candidates.check_message("Saved")
        logger.info("✓ Сохранение подтверждено")

    time.sleep(2)

    with allure.step("Перейти на страницу Recruitment и выполнить поиск по имени"):
        driver.get(URLS.RECRUITMENT)
        recruitment_page.input_search()
        recruitment_page.CANDIDATE_NAME.fill(first_name)
        logger.info(f"Поле имени заполнено значением '{first_name}'")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="search_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(3)

    with allure.step("Выбрать первого найденного кандидата"):
        recruitment_page.FIRST_FOUND_CANDIDATE.click()
        logger.info("Клик по первому найденному кандидату")

    with allure.step("Изменить статус на 'Job Offered' и выполнить поиск"):
        recruitment_page.STATUS_DROPDOWN.select_from_dropdown("Job Offered")
        recruitment_page.SEARCH_BUTTON.click()
        logger.info("Поиск по статусу 'Job Offered' выполнен")

    with allure.step("Проверить, что статус отображается в поле"):
        assert recruitment_page.STATUS_DROPDOWN.should_contain_text("Job Offered")
        logger.info("✓ Статус 'Job Offered' отображается в поле фильтра")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="status_filtered",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_search_fields ===")


@allure.epic("Страница Recruitment")
@allure.title("Проверка ошибок при загрузке файла")
def test_input_file_errors(add_candidates, recruitment_page, driver):
    logger.info("=== Начало test_input_file_errors ===")
    with allure.step("Открыть страницу добавления кандидата"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        logger.info("Форма добавления открыта")

    with allure.step("Загрузить файл с недопустимым расширением"):
        add_candidates.RESUME.send_keys(str(IMG_2))
        logger.info(f"Файл {IMG_2} выбран")
        is_error_visible = add_candidates.check_that_error_is_visible(
            "File type not allowed"
        )
        assert is_error_visible
        logger.info("✓ Ошибка 'File type not allowed' отобразилась")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="file_type_error",
            attachment_type=allure.attachment_type.PNG,
        )

    time.sleep(3)

    with allure.step("Загрузить файл с превышением допустимого размера"):
        add_candidates.RESUME.send_keys(str(BIG_FILE))
        logger.info(f"Файл {BIG_FILE} выбран")
        is_big_error_visible = add_candidates.check_that_error_is_visible(
            "Attachment Size Exceeded"
        )
        assert is_big_error_visible
        logger.info("✓ Ошибка 'Attachment Size Exceeded' отобразилась")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="file_size_error",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_input_file_errors ===")


@allure.epic("Страница Recruitment")
@allure.title("Проверка ошибок ввода дат: from={from_date}, to={to_date}")
@pytest.mark.parametrize(
    "from_date, to_date, expected",
    [
        ("2026-05-02", "2026-04-02", "To date should be after from date"),
        ("2026-05-02", "2026-04-02", "From date should be before to date"),
        ("2026-03-02", "error", "valid date in yyyy-dd-mm format"),
        ("error", "2026-04-02", "valid date in yyyy-dd-mm format"),
    ],
)
def test_search_input_date_errors(
    recruitment_page, driver, from_date, to_date, expected
):
    logger.info(
        f"=== Начало test_search_input_date_errors с параметрами {from_date}, {to_date}, {expected} ==="
    )
    with allure.step("Открыть страницу Recruitment"):
        recruitment_page.MENU_RECRUITMENT.click()
        logger.info("Меню Recruitment нажато")

    with allure.step(f"Заполнить поля дат: from={from_date}, to={to_date}"):
        if "From date should be before to date" in expected:
            recruitment_page.TO_DATE.fill(to_date)
            recruitment_page.FROM_DATE.fill(from_date)
            logger.info("Поля заполнены в обратном порядке")
        else:
            recruitment_page.FROM_DATE.fill(from_date)
            recruitment_page.TO_DATE.fill(to_date)
            logger.info("Поля заполнены в прямом порядке")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="dates_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step("Нажать кнопку Search"):
        recruitment_page.SEARCH_BUTTON.click()
        logger.info("Кнопка Search нажата")

    with allure.step(f"Проверить наличие ошибки '{expected}'"):
        is_error_visible = recruitment_page.check_that_error_is_visible(expected)
        assert is_error_visible
        logger.info(f"✓ Ошибка '{expected}' отобразилась")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="date_error_shown",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_search_input_date_errors ===")


@allure.epic("Страница Recruitment")
@allure.title("Проверка ошибок обязательных полей и формата email")
@pytest.mark.parametrize(
    "first_name, last_name, email, expected",
    [
        ("", TEST_LAST, TEST_MAIL, "Required"),
        (TEST_NAME, "", TEST_MAIL, "Required"),
        (TEST_NAME, TEST_LAST, "", "Required"),
        (TEST_NAME, TEST_LAST, "error", "Expected format: admin@example.com"),
    ],
)
def test_input_field_error(
    add_candidates, recruitment_page, driver, first_name, last_name, email, expected
):
    logger.info(
        f"=== Начало test_input_field_error с {first_name}, {last_name}, {email}, {expected} ==="
    )
    with allure.step("Открыть страницу добавления кандидата"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        logger.info("Форма добавления открыта")

    with allure.step(
        f"Заполнить поля: first='{first_name}', last='{last_name}', email='{email}'"
    ):
        add_candidates.FIRST_NAME.fill(first_name)
        add_candidates.LAST_NAME.fill(last_name)
        add_candidates.EMAIL.fill(email)

        allure.attach(
            driver.get_screenshot_as_png(),
            name="fields_filled",
            attachment_type=allure.attachment_type.PNG,
        )

    with allure.step(f"Проверить появление ошибки '{expected}'"):
        is_error_visible = add_candidates.check_that_error_is_visible(expected)
        assert is_error_visible
        logger.info(f"✓ Ошибка '{expected}' отобразилась")

        allure.attach(
            driver.get_screenshot_as_png(),
            name="error_shown",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_input_field_error ===")


@allure.epic("Страница Recruitment")
@allure.title("Проверка ошибки ввода номера телефона (нецифровые символы)")
def test_number_input_error(add_candidates, recruitment_page, driver):
    logger.info("=== Начало test_number_input_error ===")
    with allure.step("Открыть страницу добавления кандидата"):
        recruitment_page.MENU_RECRUITMENT.click()
        recruitment_page.ADD_BUTTON.click()
        logger.info("Форма добавления открыта")

    with allure.step("Ввести некорректный номер телефона 'dad'"):
        add_candidates.CONTACT_NUMBER.fill("dad")
        logger.info("Поле Contact Number заполнено")

    with allure.step("Проверить ошибку 'Allows numbers and only +'"):
        is_error_visible = add_candidates.check_that_error_is_visible(
            "Allows numbers and only +"
        )
        assert is_error_visible
        logger.info("✓ Ошибка  отобразилась")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="phone_error",
            attachment_type=allure.attachment_type.PNG,
        )

    logger.info("=== Конец test_number_input_error ===")
