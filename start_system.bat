@echo off
echo ===============================================
echo    SISTEMA DE LAMPORT - INICIO AUTOMATICO
echo ===============================================
echo.

echo Iniciando servidor UDP...
start "Servidor-UDP" cmd /k python udp_server.py

echo Esperando 3 segundos para que el servidor inicie...
timeout /t 3 /nobreak >nul

echo.
echo Iniciando launcher de clientes...
start "Launcher-Clientes" cmd /k python launch_clients.py

echo.
echo ===============================================
echo    SISTEMA INICIADO
echo ===============================================
echo.
echo - Servidor UDP ejecutandose en ventana separada
echo - Launcher de clientes ejecutandose en ventana separada
echo.
echo Presiona cualquier tecla para cerrar esta ventana...
pause >nul
