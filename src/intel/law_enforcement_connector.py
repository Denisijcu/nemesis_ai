#!/usr/bin/env python3
"""
Némesis IA - Law Enforcement Connector
Capítulo 11: APIs de la Ley

Sistema integrador de APIs de inteligencia y reporte
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from .abuseipdb_client import AbuseIPDBClient
from .spamhaus_client import SpamhausClient
from .whois_client import WHOISClient

logger = logging.getLogger(__name__)


class LawEnforcementConnector:
    """Sistema completo de inteligencia y reporte de amenazas"""
    
    def __init__(self, abuseipdb_api_key: Optional[str] = None):
        """
        Inicializa Law Enforcement Connector
        
        Args:
            abuseipdb_api_key: API key de AbuseIPDB
        """
        
        # Clientes
        self.abuseipdb = AbuseIPDBClient(abuseipdb_api_key)
        self.spamhaus = SpamhausClient()
        self.whois = WHOISClient()
        
        # Estadísticas
        self.stats = {
            "total_checks": 0,
            "total_reports": 0,
            "high_threat_ips": 0,
            "reported_to_abuseipdb": 0,
            "abuse_contacts_found": 0
        }
        
        logger.info("⚖️ LawEnforcementConnector inicializado")
    
    def comprehensive_ip_check(self, ip: str) -> Dict:
        """
        Verificación completa de IP en todas las fuentes
        
        Args:
            ip: Dirección IP
            
        Returns:
            Análisis completo de la IP
        """
        
        logger.info(f"🔍 Verificación completa de IP: {ip}")
        
        self.stats["total_checks"] += 1
        
        # 1. AbuseIPDB
        abuseipdb_result = self.abuseipdb.check_ip(ip)
        
        # 2. Spamhaus
        spamhaus_result = self.spamhaus.check_ip_all_zones(ip)
        
        # 3. WHOIS
        whois_result = self.whois.lookup_ip(ip)
        
        # Calcular threat score general
        threat_score = self._calculate_threat_score(
            abuseipdb_result,
            spamhaus_result,
            whois_result
        )
        
        # Determinar threat level
        if threat_score >= 90:
            threat_level = "CRITICAL"
        elif threat_score >= 70:
            threat_level = "HIGH"
        elif threat_score >= 40:
            threat_level = "MEDIUM"
        else:
            threat_level = "LOW"
        
        if threat_score >= 70:
            self.stats["high_threat_ips"] += 1
        
        comprehensive_result = {
            'ip': ip,
            'checked_at': datetime.now().isoformat(),
            'threat_score': threat_score,
            'threat_level': threat_level,
            'abuseipdb': abuseipdb_result,
            'spamhaus': spamhaus_result,
            'whois': whois_result,
            'recommendation': self._get_recommendation(threat_level)
        }
        
        logger.info(
            f"✅ Verificación completa: {ip} - "
            f"Score: {threat_score}, Level: {threat_level}"
        )
        
        return comprehensive_result
    
    def _calculate_threat_score(
        self,
        abuseipdb_result: Dict,
        spamhaus_result: Dict,
        whois_result: Dict
    ) -> int:
        """
        Calcula score de amenaza combinando todas las fuentes
        
        Returns:
            Score de 0-100
        """
        
        score = 0
        
        # AbuseIPDB (peso: 50%)
        abuse_score = abuseipdb_result.get('abuse_confidence_score', 0)
        score += abuse_score * 0.5
        
        # Spamhaus (peso: 40%)
        zones_listed = spamhaus_result.get('zones_listed', 0)
        spamhaus_score = min(zones_listed * 25, 100)  # 25% por zona
        score += spamhaus_score * 0.4
        
        # WHOIS - IP privada reduce score (peso: 10%)
        if whois_result.get('is_private'):
            score -= 20
        
        return max(0, min(100, int(score)))
    
    def _get_recommendation(self, threat_level: str) -> str:
        """Genera recomendación basada en threat level"""
        
        recommendations = {
            "CRITICAL": "BLOCK IMMEDIATELY. Report to authorities. Preserve all evidence.",
            "HIGH": "BLOCK and monitor. Consider reporting to AbuseIPDB and abuse contact.",
            "MEDIUM": "Monitor closely. Rate limit if possible. Document activity.",
            "LOW": "Normal monitoring. Log activity for future reference."
        }
        
        return recommendations.get(threat_level, "No action required.")
    
    def report_threat(
        self,
        ip: str,
        threat_type: str,
        evidence: str,
        auto_report: bool = True
    ) -> Dict:
        """
        Reporta amenaza a AbuseIPDB
        
        Args:
            ip: IP maliciosa
            threat_type: Tipo de amenaza
            evidence: Evidencia del ataque
            auto_report: Si reportar automáticamente
            
        Returns:
            Resultado del reporte
        """
        
        logger.info(f"📝 Reportando amenaza: {ip} ({threat_type})")
        
        self.stats["total_reports"] += 1
        
        if not auto_report:
            logger.info("⏸️ Auto-report deshabilitado, generando reporte solamente")
            return {
                'ip': ip,
                'threat_type': threat_type,
                'reported': False,
                'reason': 'Auto-report disabled'
            }
        
        # Mapear tipo de amenaza a categorías
        categories = self.abuseipdb.map_threat_to_categories(threat_type)
        
        # Construir comentario
        comment = f"[NEMESIS_IA] {threat_type} attack detected. {evidence[:900]}"
        
        # Reportar a AbuseIPDB
        result = self.abuseipdb.report_ip(
            ip=ip,
            categories=categories,
            comment=comment
        )
        
        if result.get('success'):
            self.stats["reported_to_abuseipdb"] += 1
        
        logger.info(
            f"✅ Amenaza reportada: {ip} - "
            f"Success: {result.get('success', False)}"
        )
        
        return result
    
    def bulk_threat_report(
        self,
        threats: List[Dict],
        auto_report: bool = True
    ) -> Dict:
        """
        Reporta múltiples amenazas
        
        Args:
            threats: Lista de amenazas con formato:
                    [{'ip': '1.2.3.4', 'threat_type': 'SQL_INJECTION', 'evidence': '...'}]
            auto_report: Si reportar automáticamente
            
        Returns:
            Resumen de reportes
        """
        
        logger.info(f"📋 Reportando {len(threats)} amenazas en lote...")
        
        results = {
            'total': len(threats),
            'successful': 0,
            'failed': 0,
            'reports': []
        }
        
        for threat in threats:
            result = self.report_threat(
                ip=threat['ip'],
                threat_type=threat['threat_type'],
                evidence=threat.get('evidence', 'Attack detected'),
                auto_report=auto_report
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
    
    def find_abuse_contact(self, ip: str) -> Dict:
        """
        Encuentra contacto de abuse para reportar manualmente
        
        Args:
            ip: Dirección IP
            
        Returns:
            Información de contacto
        """
        
        logger.info(f"📧 Buscando contacto abuse: {ip}")
        
        self.stats["abuse_contacts_found"] += 1
        
        # Obtener info WHOIS
        contact = self.whois.get_abuse_contact(ip)
        
        # Verificación adicional
        check = self.comprehensive_ip_check(ip)
        
        result = {
            **contact,
            'threat_level': check['threat_level'],
            'threat_score': check['threat_score'],
            'recommended_action': check['recommendation']
        }
        
        logger.info(
            f"✅ Contacto encontrado: {result['abuse_email']} "
            f"(Threat: {result['threat_level']})"
        )
        
        return result
    
    def generate_threat_intel_report(
        self,
        ips: List[str]
    ) -> Dict:
        """
        Genera reporte de inteligencia de amenazas
        
        Args:
            ips: Lista de IPs a analizar
            
        Returns:
            Reporte completo
        """
        
        logger.info(f"📊 Generando reporte de threat intel para {len(ips)} IPs...")
        
        results = []
        threat_distribution = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for ip in ips:
            check = self.comprehensive_ip_check(ip)
            results.append(check)
            
            threat_level = check['threat_level']
            threat_distribution[threat_level] = threat_distribution.get(threat_level, 0) + 1
        
        # Top IPs más peligrosas
        sorted_ips = sorted(results, key=lambda x: x['threat_score'], reverse=True)
        top_threats = sorted_ips[:10]
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_ips_analyzed': len(ips),
            'threat_distribution': threat_distribution,
            'average_threat_score': sum(r['threat_score'] for r in results) / len(results) if results else 0,
            'top_threats': top_threats,
            'full_results': results,
            'recommendations': self._generate_intel_recommendations(threat_distribution)
        }
        
        logger.info(
            f"✅ Reporte generado: {len(ips)} IPs, "
            f"Avg Score: {report['average_threat_score']:.1f}"
        )
        
        return report
    
    def _generate_intel_recommendations(
        self,
        distribution: Dict[str, int]
    ) -> List[str]:
        """Genera recomendaciones basadas en distribución de amenazas"""
        
        recommendations = []
        
        if distribution.get('CRITICAL', 0) > 0:
            recommendations.append(
                f"⚠️ {distribution['CRITICAL']} IPs CRÍTICAS detectadas - "
                "Acción inmediata requerida"
            )
        
        if distribution.get('HIGH', 0) > 5:
            recommendations.append(
                f"🔴 {distribution['HIGH']} IPs de ALTO riesgo - "
                "Considerar bloqueo masivo"
            )
        
        if distribution.get('MEDIUM', 0) > 10:
            recommendations.append(
                f"🟡 {distribution['MEDIUM']} IPs de MEDIO riesgo - "
                "Incrementar monitoreo"
            )
        
        total_threats = distribution.get('CRITICAL', 0) + distribution.get('HIGH', 0)
        if total_threats > 10:
            recommendations.append(
                "🚨 Posible ataque coordinado detectado - "
                "Alertar a equipo de seguridad"
            )
        
        if not recommendations:
            recommendations.append("✅ Nivel de amenaza bajo - Continuar monitoreo normal")
        
        return recommendations
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas completas"""
        
        return {
            'connector': self.stats,
            'abuseipdb': self.abuseipdb.get_statistics(),
            'spamhaus': self.spamhaus.get_statistics(),
            'whois': self.whois.get_statistics()
        }
    
    def generate_summary_report(self) -> str:
        """Genera reporte resumen de actividad"""
        
        stats = self.get_statistics()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║          LAW ENFORCEMENT CONNECTOR - ACTIVITY SUMMARY            ║
╚══════════════════════════════════════════════════════════════════╝

📊 General Statistics:

   Total IP Checks:       {stats['connector']['total_checks']}
   Total Reports:         {stats['connector']['total_reports']}
   High Threat IPs:       {stats['connector']['high_threat_ips']}
   Reported to AbuseIPDB: {stats['connector']['reported_to_abuseipdb']}
   Abuse Contacts Found:  {stats['connector']['abuse_contacts_found']}

🌐 AbuseIPDB:

   Checks:     {stats['abuseipdb']['checks']}
   Reports:    {stats['abuseipdb']['reports']}
   Errors:     {stats['abuseipdb']['errors']}

🛡️ Spamhaus:

   Checks:     {stats['spamhaus']['checks']}
   Blocked:    {stats['spamhaus']['blocked']}
   Clean:      {stats['spamhaus']['clean']}

🌍 WHOIS:

   Lookups:    {stats['whois']['lookups']}
   Successful: {stats['whois']['successful']}
   Failed:     {stats['whois']['failed']}

⚖️ Integration with external threat intelligence databases active.

═══════════════════════════════════════════════════════════════════
"""
        
        return summary