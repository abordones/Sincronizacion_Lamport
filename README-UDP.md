# Sistema de Sincronización de Lamport con UDP

Este proyecto implementa el algoritmo de relojes lógicos de Lamport para sincronización de procesos distribuidos usando comunicación UDP.

## 🎯 Características

- **Comunicación UDP**: Protocolo de comunicación más eficiente para mensajería
- **Algoritmo de Lamport**: Implementación completa del algoritmo de sincronización
- **Ordenamiento de Mensajes**: Los mensajes se procesan en orden lógico según timestamps de Lamport
- **Interfaz Gráfica**: Cliente con interfaz gráfica usando Tkinter
- **Eventos Internos**: Simulación de eventos internos automáticos
- **Sistema Local**: Funciona completamente en red local sin dependencias externas

## 📁 Estructura del Proyecto

```
├── lamport_clock.py        # Implementación del reloj lógico de Lamport
├── udp_server.py          # Servidor UDP que coordina los clientes
├── udp_client.py          # Cliente con interfaz gráfica
├── launch_clients.py      # Script para lanzar múltiples clientes
├── test_lamport.py        # Pruebas del algoritmo de Lamport
├── start_system.bat       # Script de inicio automático (Windows)
├── requirements.txt       # Dependencias Python
└── README-UDP.md         # Este archivo
```

## 🚀 Inicio Rápido

### Opción 1: Inicio Automático (Windows)
```bash
# Ejecutar el script de inicio automático
start_system.bat
```

### Opción 2: Inicio Manual

1. **Iniciar el servidor:**
```bash
python udp_server.py
```

2. **Iniciar clientes:**
```bash
# Opción A: Un cliente individual
python udp_client.py

# Opción B: Múltiples clientes automáticamente
python launch_clients.py
```

## 📊 Algoritmo de Lamport Implementado

### Reglas del Algoritmo

1. **Evento Interno**: `L = L + 1`
2. **Envío de Mensaje**: `L = L + 1`, enviar L con el mensaje
3. **Recepción de Mensaje**: `L = max(L, timestamp_recibido) + 1`

### Ordenamiento de Mensajes

Los mensajes se ordenan según:
1. **Timestamp de Lamport** (menor primero)
2. **ID del Proceso** (en caso de empate en timestamp)

## 🔧 Componentes del Sistema

### Servidor UDP (`udp_server.py`)

- **Puerto**: 5000 (por defecto)
- **Funciones**:
  - Registro de clientes
  - Recepción y ordenamiento de mensajes
  - Broadcast de mensajes ordenados
  - Manejo de eventos internos
  - Limpieza de clientes inactivos

### Cliente UDP (`udp_client.py`)

- **Interfaz Gráfica**: Tkinter
- **Funciones**:
  - Conexión al servidor
  - Envío de mensajes
  - Recepción de broadcasts
  - Eventos internos automáticos
  - Visualización del reloj lógico

### Reloj de Lamport (`lamport_clock.py`)

- **Thread-Safe**: Uso de locks para concurrencia
- **Métodos Principales**:
  - `increment()`: Evento interno
  - `send_event()`: Antes de enviar mensaje
  - `receive_event(timestamp)`: Al recibir mensaje

## 🧪 Pruebas

Ejecutar las pruebas del sistema:

```bash
python test_lamport.py
```

Las pruebas verifican:
- Funcionamiento del algoritmo de Lamport
- Ordenamiento correcto de mensajes
- Conectividad con el servidor

## 📋 Protocolo de Comunicación

### Tipos de Mensajes

#### 1. Registro de Cliente
```json
{
    "type": "register",
    "client_id": 1,
    "client_name": "Cliente-1",
    "timestamp": 5
}
```

#### 2. Mensaje de Cliente
```json
{
    "type": "message",
    "sender_id": 1,
    "sender_name": "Cliente-1",
    "content": "Hola mundo",
    "timestamp": 7,
    "message_id": 1
}
```

#### 3. Broadcast del Servidor
```json
{
    "type": "broadcast",
    "sender_id": 1,
    "content": "Hola mundo",
    "original_timestamp": 7,
    "server_timestamp": 8,
    "message_id": 1
}
```

#### 4. Evento Interno
```json
{
    "type": "internal_event",
    "client_id": 1,
    "timestamp": 9
}
```

#### 5. Heartbeat
```json
{
    "type": "heartbeat",
    "client_id": 1,
    "timestamp": 10
}
```

## 🎮 Uso del Cliente

### Interfaz Gráfica

1. **Reloj Lógico**: Muestra el tiempo lógico actual
2. **Estado de Conexión**: Indica si está conectado al servidor
3. **Envío de Mensajes**: Campo de texto para enviar mensajes
4. **Evento Interno**: Botón para generar eventos internos
5. **Log de Eventos**: Historial de todos los eventos

### Controles

- **Conectar**: Se conecta al servidor UDP
- **Desconectar**: Se desconecta del servidor
- **Evento Interno**: Incrementa el reloj lógico
- **Enviar Mensaje**: Envía mensaje al servidor (Enter también funciona)

## ⚙️ Configuración

### Variables de Entorno

- `PROCESS_ID`: ID único del proceso (por defecto desde línea de comandos)
- `PROCESS_NAME`: Nombre del proceso (por defecto desde línea de comandos)
- `SERVER_HOST`: Dirección del servidor (por defecto: localhost)
- `SERVER_PORT`: Puerto del servidor (por defecto: 5000)

### Parámetros del Servidor

```python
server = UDPServer(host='localhost', port=5000)
```

### Parámetros del Cliente

```python
client = UDPClient(
    client_id=1, 
    client_name="Cliente-1",
    server_host='localhost', 
    server_port=5000
)
```

## 🔍 Monitoreo

### Logs del Servidor

El servidor muestra:
- Registro/desconexión de clientes
- Mensajes recibidos con timestamps
- Mensajes procesados en orden
- Eventos internos del servidor

### Logs del Cliente

Cada cliente muestra:
- Estado de conexión
- Mensajes enviados/recibidos
- Eventos internos
- Actualizaciones del reloj lógico

## 🚨 Manejo de Errores

- **Timeout de Conexión**: 5 segundos para operaciones UDP
- **Clientes Inactivos**: Limpieza automática después de 60 segundos
- **Reconexión Automática**: Los clientes pueden reconectarse automáticamente
- **Validación de Mensajes**: Verificación de formato JSON

## 🎯 Ejemplo de Uso

1. **Iniciar servidor**:
   ```bash
   python udp_server.py
   ```

2. **Iniciar 3 clientes**:
   ```bash
   python launch_clients.py
   ```
   - Seleccionar 3 clientes
   - Se abren 3 ventanas separadas

3. **Interacción**:
   - Conectar cada cliente al servidor
   - Enviar mensajes desde diferentes clientes
   - Observar el orden de procesamiento en el servidor
   - Generar eventos internos y ver actualizaciones del reloj

## 📈 Características Avanzadas

### Ordenamiento Garantizado

- Los mensajes se procesan en orden estricto según Lamport
- Se usa una cola de prioridad (heap) para ordenamiento eficiente
- En caso de timestamps iguales, se usa el ID del proceso como desempate

### Concurrencia

- Servidor multi-hilo para manejar múltiples clientes
- Locks para proteger estructuras compartidas
- Threads separados para diferentes funcionalidades

### Robustez

- Heartbeat para detectar clientes desconectados
- Timeouts para evitar bloqueos
- Manejo de excepciones en todas las operaciones de red

## 🔧 Resolución de Problemas

### Puerto en Uso
```
Error: [Errno 10048] Only one usage of each socket address is normally permitted
```
**Solución**: Cambiar el puerto o cerrar procesos que usen el puerto 5000

### Cliente No Se Conecta
**Verificar**:
1. Servidor está ejecutándose
2. Puerto correcto (5000)
3. No hay firewall bloqueando
4. Dirección IP correcta

### Mensajes No Se Ordenan
**Verificar**:
1. Implementación correcta de `__lt__` en clase Message
2. Timestamps se actualizan correctamente
3. Cola de prioridad funciona bien

## 📝 Notas de Implementación

- **UDP vs TCP**: Se eligió UDP por simplicidad y eficiencia
- **Tkinter**: Interfaz gráfica multiplataforma incluida en Python
- **JSON**: Serialización simple y legible para mensajes
- **Threading**: Concurrencia para mejor rendimiento
- **Heap Queue**: Estructura de datos eficiente para ordenamiento

Este sistema demuestra los principios fundamentales de la sincronización distribuida usando el algoritmo de Lamport de manera práctica y visual.
