@echo off
echo ========================================
echo Sistema Distribuido - Algoritmo de Lamport
echo ========================================
echo.

echo Iniciando servicios con Docker Compose...
docker-compose up --build -d

echo.
echo Esperando que los servicios esten listos...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo Servicios iniciados correctamente!
echo ========================================
echo.
echo URLs disponibles:
echo - Servidor UNAP: http://localhost:5000
echo - Cliente 1:     http://localhost:5001
echo - Cliente 2:     http://localhost:5002
echo - Cliente 3:     http://localhost:5003
echo.
echo Para ver los logs: docker-compose logs -f
echo Para detener:      docker-compose down
echo.
pause 