"""
Implementación del reloj lógico de Lamport para sincronización de procesos distribuidos.
"""

import time
import threading
from typing import Dict, Any


class LamportClock:
    """
    Clase que implementa el algoritmo de reloj lógico de Lamport.
    
    El algoritmo de Lamport establece que:
    1. Antes de un evento interno: L = L + 1
    2. Antes de enviar un mensaje: L = L + 1, enviar L con el mensaje
    3. Al recibir un mensaje: L = max(L, timestamp_recibido) + 1
    """
    
    def __init__(self, process_id: int, process_name: str):
        """
        Inicializa el reloj lógico de Lamport.
        
        Args:
            process_id: Identificador único del proceso
            process_name: Nombre descriptivo del proceso
        """
        self.process_id = process_id
        self.process_name = process_name
        self.logical_time = 0
        self.lock = threading.Lock()
        
    def get_time(self) -> int:
        """
        Obtiene el tiempo lógico actual.
        
        Returns:
            Tiempo lógico actual
        """
        with self.lock:
            return self.logical_time
    
    def increment(self) -> int:
        """
        Incrementa el reloj lógico (evento interno).
        
        Returns:
            Nuevo tiempo lógico
        """
        with self.lock:
            self.logical_time += 1
            return self.logical_time
    
    def send_event(self) -> int:
        """
        Incrementa el reloj antes de enviar un mensaje.
        
        Returns:
            Tiempo lógico para incluir en el mensaje
        """
        return self.increment()
    
    def receive_event(self, received_timestamp: int) -> int:
        """
        Actualiza el reloj al recibir un mensaje según el algoritmo de Lamport.
        
        Args:
            received_timestamp: Timestamp recibido en el mensaje
            
        Returns:
            Nuevo tiempo lógico
        """
        with self.lock:
            self.logical_time = max(self.logical_time, received_timestamp) + 1
            return self.logical_time
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado actual del reloj lógico.
        
        Returns:
            Diccionario con información del estado del reloj
        """
        return {
            "process_id": self.process_id,
            "process_name": self.process_name,
            "logical_time": self.get_time(),
            "timestamp": time.time()
        }
    
    def __str__(self) -> str:
        """Representación en string del reloj lógico."""
        return f"{self.process_name} (ID: {self.process_id}) - Reloj Lógico: {self.get_time()}" 