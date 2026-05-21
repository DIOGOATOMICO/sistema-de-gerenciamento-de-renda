
python app.py && pause

@echo off
title Sistema de Gerenciamento de Renda

echo =====================================
echo   Verificando ambiente Python
echo =====================================
echo.

:: Verifica Python padrao
python --version >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    goto iniciar
)

:: Verifica Python Launcher
py --version >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    goto iniciar_py
)

:: Python nao encontrado
echo Python nao encontrado no sistema.
echo Abrindo pagina oficial para download...

start https://www.python.org/downloads/

echo.
pause
exit

:: Inicializacao usando python
:iniciar
echo Python encontrado:
python --version

echo.
echo =====================================
echo  Iniciando Sistema de Gerenciamento
echo =====================================
echo.

python app.py

pause
exit

:: Inicializacao usando py launcher
:iniciar_py
echo Python Launcher encontrado:
py --version

echo.
echo =====================================
echo  Iniciando Sistema de Gerenciamento
echo =====================================
echo.

py app.py

pause
exit