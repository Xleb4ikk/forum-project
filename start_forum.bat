@echo off
chcp 65001 > nul
title Запуск Форума
color 0A

echo ===============================================================
echo            ЗАПУСК ПРИЛОЖЕНИЯ ФОРУМА (Windows)
echo ===============================================================
echo.

REM Проверка наличия Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Python не найден!
    echo Пожалуйста, установите Python 3.11 с сайта https://www.python.org/
    pause
    exit /b 1
)

REM Получение версии Python
python -c "import sys; print(f'Обнаружен Python версии: {sys.version.split()[0]}')"

REM Запуск скрипта запуска форума
echo.
echo Запуск приложения...
echo.
python -c "import sys; sys.path.insert(0, '.'); from utils.run_forum import main; main()"

pause 