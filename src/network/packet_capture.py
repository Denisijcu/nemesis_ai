#!/usr/bin/env python3
"""
Némesis IA - Packet Capture
Capítulo 4: Análisis de Protocolos

Captura de paquetes en tiempo real con Scapy
"""

import logging
from typing import Optional, Callable
from scapy.all import sniff, IP, TCP, UDP, DNS, Raw
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PacketInfo:
    """Información extraída de un paquete"""
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: Optional[int]
    protocol: str
    length: int
    payload: Optional[str]
    flags: Optional[str]
    
    # Campos específicos
    http_method: Optional[str] = None
    http_uri: Optional[str] = None
    dns_query: Optional[str] = None


class PacketCapture:
    """Captura y análisis básico de paquetes"""
    
    def __init__(self, interface: str = "eth0", filter_str: str = ""):
        """
        Inicializa el capturador de paquetes
        
        Args:
            interface: Interface de red a monitorear
            filter_str: Filtro BPF (ej: "tcp port 80")
        """
        self.interface = interface
        self.filter_str = filter_str
        self.packet_count = 0
        self.is_capturing = False
        
        logger.info(f"📡 PacketCapture inicializado en {interface}")
        if filter_str:
            logger.info(f"🔍 Filtro BPF: {filter_str}")
    
    def start_capture(
        self, 
        packet_callback: Callable[[PacketInfo], None],
        count: int = 0
    ):
        """
        Inicia la captura de paquetes
        
        Args:
            packet_callback: Función a llamar por cada paquete
            count: Número de paquetes a capturar (0 = infinito)
        """
        self.is_capturing = True
        
        logger.info("🚀 Iniciando captura de paquetes...")
        
        try:
            sniff(
                iface=self.interface,
                filter=self.filter_str,
                prn=lambda pkt: self._process_packet(pkt, packet_callback),
                count=count,
                store=False
            )
        except PermissionError:
            logger.error("❌ Error: Se requieren permisos root/sudo")
            raise
        except Exception as e:
            logger.error(f"❌ Error en captura: {e}")
            raise
        finally:
            self.is_capturing = False
    
    def _process_packet(self, packet, callback: Callable[[PacketInfo], None]):
        """Procesa un paquete capturado"""
        try:
            packet_info = self._extract_packet_info(packet)
            
            if packet_info:
                self.packet_count += 1
                callback(packet_info)
        
        except Exception as e:
            logger.error(f"❌ Error procesando paquete: {e}")
    
    def _extract_packet_info(self, packet) -> Optional[PacketInfo]:
        """Extrae información relevante del paquete"""
        
        # Verificar que tenga capa IP
        if not packet.haslayer(IP):
            return None
        
        ip_layer = packet[IP]
        
        # Información básica
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        protocol = "OTHER"
        src_port = None
        dst_port = None
        flags = None
        payload = None
        
        # HTTP
        http_method = None
        http_uri = None
        
        # DNS
        dns_query = None
        
        # TCP
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            protocol = "TCP"
            src_port = tcp_layer.sport
            dst_port = tcp_layer.dport
            flags = str(tcp_layer.flags)
            
            # Extraer payload HTTP
            if packet.haslayer(Raw):
                raw_payload = packet[Raw].load
                try:
                    payload_str = raw_payload.decode('utf-8', errors='ignore')
                    payload = payload_str[:500]  # Limitar tamaño
                    
                    # Detectar HTTP
                    if any(method in payload_str[:20] for method in ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']):
                        lines = payload_str.split('\r\n')
                        if lines:
                            parts = lines[0].split()
                            if len(parts) >= 2:
                                http_method = parts[0]
                                http_uri = parts[1]
                
                except:
                    payload = str(raw_payload[:100])
        
        # UDP
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            protocol = "UDP"
            src_port = udp_layer.sport
            dst_port = udp_layer.dport
            
            # DNS
            if packet.haslayer(DNS):
                dns_layer = packet[DNS]
                protocol = "DNS"
                
                if dns_layer.qd:
                    dns_query = dns_layer.qd.qname.decode('utf-8', errors='ignore')
        
        return PacketInfo(
            timestamp=datetime.now(),
            src_ip=src_ip,
            dst_ip=dst_ip,
            src_port=src_port,
            dst_port=dst_port,
            protocol=protocol,
            length=len(packet),
            payload=payload,
            flags=flags,
            http_method=http_method,
            http_uri=http_uri,
            dns_query=dns_query
        )
    
    def stop_capture(self):
        """Detiene la captura"""
        self.is_capturing = False
        logger.info(f"⏹️  Captura detenida - {self.packet_count} paquetes procesados")