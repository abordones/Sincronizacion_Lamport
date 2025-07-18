# Configuración para Servidor con Acceso SFTP

## Información de Conexión SFTP

### Datos de FileZilla:
```
Servidor: ftp.tuempresa.com
Usuario: tu_usuario
Contraseña: tu_password
Puerto: 22 (SFTP) o 21 (FTP)
```

## Pasos de Despliegue

### 1. Subir Archivos por SFTP
1. Abrir FileZilla
2. Conectar a `ftp.tuempresa.com`
3. Subir todos los archivos del proyecto a una carpeta (ej: `/public_html/lamport/`)

### 2. Conectar por SSH al Servidor
```bash
ssh tu_usuario@tuempresa.com
# o
ssh tu_usuario@IP_DEL_SERVIDOR
```

### 3. Navegar a la Carpeta de Archivos
```bash
cd /public_html/lamport/
# o donde hayas subido los archivos
```

### 4. Verificar Requisitos
```bash
# Verificar Python
python3 --version

# Verificar Docker (si está disponible)
docker --version

# Verificar permisos
ls -la
```

### 5. Ejecutar Despliegue
```bash
# Si tienes Docker:
chmod +x deploy-cloud.sh
./deploy-cloud.sh

# Si NO tienes Docker:
python3 server.py
```

### 6. Configurar URL del Servicio
La URL del servicio será:
```
http://tuempresa.com
http://www.tuempresa.com
http://IP_DEL_SERVIDOR
```

## Configuración de Clientes Locales

### Opción 1: Script Automático
```batch
# Ejecutar start-cloud.bat
# Cuando pregunte la URL, poner:
http://tuempresa.com
```

### Opción 2: Manual
```bash
# Cliente 1
export SERVER_URL=http://tuempresa.com
export PROCESS_ID=1
export PROCESS_NAME=Cliente-1
python client-cloud.py

# Cliente 2
export SERVER_URL=http://tuempresa.com
export PROCESS_ID=2
export PROCESS_NAME=Cliente-2
python client-cloud.py

# Cliente 3
export SERVER_URL=http://tuempresa.com
export PROCESS_ID=3
export PROCESS_NAME=Cliente-3
python client-cloud.py
```

## Verificación

### 1. Verificar que el Servidor Responda
```bash
# Desde tu computadora local:
curl http://tuempresa.com/status
```

### 2. Verificar desde Navegador
```
http://tuempresa.com
```

### 3. Verificar Clientes
```
http://localhost:5001  # Cliente 1
http://localhost:5002  # Cliente 2
http://localhost:5003  # Cliente 3
```

## Troubleshooting

### Problema: No puedo conectar por SSH
```bash
# Verificar si el servidor permite SSH
# Contactar al administrador del servidor
```

### Problema: Python no está instalado
```bash
# Instalar Python en el servidor
sudo apt update
sudo apt install python3 python3-pip
```

### Problema: Puerto 80 no está abierto
```bash
# Verificar puertos abiertos
netstat -tlnp

# Contactar al administrador para abrir puerto 80
```

### Problema: Clientes no se conectan
```bash
# Verificar URL correcta
curl http://tuempresa.com/status

# Verificar firewall local
# Verificar que el servidor esté corriendo
```

## Comandos Útiles en el Servidor

```bash
# Ver procesos corriendo
ps aux | grep python

# Ver puertos en uso
netstat -tlnp

# Ver logs del servidor
tail -f /var/log/apache2/error.log
# o
tail -f /var/log/nginx/error.log

# Reiniciar servidor web
sudo systemctl restart apache2
# o
sudo systemctl restart nginx
```

## Notas Importantes

1. **La URL SFTP** es solo para subir archivos
2. **La URL del servicio** es para que los clientes se conecten
3. **Necesitas acceso SSH** para ejecutar comandos en el servidor
4. **El puerto 80** debe estar abierto para HTTP
5. **Python debe estar instalado** en el servidor 