"""
Servidor UDP con algoritmo de Lamport para sincronización de procesos distribuidos.
Mantiene el orden de mensajes usando relojes lógicos.
"""

import socket
import threading
import json
import time
from typing import Dict, List, Tuple
from lamport_clock import LamportClock
import heapq
from collections import defaultdict

class Message:
    """Clase para representar un mensaje con timestamp de Lamport."""
    def __init__(self, sender_id: int, content: str, timestamp: int, message_id: int):
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp
        self.message_id = message_id
        self.received_time = time.time()
    
    def __lt__(self, other):
        """Comparación para ordenar mensajes según algoritmo de Lamport."""
        if self.timestamp == other.timestamp:
            return self.sender_id < other.sender_id
        return self.timestamp < other.timestamp
    
    def __str__(self):
        return f"[{self.timestamp}] Cliente-{self.sender_id}: {self.content}"

class UDPServer:
    """Servidor UDP que implementa el algoritmo de Lamport."""
    
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Reloj lógico del servidor
        self.lamport_clock = LamportClock(0, "Servidor-UDP")
        
        # Clientes conectados: {client_id: (address, last_seen)}
        self.connected_clients = {}
        self.clients_lock = threading.Lock()
        
        # Cola de mensajes ordenada por timestamp de Lamport
        self.message_queue = []
        self.queue_lock = threading.Lock()
        
        # Contadores de mensajes por cliente
        self.message_counters = defaultdict(int)
        
        # Lista de eventos para mostrar
        self.events = []
        self.events_lock = threading.Lock()
        
        self.running = False
        
    def add_event(self, description: str):
        """Agrega un evento al log."""
        with self.events_lock:
            timestamp = time.strftime('%H:%M:%S')
            self.events.append(f"[{timestamp}] {description}")
            if len(self.events) > 50:
                self.events.pop(0)
            print(f"[SERVIDOR] {description}")
    
    def start(self):
        """Inicia el servidor UDP."""
        try:
            self.socket.bind((self.host, self.port))
            self.running = True
            self.add_event(f"Servidor iniciado en {self.host}:{self.port}")
            self.add_event(f"Reloj lógico inicial: {self.lamport_clock.get_time()}")
            
            # Hilo para procesar mensajes ordenados
            message_processor = threading.Thread(target=self.process_ordered_messages, daemon=True)
            message_processor.start()
            
            # Hilo para eventos internos
            internal_events = threading.Thread(target=self.internal_events, daemon=True)
            internal_events.start()
            
            # Hilo para limpiar clientes inactivos
            cleanup_thread = threading.Thread(target=self.cleanup_inactive_clients, daemon=True)
            cleanup_thread.start()
            
            print(f"🚀 Servidor UDP iniciado en {self.host}:{self.port}")
            print(f"📊 Reloj lógico inicial: {self.lamport_clock.get_time()}")
            print("💡 Esperando clientes...")
            
            self.listen()
            
        except Exception as e:
            self.add_event(f"Error al iniciar servidor: {e}")
            print(f"Error: {e}")
    
    def listen(self):
        """Escucha mensajes UDP entrantes."""
        while self.running:
            try:
                data, address = self.socket.recvfrom(1024)
                message_data = json.loads(data.decode())
                
                # Procesar mensaje en hilo separado
                handler = threading.Thread(
                    target=self.handle_message, 
                    args=(message_data, address),
                    daemon=True
                )
                handler.start()
                
            except Exception as e:
                if self.running:
                    self.add_event(f"Error al recibir mensaje: {e}")
    
    def handle_message(self, message_data: dict, address: tuple):
        """Maneja un mensaje recibido."""
        try:
            msg_type = message_data.get('type')
            client_timestamp = message_data.get('timestamp', 0)
            
            if msg_type == 'register':
                self.handle_registration(message_data, address)
                
            elif msg_type == 'message':
                self.handle_client_message(message_data, address)
                
            elif msg_type == 'heartbeat':
                self.handle_heartbeat(message_data, address)
                
            elif msg_type == 'internal_event':
                self.handle_internal_event(message_data, address)
                
        except Exception as e:
            self.add_event(f"Error procesando mensaje: {e}")
    
    def handle_registration(self, data: dict, address: tuple):
        """Maneja el registro de un nuevo cliente."""
        client_id = data.get('client_id')
        client_name = data.get('client_name')
        client_timestamp = data.get('timestamp', 0)
        
        # Actualizar reloj según algoritmo de Lamport
        new_time = self.lamport_clock.receive_event(client_timestamp)
        
        with self.clients_lock:
            self.connected_clients[client_id] = {
                'address': address,
                'name': client_name,
                'last_seen': time.time(),
                'registered_at': new_time
            }
        
        self.add_event(f"Cliente {client_name} (ID: {client_id}) registrado desde {address}")
        self.add_event(f"Reloj actualizado a: {new_time}")
        
        # Responder al cliente
        response = {
            'type': 'register_response',
            'status': 'success',
            'server_timestamp': new_time,
            'message': f'Registrado como {client_name}'
        }
        self.send_to_client(response, address)
    
    def handle_client_message(self, data: dict, address: tuple):
        """Maneja un mensaje de cliente."""
        client_id = data.get('sender_id')
        content = data.get('content')
        client_timestamp = data.get('timestamp')
        
        # Actualizar reloj según algoritmo de Lamport
        new_time = self.lamport_clock.receive_event(client_timestamp)
        
        # Crear mensaje con timestamp de Lamport
        self.message_counters[client_id] += 1
        message = Message(
            sender_id=client_id,
            content=content,
            timestamp=client_timestamp,  # Usar timestamp del cliente para ordenar
            message_id=self.message_counters[client_id]
        )
        
        # Agregar a cola ordenada
        with self.queue_lock:
            heapq.heappush(self.message_queue, message)
        
        # Actualizar información del cliente
        with self.clients_lock:
            if client_id in self.connected_clients:
                self.connected_clients[client_id]['last_seen'] = time.time()
        
        self.add_event(f"Mensaje recibido de Cliente-{client_id} [T:{client_timestamp}]: {content}")
        self.add_event(f"Reloj del servidor actualizado a: {new_time}")
        
        # Responder confirmación
        response = {
            'type': 'message_ack',
            'status': 'received',
            'server_timestamp': new_time,
            'original_timestamp': client_timestamp
        }
        self.send_to_client(response, address)
    
    def handle_heartbeat(self, data: dict, address: tuple):
        """Maneja heartbeat de cliente."""
        client_id = data.get('client_id')
        client_timestamp = data.get('timestamp', 0)
        
        # Actualizar tiempo de última conexión
        with self.clients_lock:
            if client_id in self.connected_clients:
                self.connected_clients[client_id]['last_seen'] = time.time()
        
        # Actualizar reloj
        new_time = self.lamport_clock.receive_event(client_timestamp)
        
        # Responder heartbeat
        response = {
            'type': 'heartbeat_ack',
            'server_timestamp': new_time
        }
        self.send_to_client(response, address)
    
    def handle_internal_event(self, data: dict, address: tuple):
        """Maneja evento interno de cliente."""
        client_id = data.get('client_id')
        client_timestamp = data.get('timestamp')
        
        # Actualizar reloj
        new_time = self.lamport_clock.receive_event(client_timestamp)
        self.add_event(f"Evento interno de Cliente-{client_id} [T:{client_timestamp}]")
        self.add_event(f"Reloj del servidor: {new_time}")
    
    def process_ordered_messages(self):
        """Procesa mensajes en orden según timestamp de Lamport."""
        while self.running:
            try:
                with self.queue_lock:
                    if self.message_queue:
                        # Procesar el mensaje más antiguo
                        message = heapq.heappop(self.message_queue)
                        self.add_event(f"PROCESANDO ORDENADAMENTE: {message}")
                        
                        # Retransmitir a todos los clientes conectados
                        self.broadcast_message(message)
                
                time.sleep(0.5)  # Procesar cada 0.5 segundos
                
            except Exception as e:
                self.add_event(f"Error procesando mensajes ordenados: {e}")
    
    def broadcast_message(self, message: Message):
        """Retransmite un mensaje a todos los clientes conectados."""
        timestamp = self.lamport_clock.send_event()
        
        broadcast_data = {
            'type': 'broadcast',
            'sender_id': message.sender_id,
            'content': message.content,
            'original_timestamp': message.timestamp,
            'server_timestamp': timestamp,
            'message_id': message.message_id
        }
        
        with self.clients_lock:
            for client_id, client_info in self.connected_clients.items():
                if client_id != message.sender_id:  # No enviar de vuelta al emisor
                    try:
                        self.send_to_client(broadcast_data, client_info['address'])
                    except Exception as e:
                        self.add_event(f"Error enviando broadcast a Cliente-{client_id}: {e}")
    
    def send_to_client(self, data: dict, address: tuple):
        """Envía datos a un cliente específico."""
        try:
            message = json.dumps(data).encode()
            self.socket.sendto(message, address)
        except Exception as e:
            self.add_event(f"Error enviando a {address}: {e}")
    
    def internal_events(self):
        """Genera eventos internos periódicamente."""
        while self.running:
            time.sleep(5)  # Evento interno cada 5 segundos
            new_time = self.lamport_clock.increment()
            self.add_event(f"Evento interno del servidor - Reloj: {new_time}")
    
    def cleanup_inactive_clients(self):
        """Limpia clientes inactivos."""
        while self.running:
            time.sleep(30)  # Revisar cada 30 segundos
            current_time = time.time()
            
            with self.clients_lock:
                inactive_clients = []
                for client_id, client_info in self.connected_clients.items():
                    if current_time - client_info['last_seen'] > 60:  # 60 segundos timeout
                        inactive_clients.append(client_id)
                
                for client_id in inactive_clients:
                    client_name = self.connected_clients[client_id]['name']
                    del self.connected_clients[client_id]
                    self.add_event(f"Cliente {client_name} (ID: {client_id}) desconectado por inactividad")
    
    def get_status(self):
        """Obtiene el estado actual del servidor."""
        with self.clients_lock:
            clients = len(self.connected_clients)
        
        with self.queue_lock:
            pending_messages = len(self.message_queue)
        
        return {
            'logical_time': self.lamport_clock.get_time(),
            'connected_clients': clients,
            'pending_messages': pending_messages,
            'events': self.events[-10:] if self.events else []
        }
    
    def stop(self):
        """Detiene el servidor."""
        self.running = False
        self.socket.close()
        self.add_event("Servidor detenido")

if __name__ == '__main__':
    server = UDPServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        server.stop()
