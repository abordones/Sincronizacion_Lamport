"""
Script para lanzar múltiples clientes UDP de forma automática.
"""

import subprocess
import time
import sys
import os

def launch_client(client_id: int, client_name: str, server_host="localhost", server_port=5000):
    """Lanza un cliente UDP en una nueva ventana de comando."""
    try:
        # Comando para ejecutar cliente
        python_cmd = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "udp_client.py")
        
        # En Windows, usar start para abrir nueva ventana
        if os.name == 'nt':  # Windows
            cmd = f'start "Cliente-{client_id}" cmd /k "{python_cmd}" "{script_path}" {client_id} "{client_name}"'
            subprocess.run(cmd, shell=True)
        else:  # Linux/Mac
            cmd = [python_cmd, script_path, str(client_id), client_name]
            subprocess.Popen(cmd)
        
        print(f"✅ Cliente {client_name} (ID: {client_id}) iniciado")
        
    except Exception as e:
        print(f"❌ Error iniciando cliente {client_id}: {e}")

def main():
    """Función principal."""
    print("🚀 Launcher de Clientes UDP - Algoritmo de Lamport")
    print("=" * 50)
    
    # Configuración por defecto
    server_host = input("Servidor (localhost): ").strip() or "localhost"
    server_port = int(input("Puerto del servidor (5000): ") or "5000")
    
    print(f"Servidor configurado: {server_host}:{server_port}")
    print()
    
    # Preguntar cuántos clientes lanzar
    try:
        num_clients = int(input("¿Cuántos clientes lanzar? (1-10): ") or "3")
        if num_clients < 1 or num_clients > 10:
            num_clients = 3
    except ValueError:
        num_clients = 3
    
    print(f"Lanzando {num_clients} clientes...")
    print()
    
    # Lanzar clientes
    for i in range(1, num_clients + 1):
        client_name = f"Cliente-{i}"
        launch_client(i, client_name, server_host, server_port)
        time.sleep(1)  # Esperar 1 segundo entre lanzamientos
    
    print()
    print(f"✅ Se han lanzado {num_clients} clientes")
    print("💡 Cada cliente se abre en su propia ventana")
    print("🔍 Revisa las ventanas de comando para ver los clientes")
    print()
    print("Presiona Enter para salir...")
    input()

if __name__ == '__main__':
    main()
