#!/usr/bin/env python3
"""
Némesis IA - Spamhaus Client
Capítulo 11: APIs de la Ley

Cliente para Spamhaus DNSBL
"""

import logging
import socket
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SpamhausClient:
    """Cliente para Spamhaus DNSBL"""
    
    # Zonas DNSBL de Spamhaus
    DNSBL_ZONES = {
        'zen.spamhaus.org': 'Combined blocklist',
        'sbl.spamhaus.org': 'Spamhaus Block List',
        'xbl.spamhaus.org': 'Exploits Block List',
        'pbl.spamhaus.org': 'Policy Block List',
        'dbl.spamhaus.org': 'Domain Block List'
    }
    
    # Códigos de retorno
    RETURN_CODES = {
        '127.0.0.2': 'SBL - Spammer',
        '127.0.0.3': 'SBL - Spammer',
        '127.0.0.4': 'XBL - Exploited',
        '127.0.0.9': 'SBL - Spammer (CSS)',
        '127.0.0.10': 'PBL - Policy',
        '127.0.0.11': 'PBL - Policy'
    }
    
    def __init__(self):
        """Inicializa cliente Spamhaus"""
        
        self.stats = {
            "checks": 0,
            "blocked": 0,
            "clean": 0
        }
        
        logger.info("🛡️ Spamhaus Client inicializado")
    
    def check_ip(self, ip: str, zone: str = 'zen.spamhaus.org') -> Dict:
        """
        Verifica IP en DNSBL de Spamhaus
        
        Args:
            ip: Dirección IP
            zone: Zona DNSBL a consultar
            
        Returns:
            Resultado de la consulta
        """
        
        logger.info(f"🔍 Consultando IP en Spamhaus: {ip}")
        
        self.stats["checks"] += 1
        
        # Invertir IP para consulta DNSBL
        reversed_ip = '.'.join(reversed(ip.split('.')))
        query = f"{reversed_ip}.{zone}"
        
        try:
            # Consulta DNS
            result = socket.gethostbyname(query)
            
            # IP está en lista negra
            self.stats["blocked"] += 1
            
            listed_reason = self.RETURN_CODES.get(result, 'Listed in DNSBL')
            
            logger.warning(f"⚠️ IP {ip} está en blacklist: {listed_reason}")
            
            return {
                'ip': ip,
                'listed': True,
                'zone': zone,
                'return_code': result,
                'reason': listed_reason,
                'threat_level': 'HIGH'
            }
        
        except socket.gaierror:
            # IP no está en lista negra
            self.stats["clean"] += 1
            
            logger.info(f"✅ IP {ip} limpia en Spamhaus")
            
            return {
                'ip': ip,
                'listed': False,
                'zone': zone,
                'threat_level': 'LOW'
            }
        
        except Exception as e:
            logger.error(f"❌ Error consultando Spamhaus: {e}")
            
            return {
                'ip': ip,
                'error': str(e),
                'listed': None
            }
    
    def check_ip_all_zones(self, ip: str) -> Dict:
        """
        Verifica IP en todas las zonas DNSBL
        
        Args:
            ip: Dirección IP
            
        Returns:
            Resultados combinados
        """
        
        logger.info(f"🔍 Consultando IP en todas las zonas: {ip}")
        
        results = {
            'ip': ip,
            'zones_checked': len(self.DNSBL_ZONES),
            'zones_listed': 0,
            'zone_results': {}
        }
        
        for zone, description in self.DNSBL_ZONES.items():
            result = self.check_ip(ip, zone)
            results['zone_results'][zone] = result
            
            if result.get('listed'):
                results['zones_listed'] += 1
        
        # Determinar threat level general
        if results['zones_listed'] >= 3:
            results['overall_threat'] = 'CRITICAL'
        elif results['zones_listed'] >= 2:
            results['overall_threat'] = 'HIGH'
        elif results['zones_listed'] == 1:
            results['overall_threat'] = 'MEDIUM'
        else:
            results['overall_threat'] = 'LOW'
        
        logger.info(
            f"✅ IP {ip}: Listed en {results['zones_listed']}/{results['zones_checked']} zonas "
            f"(Threat: {results['overall_threat']})"
        )
        
        return results
    
    def check_domain(self, domain: str) -> Dict:
        """
        Verifica dominio en DBL (Domain Block List)
        
        Args:
            domain: Nombre de dominio
            
        Returns:
            Resultado de la consulta
        """
        
        logger.info(f"🔍 Consultando dominio en Spamhaus DBL: {domain}")
        
        query = f"{domain}.dbl.spamhaus.org"
        
        try:
            result = socket.gethostbyname(query)
            
            logger.warning(f"⚠️ Dominio {domain} está en blacklist")
            
            return {
                'domain': domain,
                'listed': True,
                'return_code': result,
                'threat_level': 'HIGH'
            }
        
        except socket.gaierror:
            logger.info(f"✅ Dominio {domain} limpio")
            
            return {
                'domain': domain,
                'listed': False,
                'threat_level': 'LOW'
            }
        
        except Exception as e:
            logger.error(f"❌ Error consultando DBL: {e}")
            
            return {
                'domain': domain,
                'error': str(e),
                'listed': None
            }
    
    def bulk_check(self, ips: List[str]) -> Dict:
        """
        Verifica múltiples IPs
        
        Args:
            ips: Lista de IPs
            
        Returns:
            Resumen de verificación
        """
        
        logger.info(f"📋 Verificando {len(ips)} IPs en lote...")
        
        results = {
            'total': len(ips),
            'clean': 0,
            'listed': 0,
            'errors': 0,
            'details': []
        }
        
        for ip in ips:
            result = self.check_ip(ip)
            results['details'].append(result)
            
            if result.get('listed') is True:
                results['listed'] += 1
            elif result.get('listed') is False:
                results['clean'] += 1
            else:
                results['errors'] += 1
        
        logger.info(
            f"✅ Verificación completada: "
            f"{results['clean']} clean, {results['listed']} listed"
        )
        
        return results
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de uso"""
        return self.stats.copy()