# Despliegue con Solo Acceso SFTP

## Situación: Solo tienes acceso SFTP (sin SSH)

### Herramientas que puedes usar:
- ✅ **FileZilla**: Subir archivos
- ✅ **cPanel** (si está disponible): Gestión web
- ✅ **Panel de control del hosting**: Configuración
- ❌ **SSH**: No disponible
- ❌ **Comandos directos**: No disponibles

## Opciones de Despliegue

### Opción 1: Hosting con Python (Recomendado)

#### Verificar si tu hosting soporta Python:
1. **Acceder al panel de control** del hosting
2. **Buscar sección "Python"** o "Aplicaciones"
3. **Verificar versión de Python** disponible

#### Si soporta Python:
```bash
# En el panel de control, crear aplicación Python
# Subir archivos por FileZilla
# Configurar punto de entrada: server.py
```

### Opción 2: Servicios de Nube Gratuitos

#### Heroku (Gratis):
```bash
# Crear cuenta en Heroku
# Conectar repositorio Git
# Desplegar automáticamente
```

#### Railway (Gratis):
```bash
# Conectar GitHub
# Desplegar automáticamente
# Obtener URL pública
```

#### Render (Gratis):
```bash
# Conectar repositorio
# Configurar como servicio web
# Desplegar automáticamente
```

### Opción 3: VPS Económico

#### DigitalOcean ($5/mes):
```bash
# Crear Droplet
# Acceso SSH completo
# Control total del servidor
```

#### Vultr ($2.50/mes):
```bash
# Instancia pequeña
# Acceso SSH
# Configuración completa
```

## Configuración para Servicios Gratuitos

### Heroku:
```bash
# Crear archivo Procfile
echo "web: python server.py" > Procfile

# Crear archivo runtime.txt
echo "python-3.9.16" > runtime.txt

# Subir a GitHub
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Railway:
```bash
# Conectar repositorio GitHub
# Configurar variables de entorno:
# - PROCESS_ID=0
# - PROCESS_NAME=UNAP-Server
# - PORT=5000
```

## Verificar Capacidades del Hosting

### Preguntas para el Administrador:
```
1. ¿El hosting soporta Python?
2. ¿Qué versión de Python está disponible?
3. ¿Puedo ejecutar aplicaciones web?
4. ¿Qué puertos están abiertos?
5. ¿Hay límites de CPU/RAM?
6. ¿Puedo instalar paquetes Python?
```

### Verificar en el Panel de Control:
```
- Sección "Python" o "Aplicaciones"
- Sección "Cron Jobs" (para tareas automáticas)
- Sección "Logs" (para debugging)
- Sección "Bases de datos" (si necesitas)
```

## Alternativa: Servidor Local + Túnel

### Si no puedes usar el servidor remoto:

#### Opción A: Servidor local con ngrok
```bash
# Ejecutar servidor localmente
python server.py

# Crear túnel público con ngrok
ngrok http 5000

# Usar URL de ngrok en los clientes
# Ejemplo: https://abc123.ngrok.io
```

#### Opción B: Servidor local con port forwarding
```bash
# Configurar router para abrir puerto 80
# Usar IP pública en los clientes
# Ejemplo: http://tu-ip-publica
```

## Recomendación Final

### Para tu situación, recomiendo:

1. **Verificar capacidades del hosting** actual
2. **Si no soporta Python**: Usar servicio gratuito (Heroku/Railway)
3. **Si soporta Python**: Configurar en el hosting
4. **Como última opción**: VPS económico ($5/mes)

### Servicios Gratuitos Recomendados:
- **Railway**: Más fácil de usar
- **Render**: Muy confiable
- **Heroku**: Más popular (pero requiere tarjeta)

### VPS Económico:
- **DigitalOcean**: $5/mes, control total
- **Vultr**: $2.50/mes, muy económico
- **Linode**: $5/mes, muy confiable

## Próximos Pasos

1. **Verificar tu hosting actual**
2. **Elegir opción según capacidades**
3. **Configurar despliegue**
4. **Probar conectividad**
5. **Configurar clientes locales**

¿Qué tipo de hosting tienes actualmente? ¿Tienes acceso al panel de control? 