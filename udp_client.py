"""
Cliente UDP con interfaz gráfica que implementa el algoritmo de Lamport.
Se conecta al servidor UDP y permite enviar mensajes y eventos internos.
"""

import socket
import threading
import json
import time
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from lamport_clock import LamportClock
from typing import Optional

class UDPClient:
    """Cliente UDP con interfaz gráfica que implementa algoritmo de Lamport."""
    
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
        
        # Estado de conexión
        self.connected = False
        self.running = False
        
        # Lista de eventos
        self.events = []
        self.events_lock = threading.Lock()
        
        # Contador de mensajes
        self.message_counter = 0
        
        # Interfaz gráfica
        self.root = None
        self.setup_gui()
        
    def add_event(self, description: str):
        """Agrega un evento al log."""
        with self.events_lock:
            timestamp = time.strftime('%H:%M:%S')
            event = f"[{timestamp}] {description}"
            self.events.append(event)
            if len(self.events) > 100:
                self.events.pop(0)
            
            # Actualizar GUI si existe
            if self.root:
                self.root.after(0, lambda: self.update_events_display())
            
            print(f"[{self.client_name}] {description}")
    
    def setup_gui(self):
        """Configura la interfaz gráfica."""
        self.root = tk.Tk()
        self.root.title(f"{self.client_name} - Algoritmo de Lamport")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Título
        title_frame = tk.Frame(self.root, bg="#f0f0f0")
        title_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(title_frame, text=f"🕐 {self.client_name}", 
                font=("Arial", 16, "bold"), bg="#f0f0f0").pack(side="left")
        
        # Frame para reloj lógico
        clock_frame = tk.Frame(self.root, bg="#ecf0f1", relief="raised", bd=2)
        clock_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(clock_frame, text="Reloj Lógico:", 
                font=("Arial", 12), bg="#ecf0f1").pack(side="left", padx=10)
        
        self.clock_label = tk.Label(clock_frame, text="0", 
                                   font=("Arial", 14, "bold"), fg="#e74c3c", bg="#ecf0f1")
        self.clock_label.pack(side="left")
        
        # Estado de conexión
        self.status_label = tk.Label(clock_frame, text="Desconectado", 
                                    font=("Arial", 10), fg="#dc3545", bg="#ecf0f1")
        self.status_label.pack(side="right", padx=10)
        
        # Frame de información
        info_frame = tk.Frame(self.root, bg="#f0f0f0")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(info_frame, text=f"ID: {self.client_id} | Servidor: {self.server_host}:{self.server_port}", 
                font=("Arial", 10), bg="#f0f0f0").pack(side="left")
        
        # Frame de acciones
        action_frame = tk.Frame(self.root, bg="#f0f0f0")
        action_frame.pack(fill="x", padx=10, pady=10)
        
        # Botones de control
        tk.Button(action_frame, text="Conectar", command=self.connect_to_server,
                 bg="#28a745", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Desconectar", command=self.disconnect,
                 bg="#dc3545", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Evento Interno", command=self.internal_event,
                 bg="#007bff", fg="white", font=("Arial", 10)).pack(side="left", padx=5)
        
        # Frame para envío de mensajes
        message_frame = tk.Frame(self.root, bg="#f0f0f0")
        message_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(message_frame, text="Mensaje:", font=("Arial", 10), bg="#f0f0f0").pack(side="left")
        
        self.message_entry = tk.Entry(message_frame, font=("Arial", 10), width=50)
        self.message_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        tk.Button(message_frame, text="Enviar", command=self.send_message,
                 bg="#28a745", fg="white", font=("Arial", 10)).pack(side="right", padx=5)
        
        # Área de eventos
        events_frame = tk.Frame(self.root, bg="#f0f0f0")
        events_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(events_frame, text="Registro de Eventos:", 
                font=("Arial", 12, "bold"), bg="#f0f0f0").pack(anchor="w")
        
        self.events_text = scrolledtext.ScrolledText(events_frame, height=15, 
                                                    font=("Courier", 9), bg="#fff3cd")
        self.events_text.pack(fill="both", expand=True, pady=5)
        
        # Iniciar actualizador de reloj
        self.update_clock_display()
        
        # Al cerrar ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def connect_to_server(self):
        """Conecta al servidor UDP."""
        if self.connected:
            messagebox.showwarning("Advertencia", "Ya está conectado al servidor")
            return
        
        try:
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
                    
                    self.add_event(f"Conectado al servidor - Reloj: {new_time}")
                    self.status_label.config(text="Conectado", fg="#28a745")
                    
                    # Iniciar hilos
                    self.start_background_threads()
                    
                else:
                    self.add_event("Error en registro con servidor")
                    
            except socket.timeout:
                self.add_event("Timeout conectando al servidor")
                
        except Exception as e:
            self.add_event(f"Error conectando: {e}")
            messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")
    
    def disconnect(self):
        """Desconecta del servidor."""
        self.running = False
        self.connected = False
        self.status_label.config(text="Desconectado", fg="#dc3545")
        self.add_event("Desconectado del servidor")
    
    def send_message(self):
        """Envía un mensaje al servidor."""
        if not self.connected:
            messagebox.showwarning("Advertencia", "No está conectado al servidor")
            return
        
        message_content = self.message_entry.get().strip()
        if not message_content:
            return
        
        try:
            # Incrementar reloj antes de enviar
            timestamp = self.lamport_clock.send_event()
            self.message_counter += 1
            
            message_data = {
                'type': 'message',
                'sender_id': self.client_id,
                'sender_name': self.client_name,
                'content': message_content,
                'timestamp': timestamp,
                'message_id': self.message_counter
            }
            
            message = json.dumps(message_data).encode()
            self.socket.sendto(message, (self.server_host, self.server_port))
            
            self.add_event(f"Mensaje enviado [T:{timestamp}]: {message_content}")
            self.message_entry.delete(0, tk.END)
            
        except Exception as e:
            self.add_event(f"Error enviando mensaje: {e}")
    
    def internal_event(self):
        """Realiza un evento interno."""
        new_time = self.lamport_clock.increment()
        self.add_event(f"Evento interno - Nuevo reloj: {new_time}")
        
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
                self.add_event(f"Error notificando evento interno: {e}")
    
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
                    self.add_event(f"Error recibiendo mensajes: {e}")
    
    def handle_broadcast(self, data: dict):
        """Maneja un mensaje broadcast del servidor."""
        sender_id = data.get('sender_id')
        content = data.get('content')
        original_timestamp = data.get('original_timestamp')
        server_timestamp = data.get('server_timestamp')
        
        # Actualizar reloj con timestamp del servidor
        new_time = self.lamport_clock.receive_event(server_timestamp)
        
        self.add_event(f"Mensaje de Cliente-{sender_id} [T:{original_timestamp}]: {content}")
        self.add_event(f"Reloj actualizado a: {new_time}")
    
    def handle_message_ack(self, data: dict):
        """Maneja confirmación de mensaje."""
        server_timestamp = data.get('server_timestamp')
        new_time = self.lamport_clock.receive_event(server_timestamp)
        self.add_event(f"Mensaje confirmado por servidor - Reloj: {new_time}")
    
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
                    self.add_event(f"Error en heartbeat: {e}")
    
    def auto_internal_events(self):
        """Genera eventos internos automáticamente."""
        while self.running:
            time.sleep(random.randint(8, 15))  # Evento cada 8-15 segundos
            if self.connected:
                self.internal_event()
    
    def update_clock_display(self):
        """Actualiza la visualización del reloj."""
        if self.root:
            self.clock_label.config(text=str(self.lamport_clock.get_time()))
            self.root.after(1000, self.update_clock_display)  # Actualizar cada segundo
    
    def update_events_display(self):
        """Actualiza la visualización de eventos."""
        if self.events_text:
            self.events_text.delete(1.0, tk.END)
            with self.events_lock:
                recent_events = self.events[-50:] if len(self.events) > 50 else self.events
                for event in recent_events:
                    self.events_text.insert(tk.END, event + "\n")
            
            # Scroll al final
            self.events_text.see(tk.END)
    
    def on_closing(self):
        """Maneja el cierre de la ventana."""
        self.disconnect()
        self.socket.close()
        self.root.destroy()
    
    def run(self):
        """Ejecuta la interfaz gráfica."""
        self.add_event(f"Cliente {self.client_name} iniciado")
        self.add_event(f"Reloj lógico inicial: {self.lamport_clock.get_time()}")
        self.root.mainloop()

def main():
    """Función principal para crear y ejecutar un cliente."""
    import sys
    
    # Obtener parámetros desde línea de comandos o usar valores por defecto
    if len(sys.argv) >= 3:
        client_id = int(sys.argv[1])
        client_name = sys.argv[2]
    else:
        client_id = int(input("Ingrese ID del cliente (1-99): "))
        client_name = input("Ingrese nombre del cliente: ") or f"Cliente-{client_id}"
    
    server_host = input("Servidor (localhost): ").strip() or "localhost"
    server_port = int(input("Puerto del servidor (5000): ") or "5000")
    
    # Crear y ejecutar cliente
    client = UDPClient(client_id, client_name, server_host, server_port)
    client.run()

if __name__ == '__main__':
    main()
