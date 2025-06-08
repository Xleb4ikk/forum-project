import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def print_header():
    """Вывод заголовка при запуске скрипта"""
    print("\n" + "="*70)
    print(" "*25 + "ФОРУМ - ЗАПУСК ПРИЛОЖЕНИЯ")
    print("="*70 + "\n")

def setup_environment():
    """Проверка и настройка окружения"""
    print("🔍 Проверка окружения...")
    
    # Проверка наличия файла .env
    if not os.path.exists('.env'):
        print("⚠️ Файл .env не найден. Создаем из example.env...")
        if os.path.exists('example.env'):
            with open('example.env', 'r') as src:
                with open('.env', 'w') as dest:
                    dest.write(src.read())
            print("✅ Файл .env создан! Пожалуйста, проверьте и отредактируйте настройки при необходимости.")
        else:
            print("❌ Файл example.env не найден. Пожалуйста, создайте файл .env вручную.")
            return False
    
    # Проверка и установка зависимостей
    try:
        import pymysql
        import flask
        import sqlalchemy
        import flask_admin
        print("✅ Все необходимые зависимости установлены.")
    except ImportError as e:
        print(f"❌ Не удалось импортировать модуль: {e}")
        print("⚙️ Установка зависимостей...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    return True

def generate_test_data():
    """Генерация тестовых данных"""
    print("\n🧪 Генерация тестовых данных для базы данных...")
    try:
        from utils.generate_test_data import generate_test_data
        from app import create_app
        app = create_app()
        generate_test_data(app)
        print("✅ Тестовые данные успешно сгенерированы!")
    except Exception as e:
        print(f"❌ Ошибка при генерации тестовых данных: {e}")
        return False
    
    return True

def run_application():
    """Запуск веб-приложения"""
    print("\n🚀 Запуск веб-приложения...")
    print("📊 Приложение будет доступно по адресу: http://localhost:5000")
    print("⚙️ Панель администратора: http://localhost:5000/admin")
    print("👤 Логин: admin")
    print("🔑 Пароль: admin123")
    print("\n🔴 Для остановки приложения нажмите Ctrl+C\n")
    
    # Запуск приложения
    try:
        subprocess.run([sys.executable, "run.py"])
    except KeyboardInterrupt:
        print("\n🛑 Приложение остановлено пользователем.")
    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        return False
    
    return True

def main():
    """Основная функция"""
    parser = argparse.ArgumentParser(description="Запуск приложения форума")
    parser.add_argument("--no-data", action="store_true", help="Не генерировать тестовые данные")
    parser.add_argument("--setup-only", action="store_true", help="Только настройка окружения без запуска")
    args = parser.parse_args()
    
    print_header()
    
    # Настройка окружения
    if not setup_environment():
        print("❌ Не удалось настроить окружение. Остановка запуска.")
        return
    
    # Генерация тестовых данных (если не отключено)
    if not args.no_data:
        generate_test_data()
    
    # Запуск приложения (если не только настройка)
    if not args.setup_only:
        run_application()

if __name__ == "__main__":
    main() 