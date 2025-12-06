#!/usr/bin/env python3
"""
Némesis IA - Anomaly Detector
Capítulo 6: Análisis de Tráfico de Red

Detecta anomalías específicas: DDoS, Port Scanning, Data Exfiltration
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)


@dataclass
class Anomaly:
    """Representa una anomalía detectada"""
    timestamp: datetime
    anomaly_type: str
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL
    source_ip: str
    description: str
    details: Dict
    confidence: float  # 0.0 - 1.0


class AnomalyDetector:
    """Detector de anomalías de red"""
    
    def __init__(self):
        """Inicializa el detector"""
        
        # Tracking de IPs para detección
        self.ip_tracking: Dict[str, Dict] = defaultdict(lambda: {
            "first_seen": None,
            "last_seen": None,
            "total_packets": 0,
            "total_bytes": 0,
            "ports_contacted": set(),
            "dst_ips_contacted": set(),
            "connections_per_minute": [],
            "upload_rate": 0,
            "download_rate": 0
        })
        
        # Histórico de anomalías detectadas
        self.detected_anomalies: List[Anomaly] = []
        
        # Thresholds para detección
        self.thresholds = {
            "ddos_pps": 1000,              # Packets per second para DDoS
            "ddos_connections": 100,        # Connections per minute para DDoS
            "port_scan_ports": 10,          # Puertos diferentes en corto tiempo
            "port_scan_time": 60,           # Segundos para port scan
            "data_exfil_rate": 10_000_000,  # 10MB/s upload inusual
            "suspicious_port_usage": 5       # Uso repetido de puerto no común
        }
        
        logger.info("🔍 AnomalyDetector inicializado")
    
    def update_tracking(self, packet_info: Dict):
        """
        Actualiza el tracking de IPs con información de paquete
        
        Args:
            packet_info: Información del paquete
        """
        src_ip = packet_info.get('src_ip')
        dst_ip = packet_info.get('dst_ip')
        dst_port = packet_info.get('dst_port')
        size = packet_info.get('size', 0)
        timestamp = packet_info.get('timestamp', datetime.now())
        
        if not src_ip:
            return
        
        tracking = self.ip_tracking[src_ip]
        
        # Primera vez que vemos esta IP
        if tracking['first_seen'] is None:
            tracking['first_seen'] = timestamp
        
        tracking['last_seen'] = timestamp
        tracking['total_packets'] += 1
        tracking['total_bytes'] += size
        
        # Tracking de puertos contactados
        if dst_port:
            tracking['ports_contacted'].add(dst_port)
        
        # Tracking de IPs destino contactadas
        if dst_ip:
            tracking['dst_ips_contacted'].add(dst_ip)
    
    def detect_ddos(self, stats: Dict, source_ip: str = None) -> Optional[Anomaly]:
        """
        Detecta ataques DDoS
        
        Args:
            stats: Estadísticas de tráfico actuales
            source_ip: IP específica a analizar (opcional)
            
        Returns:
            Anomaly si se detecta DDoS, None si no
        """
        
        # DDoS por volumen de paquetes
        pps = stats.get('packets_per_second', 0)
        
        if pps > self.thresholds['ddos_pps']:
            # Identificar IP principal si no se especificó
            if not source_ip:
                top_senders = stats.get('top_senders', [])
                if top_senders:
                    source_ip = top_senders[0][0]
            
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="DDOS_ATTACK",
                severity="CRITICAL",
                source_ip=source_ip or "MULTIPLE",
                description=f"Posible ataque DDoS detectado: {pps:.0f} pps",
                details={
                    "packets_per_second": pps,
                    "threshold": self.thresholds['ddos_pps'],
                    "attack_vector": "HIGH_PACKET_RATE"
                },
                confidence=0.95
            )
        
        # DDoS por tasa de conexiones
        new_connections = stats.get('new_connections', 0)
        
        if new_connections > self.thresholds['ddos_connections']:
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="DDOS_ATTACK",
                severity="CRITICAL",
                source_ip=source_ip or "MULTIPLE",
                description=f"Posible ataque DDoS por conexiones: {new_connections} conexiones/min",
                details={
                    "connections_per_minute": new_connections,
                    "threshold": self.thresholds['ddos_connections'],
                    "attack_vector": "HIGH_CONNECTION_RATE"
                },
                confidence=0.90
            )
        
        return None
    
    def detect_port_scan(self, source_ip: str) -> Optional[Anomaly]:
        """
        Detecta port scanning
        
        Args:
            source_ip: IP a analizar
            
        Returns:
            Anomaly si se detecta port scan, None si no
        """
        
        tracking = self.ip_tracking.get(source_ip)
        if not tracking or tracking['first_seen'] is None:
            return None
        
        # Calcular tiempo transcurrido
        time_span = (tracking['last_seen'] - tracking['first_seen']).total_seconds()
        
        # Número de puertos diferentes contactados
        ports_count = len(tracking['ports_contacted'])
        
        # Port scan: muchos puertos en poco tiempo
        if ports_count >= self.thresholds['port_scan_ports'] and time_span <= self.thresholds['port_scan_time']:
            
            # Determinar tipo de scan
            scan_type = "HORIZONTAL" if len(tracking['dst_ips_contacted']) > 5 else "VERTICAL"
            
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="PORT_SCAN",
                severity="HIGH",
                source_ip=source_ip,
                description=f"Port scanning detectado: {ports_count} puertos en {time_span:.0f}s",
                details={
                    "ports_scanned": ports_count,
                    "time_span": time_span,
                    "scan_type": scan_type,
                    "dst_ips": len(tracking['dst_ips_contacted']),
                    "ports": list(tracking['ports_contacted'])[:20]
                },
                confidence=0.92
            )
        
        return None
    
    def detect_data_exfiltration(self, source_ip: str, upload_rate: float) -> Optional[Anomaly]:
        """
        Detecta posible exfiltración de datos
        
        Args:
            source_ip: IP a analizar
            upload_rate: Tasa de upload en bytes/segundo
            
        Returns:
            Anomaly si se detecta exfiltración, None si no
        """
        
        # Upload rate anormalmente alto
        if upload_rate > self.thresholds['data_exfil_rate']:
            
            tracking = self.ip_tracking.get(source_ip, {})
            
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="DATA_EXFILTRATION",
                severity="CRITICAL",
                source_ip=source_ip,
                description=f"Posible exfiltración de datos: {upload_rate/1_000_000:.2f} MB/s",
                details={
                    "upload_rate_bps": upload_rate,
                    "upload_rate_mbps": upload_rate / 1_000_000,
                    "threshold_mbps": self.thresholds['data_exfil_rate'] / 1_000_000,
                    "total_bytes": tracking.get('total_bytes', 0)
                },
                confidence=0.85
            )
        
        return None
    
    def detect_suspicious_ports(self, port_usage: Dict[int, int]) -> List[Anomaly]:
        """
        Detecta uso de puertos sospechosos
        
        Args:
            port_usage: Diccionario {port: count}
            
        Returns:
            Lista de anomalías detectadas
        """
        
        anomalies = []
        
        # Lista de puertos sospechosos conocidos
        suspicious_ports = {
            31337: "Back Orifice",
            12345: "NetBus",
            27374: "SubSeven",
            6667: "IRC (posible botnet)",
            6697: "IRC SSL",
            1337: "Elite/Leet",
            3389: "RDP (expuesto)",
            5900: "VNC (expuesto)",
            4444: "Metasploit default",
            8888: "Proxy/backdoor común"
        }
        
        for port, count in port_usage.items():
            if port in suspicious_ports and count >= self.thresholds['suspicious_port_usage']:
                anomalies.append(Anomaly(
                    timestamp=datetime.now(),
                    anomaly_type="SUSPICIOUS_PORT",
                    severity="MEDIUM",
                    source_ip="MULTIPLE",
                    description=f"Uso de puerto sospechoso {port} ({suspicious_ports[port]}): {count} veces",
                    details={
                        "port": port,
                        "count": count,
                        "port_description": suspicious_ports[port]
                    },
                    confidence=0.75
                ))
        
        return anomalies
    
    def detect_unusual_protocol(self, protocol: str, percentage: float, baseline_protocols: Dict) -> Optional[Anomaly]:
        """
        Detecta protocolos inusuales comparado con baseline
        
        Args:
            protocol: Protocolo a analizar
            percentage: Porcentaje actual del protocolo
            baseline_protocols: Distribución de protocolos del baseline
            
        Returns:
            Anomaly si el protocolo es inusual, None si no
        """
        
        # Protocolo no visto en baseline
        if protocol not in baseline_protocols:
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="UNUSUAL_PROTOCOL",
                severity="MEDIUM",
                source_ip="MULTIPLE",
                description=f"Protocolo inusual detectado: {protocol} ({percentage:.1f}%)",
                details={
                    "protocol": protocol,
                    "current_percentage": percentage,
                    "in_baseline": False
                },
                confidence=0.70
            )
        
        # Protocolo con porcentaje muy diferente al baseline
        baseline_pct = baseline_protocols[protocol]
        if abs(percentage - baseline_pct) > 30:  # 30% de diferencia
            return Anomaly(
                timestamp=datetime.now(),
                anomaly_type="PROTOCOL_DEVIATION",
                severity="LOW",
                source_ip="MULTIPLE",
                description=f"Desviación en protocolo {protocol}: {percentage:.1f}% vs baseline {baseline_pct:.1f}%",
                details={
                    "protocol": protocol,
                    "current_percentage": percentage,
                    "baseline_percentage": baseline_pct,
                    "deviation": abs(percentage - baseline_pct)
                },
                confidence=0.65
            )
        
        return None
    
    def detect_off_hours_activity(self, current_time: datetime, activity_level: float, baseline_avg: float) -> Optional[Anomaly]:
        """
        Detecta actividad sospechosa fuera de horario
        
        Args:
            current_time: Hora actual
            activity_level: Nivel de actividad actual
            baseline_avg: Promedio de actividad normal
            
        Returns:
            Anomaly si hay actividad sospechosa, None si no
        """
        
        hour = current_time.hour
        
        # Horario nocturno (00:00 - 06:00)
        if 0 <= hour < 6:
            # Actividad alta en horario nocturno
            if activity_level > baseline_avg * 0.5:  # 50% del promedio es mucho de noche
                return Anomaly(
                    timestamp=current_time,
                    anomaly_type="OFF_HOURS_ACTIVITY",
                    severity="MEDIUM",
                    source_ip="MULTIPLE",
                    description=f"Actividad inusual a las {hour:02d}:00",
                    details={
                        "hour": hour,
                        "activity_level": activity_level,
                        "baseline_avg": baseline_avg,
                        "percentage_of_baseline": (activity_level / baseline_avg) * 100
                    },
                    confidence=0.80
                )
        
        return None
    
    def analyze_traffic(self, traffic_data: Dict, baseline: Optional[Dict] = None) -> List[Anomaly]:
        """
        Analiza tráfico completo y detecta todas las anomalías
        
        Args:
            traffic_data: Datos de tráfico a analizar
            baseline: Baseline opcional para comparación
            
        Returns:
            Lista de todas las anomalías detectadas
        """
        
        anomalies = []
        
        # DDoS detection
        ddos = self.detect_ddos(traffic_data)
        if ddos:
            anomalies.append(ddos)
            self.detected_anomalies.append(ddos)
        
        # Port scan detection para cada IP
        for ip in self.ip_tracking.keys():
            port_scan = self.detect_port_scan(ip)
            if port_scan:
                anomalies.append(port_scan)
                self.detected_anomalies.append(port_scan)
        
        # Data exfiltration detection
        top_senders = traffic_data.get('top_senders', [])
        for ip, bytes_sent in top_senders[:5]:
            # Calcular upload rate aproximado
            tracking = self.ip_tracking.get(ip, {})
            if tracking.get('first_seen'):
                time_span = (tracking['last_seen'] - tracking['first_seen']).total_seconds()
                if time_span > 0:
                    upload_rate = bytes_sent / time_span
                    
                    exfil = self.detect_data_exfiltration(ip, upload_rate)
                    if exfil:
                        anomalies.append(exfil)
                        self.detected_anomalies.append(exfil)
        
        # Suspicious ports
        port_usage = traffic_data.get('port_usage', {})
        suspicious = self.detect_suspicious_ports(port_usage)
        anomalies.extend(suspicious)
        self.detected_anomalies.extend(suspicious)
        
        # Unusual protocols (si hay baseline)
        if baseline and 'protocol_distribution' in baseline:
            protocols = traffic_data.get('protocols', {})
            for protocol, percentage in protocols.items():
                unusual = self.detect_unusual_protocol(
                    protocol,
                    percentage,
                    baseline['protocol_distribution']
                )
                if unusual:
                    anomalies.append(unusual)
                    self.detected_anomalies.append(unusual)
        
        # Off-hours activity
        if baseline and 'avg_bps' in baseline:
            current_bps = traffic_data.get('bytes_per_second', 0)
            off_hours = self.detect_off_hours_activity(
                datetime.now(),
                current_bps,
                baseline['avg_bps']
            )
            if off_hours:
                anomalies.append(off_hours)
                self.detected_anomalies.append(off_hours)
        
        return anomalies
    
    def get_anomaly_summary(self) -> Dict:
        """Retorna resumen de anomalías detectadas"""
        
        # Contar por tipo
        type_counts = Counter(a.anomaly_type for a in self.detected_anomalies)
        
        # Contar por severidad
        severity_counts = Counter(a.severity for a in self.detected_anomalies)
        
        # Top IPs con más anomalías
        ip_counts = Counter(a.source_ip for a in self.detected_anomalies if a.source_ip != "MULTIPLE")
        
        return {
            "total_anomalies": len(self.detected_anomalies),
            "by_type": dict(type_counts),
            "by_severity": dict(severity_counts),
            "top_malicious_ips": ip_counts.most_common(10),
            "recent_anomalies": [
                {
                    "timestamp": a.timestamp.isoformat(),
                    "type": a.anomaly_type,
                    "severity": a.severity,
                    "source_ip": a.source_ip,
                    "description": a.description,
                    "confidence": a.confidence
                }
                for a in self.detected_anomalies[-10:]
            ]
        }