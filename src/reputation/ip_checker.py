#!/usr/bin/env python3
"""
Némesis IA - IP Reputation Checker
Capítulo 7: Sistema de Reputación de IPs

Consulta múltiples fuentes para determinar reputación de IPs
"""

import logging
import time
import json
from typing import Dict, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import socket

logger = logging.getLogger(__name__)


@dataclass
class IPReputation:
    """Reputación de una IP"""
    ip: str
    reputation_score: int  # 0-100 (0=malicious, 100=trusted)
    is_blacklisted: bool
    is_whitelisted: bool
    
    # Geolocation
    country: Optional[str] = None
    city: Optional[str] = None
    isp: Optional[str] = None
    asn: Optional[str] = None
    
    # Threat info
    threat_level: str = "UNKNOWN"  # LOW, MEDIUM, HIGH, CRITICAL
    abuse_reports: int = 0
    last_seen_malicious: Optional[datetime] = None
    
    # Categories
    categories: List[str] = None
    
    # Metadata
    checked_at: datetime = None
    data_source: str = "LOCAL"
    
    def __post_init__(self):
        if self.categories is None:
            self.categories = []
        if self.checked_at is None:
            self.checked_at = datetime.now()


class IPReputationChecker:
    """Verificador de reputación de IPs"""
    
    def __init__(self, cache_ttl: int = 3600):
        """
        Inicializa el checker
        
        Args:
            cache_ttl: Tiempo de vida del cache en segundos
        """
        self.cache_ttl = cache_ttl
        self.cache: Dict[str, IPReputation] = {}
        
        # Rate limiting
        self.last_api_call = 0
        self.min_api_interval = 2  # Segundos entre llamadas API
        
        # Listas locales
        self.local_whitelist: set = set()
        self.local_blacklist: set = set()
        
        # Known malicious patterns
        self.malicious_patterns = {
            "tor_exit_nodes": [],
            "known_botnets": [],
            "vpn_providers": []
        }
        
        logger.info("🔍 IPReputationChecker inicializado")
    
    def check_ip(self, ip: str, force_refresh: bool = False) -> IPReputation:
        """
        Verifica la reputación de una IP
        
        Args:
            ip: Dirección IP a verificar
            force_refresh: Forzar actualización ignorando cache
            
        Returns:
            IPReputation con información completa
        """
        
        # Validar IP
        if not self._is_valid_ip(ip):
            logger.warning(f"IP inválida: {ip}")
            return self._create_invalid_reputation(ip)
        
        # Verificar cache
        if not force_refresh and ip in self.cache:
            cached = self.cache[ip]
            age = (datetime.now() - cached.checked_at).total_seconds()
            
            if age < self.cache_ttl:
                logger.debug(f"Cache hit para {ip}")
                return cached
        
        # Verificar listas locales primero
        if ip in self.local_whitelist:
            return self._create_whitelisted_reputation(ip)
        
        if ip in self.local_blacklist:
            return self._create_blacklisted_reputation(ip)
        
        # Verificar si es IP privada/local
        if self._is_private_ip(ip):
            return self._create_private_reputation(ip)
        
        # Construir reputación completa
        reputation = self._build_reputation(ip)
        
        # Guardar en cache
        self.cache[ip] = reputation
        
        return reputation
    
    def _build_reputation(self, ip: str) -> IPReputation:
        """Construye reputación completa de una IP"""
        
        # Inicializar con datos básicos
        reputation = IPReputation(
            ip=ip,
            reputation_score=50,  # Neutral por defecto
            is_blacklisted=False,
            is_whitelisted=False,
            threat_level="UNKNOWN"
        )
        
        # Geolocation (simulado - en producción usar API real)
        geo_info = self._get_geolocation(ip)
        reputation.country = geo_info.get('country')
        reputation.city = geo_info.get('city')
        reputation.isp = geo_info.get('isp')
        reputation.asn = geo_info.get('asn')
        
        # Calcular score basado en heurísticas
        score = self._calculate_reputation_score(ip, geo_info)
        reputation.reputation_score = score
        
        # Determinar threat level
        reputation.threat_level = self._determine_threat_level(score)
        
        # Categorías
        reputation.categories = self._categorize_ip(ip, geo_info)
        
        logger.info(f"Reputación calculada para {ip}: {score}/100 ({reputation.threat_level})")
        
        return reputation
    
    def _get_geolocation(self, ip: str) -> Dict:
        """
        Obtiene información de geolocalización
        
        En producción, esto usaría APIs como:
        - ipapi.co
        - ip-api.com
        - MaxMind GeoIP2
        
        Por ahora, simulamos con datos básicos
        """
        
        # Simulación básica basada en rangos de IP
        first_octet = int(ip.split('.')[0])
        
        # Simulación de países por rangos
        country_map = {
            range(1, 50): "United States",
            range(50, 100): "China",
            range(100, 150): "Russia",
            range(150, 200): "Germany",
            range(200, 256): "Brazil"
        }
        
        country = "Unknown"
        for ip_range, country_name in country_map.items():
            if first_octet in ip_range:
                country = country_name
                break
        
        # ISP simulado
        isp_map = {
            "United States": "Amazon AWS",
            "China": "China Telecom",
            "Russia": "Rostelecom",
            "Germany": "Deutsche Telekom",
            "Brazil": "Telefonica Brazil"
        }
        
        return {
            "country": country,
            "city": "Unknown",
            "isp": isp_map.get(country, "Unknown ISP"),
            "asn": f"AS{first_octet * 100}"
        }
    
    def _calculate_reputation_score(self, ip: str, geo_info: Dict) -> int:
        """
        Calcula score de reputación (0-100)
        
        Factores:
        - País de origen
        - ISP
        - Rangos conocidos maliciosos
        - Patrones en la IP
        """
        
        score = 50  # Neutral
        
        # País de alto riesgo (simulación)
        high_risk_countries = ["Russia", "China", "North Korea"]
        if geo_info.get('country') in high_risk_countries:
            score -= 20
        
        # ISP conocido (positivo)
        trusted_isps = ["Amazon AWS", "Google Cloud", "Microsoft Azure"]
        if any(isp in geo_info.get('isp', '') for isp in trusted_isps):
            score += 15
        
        # Patrón de IP sospechoso
        octets = list(map(int, ip.split('.')))
        
        # IPs con patrones secuenciales (posible scanning)
        if octets[2] == octets[3]:
            score -= 10
        
        # Rangos de hosting conocidos (neutral a positivo)
        if octets[0] in [3, 4, 13, 23, 34, 35, 52, 54]:  # AWS ranges
            score += 10
        
        # Limitar entre 0-100
        return max(0, min(100, score))
    
    def _determine_threat_level(self, score: int) -> str:
        """Determina nivel de amenaza basado en score"""
        
        if score >= 80:
            return "LOW"
        elif score >= 60:
            return "MEDIUM"
        elif score >= 40:
            return "HIGH"
        else:
            return "CRITICAL"
    
    def _categorize_ip(self, ip: str, geo_info: Dict) -> List[str]:
        """Categoriza la IP"""
        
        categories = []
        
        isp = geo_info.get('isp', '').lower()
        
        if 'amazon' in isp or 'aws' in isp:
            categories.append("CLOUD_PROVIDER")
        
        if 'google' in isp:
            categories.append("CLOUD_PROVIDER")
        
        if 'telecom' in isp or 'isp' in isp:
            categories.append("RESIDENTIAL")
        
        if 'hosting' in isp or 'server' in isp:
            categories.append("HOSTING")
        
        # Verificar si es conocida por VPN
        if self._is_vpn_ip(ip):
            categories.append("VPN")
        
        return categories
    
    def _is_vpn_ip(self, ip: str) -> bool:
        """Verifica si es IP de VPN conocida"""
        # En producción, consultar base de datos de VPN providers
        # Por ahora, heurística simple
        return False
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Valida formato de IP"""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False
    
    def _is_private_ip(self, ip: str) -> bool:
        """Verifica si es IP privada/local"""
        octets = ip.split('.')
        
        if len(octets) != 4:
            return False
        
        try:
            first = int(octets[0])
            second = int(octets[1])
            
            # 10.0.0.0/8
            if first == 10:
                return True
            
            # 172.16.0.0/12
            if first == 172 and 16 <= second <= 31:
                return True
            
            # 192.168.0.0/16
            if first == 192 and second == 168:
                return True
            
            # 127.0.0.0/8 (localhost)
            if first == 127:
                return True
            
            return False
        
        except ValueError:
            return False
    
    def _create_whitelisted_reputation(self, ip: str) -> IPReputation:
        """Crea reputación para IP en whitelist"""
        return IPReputation(
            ip=ip,
            reputation_score=100,
            is_blacklisted=False,
            is_whitelisted=True,
            threat_level="LOW",
            categories=["WHITELISTED"],
            data_source="LOCAL_WHITELIST"
        )
    
    def _create_blacklisted_reputation(self, ip: str) -> IPReputation:
        """Crea reputación para IP en blacklist"""
        return IPReputation(
            ip=ip,
            reputation_score=0,
            is_blacklisted=True,
            is_whitelisted=False,
            threat_level="CRITICAL",
            categories=["BLACKLISTED"],
            data_source="LOCAL_BLACKLIST"
        )
    
    def _create_private_reputation(self, ip: str) -> IPReputation:
        """Crea reputación para IP privada"""
        return IPReputation(
            ip=ip,
            reputation_score=100,
            is_blacklisted=False,
            is_whitelisted=False,
            threat_level="LOW",
            country="Local",
            categories=["PRIVATE"],
            data_source="LOCAL"
        )
    
    def _create_invalid_reputation(self, ip: str) -> IPReputation:
        """Crea reputación para IP inválida"""
        return IPReputation(
            ip=ip,
            reputation_score=0,
            is_blacklisted=False,
            is_whitelisted=False,
            threat_level="UNKNOWN",
            categories=["INVALID"],
            data_source="ERROR"
        )
    
    def add_to_whitelist(self, ip: str):
        """Añade IP a whitelist local"""
        self.local_whitelist.add(ip)
        
        # Invalidar cache
        if ip in self.cache:
            del self.cache[ip]
        
        logger.info(f"✅ IP añadida a whitelist: {ip}")
    
    def add_to_blacklist(self, ip: str):
        """Añade IP a blacklist local"""
        self.local_blacklist.add(ip)
        
        # Invalidar cache
        if ip in self.cache:
            del self.cache[ip]
        
        logger.info(f"🚫 IP añadida a blacklist: {ip}")
    
    def remove_from_whitelist(self, ip: str):
        """Remueve IP de whitelist"""
        self.local_whitelist.discard(ip)
        if ip in self.cache:
            del self.cache[ip]
        logger.info(f"Removida de whitelist: {ip}")
    
    def remove_from_blacklist(self, ip: str):
        """Remueve IP de blacklist"""
        self.local_blacklist.discard(ip)
        if ip in self.cache:
            del self.cache[ip]
        logger.info(f"Removida de blacklist: {ip}")
    
    def get_cache_stats(self) -> Dict:
        """Retorna estadísticas del cache"""
        return {
            "cached_ips": len(self.cache),
            "whitelist_size": len(self.local_whitelist),
            "blacklist_size": len(self.local_blacklist),
            "cache_ttl": self.cache_ttl
        }
    
    def clear_cache(self):
        """Limpia el cache"""
        cleared = len(self.cache)
        self.cache.clear()
        logger.info(f"Cache limpiado: {cleared} entradas removidas")