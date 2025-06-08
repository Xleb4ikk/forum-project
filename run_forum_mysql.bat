@echo off
chcp 65001 > nul
title Запуск Форума с MySQL
color 0A

echo ===============================================================
echo            ЗАПУСК ПРИЛОЖЕНИЯ ФОРУМА С MySQL (Windows)
echo ===============================================================
echo.

REM Активация виртуального окружения Python 3.11
call venv311\Scripts\activate.bat

REM Импорт данных из SQL файла
python import_sql.py

REM Запуск приложения
python run.py

pause 