import logging
import os
import pytest

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


@pytest.fixture(scope="function")
def driver():
    opts = ChromeOptions()
    opts.headless = True
    opts.add_argument("--window-size=1080,1680")
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def driver_chrome():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def pytest_addoption(parser):

    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="Environment: test, staging, production",
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

    # Форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Файловый обработчик
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Удаляем старые обработчики если есть
    logger.handlers.clear()

    # Добавляем обработчики
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
    logger.info(f"Starting test: {test_name}")
    yield
    logger.info(f"Finished test: {test_name}")