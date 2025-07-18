@echo off
echo ========================================
echo Clientes - Sistema Distribuido Lamport
echo Conectando a Servidor Remoto
echo ========================================
echo.

REM Configurar URL del servidor remoto
set /p SERVER_URL="Ingresa la URL del servidor remoto (ej: http://tu-servidor.com): "

if "%SERVER_URL%"=="" (
    echo ❌ URL del servidor requerida
    pause
    exit /b 1
)

echo.
echo Configurando clientes para conectarse a: %SERVER_URL%
echo.

REM Cliente 1
echo Iniciando Cliente 1...
start "Cliente 1" cmd /k "set PROCESS_ID=1 && set PROCESS_NAME=Cliente-1 && set SERVER_URL=%SERVER_URL% && python client-cloud.py"

REM Cliente 2  
echo Iniciando Cliente 2...
start "Cliente 2" cmd /k "set PROCESS_ID=2 && set PROCESS_NAME=Cliente-2 && set SERVER_URL=%SERVER_URL% && python client-cloud.py"

REM Cliente 3
echo Iniciando Cliente 3...
start "Cliente 2" cmd /k "set PROCESS_ID=3 && set PROCESS_NAME=Cliente-3 && set SERVER_URL=%SERVER_URL% && python client-cloud.py"

echo.
echo ========================================
echo Clientes iniciados correctamente!
echo ========================================
echo.
echo URLs locales disponibles:
echo - Cliente 1: http://localhost:5001
echo - Cliente 2: http://localhost:5002  
echo - Cliente 3: http://localhost:5003
echo.
echo Servidor remoto: %SERVER_URL%
echo.
echo Para detener: Cerrar las ventanas de los clientes
echo.
pause 