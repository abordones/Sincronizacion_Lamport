"""
Script de prueba para verificar el funcionamiento del algoritmo de Lamport.
"""

import threading
import time
import json
import socket
from lamport_clock import LamportClock

def test_lamport_ordering():
    """Prueba el ordenamiento de mensajes según Lamport."""
    print("🧪 Probando ordenamiento de Lamport...")
    
    # Crear varios relojes lógicos
    clock1 = LamportClock(1, "Proceso-1")
    clock2 = LamportClock(2, "Proceso-2")
    clock3 = LamportClock(3, "Proceso-3")
    
    # Simular eventos
    print(f"Estado inicial:")
    print(f"  {clock1}")
    print(f"  {clock2}")
    print(f"  {clock3}")
    print()
    
    # Eventos internos
    print("Eventos internos:")
    t1 = clock1.increment()
    print(f"  Proceso-1 evento interno: {t1}")
    
    t2 = clock2.increment()
    print(f"  Proceso-2 evento interno: {t2}")
    
    t3 = clock3.increment()
    print(f"  Proceso-3 evento interno: {t3}")
    print()
    
    # Envío de mensajes
    print("Envío de mensajes:")
    send_time_1 = clock1.send_event()
    print(f"  Proceso-1 envía mensaje con timestamp: {send_time_1}")
    
    send_time_2 = clock2.send_event()
    print(f"  Proceso-2 envía mensaje con timestamp: {send_time_2}")
    print()
    
    # Recepción de mensajes
    print("Recepción de mensajes:")
    recv_time_3_from_1 = clock3.receive_event(send_time_1)
    print(f"  Proceso-3 recibe mensaje de Proceso-1: reloj actualizado a {recv_time_3_from_1}")
    
    recv_time_3_from_2 = clock3.receive_event(send_time_2)
    print(f"  Proceso-3 recibe mensaje de Proceso-2: reloj actualizado a {recv_time_3_from_2}")
    print()
    
    print("Estado final:")
    print(f"  {clock1}")
    print(f"  {clock2}")
    print(f"  {clock3}")
    print()

def test_server_connection():
    """Prueba la conexión con el servidor UDP."""
    print("🔌 Probando conexión con servidor UDP...")
    
    try:
        # Crear socket de prueba
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.settimeout(3.0)
        
        # Intentar enviar ping al servidor
        ping_data = {
            'type': 'ping',
            'timestamp': int(time.time())
        }
        
        message = json.dumps(ping_data).encode()
        test_socket.sendto(message, ('localhost', 5000))
        
        print("✅ Mensaje enviado al servidor")
        
        # Intentar recibir respuesta (opcional)
        try:
            data, addr = test_socket.recvfrom(1024)
            print(f"✅ Respuesta recibida de {addr}")
        except socket.timeout:
            print("⚠️  No se recibió respuesta (normal si servidor no maneja ping)")
        
        test_socket.close()
        
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        print("💡 Asegúrate de que el servidor UDP esté ejecutándose")

def test_message_ordering():
    """Prueba el ordenamiento de mensajes."""
    print("📋 Probando ordenamiento de mensajes...")
    
    # Simular mensajes con diferentes timestamps
    messages = [
        {'sender': 1, 'timestamp': 5, 'content': 'Mensaje A'},
        {'sender': 2, 'timestamp': 3, 'content': 'Mensaje B'},
        {'sender': 3, 'timestamp': 7, 'content': 'Mensaje C'},
        {'sender': 1, 'timestamp': 3, 'content': 'Mensaje D'},  # Mismo timestamp que B
        {'sender': 2, 'timestamp': 6, 'content': 'Mensaje E'},
    ]
    
    print("Mensajes sin ordenar:")
    for msg in messages:
        print(f"  [T:{msg['timestamp']}] Sender-{msg['sender']}: {msg['content']}")
    
    # Ordenar según algoritmo de Lamport
    def lamport_compare(msg1, msg2):
        if msg1['timestamp'] == msg2['timestamp']:
            return msg1['sender'] - msg2['sender']
        return msg1['timestamp'] - msg2['timestamp']
    
    from functools import cmp_to_key
    sorted_messages = sorted(messages, key=cmp_to_key(lamport_compare))
    
    print("\nMensajes ordenados según Lamport:")
    for msg in sorted_messages:
        print(f"  [T:{msg['timestamp']}] Sender-{msg['sender']}: {msg['content']}")
    print()

def main():
    """Función principal de pruebas."""
    print("🧪 PRUEBAS DEL SISTEMA DE LAMPORT")
    print("=" * 40)
    print()
    
    # Ejecutar pruebas
    test_lamport_ordering()
    print("-" * 40)
    test_message_ordering()
    print("-" * 40)
    test_server_connection()
    
    print()
    print("✅ Pruebas completadas")
    print()
    print("💡 Para usar el sistema:")
    print("   1. Ejecuta: python udp_server.py")
    print("   2. Ejecuta: python udp_client.py")
    print("   3. O usa: python launch_clients.py para múltiples clientes")

if __name__ == '__main__':
    main()
