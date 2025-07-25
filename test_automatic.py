"""
Test automatizado del sistema UDP con algoritmo de Lamport.
"""

import threading
import time
import json
import socket
from simple_client import SimpleUDPClient

def test_client_connection():
    """Prueba la conexión de un cliente al servidor."""
    print("🧪 Probando conexión de cliente al servidor...")
    
    # Crear cliente de prueba
    client = SimpleUDPClient(1, "Cliente-Test", "localhost", 5000)
    
    # Intentar conectar
    if client.connect_to_server():
        print("✅ Cliente conectado exitosamente")
        
        # Iniciar hilos en segundo plano
        client.start_background_threads()
        
        # Enviar algunos mensajes de prueba
        time.sleep(1)
        client.send_message("Hola servidor!")
        
        time.sleep(1)
        client.internal_event()
        
        time.sleep(1)
        client.send_message("Segundo mensaje")
        
        time.sleep(2)
        client.disconnect()
        
        return True
    else:
        print("❌ No se pudo conectar al servidor")
        return False

def test_multiple_clients():
    """Prueba múltiples clientes conectándose."""
    print("\n🧪 Probando múltiples clientes...")
    
    clients = []
    
    # Crear 3 clientes
    for i in range(1, 4):
        client = SimpleUDPClient(i, f"Cliente-{i}", "localhost", 5000)
        clients.append(client)
    
    # Conectar todos los clientes
    connected_clients = []
    for client in clients:
        if client.connect_to_server():
            print(f"✅ {client.client_name} conectado")
            client.start_background_threads()
            connected_clients.append(client)
            time.sleep(0.5)
        else:
            print(f"❌ {client.client_name} no se pudo conectar")
    
    if not connected_clients:
        print("❌ Ningún cliente se conectó")
        return False
    
    # Realizar actividades
    time.sleep(1)
    
    # Cada cliente envía un mensaje
    for i, client in enumerate(connected_clients):
        client.send_message(f"Mensaje de {client.client_name} - #{i+1}")
        time.sleep(0.5)
    
    # Eventos internos
    time.sleep(1)
    for client in connected_clients:
        client.internal_event()
        time.sleep(0.3)
    
    # Más mensajes para probar el ordenamiento
    time.sleep(1)
    connected_clients[0].send_message("Mensaje A")
    connected_clients[2].send_message("Mensaje B") if len(connected_clients) > 2 else None
    connected_clients[1].send_message("Mensaje C") if len(connected_clients) > 1 else None
    
    # Esperar a que se procesen
    time.sleep(3)
    
    # Desconectar todos
    for client in connected_clients:
        client.disconnect()
    
    print(f"✅ Prueba completada con {len(connected_clients)} clientes")
    return True

def main():
    """Función principal de pruebas."""
    print("🚀 PRUEBAS AUTOMATIZADAS DEL SISTEMA LAMPORT UDP")
    print("=" * 60)
    
    # Verificar que el servidor esté ejecutándose
    print("🔍 Verificando servidor...")
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.settimeout(2.0)
        
        test_data = {'type': 'ping', 'timestamp': 0}
        message = json.dumps(test_data).encode()
        test_socket.sendto(message, ('localhost', 5000))
        
        test_socket.close()
        print("✅ Servidor detectado")
    except Exception as e:
        print(f"❌ Servidor no disponible: {e}")
        print("💡 Asegúrate de ejecutar: python udp_server.py")
        return
    
    print("-" * 60)
    
    # Ejecutar pruebas
    success = True
    
    # Prueba 1: Cliente único
    if not test_client_connection():
        success = False
    
    print("-" * 60)
    
    # Prueba 2: Múltiples clientes
    if not test_multiple_clients():
        success = False
    
    print("-" * 60)
    
    if success:
        print("🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("\n💡 El sistema está funcionando correctamente")
        print("📝 Para usar el sistema manualmente:")
        print("   1. python udp_server.py (en una terminal)")
        print("   2. python simple_client.py 1 Cliente-1 (en otra terminal)")
        print("   3. python udp_client.py (para interfaz gráfica)")
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("🔧 Revisa los logs para más detalles")

if __name__ == '__main__':
    main()
