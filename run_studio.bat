@echo off
chcp 65001 >nul
title Elvira Astashkina - Mathematical Animation Studio (Klimt x ML)
cd /d "%~dp0"

echo ======================================================================
echo    ELVIRA ASTASHKINA // BRAND SYSTEM
echo    Mathematical Infographic & Animation Studio (Klimt x Applied ML)
echo ======================================================================
echo.

if not defined PYTHON_EXE (
    set PYTHON_EXE=python
)

echo [STARTING] Launching Studio server with Python: %PYTHON_EXE%
echo [BROWSER]  Opening http://localhost:8055 ...
echo.

start "" "http://localhost:8055"
"%PYTHON_EXE%" studio.py

pause
