#!/usr/bin/env python3
"""
Némesis IA - WHOIS Client
Capítulo 11: APIs de la Ley

Cliente para consultas WHOIS e información de ISP
"""

import logging
import socket
import ipaddress
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class WHOISClient:
    """Cliente para consultas WHOIS"""
    
    def __init__(self):
        """Inicializa cliente WHOIS"""
        
        self.stats = {
            "lookups": 0,
            "successful": 0,
            "failed": 0
        }
        
        logger.info("🌍 WHOIS Client inicializado")
    
    def lookup_ip(self, ip: str) -> Dict:
        """
        Realiza lookup de información de IP
        
        Args:
            ip: Dirección IP
            
        Returns:
            Información de la IP
        """
        
        logger.info(f"🔍 WHOIS lookup: {ip}")
        
        self.stats["lookups"] += 1
        
        try:
            # Información básica
            hostname = self._get_hostname(ip)
            is_private = self._is_private_ip(ip)
            
            # Simular información WHOIS (en producción usar python-whois)
            info = {
                'ip': ip,
                'hostname': hostname,
                'is_private': is_private,
                'country': self._guess_country_from_ip(ip),
                'organization': f"ISP for {ip}",
                'abuse_email': f"abuse@{hostname.split('.')[-2] if hostname else 'isp'}.com",
                'network_range': self._get_network_range(ip)
            }
            
            self.stats["successful"] += 1
            
            logger.info(f"✅ WHOIS info obtenida: {ip} ({info['hostname']})")
            
            return info
        
        except Exception as e:
            self.stats["failed"] += 1
            logger.error(f"❌ Error en WHOIS lookup: {e}")
            
            return {
                'ip': ip,
                'error': str(e)
            }
    
    def _get_hostname(self, ip: str) -> Optional[str]:
        """Obtiene hostname desde IP"""
        
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except:
            return None
    
    def _is_private_ip(self, ip: str) -> bool:
        """Verifica si IP es privada"""
        
        try:
            return ipaddress.ip_address(ip).is_private
        except:
            return False
    
    def _guess_country_from_ip(self, ip: str) -> str:
        """
        Adivina país desde IP (simplificado)
        En producción usar GeoIP2 o similar
        """
        
        # Simplificación educativa
        first_octet = int(ip.split('.')[0])
        
        if first_octet < 50:
            return "US"
        elif first_octet < 100:
            return "EU"
        elif first_octet < 150:
            return "ASIA"
        else:
            return "OTHER"
    
    def _get_network_range(self, ip: str) -> str:
        """Obtiene rango de red (simplificado)"""
        
        octets = ip.split('.')
        return f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
    
    def get_abuse_contact(self, ip: str) -> Dict:
        """
        Obtiene contacto de abuse para una IP
        
        Args:
            ip: Dirección IP
            
        Returns:
            Información de contacto
        """
        
        logger.info(f"📧 Buscando contacto abuse: {ip}")
        
        whois_info = self.lookup_ip(ip)
        
        abuse_contact = {
            'ip': ip,
            'abuse_email': whois_info.get('abuse_email', 'abuse@unknown.com'),
            'organization': whois_info.get('organization', 'Unknown ISP'),
            'country': whois_info.get('country', 'Unknown')
        }
        
        logger.info(
            f"✅ Contacto abuse: {abuse_contact['abuse_email']} "
            f"({abuse_contact['organization']})"
        )
        
        return abuse_contact
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas"""
        return self.stats.copy()