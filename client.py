"""
Cliente del sistema distribuido con reloj lógico de Lamport.
Cada cliente mantiene su propio reloj y se comunica con el servidor UNAP.
"""

import os
import time
import threading
import random
import requests
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from lamport_clock import LamportClock

# Configuración del cliente
app = Flask(__name__)
CORS(app)

# Variables de entorno
PROCESS_ID = int(os.getenv('PROCESS_ID', 1))
PROCESS_NAME = os.getenv('PROCESS_NAME', 'Cliente')
SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:5000')

# Inicializar reloj lógico de Lamport
lamport_clock = LamportClock(PROCESS_ID, PROCESS_NAME)

# Plantilla HTML para mostrar el estado del cliente
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ process_name }} - Reloj Lógico de Lamport</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .clock-display { font-size: 24px; font-weight: bold; color: #2c3e50; text-align: center; margin: 20px 0; padding: 20px; background: #ecf0f1; border-radius: 5px; }
        .status { margin: 20px 0; }
        .event-log { background: #fff3cd; padding: 15px; border-radius: 5px; margin: 10px 0; max-height: 300px; overflow-y: auto; }
        .event { margin: 5px 0; padding: 5px; background: white; border-left: 3px solid #28a745; }
        .btn { background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #218838; }
        .btn-danger { background: #dc3545; }
        .btn-danger:hover { background: #c82333; }
        .auto-refresh { margin: 20px 0; }
        .connection-status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .connected { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .disconnected { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
    <script>
        function refreshPage() {
            location.reload();
        }
        
        function sendMessage() {
            const message = document.getElementById('messageInput').value;
            if (message.trim()) {
                fetch('/send_message', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                }).then(() => {
                    document.getElementById('messageInput').value = '';
                    setTimeout(refreshPage, 1000);
                });
            }
        }
        
        function performInternalEvent() {
            fetch('/internal_event', {method: 'POST'})
                .then(() => setTimeout(refreshPage, 1000));
        }
        
        // Auto-refresh cada 3 segundos
        setInterval(refreshPage, 3000);
    </script>
</head>
<body>
    <div class="container">
        <h1>🕐 {{ process_name }} - Algoritmo de Lamport</h1>
        
        <div class="clock-display">
            Reloj Lógico: <span style="color: #e74c3c;">{{ clock_time }}</span>
        </div>
        
        <div class="connection-status {{ 'connected' if server_connected else 'disconnected' }}">
            <strong>Estado del Servidor:</strong> {{ 'Conectado' if server_connected else 'Desconectado' }}
        </div>
        
        <div class="status">
            <h3>Estado del Cliente:</h3>
            <p><strong>ID del Proceso:</strong> {{ process_id }}</p>
            <p><strong>Nombre:</strong> {{ process_name }}</p>
            <p><strong>Servidor:</strong> {{ server_url }}</p>
        </div>
        
        <div style="margin: 20px 0;">
            <h3>Acciones:</h3>
            <input type="text" id="messageInput" placeholder="Escribe un mensaje..." style="padding: 10px; width: 300px; margin-right: 10px;">
            <button class="btn" onclick="sendMessage()">Enviar Mensaje</button>
            <button class="btn" onclick="performInternalEvent()">Evento Interno</button>
            <button class="btn btn-danger" onclick="refreshPage()">Actualizar</button>
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
            <span style="color: #6c757d; font-size: 12px;">(Auto-actualización cada 3 segundos)</span>
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
        # Mantener solo los últimos 30 eventos
        if len(events) > 30:
            events.pop(0)

def register_with_server():
    """Registra el cliente con el servidor UNAP."""
    try:
        response = requests.post(f"{SERVER_URL}/register", json={
            'process_id': PROCESS_ID,
            'process_name': PROCESS_NAME,
            'logical_time': lamport_clock.get_time()
        }, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Actualizar reloj con la respuesta del servidor
            lamport_clock.receive_event(data.get('server_clock', 0))
            add_event(f"Registrado exitosamente con el servidor - Reloj: {lamport_clock.get_time()}")
            return True
        else:
            add_event(f"Error al registrarse: {response.status_code}")
            return False
    except Exception as e:
        add_event(f"Error de conexión: {str(e)}")
        return False

def send_message_to_server(message: str):
    """Envía un mensaje al servidor."""
    try:
        # Incrementar reloj antes de enviar
        send_time = lamport_clock.send_event()
        
        response = requests.post(f"{SERVER_URL}/message", json={
            'sender_id': PROCESS_ID,
            'sender_name': PROCESS_NAME,
            'message': message,
            'logical_time': send_time
        }, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Actualizar reloj con la respuesta del servidor
            lamport_clock.receive_event(data.get('server_clock', 0))
            add_event(f"Mensaje enviado: '{message}' - Reloj: {lamport_clock.get_time()}")
            return True
        else:
            add_event(f"Error al enviar mensaje: {response.status_code}")
            return False
    except Exception as e:
        add_event(f"Error de conexión al enviar: {str(e)}")
        return False

def perform_internal_events():
    """Realiza eventos internos periódicamente."""
    while True:
        time.sleep(random.randint(4, 10))  # Evento cada 4-10 segundos
        new_time = lamport_clock.increment()
        add_event(f"Evento interno automático - Nuevo reloj: {new_time}")

@app.route('/')
def index():
    """Página principal del cliente."""
    # Verificar conexión con el servidor
    server_connected = False
    try:
        response = requests.get(f"{SERVER_URL}/status", timeout=2)
        server_connected = response.status_code == 200
    except:
        pass
    
    with events_lock:
        recent_events = events[-10:]  # Últimos 10 eventos
    
    return render_template_string(HTML_TEMPLATE,
        clock_time=lamport_clock.get_time(),
        process_id=PROCESS_ID,
        process_name=PROCESS_NAME,
        server_url=SERVER_URL,
        server_connected=server_connected,
        events=recent_events
    )

@app.route('/send_message', methods=['POST'])
def send_message():
    """Envía un mensaje al servidor."""
    data = request.get_json()
    message = data.get('message', 'Mensaje del cliente')
    
    success = send_message_to_server(message)
    
    return jsonify({
        'status': 'success' if success else 'error',
        'message': 'Mensaje enviado' if success else 'Error al enviar'
    })

@app.route('/internal_event', methods=['POST'])
def internal_event():
    """Realiza un evento interno manual."""
    new_time = lamport_clock.increment()
    add_event(f"Evento interno manual - Nuevo reloj: {new_time}")
    
    return jsonify({
        'status': 'success',
        'new_time': new_time
    })

@app.route('/status')
def get_status():
    """Obtiene el estado actual del cliente."""
    return jsonify(lamport_clock.get_status())

if __name__ == '__main__':
    # Iniciar thread para eventos internos automáticos
    internal_thread = threading.Thread(target=perform_internal_events, daemon=True)
    internal_thread.start()
    
    # Intentar registrar con el servidor
    add_event(f"Cliente {PROCESS_NAME} iniciado - Reloj inicial: {lamport_clock.get_time()}")
    
    # Esperar un poco antes de intentar registrar
    time.sleep(2)
    
    # Intentar registro inicial
    if register_with_server():
        print(f"✅ Cliente {PROCESS_NAME} registrado exitosamente")
    else:
        print(f"⚠️ Cliente {PROCESS_NAME} no pudo registrarse inicialmente")
    
    port = 5000 + PROCESS_ID
    print(f"🚀 Cliente {PROCESS_NAME} iniciado en puerto {port}")
    print(f"📊 Reloj lógico inicial: {lamport_clock.get_time()}")
    print(f"🌐 Accede a http://localhost:{port} para ver el estado")
    
    app.run(host='0.0.0.0', port=port, debug=False) 