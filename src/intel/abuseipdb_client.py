#!/usr/bin/env python3
"""
Némesis IA - AbuseIPDB Client
Capítulo 11: APIs de la Ley

Cliente para AbuseIPDB API
"""

import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AbuseIPDBClient:
    """Cliente para AbuseIPDB API"""
    
    # Categorías de AbuseIPDB
    CATEGORIES = {
        3: "Fraud Orders",
        4: "DDoS Attack",
        5: "FTP Brute-Force",
        6: "Ping of Death",
        7: "Phishing",
        8: "Fraud VoIP",
        9: "Open Proxy",
        10: "Web Spam",
        11: "Email Spam",
        12: "Blog Spam",
        13: "VPN IP",
        14: "Port Scan",
        15: "Hacking",
        16: "SQL Injection",
        17: "Spoofing",
        18: "Brute-Force",
        19: "Bad Web Bot",
        20: "Exploited Host",
        21: "Web App Attack",
        22: "SSH",
        23: "IoT Targeted"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa cliente AbuseIPDB
        
        Args:
            api_key: API key de AbuseIPDB (obtener en abuseipdb.com)
        """
        
        self.api_key = api_key or "YOUR_ABUSEIPDB_API_KEY"
        self.base_url = "https://api.abuseipdb.com/api/v2"
        
        self.headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        
        # Estadísticas
        self.stats = {
            "checks": 0,
            "reports": 0,
            "errors": 0
        }
        
        logger.info("🌐 AbuseIPDB Client inicializado")
    
    def check_ip(self, ip: str, max_age_days: int = 90) -> Dict:
        """
        Consulta información de una IP
        
        Args:
            ip: Dirección IP
            max_age_days: Máximo días de historial
            
        Returns:
            Diccionario con información de la IP
        """
        
        logger.info(f"🔍 Consultando IP en AbuseIPDB: {ip}")
        
        endpoint = f"{self.base_url}/check"
        
        params = {
            'ipAddress': ip,
            'maxAgeInDays': max_age_days,
            'verbose': ''
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            self.stats["checks"] += 1
            
            if 'data' in data:
                ip_data = data['data']
                
                result = {
                    'ip': ip_data.get('ipAddress'),
                    'is_whitelisted': ip_data.get('isWhitelisted', False),
                    'abuse_confidence_score': ip_data.get('abuseConfidenceScore', 0),
                    'country_code': ip_data.get('countryCode'),
                    'usage_type': ip_data.get('usageType'),
                    'isp': ip_data.get('isp'),
                    'domain': ip_data.get('domain'),
                    'total_reports': ip_data.get('totalReports', 0),
                    'num_distinct_users': ip_data.get('numDistinctUsers', 0),
                    'last_reported_at': ip_data.get('lastReportedAt'),
                    'is_public': ip_data.get('isPublic', True),
                    'is_tor': ip_data.get('isTor', False)
                }
                
                logger.info(
                    f"✅ IP {ip}: Score {result['abuse_confidence_score']}%, "
                    f"Reports: {result['total_reports']}"
                )
                
                return result
            
            return {}
        
        except requests.exceptions.RequestException as e:
            self.stats["errors"] += 1
            logger.error(f"❌ Error consultando AbuseIPDB: {e}")
            
            # Retornar datos simulados en caso de error (para testing)
            return {
                'ip': ip,
                'error': str(e),
                'abuse_confidence_score': 0,
                'simulated': True
            }
    
    def report_ip(
        self,
        ip: str,
        categories: List[int],
        comment: str
    ) -> Dict:
        """
        Reporta una IP abusiva
        
        Args:
            ip: Dirección IP
            categories: Lista de IDs de categorías
            comment: Comentario descriptivo
            
        Returns:
            Resultado del reporte
        """
        
        logger.info(f"📝 Reportando IP a AbuseIPDB: {ip}")
        
        endpoint = f"{self.base_url}/report"
        
        data = {
            'ip': ip,
            'categories': ','.join(map(str, categories)),
            'comment': comment[:1024]  # Max 1024 chars
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=data,
                timeout=10
            )
            
            response.raise_for_status()
            result = response.json()
            
            self.stats["reports"] += 1
            
            logger.info(f"✅ IP {ip} reportada exitosamente")
            
            return {
                'success': True,
                'ip': ip,
                'abuse_confidence_score': result.get('data', {}).get('abuseConfidenceScore', 0),
                'reported_at': datetime.now().isoformat()
            }
        
        except requests.exceptions.RequestException as e:
            self.stats["errors"] += 1
            logger.error(f"❌ Error reportando a AbuseIPDB: {e}")
            
            # Simular éxito para testing
            return {
                'success': False,
                'error': str(e),
                'ip': ip,
                'simulated': True
            }
    
    def bulk_report(self, reports: List[Dict]) -> Dict:
        """
        Reporta múltiples IPs en lote
        
        Args:
            reports: Lista de reportes con formato:
                    [{'ip': '1.2.3.4', 'categories': [14,15], 'comment': '...'}]
        
        Returns:
            Resumen de reportes
        """
        
        logger.info(f"📋 Reportando {len(reports)} IPs en lote...")
        
        results = {
            'total': len(reports),
            'successful': 0,
            'failed': 0,
            'reports': []
        }
        
        for report in reports:
            result = self.report_ip(
                ip=report['ip'],
                categories=report['categories'],
                comment=report['comment']
            )
            
            results['reports'].append(result)
            
            if result.get('success'):
                results['successful'] += 1
            else:
                results['failed'] += 1
        
        logger.info(
            f"✅ Reporte en lote completado: "
            f"{results['successful']}/{results['total']} exitosos"
        )
        
        return results
    
    def get_blacklist(self, limit: int = 10000) -> List[str]:
        """
        Obtiene lista negra de IPs (requiere plan premium)
        
        Args:
            limit: Número máximo de IPs
            
        Returns:
            Lista de IPs maliciosas
        """
        
        logger.info(f"📥 Obteniendo blacklist (limit: {limit})...")
        
        endpoint = f"{self.base_url}/blacklist"
        
        params = {
            'limit': limit,
            'confidenceMinimum': 90
        }
        
        try:
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            blacklist = [
                item['ipAddress'] 
                for item in data.get('data', [])
            ]
            
            logger.info(f"✅ Blacklist obtenida: {len(blacklist)} IPs")
            
            return blacklist
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error obteniendo blacklist: {e}")
            return []
    
    def map_threat_to_categories(self, threat_type: str) -> List[int]:
        """
        Mapea tipo de amenaza a categorías de AbuseIPDB
        
        Args:
            threat_type: Tipo de amenaza detectada
            
        Returns:
            Lista de IDs de categorías
        """
        
        mapping = {
            'SQL_INJECTION': [16],
            'XSS': [21],
            'BRUTE_FORCE': [18],
            'SSH_ATTACK': [22],
            'DDOS': [4],
            'PORT_SCAN': [14],
            'WEB_ATTACK': [21],
            'EXPLOIT': [15],
            'PHISHING': [7],
            'SPAM': [10, 11],
            'BOTNET': [20],
            'MALWARE': [15, 20],
            'IOT_ATTACK': [23]
        }
        
        return mapping.get(threat_type, [15])  # Default: Hacking
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de uso"""
        return self.stats.copy()