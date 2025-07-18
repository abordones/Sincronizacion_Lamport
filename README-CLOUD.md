# Despliegue en la Nube - Sistema Distribuido Lamport

## Arquitectura en la Nube

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente 1     │    │   Cliente 2     │    │   Cliente 3     │
│   (Local)       │    │   (Local)       │    │   (Local)       │
│   Puerto: 5001  │    │   Puerto: 5002  │    │   Puerto: 5003  │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Servidor UNAP           │
                    │   (Nube - AWS/GCP/Azure)  │
                    │   Puerto: 80/443          │
                    └───────────────────────────┘
```

## Requisitos del Servidor en la Nube

### Requisitos Mínimos
- **Sistema Operativo**: Ubuntu 20.04+ o CentOS 8+
- **RAM**: 1GB mínimo (2GB recomendado)
- **CPU**: 1 vCPU mínimo
- **Almacenamiento**: 10GB mínimo
- **Docker**: Instalado y configurado
- **Docker Compose**: Instalado
- **Puertos abiertos**: 80 (HTTP) y 443 (HTTPS)

### Requisitos Recomendados
- **RAM**: 4GB
- **CPU**: 2 vCPU
- **Almacenamiento**: 20GB SSD
- **Nginx**: Para proxy reverso y SSL
- **Dominio**: Para acceso público

## Despliegue del Servidor en la Nube

### 1. Preparar el Servidor

```bash
# Conectar al servidor
ssh usuario@tu-servidor.com

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
sudo apt install -y curl wget git
```

### 2. Ejecutar Script de Despliegue

```bash
# Clonar o subir el proyecto al servidor
git clone <tu-repositorio> /opt/lamport-system
cd /opt/lamport-system

# Dar permisos de ejecución
chmod +x deploy-cloud.sh

# Ejecutar script de despliegue
./deploy-cloud.sh
```

### 3. Configurar Dominio (Opcional)

```bash
# Instalar Certbot para SSL
sudo apt install certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Renovar automáticamente
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Configuración de Clientes Locales

### Opción 1: Script Automático (Windows)

```batch
# Ejecutar el script
start-cloud.bat

# Ingresar la URL del servidor cuando se solicite
# Ejemplo: http://tu-servidor.com
```

### Opción 2: Manual (Cualquier OS)

```bash
# Cliente 1
export PROCESS_ID=1
export PROCESS_NAME=Cliente-1
export SERVER_URL=http://tu-servidor.com
python client-cloud.py

# Cliente 2 (en otra terminal)
export PROCESS_ID=2
export PROCESS_NAME=Cliente-2
export SERVER_URL=http://tu-servidor.com
python client-cloud.py

# Cliente 3 (en otra terminal)
export PROCESS_ID=3
export PROCESS_NAME=Cliente-3
export SERVER_URL=http://tu-servidor.com
python client-cloud.py
```

### Opción 3: Docker Compose Local

```yaml
# docker-compose.local.yml
version: '3.8'

services:
  client1:
    build: .
    ports:
      - "5001:5001"
    environment:
      - PROCESS_ID=1
      - PROCESS_NAME=Cliente-1
      - SERVER_URL=http://tu-servidor.com
    command: python client-cloud.py

  client2:
    build: .
    ports:
      - "5002:5002"
    environment:
      - PROCESS_ID=2
      - PROCESS_NAME=Cliente-2
      - SERVER_URL=http://tu-servidor.com
    command: python client-cloud.py

  client3:
    build: .
    ports:
      - "5003:5003"
    environment:
      - PROCESS_ID=3
      - PROCESS_NAME=Cliente-3
      - SERVER_URL=http://tu-servidor.com
    command: python client-cloud.py
```

```bash
# Ejecutar clientes locales
docker-compose -f docker-compose.local.yml up --build
```

## Gestión del Servidor en la Nube

### Comandos Útiles

```bash
# Ver estado del servicio
sudo systemctl status lamport-system

# Reiniciar servicio
sudo systemctl restart lamport-system

# Ver logs en tiempo real
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs de un servicio específico
docker-compose -f docker-compose.prod.yml logs -f unap-server

# Actualizar código
cd /opt/lamport-system
git pull
docker-compose -f docker-compose.prod.yml up --build -d

# Hacer backup
docker-compose -f docker-compose.prod.yml down
tar -czf backup-$(date +%Y%m%d).tar.gz /opt/lamport-system
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoreo

```bash
# Ver uso de recursos
htop
df -h
docker stats

# Ver puertos abiertos
netstat -tlnp
sudo ufw status
```

## Seguridad

### Firewall

```bash
# Configurar firewall
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 5000/tcp   # Bloquear puerto interno
sudo ufw --force enable
```

### SSL/TLS

```bash
# Configurar SSL automático
sudo certbot --nginx -d tu-dominio.com

# Verificar renovación
sudo certbot renew --dry-run
```

### Variables de Entorno

```bash
# Crear archivo .env en el servidor
cat > /opt/lamport-system/.env << EOF
FLASK_ENV=production
PROCESS_ID=0
PROCESS_NAME=UNAP-Server-Cloud
SECRET_KEY=tu-clave-secreta-muy-segura
EOF
```

## Troubleshooting

### Problemas Comunes

1. **Servidor no responde**
   ```bash
   # Verificar que el servicio esté corriendo
   sudo systemctl status lamport-system
   
   # Ver logs
   docker-compose -f docker-compose.prod.yml logs unap-server
   ```

2. **Clientes no se conectan**
   ```bash
   # Verificar conectividad
   curl -v http://tu-servidor.com/status
   
   # Verificar firewall
   sudo ufw status
   ```

3. **Error de SSL**
   ```bash
   # Renovar certificado
   sudo certbot renew
   
   # Verificar configuración de Nginx
   sudo nginx -t
   ```

### Logs de Diagnóstico

```bash
# Logs del sistema
sudo journalctl -u lamport-system -f

# Logs de Docker
docker-compose -f docker-compose.prod.yml logs -f

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## Escalabilidad

### Múltiples Instancias

```bash
# Crear múltiples servidores
# Servidor 1: tu-servidor1.com
# Servidor 2: tu-servidor2.com
# Servidor 3: tu-servidor3.com

# Configurar balanceador de carga
# Usar Nginx, HAProxy o servicios de nube
```

### Monitoreo Avanzado

```bash
# Instalar herramientas de monitoreo
sudo apt install -y prometheus node-exporter grafana

# Configurar alertas
# Usar servicios como UptimeRobot, Pingdom
```

## Costos Estimados

### AWS EC2 (ejemplo)
- **t3.micro**: ~$8-15/mes
- **t3.small**: ~$15-30/mes
- **t3.medium**: ~$30-60/mes

### Google Cloud Platform
- **e2-micro**: ~$6-12/mes
- **e2-small**: ~$12-24/mes
- **e2-medium**: ~$24-48/mes

### Azure
- **B1s**: ~$10-20/mes
- **B1ms**: ~$20-40/mes
- **B2s**: ~$40-80/mes

## Resumen de Archivos

- `docker-compose.prod.yml`: Configuración para producción
- `client-cloud.py`: Cliente que se conecta a servidor remoto
- `deploy-cloud.sh`: Script de despliegue automático
- `start-cloud.bat`: Script para iniciar clientes locales
- `README-CLOUD.md`: Esta documentación 