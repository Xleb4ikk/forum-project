@echo off
chcp 65001 > nul
title Запуск Форума
color 0A

echo ===============================================================
echo            ЗАПУСК ПРИЛОЖЕНИЯ ФОРУМА (Windows)
echo ===============================================================
echo.

REM Активация виртуального окружения Python 3.11
call venv311\Scripts\activate.bat

REM Устанавливаем переменную для использования SQLite
set USE_SQLITE=true

REM Запуск приложения
python run.py

pause 