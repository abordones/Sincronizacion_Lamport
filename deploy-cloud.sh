#!/bin/bash

# Script de despliegue para servidor en la nube
# Sistema Distribuido - Algoritmo de Lamport

echo "=========================================="
echo "Despliegue en la Nube - Algoritmo de Lamport"
echo "=========================================="

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker instalado. Reinicia la sesión y ejecuta el script nuevamente."
    exit 1
fi

# Verificar que Docker Compose esté instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Instalando..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose instalado."
fi

# Crear directorio para el proyecto
PROJECT_DIR="/opt/lamport-system"
echo "📁 Creando directorio del proyecto: $PROJECT_DIR"
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Copiar archivos del proyecto
echo "📋 Copiando archivos del proyecto..."
cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# Configurar firewall (si está disponible)
if command -v ufw &> /dev/null; then
    echo "🔥 Configurando firewall..."
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 22/tcp
    sudo ufw --force enable
    echo "✅ Firewall configurado."
fi

# Crear archivo de configuración de entorno
echo "⚙️ Creando configuración de entorno..."
cat > .env << EOF
# Configuración del servidor en la nube
FLASK_ENV=production
PROCESS_ID=0
PROCESS_NAME=UNAP-Server-Cloud
EOF

# Crear script de inicio automático
echo "🚀 Configurando inicio automático..."
sudo tee /etc/systemd/system/lamport-system.service > /dev/null << EOF
[Unit]
Description=Lamport System - Distributed Clock Synchronization
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/local/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

# Habilitar servicio
sudo systemctl enable lamport-system.service
sudo systemctl daemon-reload

# Construir y ejecutar
echo "🔨 Construyendo y ejecutando servicios..."
docker-compose -f docker-compose.prod.yml up --build -d

# Verificar que los servicios estén funcionando
echo "🔍 Verificando servicios..."
sleep 10

if curl -f http://localhost/status > /dev/null 2>&1; then
    echo "✅ Servidor UNAP funcionando correctamente"
else
    echo "❌ Error: El servidor no responde"
    echo "📋 Logs del servidor:"
    docker-compose -f docker-compose.prod.yml logs unap-server
    exit 1
fi

# Mostrar información final
echo ""
echo "=========================================="
echo "🎉 Despliegue completado exitosamente!"
echo "=========================================="
echo ""
echo "📋 Información del servidor:"
echo "- URL del servidor: http://$(curl -s ifconfig.me)"
echo "- Puerto HTTP: 80"
echo "- Puerto HTTPS: 443 (si configuras SSL)"
echo ""
echo "🔧 Comandos útiles:"
echo "- Ver logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "- Reiniciar: sudo systemctl restart lamport-system"
echo "- Detener: sudo systemctl stop lamport-system"
echo "- Estado: sudo systemctl status lamport-system"
echo ""
echo "💡 Para configurar SSL con Let's Encrypt:"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d tu-dominio.com"
echo ""
echo "🌐 Los clientes locales pueden conectarse usando:"
echo "   SERVER_URL=http://$(curl -s ifconfig.me) python client-cloud.py" 