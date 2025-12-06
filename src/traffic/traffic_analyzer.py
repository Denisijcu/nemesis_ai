#!/usr/bin/env python3
"""
Némesis IA - Traffic Analyzer
Capítulo 6: Análisis de Tráfico de Red

Analiza patrones de tráfico y genera baselines
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import statistics

from .traffic_collector import TrafficCollector, TrafficStats

logger = logging.getLogger(__name__)


@dataclass
class TrafficBaseline:
    """Baseline de tráfico normal"""
    # Packets per second
    avg_pps: float
    std_pps: float
    max_pps: float
    
    # Bytes per second
    avg_bps: float
    std_bps: float
    max_bps: float
    
    # Connections per minute
    avg_cpm: float
    std_cpm: float
    max_cpm: float
    
    # Protocol distribution (percentages)
    protocol_distribution: Dict[str, float]
    
    # Top ports used
    common_ports: List[int]
    
    # Timestamp
    created_at: datetime
    samples: int


@dataclass
class TrafficReport:
    """Reporte de análisis de tráfico"""
    timestamp: datetime
    
    # Métricas actuales
    current_pps: float
    current_bps: float
    current_connections: int
    
    # Top IPs
    top_senders: List[Tuple[str, int]]  # (ip, bytes)
    top_receivers: List[Tuple[str, int]]
    
    # Protocol breakdown
    protocol_breakdown: Dict[str, float]  # {protocol: percentage}
    
    # Port analysis
    top_ports: List[Tuple[int, int]]  # (port, count)
    unusual_ports: List[int]
    
    # Connection analysis
    total_connections: int
    new_connections: int
    closed_connections: int
    
    # Bandwidth analysis
    total_bandwidth: int
    upload_bandwidth: int
    download_bandwidth: int
    
    # Deviations from baseline (if available)
    pps_deviation: Optional[float] = None
    bps_deviation: Optional[float] = None
    unusual_protocols: List[str] = None


class TrafficAnalyzer:
    """Analizador de tráfico con baseline learning"""
    
    def __init__(self, collector: TrafficCollector):
        """
        Inicializa el analyzer
        
        Args:
            collector: Instancia de TrafficCollector
        """
        self.collector = collector
        self.baseline: Optional[TrafficBaseline] = None
        
        # Lista de puertos comunes conocidos
        self.common_ports = {
            20, 21,    # FTP
            22,        # SSH
            23,        # Telnet
            25,        # SMTP
            53,        # DNS
            80, 443,   # HTTP/HTTPS
            110, 143,  # POP3/IMAP
            3306,      # MySQL
            5432,      # PostgreSQL
            6379,      # Redis
            8080, 8443 # HTTP alt
        }
        
        logger.info("📊 TrafficAnalyzer inicializado")
    
    def generate_baseline(self, min_samples: int = 10) -> Optional[TrafficBaseline]:
        """
        Genera un baseline de tráfico normal
        
        Args:
            min_samples: Mínimo de muestras requeridas
            
        Returns:
            TrafficBaseline o None si no hay suficientes datos
        """
        history = self.collector.get_stats_history(periods=60)
        
        if len(history) < min_samples:
            logger.warning(f"No hay suficientes muestras para baseline ({len(history)}/{min_samples})")
            return None
        
        # Calcular métricas
        pps_values = []
        bps_values = []
        cpm_values = []
        protocol_counts = {}
        port_counts = {}
        
        for stats in history:
            # Calcular rates (asumiendo ventana de 60s)
            window = self.collector.window_seconds
            
            pps = stats.total_packets / window
            bps = stats.total_bytes / window
            cpm = stats.new_connections
            
            pps_values.append(pps)
            bps_values.append(bps)
            cpm_values.append(cpm)
            
            # Acumular protocolos
            for proto, count in stats.protocol_packets.items():
                protocol_counts[proto] = protocol_counts.get(proto, 0) + count
            
            # Acumular puertos
            for port, count in stats.port_usage.items():
                port_counts[port] = port_counts.get(port, 0) + count
        
        # Calcular estadísticas
        baseline = TrafficBaseline(
            avg_pps=statistics.mean(pps_values),
            std_pps=statistics.stdev(pps_values) if len(pps_values) > 1 else 0,
            max_pps=max(pps_values),
            
            avg_bps=statistics.mean(bps_values),
            std_bps=statistics.stdev(bps_values) if len(bps_values) > 1 else 0,
            max_bps=max(bps_values),
            
            avg_cpm=statistics.mean(cpm_values),
            std_cpm=statistics.stdev(cpm_values) if len(cpm_values) > 1 else 0,
            max_cpm=max(cpm_values),
            
            protocol_distribution=self._calculate_distribution(protocol_counts),
            common_ports=self._get_top_items(port_counts, 20),
            
            created_at=datetime.now(),
            samples=len(history)
        )
        
        self.baseline = baseline
        
        logger.info(f"✅ Baseline generado con {len(history)} muestras")
        logger.info(f"   • PPS promedio: {baseline.avg_pps:.1f}")
        logger.info(f"   • BPS promedio: {baseline.avg_bps:,.0f}")
        
        return baseline
    
    def _calculate_distribution(self, counts: Dict) -> Dict[str, float]:
        """Calcula distribución porcentual"""
        total = sum(counts.values())
        if total == 0:
            return {}
        
        return {
            key: (count / total) * 100
            for key, count in counts.items()
        }
    
    def _get_top_items(self, counts: Dict, limit: int) -> List:
        """Obtiene top N items"""
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return [item[0] for item in sorted_items[:limit]]
    
    def analyze_current_traffic(self) -> TrafficReport:
        """
        Analiza el tráfico actual y genera un reporte
        
        Returns:
            TrafficReport con análisis completo
        """
        stats = self.collector.get_current_stats()
        bandwidth = self.collector.get_bandwidth_usage()
        
        # Top IPs
        top_senders = self.collector.get_top_talkers(10)
        
        # Top receivers (invertir para ver quién recibe más)
        top_receivers = sorted(
            stats.ip_bytes_recv.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Protocol breakdown
        protocol_breakdown = self.collector.get_protocol_distribution()
        
        # Top ports
        top_ports = sorted(
            stats.port_usage.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        # Unusual ports (no comunes)
        unusual_ports = [
            port for port, count in stats.port_usage.items()
            if port not in self.common_ports and count > 5
        ]
        
        # Calcular bandwidth total y por dirección
        total_upload = sum(stats.ip_bytes_sent.values())
        total_download = sum(stats.ip_bytes_recv.values())
        
        # Crear reporte
        report = TrafficReport(
            timestamp=datetime.now(),
            current_pps=bandwidth['packets_per_second'],
            current_bps=bandwidth['bytes_per_second'],
            current_connections=stats.active_connections,
            top_senders=top_senders,
            top_receivers=top_receivers,
            protocol_breakdown=protocol_breakdown,
            top_ports=top_ports,
            unusual_ports=unusual_ports[:10],
            total_connections=stats.active_connections,
            new_connections=stats.new_connections,
            closed_connections=stats.closed_connections,
            total_bandwidth=stats.total_bytes,
            upload_bandwidth=total_upload,
            download_bandwidth=total_download
        )
        
        # Calcular desviaciones del baseline si existe
        if self.baseline:
            report.pps_deviation = self._calculate_deviation(
                report.current_pps,
                self.baseline.avg_pps,
                self.baseline.std_pps
            )
            
            report.bps_deviation = self._calculate_deviation(
                report.current_bps,
                self.baseline.avg_bps,
                self.baseline.std_bps
            )
            
            # Protocolos inusuales (no en baseline)
            report.unusual_protocols = [
                proto for proto in protocol_breakdown.keys()
                if proto not in self.baseline.protocol_distribution
            ]
        
        return report
    
    def _calculate_deviation(self, current: float, avg: float, std: float) -> float:
        """
        Calcula desviación en sigmas
        
        Returns:
            Número de desviaciones estándar del promedio
        """
        if std == 0:
            return 0.0
        
        return (current - avg) / std
    
    def detect_traffic_anomalies(self, report: TrafficReport) -> List[Dict]:
        """
        Detecta anomalías en el tráfico
        
        Args:
            report: TrafficReport a analizar
            
        Returns:
            Lista de anomalías detectadas
        """
        anomalies = []
        
        if not self.baseline:
            return anomalies
        
        # Anomalía: PPS muy alto (> 3 sigmas)
        if report.pps_deviation and report.pps_deviation > 3:
            anomalies.append({
                "type": "HIGH_PACKET_RATE",
                "severity": "HIGH",
                "description": f"Tasa de paquetes anormal: {report.current_pps:.1f} pps ({report.pps_deviation:.1f} sigmas)",
                "current": report.current_pps,
                "baseline": self.baseline.avg_pps,
                "deviation": report.pps_deviation
            })
        
        # Anomalía: BPS muy alto (> 3 sigmas)
        if report.bps_deviation and report.bps_deviation > 3:
            anomalies.append({
                "type": "HIGH_BANDWIDTH",
                "severity": "HIGH",
                "description": f"Ancho de banda anormal: {report.current_bps:,.0f} bps ({report.bps_deviation:.1f} sigmas)",
                "current": report.current_bps,
                "baseline": self.baseline.avg_bps,
                "deviation": report.bps_deviation
            })
        
        # Anomalía: Protocolos inusuales
        if report.unusual_protocols:
            anomalies.append({
                "type": "UNUSUAL_PROTOCOLS",
                "severity": "MEDIUM",
                "description": f"Protocolos no vistos en baseline: {', '.join(report.unusual_protocols)}",
                "protocols": report.unusual_protocols
            })
        
        # Anomalía: Puertos inusuales muy activos
        if report.unusual_ports:
            anomalies.append({
                "type": "UNUSUAL_PORTS",
                "severity": "MEDIUM",
                "description": f"Puertos no comunes activos: {', '.join(map(str, report.unusual_ports[:5]))}",
                "ports": report.unusual_ports
            })
        
        # Anomalía: Una IP dominando el tráfico (> 50%)
        if report.top_senders:
            top_sender_bytes = report.top_senders[0][1]
            if top_sender_bytes > report.total_bandwidth * 0.5:
                anomalies.append({
                    "type": "TRAFFIC_CONCENTRATION",
                    "severity": "HIGH",
                    "description": f"IP {report.top_senders[0][0]} genera {(top_sender_bytes/report.total_bandwidth)*100:.1f}% del tráfico",
                    "ip": report.top_senders[0][0],
                    "percentage": (top_sender_bytes/report.total_bandwidth)*100
                })
        
        # Anomalía: Muchas conexiones nuevas (posible scanning)
        if self.baseline and report.new_connections > self.baseline.avg_cpm * 5:
            anomalies.append({
                "type": "HIGH_CONNECTION_RATE",
                "severity": "HIGH",
                "description": f"Tasa de nuevas conexiones muy alta: {report.new_connections}",
                "current": report.new_connections,
                "baseline": self.baseline.avg_cpm
            })
        
        return anomalies
    
    def generate_summary_report(self) -> Dict:
        """Genera un reporte resumen completo"""
        report = self.analyze_current_traffic()
        anomalies = self.detect_traffic_anomalies(report)
        
        return {
            "timestamp": report.timestamp.isoformat(),
            "metrics": {
                "packets_per_second": report.current_pps,
                "bytes_per_second": report.current_bps,
                "active_connections": report.current_connections,
                "new_connections": report.new_connections
            },
            "top_talkers": {
                "senders": report.top_senders[:5],
                "receivers": report.top_receivers[:5]
            },
            "protocols": report.protocol_breakdown,
            "ports": {
                "top_used": report.top_ports[:5],
                "unusual": report.unusual_ports[:5]
            },
            "bandwidth": {
                "total": report.total_bandwidth,
                "upload": report.upload_bandwidth,
                "download": report.download_bandwidth
            },
            "baseline": {
                "available": self.baseline is not None,
                "pps_deviation": report.pps_deviation,
                "bps_deviation": report.bps_deviation
            } if self.baseline else None,
            "anomalies": anomalies
        }