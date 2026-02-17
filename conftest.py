import logging
import os
import re
from datetime import datetime

import pytest
from playwright.sync_api import Page, sync_playwright


# -------------------------------------------------------------------
# Логирование
# -------------------------------------------------------------------
def create_logger():
    logger = logging.getLogger()

    logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logger.setLevel(level_map.get(logger_level, logging.INFO))

    log_dir = "test_logs"
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_{timestamp}.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.info(f"Логгер инициализирован. Уровень: {logger_level}")
    logger.info(f"Логи будут сохраняться в: {log_file}")

    return logger


logger = create_logger()


# -------------------------------------------------------------------
# Pytest опции командной строки
# -------------------------------------------------------------------
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment: test, staging, production",
    )
    parser.addoption(
        "--browser-type",
        action="store",
        default="chromium",
        help="Browser: chromium, firefox, webkit (для Playwright)",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode",
    )
    # Оставляем для обратной совместимости, но не используем
    parser.addoption(
        "--remote-url",
        action="store",
        default=None,
        help="(Ignored) Selenium Grid remote URL – не используется в Playwright",
    )


# -------------------------------------------------------------------
# Фикстуры Playwright
# -------------------------------------------------------------------
@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright, request):
    browser_type = request.config.getoption("--browser-type").lower()
    headless = request.config.getoption("--headless")

    launch_options = {"headless": headless, "args": ["--window-size=1080,1680"]}

    if browser_type == "chromium":
        browser = playwright.chromium.launch(**launch_options)
    elif browser_type == "firefox":
        browser = playwright.firefox.launch(**launch_options)
    elif browser_type == "webkit":
        browser = playwright.webkit.launch(**launch_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_type}")

    logger.info(f"Запущен браузер: {browser_type}, headless={headless}")
    yield browser
    browser.close()
    logger.info("Браузер закрыт")


@pytest.fixture
def context(browser):
    context = browser.new_context(
        viewport={"width": 1080, "height": 1680},  # type: ignore
        accept_downloads=True,
    )
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    # Устанавливаем таймаут для ожиданий (аналог implicit_wait)
    page.set_default_timeout(10000)  # 10 секунд
    yield page
    page.close()


# -------------------------------------------------------------------
# Фикстура для Allure (создание директории)
# -------------------------------------------------------------------
def pytest_configure(config):
    allure_dir = "allure-results"
    os.makedirs(allure_dir, exist_ok=True)


# -------------------------------------------------------------------
# Логирование начала и конца теста
# -------------------------------------------------------------------
@pytest.fixture(autouse=True)
def log_test(request):
    test_name = request.node.name
    logger.info(f"=== Начало теста: {test_name} ===")
    yield
    logger.info(f"=== Конец теста: {test_name} ===")


@pytest.fixture
def login_page(page: Page):
    from Diplom.pages.login_page import LoginPage

    return LoginPage(page)


@pytest.fixture
def buzz_page(page: Page, login_page):
    # Автоматический логин для всех тестов Buzz
    login_page.open()
    login_page.login("Admin", "admin123")
    from Diplom.pages.buzz_page import BuzzPage

    return BuzzPage(page)


@pytest.fixture(scope="session")
def api_context(playwright):
    """Создаёт API контекст с базовым URL и выполняет логин."""
    # Создаём новый контекст запросов
    request_ctx = playwright.request.new_context(
        base_url="https://opensource-demo.orangehrmlive.com"
    )

    # Данные для логина
    login_data = {
        "username": "Admin",
        "password": "admin123",
    }

    # 1. Получаем страницу логина для CSRF-токена
    login_page_resp = request_ctx.get("/web/index.php/auth/login")
    csrf_token = extract_csrf_token(login_page_resp.text())
    if csrf_token:
        login_data["_csrf"] = csrf_token

    # 2. Отправляем POST-запрос на валидацию
    request_ctx.post(
        "/web/index.php/auth/validate",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    # Куки сессии сохранятся автоматически

    # 3. После успешного логина получаем страницу дашборда для API-токена
    dashboard_resp = request_ctx.get("/web/index.php/dashboard/index")
    api_csrf = extract_csrf_token(dashboard_resp.text())
    if api_csrf:
        request_ctx.set_extra_http_headers({"X-CSRF-TOKEN": api_csrf})  # type: ignore

    yield request_ctx
    request_ctx.dispose()


def extract_csrf_token(html: str) -> str:
    """Извлекает CSRF-токен из HTML."""
    patterns = [
        r'<meta name="csrf-token" content="([^"]+)"',
        r'<input type="hidden" name="_csrf" value="([^"]+)"',
        r"window\.csrfToken = '([^']+)'",
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)
    return ""
