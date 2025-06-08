import os
import subprocess
import sys
import pymysql
import re

# Функция для чтения и выполнения SQL-скрипта
def execute_sql_file(file_path, connection):
    print(f"Импорт данных из файла {file_path}...")
    
    try:
        # Чтение файла
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Разделение на отдельные SQL команды
        # Регулярное выражение для разделения по точке с запятой, 
        # пропуская точки с запятой внутри строк и комментариев
        sql_commands = re.split(r';(?=(?:[^\']*\'[^\']*\')*[^\']*$)(?=(?:[^"]*"[^"]*")*[^"]*$)', sql_content)
        
        cursor = connection.cursor()
        
        # Выполнение каждой команды
        for command in sql_commands:
            command = command.strip()
            if command:
                print(f"Выполнение команды: {command[:50]}...")
                try:
                    cursor.execute(command)
                except Exception as e:
                    print(f"Ошибка при выполнении команды: {e}")
        
        # Подтверждение изменений
        connection.commit()
        print("Импорт данных успешно завершен!")
        
    except Exception as e:
        print(f"Произошла ошибка при импорте данных: {e}")
        connection.rollback()

# Прямой импорт SQL файла через команду mysql
def import_sql_direct(sql_file_path, db_user, db_password, db_name):
    print(f"Прямой импорт данных из файла {sql_file_path} в базу {db_name}...")
    
    # Командная строка для импорта
    command = f'mysql -u {db_user} -p{db_password} {db_name} < "{sql_file_path}"'
    
    try:
        # Выполнение команды
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stderr:
            print(f"Предупреждения/ошибки: {result.stderr}")
        print("Импорт данных успешно завершен!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при импорте данных: {e}")
        if e.stderr:
            print(f"Детали ошибки: {e.stderr}")
        return False
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
        return False

# Подключение к базе данных
def connect_to_mysql():
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'root')
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = int(os.environ.get('DB_PORT', 3306))
    db_name = os.environ.get('DB_NAME', 'forumdb')
    
    print(f"Подключение к MySQL ({db_host}:{db_port})...")
    
    try:
        # Сначала подключаемся без указания базы данных
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Удаляем базу данных, если она существует
        print(f"Удаление существующей базы данных '{db_name}', если она существует...")
        cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
        connection.commit()
        
        # Создаем базу данных заново
        print(f"Создание базы данных '{db_name}'...")
        cursor.execute(f"CREATE DATABASE `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        connection.commit()
        print(f"База данных '{db_name}' успешно создана!")
        
        # Закрываем соединение и открываем новое с указанием базы данных
        connection.close()
        
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            port=db_port,
            charset='utf8mb4'
        )
        
        print("Подключение успешно установлено!")
        return connection, db_user, db_password, db_name
        
    except Exception as e:
        print(f"Ошибка подключения к MySQL: {e}")
        return None, None, None, None

if __name__ == "__main__":
    # Получаем путь к SQL файлу
    sql_file_path = os.path.join('db', 'forum.sql')
    
    if not os.path.exists(sql_file_path):
        print(f"Файл {sql_file_path} не найден!")
        exit(1)
    
    # Подключаемся к MySQL
    connection, db_user, db_password, db_name = connect_to_mysql()
    
    if connection:
        try:
            # Сначала пробуем прямой импорт
            if import_sql_direct(sql_file_path, db_user, db_password, db_name):
                print("Прямой импорт успешно завершен.")
            else:
                print("Прямой импорт не удался, пробуем альтернативный метод...")
                # Если прямой импорт не удался, используем альтернативный метод
                execute_sql_file(sql_file_path, connection)
        finally:
            connection.close()
    
    print("Импорт завершен. Теперь запустите форум с MySQL: python run.py") 