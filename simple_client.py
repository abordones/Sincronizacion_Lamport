"""
Cliente UDP simple para probar el sistema de Lamport sin interfaz gráfica.
"""

import socket
import threading
import json
import time
import random
from lamport_clock import LamportClock

class SimpleUDPClient:
    """Cliente UDP simple para pruebas."""
    
    def __init__(self, client_id: int, client_name: str, server_host='localhost', server_port=5000):
        self.client_id = client_id
        self.client_name = client_name
        self.server_host = server_host
        self.server_port = server_port
        
        # Socket UDP
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(5.0)
        
        # Reloj lógico de Lamport
        self.lamport_clock = LamportClock(client_id, client_name)
        
        # Estado
        self.connected = False
        self.running = False
        self.message_counter = 0
        
    def log(self, message):
        """Imprime un mensaje con timestamp."""
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] [{self.client_name}] {message}")
    
    def connect_to_server(self):
        """Conecta al servidor UDP."""
        try:
            self.log("Intentando conectar al servidor...")
            
            # Enviar registro
            timestamp = self.lamport_clock.send_event()
            register_data = {
                'type': 'register',
                'client_id': self.client_id,
                'client_name': self.client_name,
                'timestamp': timestamp
            }
            
            message = json.dumps(register_data).encode()
            self.socket.sendto(message, (self.server_host, self.server_port))
            self.log(f"Registro enviado con timestamp: {timestamp}")
            
            # Esperar respuesta
            try:
                data, _ = self.socket.recvfrom(1024)
                response = json.loads(data.decode())
                
                if response.get('type') == 'register_response' and response.get('status') == 'success':
                    self.connected = True
                    self.running = True
                    
                    # Actualizar reloj con respuesta del servidor
                    server_timestamp = response.get('server_timestamp', 0)
                    new_time = self.lamport_clock.receive_event(server_timestamp)
                    
                    self.log(f"✅ Conectado al servidor - Reloj actualizado: {new_time}")
                    return True
                else:
                    self.log("❌ Error en registro con servidor")
                    return False
                    
            except socket.timeout:
                self.log("❌ Timeout conectando al servidor")
                return False
                
        except Exception as e:
            self.log(f"❌ Error conectando: {e}")
            return False
    
    def send_message(self, content):
        """Envía un mensaje al servidor."""
        if not self.connected:
            self.log("❌ No conectado al servidor")
            return False
        
        try:
            # Incrementar reloj antes de enviar
            timestamp = self.lamport_clock.send_event()
            self.message_counter += 1
            
            message_data = {
                'type': 'message',
                'sender_id': self.client_id,
                'sender_name': self.client_name,
                'content': content,
                'timestamp': timestamp,
                'message_id': self.message_counter
            }
            
            message = json.dumps(message_data).encode()
            self.socket.sendto(message, (self.server_host, self.server_port))
            
            self.log(f"📤 Mensaje enviado [T:{timestamp}]: {content}")
            return True
            
        except Exception as e:
            self.log(f"❌ Error enviando mensaje: {e}")
            return False
    
    def internal_event(self):
        """Realiza un evento interno."""
        new_time = self.lamport_clock.increment()
        self.log(f"🔄 Evento interno - Nuevo reloj: {new_time}")
        
        # Notificar al servidor del evento interno
        if self.connected:
            try:
                event_data = {
                    'type': 'internal_event',
                    'client_id': self.client_id,
                    'timestamp': new_time
                }
                message = json.dumps(event_data).encode()
                self.socket.sendto(message, (self.server_host, self.server_port))
            except Exception as e:
                self.log(f"❌ Error notificando evento interno: {e}")
        
        return new_time
    
    def start_background_threads(self):
        """Inicia hilos en segundo plano."""
        # Hilo para recibir mensajes
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        # Hilo para heartbeat
        heartbeat_thread = threading.Thread(target=self.heartbeat, daemon=True)
        heartbeat_thread.start()
        
        # Hilo para eventos internos automáticos
        auto_events_thread = threading.Thread(target=self.auto_internal_events, daemon=True)
        auto_events_thread.start()
    
    def receive_messages(self):
        """Recibe mensajes del servidor."""
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1024)
                message_data = json.loads(data.decode())
                
                msg_type = message_data.get('type')
                
                if msg_type == 'broadcast':
                    self.handle_broadcast(message_data)
                elif msg_type == 'message_ack':
                    self.handle_message_ack(message_data)
                elif msg_type == 'heartbeat_ack':
                    pass  # Solo para mantener conexión
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    self.log(f"❌ Error recibiendo mensajes: {e}")
    
    def handle_broadcast(self, data: dict):
        """Maneja un mensaje broadcast del servidor."""
        sender_id = data.get('sender_id')
        content = data.get('content')
        original_timestamp = data.get('original_timestamp')
        server_timestamp = data.get('server_timestamp')
        
        # Actualizar reloj con timestamp del servidor
        new_time = self.lamport_clock.receive_event(server_timestamp)
        
        self.log(f"📨 Mensaje de Cliente-{sender_id} [T:{original_timestamp}]: {content}")
        self.log(f"🕐 Reloj actualizado a: {new_time}")
    
    def handle_message_ack(self, data: dict):
        """Maneja confirmación de mensaje."""
        server_timestamp = data.get('server_timestamp')
        new_time = self.lamport_clock.receive_event(server_timestamp)
        self.log(f"✅ Mensaje confirmado por servidor - Reloj: {new_time}")
    
    def heartbeat(self):
        """Envía heartbeat al servidor."""
        while self.running:
            try:
                time.sleep(10)  # Heartbeat cada 10 segundos
                if self.connected:
                    heartbeat_data = {
                        'type': 'heartbeat',
                        'client_id': self.client_id,
                        'timestamp': self.lamport_clock.get_time()
                    }
                    message = json.dumps(heartbeat_data).encode()
                    self.socket.sendto(message, (self.server_host, self.server_port))
            except Exception as e:
                if self.running:
                    self.log(f"❌ Error en heartbeat: {e}")
    
    def auto_internal_events(self):
        """Genera eventos internos automáticamente."""
        while self.running:
            time.sleep(random.randint(5, 10))  # Evento cada 5-10 segundos
            if self.connected:
                self.internal_event()
    
    def disconnect(self):
        """Desconecta del servidor."""
        self.running = False
        self.connected = False
        self.socket.close()
        self.log("🔌 Desconectado del servidor")
    
    def run_interactive(self):
        """Ejecuta el cliente en modo interactivo."""
        self.log(f"Cliente {self.client_name} iniciado")
        self.log(f"Reloj lógico inicial: {self.lamport_clock.get_time()}")
        
        if not self.connect_to_server():
            return
        
        self.start_background_threads()
        
        print("\n" + "="*50)
        print("COMANDOS DISPONIBLES:")
        print("  m <mensaje>  - Enviar mensaje")
        print("  i            - Evento interno")
        print("  s            - Ver estado")
        print("  q            - Salir")
        print("="*50)
        
        try:
            while self.running:
                command = input(f"\n[{self.client_name}] > ").strip()
                
                if command.lower() == 'q':
                    break
                elif command.lower() == 'i':
                    self.internal_event()
                elif command.lower() == 's':
                    self.log(f"Estado: Reloj={self.lamport_clock.get_time()}, Conectado={self.connected}")
                elif command.startswith('m '):
                    message_content = command[2:].strip()
                    if message_content:
                        self.send_message(message_content)
                    else:
                        print("Uso: m <mensaje>")
                elif command == '':
                    continue
                else:
                    print("Comando no reconocido. Usa 'q' para salir.")
        
        except KeyboardInterrupt:
            pass
        
        self.disconnect()

def main():
    """Función principal."""
    import sys
    
    print("🚀 Cliente UDP Simple - Algoritmo de Lamport")
    print("=" * 50)
    
    # Obtener parámetros
    if len(sys.argv) >= 3:
        client_id = int(sys.argv[1])
        client_name = sys.argv[2]
    else:
        try:
            client_id = int(input("Ingrese ID del cliente (1-99): "))
            client_name = input("Ingrese nombre del cliente: ") or f"Cliente-{client_id}"
        except ValueError:
            print("ID inválido")
            return
    
    server_host = input("Servidor (localhost): ").strip() or "localhost"
    try:
        server_port = int(input("Puerto del servidor (5000): ") or "5000")
    except ValueError:
        server_port = 5000
    
    print(f"\nConfiguracion:")
    print(f"  Cliente: {client_name} (ID: {client_id})")
    print(f"  Servidor: {server_host}:{server_port}")
    print()
    
    # Crear y ejecutar cliente
    client = SimpleUDPClient(client_id, client_name, server_host, server_port)
    client.run_interactive()

if __name__ == '__main__':
    main()
