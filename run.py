import os
import sys
import time
import socket
import pymysql
from dotenv import load_dotenv
from app import create_app

# Загрузка переменных окружения
load_dotenv()

# Проверка версии Python
if sys.version_info.major != 3 or sys.version_info.minor > 12:
    print(f"ВНИМАНИЕ: Приложение разработано для Python 3.11.")
    print(f"Текущая версия: Python {sys.version_info.major}.{sys.version_info.minor}")
    user_input = input("Продолжить выполнение? (y/n): ")
    if user_input.lower() != 'y':
        sys.exit(1)

def check_mysql_connection():
    """Проверка доступности MySQL"""
    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    database = os.getenv('DB_NAME', 'forum')
    port = int(os.getenv('DB_PORT', 3306))
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Проверка сначала, доступен ли хост
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result != 0:
                print(f"Не удалось подключиться к серверу MySQL на {host}:{port}")
                if attempt < max_retries - 1:
                    print(f"Повторная попытка через {retry_delay} секунд...")
                    time.sleep(retry_delay)
                continue
            
            # Проверка доступа к базе данных
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            connection.close()
            print("Подключение к MySQL успешно установлено!")
            return True
            
        except pymysql.MySQLError as e:
            error_code = e.args[0]
            error_message = e.args[1] if len(e.args) > 1 else str(e)
            
            if error_code == 1045:  # Неправильный логин/пароль
                print(f"Ошибка авторизации в MySQL: {error_message}")
                print("Проверьте настройки в файле .env (DB_USER, DB_PASSWORD)")
                return False
            
            elif error_code == 1049:  # База данных не существует
                print(f"База данных '{database}' не существует.")
                create_db = input("Создать базу данных? (y/n): ")
                if create_db.lower() == 'y':
                    try:
                        connection = pymysql.connect(
                            host=host,
                            user=user,
                            password=password,
                            port=port
                        )
                        with connection.cursor() as cursor:
                            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
                        connection.close()
                        print(f"База данных '{database}' успешно создана!")
                        return True
                    except pymysql.MySQLError as e:
                        print(f"Не удалось создать базу данных: {e}")
                        return False
                else:
                    return False
            
            else:
                print(f"Ошибка подключения к MySQL: {error_message}")
                if attempt < max_retries - 1:
                    print(f"Повторная попытка через {retry_delay} секунд...")
                    time.sleep(retry_delay)
    
    print("Не удалось подключиться к MySQL после нескольких попыток.")
    return False

if __name__ == '__main__':
    # Проверка подключения к MySQL
    db_available = check_mysql_connection()
    
    if not db_available:
        print("\nВНИМАНИЕ: Работа с базой данных MySQL недоступна!")
        continue_anyway = input("Запустить приложение с SQLite вместо MySQL? (y/n): ")
        if continue_anyway.lower() == 'y':
            # Set environment variable to use SQLite
            os.environ['USE_SQLITE'] = 'true'
            print("Используем SQLite для запуска приложения.")
        else:
            sys.exit(1)
    
    # Создание и запуск приложения
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False) 