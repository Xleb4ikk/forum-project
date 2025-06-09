import os
import sys

# Установка переменных окружения
os.environ['DB_NAME'] = 'forumdb'  # Используем forumdb вместо forum
os.environ['USE_SQLITE'] = 'false'  # Убедимся, что используется MySQL

# Импортируем необходимые модули
from app import create_app
from app.config import Config

# Создаем приложение
app = create_app()

if __name__ == "__main__":
    print("Запуск форума с базой данных...")
    print(f"Строка подключения: {Config.SQLALCHEMY_DATABASE_URI}")
    print(f"Используется имя базы данных: {Config.DB_NAME}")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=True) 