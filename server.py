"""
Servidor UNAP - Coordinador principal del sistema distribuido con relojes lógicos de Lamport.
"""

import os
import time
import threading
import random
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from lamport_clock import LamportClock

# Configuración del servidor
app = Flask(__name__)
CORS(app)

# Variables de entorno
PROCESS_ID = int(os.getenv('PROCESS_ID', 0))
PROCESS_NAME = os.getenv('PROCESS_NAME', 'UNAP-Server')

# Inicializar reloj lógico de Lamport
lamport_clock = LamportClock(PROCESS_ID, PROCESS_NAME)

# Almacenar información de clientes conectados
connected_clients = {}
client_lock = threading.Lock()

# Plantilla HTML para mostrar el estado del servidor
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Servidor UNAP - Reloj Lógico de Lamport</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .clock-display { font-size: 24px; font-weight: bold; color: #2c3e50; text-align: center; margin: 20px 0; padding: 20px; background: #ecf0f1; border-radius: 5px; }
        .status { margin: 20px 0; }
        .client-list { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
        .event-log { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto; }
        .event { margin: 5px 0; padding: 5px; background: white; border-left: 3px solid #007bff; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .auto-refresh { margin: 20px 0; }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        // Auto-refresh cada 2 segundos
        setInterval(refreshPage, 2000);
    </script>
</head>
<body>
    <div class="container">
        <h1>🕐 Servidor UNAP - Algoritmo de Lamport</h1>
        
        <div class="clock-display">
            Reloj Lógico: <span style="color: #e74c3c;">{{ clock_time }}</span>
        </div>
        
        <div class="status">
            <h3>Estado del Servidor:</h3>
            <p><strong>ID del Proceso:</strong> {{ process_id }}</p>
            <p><strong>Nombre:</strong> {{ process_name }}</p>
            <p><strong>Clientes Conectados:</strong> {{ client_count }}</p>
        </div>
        
        <div class="client-list">
            <h3>Clientes Registrados:</h3>
            {% for client in clients %}
            <div class="event">
                <strong>{{ client.name }}</strong> (ID: {{ client.id }}) - Reloj: {{ client.clock }}
            </div>
            {% endfor %}
        </div>
        
        <div class="event-log">
            <h3>Registro de Eventos:</h3>
            {% for event in events %}
            <div class="event">
                <strong>{{ event.timestamp }}</strong> - {{ event.description }}
            </div>
            {% endfor %}
        </div>
        
        <div class="auto-refresh">
            <button class="btn" onclick="refreshPage()">Actualizar Manualmente</button>
            <span style="color: #6c757d; font-size: 12px;">(Auto-actualización cada 2 segundos)</span>
        </div>
    </div>
</body>
</html>
"""

# Lista para almacenar eventos
events = []
events_lock = threading.Lock()

def add_event(description: str):
    """Agrega un evento al registro."""
    with events_lock:
        events.append({
            'timestamp': time.strftime('%H:%M:%S'),
            'description': description
        })
        # Mantener solo los últimos 50 eventos
        if len(events) > 50:
            events.pop(0)

def perform_internal_events():
    """Realiza eventos internos periódicamente."""
    while True:
        time.sleep(random.randint(3, 8))  # Evento cada 3-8 segundos
        new_time = lamport_clock.increment()
        add_event(f"Evento interno - Nuevo reloj: {new_time}")

@app.route('/')
def index():
    """Página principal del servidor."""
    with client_lock:
        clients = list(connected_clients.values())
    
    with events_lock:
        recent_events = events[-10:]  # Últimos 10 eventos
    
    return render_template_string(HTML_TEMPLATE,
        clock_time=lamport_clock.get_time(),
        process_id=PROCESS_ID,
        process_name=PROCESS_NAME,
        client_count=len(connected_clients),
        clients=clients,
        events=recent_events
    )

@app.route('/register', methods=['POST'])
def register_client():
    """Registra un nuevo cliente."""
    data = request.get_json()
    client_id = data.get('process_id')
    client_name = data.get('process_name')
    client_clock = data.get('logical_time')
    
    with client_lock:
        connected_clients[client_id] = {
            'id': client_id,
            'name': client_name,
            'clock': client_clock
        }
    
    # Actualizar reloj al recibir registro
    new_time = lamport_clock.receive_event(client_clock)
    add_event(f"Cliente {client_name} registrado - Reloj actualizado: {new_time}")
    
    return jsonify({
        'status': 'success',
        'message': f'Cliente {client_name} registrado exitosamente',
        'server_clock': new_time
    })

@app.route('/message', methods=['POST'])
def receive_message():
    """Recibe un mensaje de un cliente."""
    data = request.get_json()
    sender_id = data.get('sender_id')
    sender_name = data.get('sender_name')
    message = data.get('message')
    sender_clock = data.get('logical_time')
    
    # Actualizar reloj según algoritmo de Lamport
    new_time = lamport_clock.receive_event(sender_clock)
    
    # Actualizar información del cliente
    with client_lock:
        if sender_id in connected_clients:
            connected_clients[sender_id]['clock'] = sender_clock
    
    add_event(f"Mensaje de {sender_name}: '{message}' - Reloj actualizado: {new_time}")
    
    return jsonify({
        'status': 'success',
        'message': 'Mensaje recibido',
        'server_clock': new_time
    })

@app.route('/status')
def get_status():
    """Obtiene el estado actual del servidor."""
    return jsonify(lamport_clock.get_status())

@app.route('/broadcast', methods=['POST'])
def broadcast_message():
    """Envía un mensaje broadcast a todos los clientes."""
    data = request.get_json()
    message = data.get('message', 'Mensaje del servidor')
    
    # Incrementar reloj antes de enviar
    new_time = lamport_clock.send_event()
    
    add_event(f"Broadcast enviado: '{message}' - Reloj: {new_time}")
    
    return jsonify({
        'status': 'success',
        'message': 'Broadcast enviado',
        'server_clock': new_time
    })

if __name__ == '__main__':
    # Iniciar thread para eventos internos
    internal_thread = threading.Thread(target=perform_internal_events, daemon=True)
    internal_thread.start()
    
    add_event(f"Servidor UNAP iniciado - Reloj inicial: {lamport_clock.get_time()}")
    
    print(f"🚀 Servidor UNAP iniciado en puerto 5000")
    print(f"📊 Reloj lógico inicial: {lamport_clock.get_time()}")
    print(f"🌐 Accede a http://localhost:5000 para ver el estado")
    
    # Obtener puerto desde variable de entorno (para Railway)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 