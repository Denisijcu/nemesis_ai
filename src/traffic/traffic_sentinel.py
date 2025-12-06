#!/usr/bin/env python3
"""
Némesis IA - Traffic Sentinel
Capítulo 6: Análisis de Tráfico de Red

Sistema completo de monitoreo y detección de anomalías de tráfico
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional, Callable

from .traffic_collector import TrafficCollector
from .traffic_analyzer import TrafficAnalyzer
from .anomaly_detector import AnomalyDetector

logger = logging.getLogger(__name__)


class TrafficSentinel:
    """Sistema completo de análisis de tráfico"""
    
    def __init__(
        self,
        database=None,
        alert_manager=None,
        window_seconds: int = 60,
        baseline_samples: int = 15
    ):
        """
        Inicializa el Traffic Sentinel
        
        Args:
            database: Instancia de ThreatDatabase (opcional)
            alert_manager: Instancia de AlertManager (opcional)
            window_seconds: Ventana de tiempo para estadísticas
            baseline_samples: Mínimo de muestras para generar baseline
        """
        
        # Componentes del sistema
        self.collector = TrafficCollector(window_seconds=window_seconds)
        self.analyzer = TrafficAnalyzer(self.collector)
        self.detector = AnomalyDetector()
        
        # Integración externa
        self.database = database
        self.alert_manager = alert_manager
        
        # Configuración
        self.baseline_samples = baseline_samples
        self.baseline_generated = False
        
        # Callbacks
        self.on_anomaly_callback: Optional[Callable] = None
        
        # Estadísticas
        self.stats = {
            "packets_processed": 0,
            "anomalies_detected": 0,
            "threats_blocked": 0,
            "alerts_sent": 0
        }
        
        logger.info("🎖️  TrafficSentinel inicializado")
    
    def set_anomaly_callback(self, callback: Callable):
        """
        Establece callback para cuando se detecte una anomalía
        
        Args:
            callback: Función a llamar con la anomalía detectada
        """
        self.on_anomaly_callback = callback
    
    def process_packet(self, packet_info: dict):
        """
        Procesa un paquete a través de todo el pipeline
        
        Args:
            packet_info: Información del paquete
        """
        
        # 1. Recolectar estadísticas
        self.collector.process_packet(packet_info)
        self.stats["packets_processed"] += 1
        
        # 2. Actualizar tracking del detector
        self.detector.update_tracking(packet_info)
        
        # 3. Generar baseline si es necesario
        if not self.baseline_generated:
            history_len = len(self.collector.get_stats_history())
            if history_len >= self.baseline_samples:
                baseline = self.analyzer.generate_baseline(
                    min_samples=self.baseline_samples
                )
                if baseline:
                    self.baseline_generated = True
                    logger.info("✅ Baseline de tráfico generado automáticamente")
    
    def analyze_current_traffic(self) -> dict:
        """
        Analiza el tráfico actual y detecta anomalías
        
        Returns:
            Diccionario con análisis completo
        """
        
        # Obtener reporte de tráfico
        report = self.analyzer.analyze_current_traffic()
        
        # Preparar datos para el detector
        traffic_data = {
            "packets_per_second": report.current_pps,
            "bytes_per_second": report.current_bps,
            "new_connections": report.new_connections,
            "top_senders": report.top_senders,
            "port_usage": dict(report.top_ports),
            "protocols": report.protocol_breakdown
        }
        
        # Agregar baseline si está disponible
        baseline_data = None
        if self.analyzer.baseline:
            baseline_data = {
                "avg_pps": self.analyzer.baseline.avg_pps,
                "avg_bps": self.analyzer.baseline.avg_bps,
                "protocol_distribution": self.analyzer.baseline.protocol_distribution
            }
        
        # Detectar anomalías
        anomalies = self.detector.analyze_traffic(traffic_data, baseline_data)
        
        # Procesar anomalías detectadas
        for anomaly in anomalies:
            self._handle_anomaly(anomaly)
        
        return {
            "report": report,
            "anomalies": anomalies,
            "baseline_active": self.baseline_generated
        }
    
    def _handle_anomaly(self, anomaly):
        """
        Maneja una anomalía detectada
        
        Args:
            anomaly: Anomaly detectada
        """
        
        self.stats["anomalies_detected"] += 1
        
        logger.warning(
            f"🚨 Anomalía detectada: {anomaly.anomaly_type} "
            f"({anomaly.severity}) - {anomaly.source_ip}"
        )
        
        # Guardar en base de datos
        if self.database and anomaly.source_ip != "MULTIPLE":
            try:
                # Mapear tipo de anomalía a tipo de amenaza
                attack_type_map = {
                    "DDOS_ATTACK": "DDOS",
                    "PORT_SCAN": "PORT_SCAN",
                    "DATA_EXFILTRATION": "DATA_EXFILTRATION",
                    "SUSPICIOUS_PORT": "SUSPICIOUS_PORT_USAGE",
                    "UNUSUAL_PROTOCOL": "PROTOCOL_ANOMALY",
                    "OFF_HOURS_ACTIVITY": "SUSPICIOUS_TIMING"
                }
                
                attack_type = attack_type_map.get(
                    anomaly.anomaly_type,
                    "TRAFFIC_ANOMALY"
                )
                
                # Determinar acción basada en severidad
                action_map = {
                    "CRITICAL": "BLOCKED",
                    "HIGH": "BLOCKED",
                    "MEDIUM": "LOGGED",
                    "LOW": "LOGGED"
                }
                
                action = action_map.get(anomaly.severity, "LOGGED")
                
                self.database.add_threat(
                    source_ip=anomaly.source_ip,
                    attack_type=attack_type,
                    confidence=anomaly.confidence,
                    action_taken=action,
                    payload=str(anomaly.details)
                )
                
                # Bloquear IP si es crítica o alta
                if anomaly.severity in ["CRITICAL", "HIGH"]:
                    self.database.block_ip(
                        ip=anomaly.source_ip,
                        reason=f"{anomaly.anomaly_type}: {anomaly.description}"
                    )
                    self.stats["threats_blocked"] += 1
                
            except Exception as e:
                logger.error(f"Error guardando anomalía en BD: {e}")
        
        # Enviar alerta
        if self.alert_manager and anomaly.severity in ["CRITICAL", "HIGH"]:
            try:
                self.alert_manager.send_alert(
                    title=f"⚠️ {anomaly.anomaly_type}",
                    message=(
                        f"Severidad: {anomaly.severity}\n"
                        f"IP: {anomaly.source_ip}\n"
                        f"{anomaly.description}\n"
                        f"Confianza: {anomaly.confidence * 100:.0f}%"
                    ),
                    severity=anomaly.severity
                )
                self.stats["alerts_sent"] += 1
            except Exception as e:
                logger.error(f"Error enviando alerta: {e}")
        
        # Callback personalizado
        if self.on_anomaly_callback:
            try:
                self.on_anomaly_callback(anomaly)
            except Exception as e:
                logger.error(f"Error en callback de anomalía: {e}")
    
    def get_system_status(self) -> dict:
        """Retorna estado completo del sistema"""
        
        current_stats = self.collector.get_current_stats()
        bandwidth = self.collector.get_bandwidth_usage()
        
        return {
            "status": "ACTIVE",
            "baseline_generated": self.baseline_generated,
            "statistics": {
                "packets_processed": self.stats["packets_processed"],
                "anomalies_detected": self.stats["anomalies_detected"],
                "threats_blocked": self.stats["threats_blocked"],
                "alerts_sent": self.stats["alerts_sent"]
            },
            "current_traffic": {
                "packets_per_second": bandwidth["packets_per_second"],
                "bytes_per_second": bandwidth["bytes_per_second"],
                "active_connections": current_stats.active_connections
            },
            "baseline": {
                "avg_pps": self.analyzer.baseline.avg_pps if self.analyzer.baseline else None,
                "avg_bps": self.analyzer.baseline.avg_bps if self.analyzer.baseline else None
            } if self.analyzer.baseline else None
        }
    
    def get_full_report(self) -> dict:
        """Genera reporte completo del sistema"""
        
        # Análisis de tráfico
        analysis = self.analyze_current_traffic()
        
        # Resumen del analyzer
        analyzer_summary = self.analyzer.generate_summary_report()
        
        # Resumen del detector
        detector_summary = self.detector.get_anomaly_summary()
        
        # Estado del sistema
        system_status = self.get_system_status()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_status": system_status,
            "traffic_analysis": analyzer_summary,
            "anomaly_summary": detector_summary,
            "current_anomalies": [
                {
                    "type": a.anomaly_type,
                    "severity": a.severity,
                    "source_ip": a.source_ip,
                    "description": a.description,
                    "confidence": a.confidence
                }
                for a in analysis["anomalies"]
            ]
        }
    
    async def start_monitoring(self, interval: int = 10):
        """
        Inicia monitoreo continuo
        
        Args:
            interval: Intervalo de análisis en segundos
        """
        
        logger.info(f"🚀 Iniciando monitoreo continuo (intervalo: {interval}s)")
        
        try:
            while True:
                # Analizar tráfico actual
                analysis = self.analyze_current_traffic()
                
                # Log de estado
                if analysis["anomalies"]:
                    logger.warning(
                        f"⚠️  {len(analysis['anomalies'])} anomalías detectadas"
                    )
                else:
                    logger.debug("✅ Tráfico normal")
                
                # Esperar intervalo
                await asyncio.sleep(interval)
        
        except asyncio.CancelledError:
            logger.info("⏹️  Monitoreo detenido")
        except Exception as e:
            logger.error(f"❌ Error en monitoreo: {e}")