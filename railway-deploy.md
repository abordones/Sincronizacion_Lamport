# Despliegue en Railway - Sistema Lamport

## ¿Por qué Railway?

✅ **Gratis** sin tarjeta de crédito
✅ **Fácil** de configurar
✅ **Automático** desde GitHub
✅ **URL pública** inmediata
✅ **SSL incluido**
✅ **Sin configuración** de servidor

## Pasos para Desplegar

### 1. Crear Cuenta en Railway
```
1. Ir a https://railway.app/
2. Crear cuenta con GitHub
3. No requiere tarjeta de crédito
```

### 2. Preparar Repositorio GitHub
```bash
# Crear repositorio en GitHub
# Subir todos los archivos del proyecto
# Asegurar que esté público (para versión gratuita)
```

### 3. Conectar Railway con GitHub
```
1. En Railway, hacer clic en "New Project"
2. Seleccionar "Deploy from GitHub repo"
3. Seleccionar tu repositorio
4. Railway detectará automáticamente que es Python
```

### 4. Configurar Variables de Entorno
En Railway, ir a la pestaña "Variables" y agregar:
```
PROCESS_ID=0
PROCESS_NAME=UNAP-Server-Railway
PORT=5000
```

### 5. Configurar Comando de Inicio
En Railway, ir a "Settings" y configurar:
```
Start Command: python server.py
```

### 6. Obtener URL Pública
```
1. Railway generará una URL automáticamente
2. Ejemplo: https://lamport-system-production.up.railway.app
3. Esta URL será tu servidor UNAP
```

## Configuración de Clientes Locales

### Usar la URL de Railway:
```bash
# Cliente 1
export SERVER_URL=https://tu-proyecto.up.railway.app
export PROCESS_ID=1
export PROCESS_NAME=Cliente-1
python client-cloud.py

# Cliente 2
export SERVER_URL=https://tu-proyecto.up.railway.app
export PROCESS_ID=2
export PROCESS_NAME=Cliente-2
python client-cloud.py

# Cliente 3
export SERVER_URL=https://tu-proyecto.up.railway.app
export PROCESS_ID=3
export PROCESS_NAME=Cliente-3
python client-cloud.py
```

### Script Automático:
```batch
# Ejecutar start-cloud.bat
# Cuando pregunte la URL, poner:
https://tu-proyecto.up.railway.app
```

## Archivos Necesarios para Railway

### 1. requirements.txt (ya existe)
```
Flask==2.3.3
requests==2.31.0
flask-cors==4.0.0
```

### 2. runtime.txt (crear)
```
python-3.9.16
```

### 3. Procfile (crear)
```
web: python server.py
```

### 4. .gitignore (ya existe)
```
__pycache__/
*.pyc
.env
```

## Verificación del Despliegue

### 1. Verificar que Railway esté funcionando:
```
https://tu-proyecto.up.railway.app/status
```

### 2. Verificar desde navegador:
```
https://tu-proyecto.up.railway.app
```

### 3. Verificar logs en Railway:
```
1. Ir a la pestaña "Deployments"
2. Verificar que el último deployment sea exitoso
3. Revisar logs si hay errores
```

## Troubleshooting

### Problema: Error de puerto
```python
# En server.py, cambiar:
app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### Problema: Dependencias no encontradas
```bash
# Verificar que requirements.txt esté en el repositorio
# Railway instalará automáticamente las dependencias
```

### Problema: URL no funciona
```
1. Verificar que el deployment sea exitoso
2. Verificar variables de entorno
3. Revisar logs en Railway
```

## Ventajas de Railway

### Para tu situación:
✅ **No necesitas** acceso SSH
✅ **No necesitas** instalar nada
✅ **No necesitas** configurar servidor
✅ **URL pública** inmediata
✅ **SSL automático**
✅ **Gratis** para proyectos educativos

### Comparación con otras opciones:
- **Heroku**: Requiere tarjeta de crédito
- **Render**: Más lento en el despliegue
- **Vercel**: No soporta Python web apps
- **Netlify**: No soporta Python web apps

## Costos

### Railway Free Tier:
- ✅ **Gratis** para proyectos personales
- ✅ **500 horas/mes** de ejecución
- ✅ **1GB RAM** por proyecto
- ✅ **Sin límite** de proyectos
- ✅ **Sin tarjeta** de crédito requerida

### Si necesitas más:
- **$5/mes**: 1000 horas, 2GB RAM
- **$10/mes**: 2000 horas, 4GB RAM

## Próximos Pasos

1. **Crear cuenta** en Railway
2. **Subir código** a GitHub
3. **Conectar** Railway con GitHub
4. **Configurar** variables de entorno
5. **Obtener** URL pública
6. **Configurar** clientes locales
7. **Probar** el sistema

## Alternativa: Render

Si Railway no funciona, Render es la segunda mejor opción:

```
1. Ir a https://render.com/
2. Crear cuenta gratuita
3. Conectar repositorio GitHub
4. Configurar como "Web Service"
5. Obtener URL pública
```

¿Te gustaría que te ayude a configurar Railway paso a paso? 