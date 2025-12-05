#!/usr/bin/env python3
"""
Némesis IA - Network Sentinel
Capítulo 4: Análisis de Protocolos

Integración completa: Captura + Análisis + Detección
"""

import asyncio
import logging
from typing import Optional
from datetime import datetime

from .packet_capture import PacketCapture, PacketInfo
from .protocol_analyzer import ProtocolAnalyzer, HTTPRequest, DNSQuery, PortScanEvent

logger = logging.getLogger(__name__)


class NetworkSentinel:
    """Centinela de Red - Monitoreo y análisis en tiempo real"""
    
    def __init__(
        self, 
        interface: str = "eth0",
        database=None,
        alert_manager=None,
        dashboard=None
    ):
        """
        Inicializa el Network Sentinel
        
        Args:
            interface: Interface de red a monitorear
            database: Instancia de ThreatDatabase (opcional)
            alert_manager: Instancia de AlertManager (opcional)
            dashboard: Instancia de Dashboard (opcional)
        """
        self.interface = interface
        self.database = database
        self.alert_manager = alert_manager
        self.dashboard = dashboard
        
        # Componentes
        self.capture = PacketCapture(interface)
        self.analyzer = ProtocolAnalyzer()
        
        # Estadísticas
        self.packets_processed = 0
        self.http_threats = 0
        self.dns_threats = 0
        self.port_scans = 0
        
        self._is_running = False
        
        logger.info(f"🌐 NetworkSentinel inicializado en {interface}")
        if database:
            logger.info("💾 Base de datos habilitada")
        if alert_manager:
            logger.info("📢 Sistema de alertas habilitado")
    
    async def start(self, packet_count: int = 0):
        """
        Inicia el monitoreo de red
        
        Args:
            packet_count: Número de paquetes a capturar (0 = infinito)
        """
        logger.info("🚀 NetworkSentinel iniciando...")
        self._is_running = True
        
        try:
            # Iniciar captura en thread separado
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.capture.start_capture,
                self._process_packet,
                packet_count
            )
        
        except Exception as e:
            logger.error(f"❌ Error en NetworkSentinel: {e}")
            raise
        
        finally:
            self._is_running = False
            logger.info(f"⏹️  NetworkSentinel detenido")
            self._print_statistics()
    
    def _process_packet(self, packet: PacketInfo):
        """Procesa cada paquete capturado"""
        self.packets_processed += 1
        
        try:
            # Análisis HTTP
            if packet.http_method and packet.http_uri:
                self._analyze_http_packet(packet)
            
            # Análisis DNS
            if packet.dns_query:
                self._analyze_dns_packet(packet)
            
            # Port scan detection
            if packet.protocol == "TCP" and packet.dst_port:
                self._detect_port_scan(packet)
        
        except Exception as e:
            logger.error(f"❌ Error procesando paquete: {e}")
    
    def _analyze_http_packet(self, packet: PacketInfo):
        """Analiza paquete HTTP"""
        http_analysis = self.analyzer.analyze_http(
            packet.http_method,
            packet.http_uri,
            packet.payload or ""
        )
        
        # Si hay patrones sospechosos
        if http_analysis.suspicious_patterns:
            self.http_threats += 1
            
            logger.warning(
                f"🚨 HTTP THREAT #{self.http_threats}: "
                f"{http_analysis.suspicious_patterns[0].upper()} "
                f"desde {packet.src_ip}"
            )
            
            # Guardar en BD y alertar
            if self.database or self.alert_manager:
                asyncio.create_task(
                    self._save_and_alert_http(packet, http_analysis)
                )
    
    def _analyze_dns_packet(self, packet: PacketInfo):
        """Analiza paquete DNS"""
        dns_analysis = self.analyzer.analyze_dns(packet.dns_query)
        
        # Si es sospechoso
        if dns_analysis.is_suspicious:
            self.dns_threats += 1
            
            logger.warning(
                f"🚨 DNS THREAT #{self.dns_threats}: "
                f"{dns_analysis.suspicious_reasons[0]} "
                f"- {dns_analysis.domain} desde {packet.src_ip}"
            )
            
            # Guardar en BD y alertar
            if self.database or self.alert_manager:
                asyncio.create_task(
                    self._save_and_alert_dns(packet, dns_analysis)
                )
    
    def _detect_port_scan(self, packet: PacketInfo):
        """Detecta port scanning"""
        if packet.flags:
            scan_event = self.analyzer.track_connection(
                packet.src_ip,
                packet.dst_ip,
                packet.dst_port,
                packet.flags
            )
            
            if scan_event:
                self.port_scans += 1
                
                logger.warning(
                    f"🚨 PORT SCAN #{self.port_scans}: "
                    f"{scan_event.scan_type} desde {scan_event.scanner_ip} "
                    f"→ {scan_event.target_ip} "
                    f"({len(scan_event.ports_scanned)} puertos)"
                )
                
                # Guardar en BD y alertar
                if self.database or self.alert_manager:
                    asyncio.create_task(
                        self._save_and_alert_portscan(scan_event)
                    )
    
    async def _save_and_alert_http(self, packet: PacketInfo, analysis: HTTPRequest):
        """Guarda amenaza HTTP y envía alertas"""
        try:
            threat_type = analysis.suspicious_patterns[0].upper()
            
            # Guardar en BD
            if self.database:
                from database.threat_database import ThreatRecord
                
                threat = ThreatRecord(
                    id=None,
                    timestamp=datetime.now(),
                    source_ip=packet.src_ip,
                    attack_type=threat_type,
                    payload=packet.http_uri,
                    confidence=0.85,
                    action_taken="MONITOR",
                    blocked=False
                )
                
                self.database.save_threat(threat)
            
            # Enviar alerta
            if self.alert_manager:
                await self.alert_manager.send_threat_alert(
                    source_ip=packet.src_ip,
                    attack_type=threat_type,
                    confidence=0.85,
                    payload=packet.http_uri,
                    action_taken="MONITOR"
                )
        
        except Exception as e:
            logger.error(f"❌ Error guardando amenaza HTTP: {e}")
    
    async def _save_and_alert_dns(self, packet: PacketInfo, analysis: DNSQuery):
        """Guarda amenaza DNS y envía alertas"""
        try:
            threat_type = "DNS_" + analysis.suspicious_reasons[0].upper()
            
            # Guardar en BD
            if self.database:
                from database.threat_database import ThreatRecord
                
                threat = ThreatRecord(
                    id=None,
                    timestamp=datetime.now(),
                    source_ip=packet.src_ip,
                    attack_type=threat_type,
                    payload=analysis.domain,
                    confidence=0.75,
                    action_taken="MONITOR",
                    blocked=False
                )
                
                self.database.save_threat(threat)
            
            # Enviar alerta
            if self.alert_manager:
                await self.alert_manager.send_threat_alert(
                    source_ip=packet.src_ip,
                    attack_type=threat_type,
                    confidence=0.75,
                    payload=analysis.domain,
                    action_taken="MONITOR"
                )
        
        except Exception as e:
            logger.error(f"❌ Error guardando amenaza DNS: {e}")
    
    async def _save_and_alert_portscan(self, scan: PortScanEvent):
        """Guarda port scan y envía alertas"""
        try:
            # Guardar en BD
            if self.database:
                from database.threat_database import ThreatRecord
                
                threat = ThreatRecord(
                    id=None,
                    timestamp=datetime.now(),
                    source_ip=scan.scanner_ip,
                    attack_type="PORT_SCAN",
                    payload=f"{scan.scan_type}: {len(scan.ports_scanned)} ports",
                    confidence=0.95,
                    action_taken="BLOCK",
                    blocked=True
                )
                
                self.database.save_threat(threat)
                self.database.block_ip(scan.scanner_ip, "Port scanning detected")
            
            # Enviar alerta
            if self.alert_manager:
                await self.alert_manager.send_threat_alert(
                    source_ip=scan.scanner_ip,
                    attack_type="PORT_SCAN",
                    confidence=0.95,
                    payload=f"{scan.scan_type}: {scan.target_ip}",
                    action_taken="BLOCK"
                )
        
        except Exception as e:
            logger.error(f"❌ Error guardando port scan: {e}")
    
    def _print_statistics(self):
        """Imprime estadísticas finales"""
        logger.info("📊 Estadísticas del NetworkSentinel:")
        logger.info(f"   📦 Paquetes procesados: {self.packets_processed}")
        logger.info(f"   🌐 Amenazas HTTP: {self.http_threats}")
        logger.info(f"   🔍 Amenazas DNS: {self.dns_threats}")
        logger.info(f"   🔍 Port scans: {self.port_scans}")
    
    @property
    def stats(self):
        """Retorna estadísticas"""
        return {
            "packets_processed": self.packets_processed,
            "http_threats": self.http_threats,
            "dns_threats": self.dns_threats,
            "port_scans": self.port_scans,
            "total_threats": self.http_threats + self.dns_threats + self.port_scans
        }