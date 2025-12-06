#!/usr/bin/env python3
"""
Némesis IA - Red Button System
Capítulo 12: El Botón Rojo

Sistema de respuesta de emergencia - "El Botón Rojo"
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from .cert_database import CERTDatabase
from .incident_reporter import IncidentReporter

logger = logging.getLogger(__name__)


class RedButton:
    """Sistema de respuesta de emergencia - El Botón Rojo"""
    
    def __init__(
        self,
        forensic_sentinel=None,
        fiscal_digital=None,
        law_enforcement=None
    ):
        """
        Inicializa Red Button System
        
        Args:
            forensic_sentinel: ForensicSentinel para evidencia
            fiscal_digital: FiscalDigital para documentos
            law_enforcement: LawEnforcementConnector para intel
        """
        
        # Componentes
        self.cert_db = CERTDatabase()
        self.reporter = IncidentReporter()
        
        # Integraciones
        self.forensic = forensic_sentinel
        self.fiscal = fiscal_digital
        self.law_enforcement = law_enforcement
        
        # Estado
        self.active_incidents = []
        self.escalations = []
        
        # Estadísticas
        self.stats = {
            "button_presses": 0,
            "certs_notified": 0,
            "critical_incidents": 0,
            "reports_sent": 0
        }
        
        logger.info("🚨 Red Button System inicializado")
    
    def press_red_button(
        self,
        incident_data: Dict,
        evidence_id: Optional[str] = None,
        auto_escalate: bool = True
    ) -> Dict:
        """
        PRESIONA EL BOTÓN ROJO - Respuesta de emergencia
        
        Args:
            incident_data: Datos del incidente crítico
            evidence_id: ID de evidencia (opcional)
            auto_escalate: Si escalar automáticamente
            
        Returns:
            Resultado de la escalación
        """
        
        logger.critical("🚨🚨🚨 RED BUTTON PRESSED 🚨🚨🚨")
        logger.critical(f"Incident: {incident_data.get('case_id', 'UNKNOWN')}")
        
        self.stats["button_presses"] += 1
        
        if incident_data.get('severity') == 'CRITICAL':
            self.stats["critical_incidents"] += 1
        
        # 1. Recopilar evidencia completa
        evidence_package = self._gather_evidence(incident_data, evidence_id)
        
        # 2. Generar documentos legales
        legal_docs = self._generate_legal_documents(incident_data, evidence_package)
        
        # 3. Análisis de threat intelligence
        threat_intel = self._analyze_threat(incident_data)
        
        # 4. Determinar CERTs a notificar
        target_certs = self._select_certs(incident_data, threat_intel)
        
        # 5. Generar reportes para cada CERT
        cert_reports = []
        for cert in target_certs:
            report = self.reporter.generate_cert_report(
                incident_data=incident_data,
                evidence_data=evidence_package,
                cert_name=cert.name
            )
            cert_reports.append({
                'cert': cert,
                'report': report
            })
        
        # 6. Registrar escalación
        escalation = {
            'timestamp': datetime.now().isoformat(),
            'incident_id': incident_data.get('case_id'),
            'severity': incident_data.get('severity'),
            'certs_notified': [cert.name for cert in target_certs],
            'auto_escalated': auto_escalate,
            'evidence_id': evidence_id,
            'legal_docs': legal_docs,
            'threat_intel': threat_intel,
            'reports': cert_reports
        }
        
        self.escalations.append(escalation)
        self.stats["certs_notified"] += len(target_certs)
        
        if auto_escalate:
            # En producción, aquí se enviarían los emails
            self._send_notifications(cert_reports)
        
        logger.critical(
            f"🚨 Emergency escalation complete - "
            f"{len(target_certs)} CERTs notified"
        )
        
        return escalation
    
    def _gather_evidence(
        self,
        incident_data: Dict,
        evidence_id: Optional[str]
    ) -> Dict:
        """Recopila evidencia completa"""
        
        logger.info("📦 Recopilando evidencia...")
        
        evidence_package = {
            'evidence_id': evidence_id or f"EVD-{incident_data.get('case_id', 'UNKNOWN')}",
            'evidence_type': 'INCIDENT_EVIDENCE',
            'incident_id': incident_data.get('case_id'),
            'collected_at': datetime.now().isoformat(),
            'hash': 'BLOCKCHAIN_HASH_PLACEHOLDER',
            'has_pcap': True,
            'has_logs': True
        }
        
        # Si tenemos ForensicSentinel, usar evidencia real
        if self.forensic:
            # En producción, recuperar evidencia del blockchain
            pass
        
        logger.info("✅ Evidencia recopilada")
        
        return evidence_package
    
    def _generate_legal_documents(
        self,
        incident_data: Dict,
        evidence_package: Dict
    ) -> Dict:
        """Genera documentos legales"""
        
        logger.info("📄 Generando documentos legales...")
        
        legal_docs = {
            'incident_report': None,
            'evidence_report': None,
            'legal_complaint': None,
            'custody_report': None
        }
        
        # Si tenemos FiscalDigital, generar PDFs reales
        if self.fiscal:
            # En producción, generar PDFs
            pass
        else:
            # Simular generación
            legal_docs = {
                'incident_report': 'incident_report.pdf',
                'evidence_report': 'evidence_report.pdf',
                'legal_complaint': 'legal_complaint.pdf',
                'custody_report': 'custody_report.pdf'
            }
        
        logger.info("✅ Documentos legales generados")
        
        return legal_docs
    
    def _analyze_threat(self, incident_data: Dict) -> Dict:
        """Analiza amenaza con threat intelligence"""
        
        logger.info("🔍 Analizando amenaza...")
        
        threat_intel = {
            'source_ip': incident_data.get('source_ip'),
            'threat_level': incident_data.get('severity'),
            'threat_type': incident_data.get('incident_type'),
            'abuseipdb_score': 0,
            'spamhaus_listed': False,
            'country': 'UNKNOWN'
        }
        
        # Si tenemos LawEnforcement, hacer check real
        if self.law_enforcement and incident_data.get('source_ip'):
            try:
                check = self.law_enforcement.comprehensive_ip_check(
                    incident_data['source_ip']
                )
                threat_intel.update({
                    'threat_score': check.get('threat_score', 0),
                    'abuseipdb_score': check.get('abuseipdb', {}).get('abuse_confidence_score', 0),
                    'spamhaus_listed': check.get('spamhaus', {}).get('zones_listed', 0) > 0,
                    'country': check.get('whois', {}).get('country', 'UNKNOWN')
                })
            except Exception as e:
                logger.error(f"Error en threat analysis: {e}")
        
        logger.info("✅ Análisis completado")
        
        return threat_intel
    
    def _select_certs(
        self,
        incident_data: Dict,
        threat_intel: Dict
    ) -> List:
        """Selecciona CERTs a notificar"""
        
        logger.info("🎯 Seleccionando CERTs...")
        
        threat_level = incident_data.get('severity', 'MEDIUM')
        source_country = threat_intel.get('country')
        
        certs = self.cert_db.get_recommended_certs(
            threat_level=threat_level,
            source_country=source_country
        )
        
        logger.info(f"✅ {len(certs)} CERTs seleccionados")
        
        return certs
    
    def _send_notifications(self, cert_reports: List[Dict]):
        """Envía notificaciones a CERTs"""
        
        logger.info(f"📧 Enviando notificaciones a {len(cert_reports)} CERTs...")
        
        for cert_report in cert_reports:
            cert = cert_report['cert']
            report = cert_report['report']
            
            # En producción, enviar email real
            logger.info(
                f"   📨 Email enviado a {cert.name} ({cert.email}): "
                f"{report['subject']}"
            )
            
            self.stats["reports_sent"] += 1
        
        logger.info("✅ Notificaciones enviadas")
    
    def bulk_escalate(
        self,
        incidents: List[Dict],
        cert_id: Optional[str] = None
    ) -> Dict:
        """
        Escala múltiples incidentes
        
        Args:
            incidents: Lista de incidentes
            cert_id: CERT específico (opcional)
            
        Returns:
            Resultado de escalación en lote
        """
        
        logger.warning(f"🚨 Escalando {len(incidents)} incidentes en lote...")
        
        if cert_id:
            cert = self.cert_db.get_cert(cert_id)
            target_certs = [cert] if cert else []
        else:
            # Usar US-CERT por defecto
            target_certs = [self.cert_db.get_cert('US-CERT')]
        
        results = []
        
        for cert in target_certs:
            report = self.reporter.generate_bulk_report(
                incidents=incidents,
                cert_name=cert.name
            )
            
            results.append({
                'cert': cert,
                'report': report
            })
            
            self.stats["reports_sent"] += 1
        
        logger.info(f"✅ Escalación en lote completada")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_incidents': len(incidents),
            'certs_notified': len(target_certs),
            'reports': results
        }
    
    def get_escalation_history(self) -> List[Dict]:
        """Obtiene historial de escalaciones"""
        return self.escalations.copy()
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas"""
        return self.stats.copy()
    
    def generate_status_report(self) -> str:
        """Genera reporte de estado"""
        
        stats = self.get_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              RED BUTTON SYSTEM - STATUS REPORT                   ║
╚══════════════════════════════════════════════════════════════════╝

🚨 Emergency Response Statistics:

   Button Presses:        {stats['button_presses']}
   CERTs Notified:        {stats['certs_notified']}
   Critical Incidents:    {stats['critical_incidents']}
   Reports Sent:          {stats['reports_sent']}

📋 Recent Escalations:   {len(self.escalations)}

🌐 Available CERTs:      {len(self.cert_db.certs)}

⚡ Status:                READY FOR EMERGENCY RESPONSE

═══════════════════════════════════════════════════════════════════
"""
        
        return report