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
pytest Diplom/test/test_login.py::test_positive_login
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

📁 Структура проекта
text
project/
├── tests/                          
│   ├── test_login.py              
│   ├── test_dashboard.py        
│   └── conftest.py               
├── pages/                      
│   ├── login_page.py
│   ├── dashboard_page.py
│   └── base_page.py
├── utils/                 
│   ├── logger.py
│   ├── config.py
│   └── helpers.py
├── allure-results/                
├── logs/                       
├── screenshots/              
├── requirements.txt            
└── .gitignore                   