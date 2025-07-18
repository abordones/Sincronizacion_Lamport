"""
Script de prueba para verificar la funcionalidad del sistema de relojes lógicos de Lamport.
"""

import time
import requests
import threading
from lamport_clock import LamportClock

def test_lamport_clock():
    """Prueba básica del reloj lógico de Lamport."""
    print("🧪 Probando reloj lógico de Lamport...")
    
    # Crear reloj
    clock = LamportClock(1, "Test-Clock")
    
    # Probar incremento
    assert clock.get_time() == 0
    assert clock.increment() == 1
    assert clock.get_time() == 1
    
    # Probar evento de envío
    send_time = clock.send_event()
    assert send_time == 2
    assert clock.get_time() == 2
    
    # Probar evento de recepción
    receive_time = clock.receive_event(5)
    assert receive_time == 6  # max(2, 5) + 1 = 6
    assert clock.get_time() == 6
    
    print("✅ Reloj lógico funcionando correctamente")

def test_server_connection():
    """Prueba la conexión con el servidor."""
    print("🌐 Probando conexión con servidor...")
    
    try:
        response = requests.get("http://localhost:5000/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Servidor conectado - Reloj: {data.get('logical_time')}")
            return True
        else:
            print(f"❌ Error de servidor: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor (¿está ejecutándose?)")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_client_connection():
    """Prueba la conexión con los clientes."""
    print("👥 Probando conexión con clientes...")
    
    clients = [
        ("Cliente 1", "http://localhost:5001"),
        ("Cliente 2", "http://localhost:5002"),
        ("Cliente 3", "http://localhost:5003")
    ]
    
    connected = 0
    for name, url in clients:
        try:
            response = requests.get(f"{url}/status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name} conectado - Reloj: {data.get('logical_time')}")
                connected += 1
            else:
                print(f"❌ {name} error: {response.status_code}")
        except:
            print(f"❌ {name} no disponible")
    
    print(f"📊 {connected}/3 clientes conectados")
    return connected > 0

def test_message_exchange():
    """Prueba el intercambio de mensajes."""
    print("💬 Probando intercambio de mensajes...")
    
    try:
        # Enviar mensaje desde cliente 1
        response = requests.post("http://localhost:5001/send_message", 
                               json={"message": "Mensaje de prueba"}, 
                               timeout=5)
        
        if response.status_code == 200:
            print("✅ Mensaje enviado correctamente")
            
            # Verificar que el servidor recibió el mensaje
            time.sleep(1)
            server_response = requests.get("http://localhost:5000/status", timeout=5)
            if server_response.status_code == 200:
                print("✅ Servidor procesó el mensaje")
                return True
            else:
                print("❌ Error al verificar servidor")
                return False
        else:
            print(f"❌ Error al enviar mensaje: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en intercambio de mensajes: {e}")
        return False

def run_system_test():
    """Ejecuta todas las pruebas del sistema."""
    print("🚀 Iniciando pruebas del sistema de Lamport...")
    print("=" * 50)
    
    # Prueba del reloj lógico
    test_lamport_clock()
    print()
    
    # Prueba de conexión con servidor
    server_ok = test_server_connection()
    print()
    
    if server_ok:
        # Prueba de conexión con clientes
        test_client_connection()
        print()
        
        # Prueba de intercambio de mensajes
        test_message_exchange()
        print()
    
    print("=" * 50)
    print("🏁 Pruebas completadas")
    
    if server_ok:
        print("\n📋 Resumen:")
        print("- Servidor UNAP: http://localhost:5000")
        print("- Cliente 1: http://localhost:5001")
        print("- Cliente 2: http://localhost:5002")
        print("- Cliente 3: http://localhost:5003")
        print("\n💡 Abre estas URLs en tu navegador para experimentar con el sistema")

if __name__ == "__main__":
    run_system_test() 