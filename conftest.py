import logging
import os
from datetime import datetime

import pytest
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test_pages",
        help="Environment: test_pages, staging, production",
    )
    # Новые опции для Docker
    parser.addoption(
        "--selenium-browser",
        action="store",
        default="chrome",
        help="Browser: chrome, firefox, edge",
    )
    parser.addoption(
        "--remote-url",
        action="store",
        default=None,
        help="Selenium Grid remote URL (e.g., http://selenium-hub:4444/wd/hub)",
    )
    parser.addoption(
        "--headed-mode",
        action="store_true",
        default=False,
        help="Run browser in headed mode (with GUI)",
    )


@pytest.fixture(scope="function")
def driver(request, tmp_path):
    browser = request.config.getoption("--selenium-browser")
    remote_url = request.config.getoption("--remote-url")
    headed = request.config.getoption("--headed-mode")
    headless = not headed

    # Папка для загрузок – можно переопределить через переменную окружения
    download_dir = os.getenv("DOWNLOAD_DIR", str(tmp_path))

    if browser == "chrome":
        opts = ChromeOptions()
        opts.headless = headless
        opts.add_argument("--window-size=1080,1680")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True,
        }
        opts.add_experimental_option("prefs", prefs)
        if remote_url:
            driver = webdriver.Remote(command_executor=remote_url, options=opts)
        else:
            driver = webdriver.Chrome(options=opts)

    elif browser == "firefox":
        opts = FirefoxOptions()
        opts.headless = headless
        opts.add_argument("--width=1080")
        opts.add_argument("--height=1680")
        profile = FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", download_dir)
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/octet-stream,text/plain,application/pdf,application/zip",
        )
        profile.set_preference("pdfjs.disabled", True)
        opts.profile = profile
        if remote_url:
            driver = webdriver.Remote(command_executor=remote_url, options=opts)
        else:
            driver = webdriver.Firefox(options=opts)

    elif browser == "edge":
        opts = EdgeOptions()
        opts.headless = headless
        opts.add_argument("--window-size=1080,1680")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True,
        }
        opts.add_experimental_option("prefs", prefs)
        if remote_url:
            driver = webdriver.Remote(command_executor=remote_url, options=opts)
        else:
            driver = webdriver.Edge(options=opts)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def create_logger():
    logger = logging.getLogger()

    # Уровень логирования из переменной окружения
    logger_level = os.getenv("LOGGER_LEVEL", "INFO").upper()

    # Преобразуем строку в уровень логирования
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    logger.setLevel(level_map.get(logger_level, logging.INFO))

    # Создаем папку для логов если её нет
    log_dir = "test_logs"
    os.makedirs(log_dir, exist_ok=True)

    # Имя файла с timestamp
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


def pytest_configure(config):
    allure_dir = "allure-results"
    os.makedirs(allure_dir, exist_ok=True)


@pytest.fixture(scope="function")
def log_test(request):
    test_name = request.node.name
    logger.info(f"Starting test_pages: {test_name}")
    yield
    logger.info(f"Finished test_pages: {test_name}")


@pytest.fixture
def resized_image(tmp_path):
    from Diplom.files import IMG_2

    def _resize(width: int, height: int) -> str:
        dest = tmp_path / f"img_{width}x{height}.jpg"
        with Image.open(IMG_2) as img:
            resized = img.resize((width, height))
            resized.save(dest)
        return str(dest)

    return _resize
