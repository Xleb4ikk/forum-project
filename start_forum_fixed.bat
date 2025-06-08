@echo off
chcp 65001 > nul
title Запуск Форума
color 0A

echo ===============================================================
echo            ЗАПУСК ПРИЛОЖЕНИЯ ФОРУМА (Windows)
echo ===============================================================
echo.

echo Запуск приложения с Python 3.11...
echo.

REM Проверка наличия Python 3.11
py -3.11 --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Python 3.11 не найден!
    echo Пожалуйста, установите Python 3.11 с сайта https://www.python.org/
    pause
    exit /b 1
)

echo Используем Python 3.11:
py -3.11 --version

REM Активация виртуального окружения (если оно существует)
if exist venv311\Scripts\activate.bat (
    call venv311\Scripts\activate.bat
) else (
    echo Создание виртуального окружения Python 3.11...
    py -3.11 -m venv venv311
    call venv311\Scripts\activate.bat
    echo Установка зависимостей...
    pip install -r requirements.txt
    pip install werkzeug==2.3.7
)

REM Проверка наличия файла .env
if not exist .env (
    echo Создание файла .env из example.env...
    copy example.env .env
    echo Создан файл .env
    echo ВНИМАНИЕ: Отредактируйте файл .env, чтобы настроить параметры подключения к базе данных!
    echo Нажмите Enter, чтобы продолжить...
    pause > nul
)

echo.
echo Запуск приложения...
echo.
python run.py

pause 