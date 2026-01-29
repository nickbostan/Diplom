# Diplom
Мой дипломный проект автоматизированного тестирования демосайта https://opensource-demo.orangehrmlive.com/
с использованием Selenium, Allure и Pytest.

## 🧩 Стек технологий

- Python
- [pytest](https://docs.pytest.org/)
- Selenium
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

# Запуск конкретного теста
pytest tests/test_login.py::test_positive_login
```

## 🧪 Запуск тестов

### Тестовые сценарии

| Тест | Описание | 
|------|----------|
| `test_positive_login` | Успешный вход в систему |
| `test_negative_username` | Неверные учетные данные |
| `test_logout` | Выход из системы |
| `test_social_links` | Проверка социальных ссылок |


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

📁 Структура проекта
text
project/
├── tests/                          # Тесты
│   ├── test_login.py              # Тесты авторизации
│   ├── test_dashboard.py          # Тесты дашборда
│   └── conftest.py               # Конфигурация pytest
├── pages/                         # Page Object Model
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── base_page.py
├── utils/                         # Вспомогательные утилиты
│   ├── logger.py
│   ├── config.py
│   └── helpers.py
├── allure-results/                # Allure отчеты (авто)
├── logs/                         # Логи тестирования (авто)
├── screenshots/                  # Скриншоты (авто)
├── requirements.txt              # Зависимости
├── README.md                     # Этот файл
└── .gitignore                    # Игнорируемые файлы