FROM mcr.microsoft.com/playwright:python-v1.40.0-focal

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Убеждаемся, что нужный браузер установлен (в базовом образе уже есть chromium)
RUN playwright install chromium

# Запуск тестов (параметры можно переопределить через CMD)
CMD ["pytest", "-v", "--browser=chromium", "--headless=True", "--alluredir=allure-results"]
