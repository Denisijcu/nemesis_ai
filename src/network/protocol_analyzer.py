#!/usr/bin/env python3
"""
Némesis IA - Protocol Analyzer
Capítulo 4: Análisis de Protocolos

Análisis profundo de protocolos HTTP, DNS, TCP
"""

import logging
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import defaultdict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class HTTPRequest:
    """Información de request HTTP"""
    method: str
    uri: str
    host: Optional[str]
    user_agent: Optional[str]
    headers: Dict[str, str]
    suspicious_patterns: List[str]


@dataclass
class DNSQuery:
    """Información de query DNS"""
    domain: str
    query_type: str
    is_suspicious: bool
    suspicious_reasons: List[str]


@dataclass
class PortScanEvent:
    """Evento de port scanning detectado"""
    scanner_ip: str
    target_ip: str
    ports_scanned: List[int]
    scan_duration: float
    scan_type: str  # SYN, CONNECT, XMAS, etc


class ProtocolAnalyzer:
    """Analizador profundo de protocolos"""
    
    def __init__(self):
        """Inicializa el analizador"""
        self.http_patterns = self._compile_http_patterns()
        self.dns_suspicious = self._compile_dns_patterns()
        
        # Tracking de conexiones para port scan detection
        self.connection_tracker = defaultdict(lambda: {
            'ports': set(),
            'first_seen': None,
            'last_seen': None,
            'syn_packets': 0,
            'flags': []
        })
        
        logger.info("🔍 ProtocolAnalyzer inicializado")
    
    def _compile_http_patterns(self) -> Dict[str, re.Pattern]:
        """Compila patrones de ataques HTTP"""
        return {
            'sql_injection': re.compile(
                r"('|\"|;|--|\/\*|\*\/|xp_|sp_|union|select|insert|drop|delete|update|exec)",
                re.IGNORECASE
            ),
            'xss': re.compile(
                r"(<script|<iframe|javascript:|onerror=|onload=|eval\(|alert\()",
                re.IGNORECASE
            ),
            'path_traversal': re.compile(
                r"(\.\./|\.\.\\|%2e%2e|%252e)",
                re.IGNORECASE
            ),
            'command_injection': re.compile(
                r"(;|\||&&|`|\$\(|<\(|>\()",
                re.IGNORECASE
            ),
            'lfi': re.compile(
                r"(file://|php://|data://|/etc/passwd|/etc/shadow)",
                re.IGNORECASE
            )
        }
    
    def _compile_dns_patterns(self) -> List[str]:
        """Patrones de dominios sospechosos"""
        return [
            # DGA (Domain Generation Algorithm) patterns
            r'^[a-z0-9]{20,}\.com$',  # Dominios aleatorios largos
            r'^\d+\.\d+\.\d+\.\d+\.in-addr\.arpa$',  # Reverse DNS lookup
            # C2 patterns
            r'.*\.(tk|ml|ga|cf|gq)$',  # TLDs gratuitos comunes en malware
            # Fast flux
            r'.*\d{5,}.*',  # Muchos números en el dominio
        ]
    
    def analyze_http(self, http_method: str, uri: str, payload: str) -> HTTPRequest:
        """
        Analiza un request HTTP
        
        Args:
            http_method: GET, POST, etc
            uri: URI solicitada
            payload: Payload completo del request
            
        Returns:
            HTTPRequest con análisis
        """
        suspicious_patterns = []
        headers = {}
        host = None
        user_agent = None
        
        # Parsear headers
        lines = payload.split('\r\n')
        for line in lines[1:]:  # Skip primera línea (request line)
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip().lower()] = value.strip()
        
        host = headers.get('host')
        user_agent = headers.get('user-agent')
        
        # Detectar patrones sospechosos en URI
        for pattern_name, pattern in self.http_patterns.items():
            if pattern.search(uri):
                suspicious_patterns.append(pattern_name)
        
        # Detectar payloads anormalmente largos
        if len(uri) > 500:
            suspicious_patterns.append('long_uri')
        
        # Detectar encoding sospechoso
        if uri.count('%') > 10:
            suspicious_patterns.append('heavy_encoding')
        
        return HTTPRequest(
            method=http_method,
            uri=uri,
            host=host,
            user_agent=user_agent,
            headers=headers,
            suspicious_patterns=suspicious_patterns
        )
    
    def analyze_dns(self, domain: str) -> DNSQuery:
        """
        Analiza una query DNS
        
        Args:
            domain: Dominio consultado
            
        Returns:
            DNSQuery con análisis
        """
        suspicious_reasons = []
        
        # Remover punto final si existe
        domain = domain.rstrip('.')
        
        # Longitud anormal
        if len(domain) > 50:
            suspicious_reasons.append('domain_too_long')
        
        # Muchos subdominios
        if domain.count('.') > 5:
            suspicious_reasons.append('too_many_subdomains')
        
        # Entropía alta (DGA)
        entropy = self._calculate_entropy(domain)
        if entropy > 4.5:
            suspicious_reasons.append('high_entropy_dga')
        
        # Patrones sospechosos
        for pattern in self.dns_suspicious:
            if re.match(pattern, domain):
                suspicious_reasons.append('suspicious_pattern')
                break
        
        # IPs como dominio
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain):
            suspicious_reasons.append('ip_as_domain')
        
        return DNSQuery(
            domain=domain,
            query_type='A',  # Simplificado
            is_suspicious=len(suspicious_reasons) > 0,
            suspicious_reasons=suspicious_reasons
        )
    
    def track_connection(
        self, 
        src_ip: str, 
        dst_ip: str, 
        dst_port: int,
        flags: str
    ) -> Optional[PortScanEvent]:
        """
        Trackea conexiones para detectar port scanning
        
        Args:
            src_ip: IP origen
            dst_ip: IP destino
            dst_port: Puerto destino
            flags: TCP flags
            
        Returns:
            PortScanEvent si se detecta scanning, None en caso contrario
        """
        key = f"{src_ip}->{dst_ip}"
        tracker = self.connection_tracker[key]
        
        now = datetime.now()
        
        # Primera vez que vemos esta conexión
        if tracker['first_seen'] is None:
            tracker['first_seen'] = now
        
        tracker['last_seen'] = now
        tracker['ports'].add(dst_port)
        tracker['flags'].append(flags)
        
        # Contar SYN packets
        if 'S' in flags and 'A' not in flags:
            tracker['syn_packets'] += 1
        
        # Detectar port scan
        # Criterios: Múltiples puertos en corto tiempo
        time_window = (tracker['last_seen'] - tracker['first_seen']).total_seconds()
        
        if len(tracker['ports']) >= 10 and time_window < 60:
            # Port scan detectado!
            scan_type = self._identify_scan_type(tracker['flags'])
            
            event = PortScanEvent(
                scanner_ip=src_ip,
                target_ip=dst_ip,
                ports_scanned=list(tracker['ports']),
                scan_duration=time_window,
                scan_type=scan_type
            )
            
            # Reset tracker
            del self.connection_tracker[key]
            
            return event
        
        return None
    
    def _identify_scan_type(self, flags_list: List[str]) -> str:
        """Identifica el tipo de port scan"""
        
        # SYN scan (stealth)
        if all('S' in f and 'A' not in f for f in flags_list):
            return "SYN_SCAN"
        
        # Connect scan
        if any('S' in f and 'A' in f for f in flags_list):
            return "CONNECT_SCAN"
        
        # FIN scan
        if any('F' in f for f in flags_list):
            return "FIN_SCAN"
        
        # XMAS scan
        if any('FPU' in f for f in flags_list):
            return "XMAS_SCAN"
        
        # NULL scan
        if any(f == '' for f in flags_list):
            return "NULL_SCAN"
        
        return "UNKNOWN_SCAN"
    
    def _calculate_entropy(self, string: str) -> float:
        """Calcula la entropía de Shannon de una cadena"""
        import math
        from collections import Counter
        
        if not string:
            return 0.0
        
        # Contar frecuencias
        counter = Counter(string)
        length = len(string)
        
        # Calcular entropía
        entropy = 0.0
        for count in counter.values():
            probability = count / length
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def cleanup_old_connections(self, max_age_seconds: int = 300):
        """Limpia conexiones antiguas del tracker"""
        now = datetime.now()
        keys_to_delete = []
        
        for key, tracker in self.connection_tracker.items():
            if tracker['last_seen']:
                age = (now - tracker['last_seen']).total_seconds()
                if age > max_age_seconds:
                    keys_to_delete.append(key)
        
        for key in keys_to_delete:
            del self.connection_tracker[key]
        
        if keys_to_delete:
            logger.debug(f"🧹 Limpiadas {len(keys_to_delete)} conexiones antiguas")