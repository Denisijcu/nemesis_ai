#!/usr/bin/env python3
"""
Némesis IA - Traffic Collector
Capítulo 6: Análisis de Tráfico de Red

Recolecta estadísticas de tráfico en tiempo real
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import time

logger = logging.getLogger(__name__)


@dataclass
class TrafficStats:
    """Estadísticas de tráfico en una ventana de tiempo"""
    timestamp: datetime
    
    # Contadores generales
    total_packets: int = 0
    total_bytes: int = 0
    
    # Por protocolo
    protocol_packets: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    protocol_bytes: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Por IP
    ip_packets_sent: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    ip_packets_recv: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    ip_bytes_sent: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    ip_bytes_recv: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    # Por puerto
    port_usage: Dict[int, int] = field(default_factory=lambda: defaultdict(int))
    
    # Conexiones
    active_connections: int = 0
    new_connections: int = 0
    closed_connections: int = 0
    
    # Flags TCP
    syn_packets: int = 0
    ack_packets: int = 0
    rst_packets: int = 0
    fin_packets: int = 0


@dataclass
class Connection:
    """Representa una conexión de red"""
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    start_time: datetime
    last_seen: datetime
    packets: int = 0
    bytes: int = 0
    state: str = "ACTIVE"  # ACTIVE, CLOSED


class TrafficCollector:
    """Recolector de estadísticas de tráfico"""
    
    def __init__(self, window_seconds: int = 60):
        """
        Inicializa el collector
        
        Args:
            window_seconds: Ventana de tiempo para estadísticas (segundos)
        """
        self.window_seconds = window_seconds
        
        # Estadísticas actuales
        self.current_stats = TrafficStats(timestamp=datetime.now())
        
        # Historial de estadísticas
        self.stats_history: List[TrafficStats] = []
        self.max_history = 60  # Últimos 60 periodos
        
        # Conexiones activas
        self.active_connections: Dict[str, Connection] = {}
        
        # Timestamp de última rotación
        self.last_rotation = time.time()
        
        logger.info(f"📊 TrafficCollector inicializado (window: {window_seconds}s)")
    
    def process_packet(self, packet_info: dict):
        """
        Procesa un paquete y actualiza estadísticas
        
        Args:
            packet_info: Información del paquete (del PacketCapture)
        """
        
        # Verificar si es momento de rotar ventana
        self._check_rotation()
        
        # Actualizar contadores generales
        self.current_stats.total_packets += 1
        packet_size = packet_info.get('size', 0)
        self.current_stats.total_bytes += packet_size
        
        # Protocolo
        protocol = packet_info.get('protocol', 'UNKNOWN')
        self.current_stats.protocol_packets[protocol] += 1
        self.current_stats.protocol_bytes[protocol] += packet_size
        
        # IPs
        src_ip = packet_info.get('src_ip')
        dst_ip = packet_info.get('dst_ip')
        
        if src_ip:
            self.current_stats.ip_packets_sent[src_ip] += 1
            self.current_stats.ip_bytes_sent[src_ip] += packet_size
        
        if dst_ip:
            self.current_stats.ip_packets_recv[dst_ip] += 1
            self.current_stats.ip_bytes_recv[dst_ip] += packet_size
        
        # Puertos
        src_port = packet_info.get('src_port')
        dst_port = packet_info.get('dst_port')
        
        if src_port:
            self.current_stats.port_usage[src_port] += 1
        if dst_port:
            self.current_stats.port_usage[dst_port] += 1
        
        # Flags TCP
        flags = packet_info.get('flags', {})
        if flags.get('S'):  # SYN
            self.current_stats.syn_packets += 1
        if flags.get('A'):  # ACK
            self.current_stats.ack_packets += 1
        if flags.get('R'):  # RST
            self.current_stats.rst_packets += 1
        if flags.get('F'):  # FIN
            self.current_stats.fin_packets += 1
        
        # Trackear conexión
        if src_ip and dst_ip and protocol in ['TCP', 'UDP']:
            self._track_connection(packet_info)
    
    def _track_connection(self, packet_info: dict):
        """Trackea una conexión individual"""
        
        src_ip = packet_info.get('src_ip')
        dst_ip = packet_info.get('dst_ip')
        src_port = packet_info.get('src_port', 0)
        dst_port = packet_info.get('dst_port', 0)
        protocol = packet_info.get('protocol')
        packet_size = packet_info.get('size', 0)
        
        # Crear key de conexión
        conn_key = f"{src_ip}:{src_port}->{dst_ip}:{dst_port}:{protocol}"
        
        now = datetime.now()
        
        if conn_key in self.active_connections:
            # Actualizar conexión existente
            conn = self.active_connections[conn_key]
            conn.last_seen = now
            conn.packets += 1
            conn.bytes += packet_size
            
            # Verificar si la conexión se cerró
            flags = packet_info.get('flags', {})
            if flags.get('F') or flags.get('R'):  # FIN o RST
                conn.state = "CLOSED"
                self.current_stats.closed_connections += 1
        
        else:
            # Nueva conexión
            conn = Connection(
                src_ip=src_ip,
                dst_ip=dst_ip,
                src_port=src_port,
                dst_port=dst_port,
                protocol=protocol,
                start_time=now,
                last_seen=now,
                packets=1,
                bytes=packet_size
            )
            self.active_connections[conn_key] = conn
            self.current_stats.new_connections += 1
        
        # Actualizar contador de conexiones activas
        self.current_stats.active_connections = len([
            c for c in self.active_connections.values()
            if c.state == "ACTIVE"
        ])
    
    def _check_rotation(self):
        """Verifica si es momento de rotar la ventana de estadísticas"""
        
        current_time = time.time()
        
        if current_time - self.last_rotation >= self.window_seconds:
            # Guardar estadísticas actuales en historial
            self.stats_history.append(self.current_stats)
            
            # Limitar tamaño del historial
            if len(self.stats_history) > self.max_history:
                self.stats_history.pop(0)
            
            # Crear nuevas estadísticas
            self.current_stats = TrafficStats(timestamp=datetime.now())
            
            # Limpiar conexiones viejas (más de 5 minutos inactivas)
            cutoff_time = datetime.now() - timedelta(minutes=5)
            self.active_connections = {
                k: v for k, v in self.active_connections.items()
                if v.last_seen > cutoff_time
            }
            
            self.last_rotation = current_time
            
            logger.debug(f"📊 Ventana de estadísticas rotada")
    
    def get_current_stats(self) -> TrafficStats:
        """Retorna estadísticas actuales"""
        return self.current_stats
    
    def get_stats_history(self, periods: int = 10) -> List[TrafficStats]:
        """
        Retorna historial de estadísticas
        
        Args:
            periods: Número de periodos a retornar
            
        Returns:
            Lista de estadísticas históricas
        """
        return self.stats_history[-periods:]
    
    def get_top_talkers(self, limit: int = 10) -> List[tuple]:
        """
        Retorna las IPs más activas por tráfico enviado
        
        Args:
            limit: Número de IPs a retornar
            
        Returns:
            Lista de tuplas (ip, bytes_sent)
        """
        sorted_ips = sorted(
            self.current_stats.ip_bytes_sent.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_ips[:limit]
    
    def get_protocol_distribution(self) -> Dict[str, float]:
        """
        Retorna distribución porcentual de protocolos
        
        Returns:
            Diccionario {protocol: percentage}
        """
        total = self.current_stats.total_packets
        if total == 0:
            return {}
        
        return {
            protocol: (count / total) * 100
            for protocol, count in self.current_stats.protocol_packets.items()
        }
    
    def get_bandwidth_usage(self) -> Dict[str, float]:
        """
        Retorna uso de ancho de banda en bytes/segundo
        
        Returns:
            Diccionario con métricas de bandwidth
        """
        elapsed = time.time() - self.last_rotation
        if elapsed == 0:
            elapsed = 1
        
        return {
            "bytes_per_second": self.current_stats.total_bytes / elapsed,
            "packets_per_second": self.current_stats.total_packets / elapsed,
            "total_bytes": self.current_stats.total_bytes,
            "total_packets": self.current_stats.total_packets
        }
    
    def get_connection_stats(self) -> Dict[str, int]:
        """Retorna estadísticas de conexiones"""
        return {
            "active": self.current_stats.active_connections,
            "new": self.current_stats.new_connections,
            "closed": self.current_stats.closed_connections,
            "total_tracked": len(self.active_connections)
        }
    
    def get_summary(self) -> Dict:
        """Retorna un resumen completo de estadísticas"""
        return {
            "timestamp": self.current_stats.timestamp.isoformat(),
            "window_seconds": self.window_seconds,
            "general": {
                "total_packets": self.current_stats.total_packets,
                "total_bytes": self.current_stats.total_bytes
            },
            "bandwidth": self.get_bandwidth_usage(),
            "protocols": dict(self.current_stats.protocol_packets),
            "connections": self.get_connection_stats(),
            "top_talkers": self.get_top_talkers(5),
            "top_ports": sorted(
                self.current_stats.port_usage.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }