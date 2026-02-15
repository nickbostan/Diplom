import logging
import os
import pytest


from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

@pytest.fixture(scope="function")
def driver(tmp_path):
    opts = ChromeOptions()
    opts.headless = True
    opts.add_argument("--window-size=1080,1680")
    prefs = {
        "download.default_directory": str(tmp_path),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def edge_driver(tmp_path):

    opts = EdgeOptions()
    opts.headless = True
    opts.add_argument("--window-size=1080,1680")
    prefs = {
        "download.default_directory": str(tmp_path),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Edge(options=opts)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def firefox_driver(tmp_path):

    opts = FirefoxOptions()
    opts.headless = True
    opts.add_argument("--width=1080")
    opts.add_argument("--height=1680")


    profile = FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", str(tmp_path))
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                           "application/octet-stream,text/plain,application/pdf,application/zip")
    profile.set_preference("pdfjs.disabled", True)
    opts.profile = profile

    driver = webdriver.Firefox(options=opts)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def pytest_addoption(parser):

    parser.addoption(
        "--env",
        action="store",
        default="test_pages",
        help="Environment: test_pages, staging, production",
    )



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
        "CRITICAL": logging.CRITICAL
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
        datefmt="%Y-%m-%d %H:%M:%S"
    )


    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)


    file_handler = logging.FileHandler(log_file, encoding='utf-8')
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