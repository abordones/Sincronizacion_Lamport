# Sistema Distribuido - Algoritmo de Lamport

## Descripción

Este proyecto implementa un sistema distribuido que utiliza el **Algoritmo de Lamport** para sincronización de relojes lógicos entre procesos distribuidos. El sistema consta de:

- **1 Servidor UNAP** (coordinador)
- **3 Clientes** distribuidos
- **Relojes lógicos** en cada proceso
- **Interfaz web** para monitoreo en tiempo real

## Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cliente 1     │    │   Cliente 2     │    │   Cliente 3     │
│   Puerto: 5001  │    │   Puerto: 5002  │    │   Puerto: 5003  │
│   ID: 1         │    │   ID: 2         │    │   ID: 3         │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │     Servidor UNAP         │
                    │     Puerto: 5000          │
                    │     ID: 0                 │
                    └───────────────────────────┘
```

## Algoritmo de Lamport

El algoritmo implementa las siguientes reglas:

1. **Evento Interno**: `L = L + 1`
2. **Envío de Mensaje**: `L = L + 1`, enviar `L` con el mensaje
3. **Recepción de Mensaje**: `L = max(L, timestamp_recibido) + 1`

## Características

- ✅ **Relojes lógicos** en cada proceso
- ✅ **Sincronización automática** según algoritmo de Lamport
- ✅ **Interfaz web** en tiempo real
- ✅ **Eventos automáticos** y manuales
- ✅ **Comunicación HTTP** serializada
- ✅ **Docker Compose** para orquestación
- ✅ **Auto-actualización** de interfaces

## Requisitos

- Docker
- Docker Compose

## Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd taller6_lamport
```

### 2. Ejecutar con Docker Compose
```bash
docker-compose up --build
```

### 3. Acceder a las interfaces

- **Servidor UNAP**: http://localhost:5000
- **Cliente 1**: http://localhost:5001
- **Cliente 2**: http://localhost:5002
- **Cliente 3**: http://localhost:5003

### 4. Experimentar con el sistema

1. **Observar relojes lógicos** en cada interfaz
2. **Enviar mensajes** desde cualquier cliente
3. **Realizar eventos internos** manualmente
4. **Ver sincronización automática** de relojes

## Estructura del Proyecto

```
taller6_lamport/
├── docker-compose.yml      # Orquestación de contenedores
├── Dockerfile             # Imagen base de Python
├── requirements.txt       # Dependencias de Python
├── lamport_clock.py      # Implementación del reloj lógico
├── server.py             # Servidor UNAP (coordinador)
├── client.py             # Cliente distribuido
└── README.md             # Documentación
```

## Funcionalidades

### Servidor UNAP
- Coordina todos los procesos
- Mantiene registro de clientes conectados
- Procesa mensajes y actualiza relojes
- Interfaz web con estado en tiempo real

### Clientes
- Mantienen reloj lógico independiente
- Se registran automáticamente con el servidor
- Pueden enviar mensajes y realizar eventos internos
- Interfaz web individual

### Eventos Automáticos
- **Eventos internos**: Cada proceso incrementa su reloj automáticamente
- **Sincronización**: Los relojes se sincronizan al intercambiar mensajes
- **Registro**: Todos los eventos se registran con timestamps

## Comandos Útiles

### Ver logs de todos los servicios
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f unap-server
docker-compose logs -f client1
```

### Reiniciar servicios
```bash
docker-compose restart
```

### Detener y limpiar
```bash
docker-compose down
docker-compose down --volumes
```

## Experimentación

Para experimentar con el sistema:

1. **Abrir múltiples pestañas** con las diferentes interfaces
2. **Observar** cómo los relojes se incrementan automáticamente
3. **Enviar mensajes** entre procesos y ver la sincronización
4. **Realizar eventos internos** manualmente
5. **Analizar** el comportamiento del algoritmo de Lamport

## Tecnologías Utilizadas

- **Python 3.9**: Lenguaje principal
- **Flask**: Framework web para servidor y clientes
- **Docker**: Contenedores para aislamiento
- **Docker Compose**: Orquestación de servicios
- **HTTP/JSON**: Comunicación serializada entre procesos

## Notas Técnicas

- Los relojes lógicos se implementan con **threading.Lock()** para concurrencia
- La comunicación utiliza **requests** para HTTP
- Las interfaces se auto-actualizan cada 2-3 segundos
- Los eventos se almacenan en memoria (no persistencia)
- El sistema es **fault-tolerant** para desconexiones temporales 