# Diplom
Мой дипломный проект автоматизированного тестирования демосайта https://opensource-demo.orangehrmlive.com/
с использованием Selenium, Allure и Pytest.

## 🧩 Стек технологий

- Python
- [pytest](https://docs.pytest.org/)
- Selenium
- Docker
- GitActions
- Allure и Logger (для генерации отчётов)
- Page Object Pattern
- Скриншоты при ошибках и успешных регистрациях
- Визуальное тестирование

## 📋 Возможности
- ✅ Тестирование авторизации (позитивные/негативные сценарии)
- ✅ Проверка социальных ссылок
- ✅ Тестирование восстановления пароля
- ✅ Allure отчеты с скриншотами
- ✅ Параметризованные тесты
- ✅ Page Object Model архитектура
- ✅ Запуск через Docker

## 🚀 Быстрый старт

```bash
# Клонировать репозиторий
git clone https://github.com/ваш-username/ваш-проект.git

# Перейти в папку проекта
cd ваш-проект

#  Создание виртуального окружения
# Для Windows
python -m venv venv
venv\Scripts\activate

# Для macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить тесты
pytest
```

📋 Требования
Python 3.9 или выше

Google Chrome (или другой браузер)

ChromeDriver (совместимая версия)


📦 Зависимости
Все зависимости перечислены в requirements.txt

Основные команды 

```bash
# Запуск всех тестов
pytest

# Запуск тестов с маркировкой smoke
pytest -m smoke

# Запуск с подробным выводом
pytest -v

# Запуск с перезапуском упавших тестов
pytest --reruns 2 --reruns-delay 1

# Запуск конкретного теста
pytest Diplom/test/test_pages/test_login.py::test_positive_login

# Запуск на разных браузерах
pytest # тут по умолчанию Chrome
pytest --selenium-browser=firefox
pytest --selenium-browser=edge

```


## 🐳 Запуск в Docker

### Требования
- Установленные [Docker](https://docs.docker.com/get-docker/) 
- и [Docker Compose](https://docs.docker.com/compose/install/).

Запуск:

```bash
docker-compose -f docker-compose.grid.yml up --build

# Повторный запуск 
docker-compose -f docker-compose.grid.yml run tests pytest 
--selenium-browser=firefox --remote-url=http://selenium-hub:4444/wd/hub -v

# Остановка 
docker-compose -f docker-compose.grid.yml down\

# Показ статусов контейнеров
docker-compose -f docker-compose.grid.yml ps

# Очистка не использумеого
docker-compose -f docker-compose.grid.yml down -v

# Запуск конкретного теста
docker-compose -f docker-compose.grid.yml run --rm tests pytest test/test_pages/test_dashboard.py::test_search 
-v --selenium-browser=chrome --remote-url=http://selenium-hub:4444/wd/hub

# Прогон тестов с пометками
docker-compose -f docker-compose.grid.yml run --rm tests pytest -m smoke 
-v --selenium-browser=firefox --remote-url=http://selenium-hub:4444/wd/hub

# Логи хаба
docker-compose -f docker-compose.grid.yml logs -f selenium-hub

# Генерация отчетов
allure generate allure-results -o allure-report --clean
allure open allure-report
```


## 🧪 Запуск тестов

### Тестовые сценарии

| Тест | Описание | 
|------|----------|
| `test_positive_login` | Успешный вход в систему |
| `test_negative_username` | Неверные учетные данные |
| `test_logout` | Выход из системы |
| `test_social_links` | Проверка социальных ссылок |


## 🎯 API блок
Интеграция API тестов для системы OrangeHRM с поддержкой основных CRUD операций.
Но к сожалению не удалось извлечь CSFR токен для запуска тестов

## 📊 Поддерживаемые операции

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/v2/pim/employees` | Создание сотрудника |
| GET | `/api/v2/pim/employees` | Получение списка сотрудников |
| GET | `/api/v2/pim/employees/{id}/personal-details` | Получение данных сотрудника |
| PUT | `/api/v2/pim/employees/{id}/personal-details` | Обновление данных сотрудника |
| DELETE | `/api/v2/pim/employees` | Удаление сотрудника(ов) |

📊 Генерация отчетов
Allure отчеты
```bash
# Запуск тестов с генерацией Allure отчетов
pytest --alluredir=allure-results

# Генерация HTML отчета
allure generate allure-results -o allure-report --clean

# Открытие отчета в браузере
allure open allure-report
```

## 📁 Структура проекта
Diplom/
├── .github/
├── .venv/
├── allure-results/
├── Diplom/
│ ├── core/
│ │ ├── base_element.py
│ │ ├── base_page.py
│ │ └── api_service.py
│ ├── files/
│ ├── page_obj/
│ │ ├── dashboard_page.py
│ │ ├── login_page.py
│ │ └── ...
│ ├── test/
│ │ ├── test_api/
│ │ ├── test_cookies/
│ │ └── test_pages/
│ │ ├── test_dashboard.py
│ │ └── test_login.py
│ └── urls.py
├── requirements.txt
├── conftest.py
├── .gitignore
├── README.md
├── pyproject.toml
├── Dockerfile
├── docker-compose.grid.yml
├── .pre-commit-config.yaml
├── .flake8
└── test_logs/