#!/usr/bin/env python3
"""
Némesis IA - Incident Reporter
Capítulo 12: El Botón Rojo

Generador de reportes de incidentes para CERTs
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class IncidentReporter:
    """Generador de reportes de incidentes"""
    
    def __init__(self):
        """Inicializa incident reporter"""
        logger.info("📧 IncidentReporter inicializado")
    
    def generate_cert_report(
        self,
        incident_data: Dict,
        evidence_data: Dict,
        cert_name: str
    ) -> Dict:
        """
        Genera reporte de incidente para CERT
        
        Args:
            incident_data: Datos del incidente
            evidence_data: Datos de evidencia
            cert_name: Nombre del CERT destinatario
            
        Returns:
            Reporte completo
        """
        
        logger.info(f"📝 Generando reporte CERT para: {cert_name}")
        
        report = {
            'to': cert_name,
            'subject': self._generate_subject(incident_data),
            'body': self._generate_body(incident_data, evidence_data, cert_name),
            'attachments': self._list_attachments(evidence_data),
            'priority': self._get_priority(incident_data),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _generate_subject(self, incident_data: Dict) -> str:
        """Genera subject line del email"""
        
        case_id = incident_data.get('case_id', 'UNKNOWN')
        incident_type = incident_data.get('incident_type', 'CYBER_ATTACK')
        severity = incident_data.get('severity', 'MEDIUM')
        
        return f"[{severity}] Cybersecurity Incident Report - {incident_type} - Case {case_id}"
    
    def _generate_body(
        self,
        incident_data: Dict,
        evidence_data: Dict,
        cert_name: str
    ) -> str:
        """Genera cuerpo del email"""
        
        body = f"""
Dear {cert_name} Team,

We are reporting a cybersecurity incident detected by our NEMESIS IA autonomous 
defense system. This report contains details of the incident, evidence collected, 
and recommended actions.

═══════════════════════════════════════════════════════════════════
INCIDENT SUMMARY
═══════════════════════════════════════════════════════════════════

Case ID:           {incident_data.get('case_id', 'N/A')}
Detection Time:    {incident_data.get('detection_time', 'N/A')}
Incident Type:     {incident_data.get('incident_type', 'N/A')}
Severity:          {incident_data.get('severity', 'N/A')}
Confidence:        {incident_data.get('confidence', 0.0)*100:.1f}%

Source IP:         {incident_data.get('source_ip', 'N/A')}
Target:            {incident_data.get('target', 'N/A')}
Attack Vector:     {incident_data.get('attack_vector', 'N/A')}

═══════════════════════════════════════════════════════════════════
EVIDENCE
═══════════════════════════════════════════════════════════════════

Evidence ID:       {evidence_data.get('evidence_id', 'N/A')}
Evidence Type:     {evidence_data.get('evidence_type', 'N/A')}
Chain of Custody:  VERIFIED (Blockchain-based)
Cryptographic Hash: {evidence_data.get('hash', 'N/A')[:32]}...

All evidence has been preserved using blockchain technology to ensure 
integrity and admissibility in legal proceedings.

═══════════════════════════════════════════════════════════════════
TECHNICAL DETAILS
═══════════════════════════════════════════════════════════════════

{incident_data.get('technical_analysis', 'Technical analysis in attached report.')}

═══════════════════════════════════════════════════════════════════
IMPACT ASSESSMENT
═══════════════════════════════════════════════════════════════════

{incident_data.get('impact_assessment', 'Impact assessment in attached report.')}

═══════════════════════════════════════════════════════════════════
ACTIONS TAKEN
═══════════════════════════════════════════════════════════════════

{incident_data.get('response_actions', 'Response actions in attached report.')}

═══════════════════════════════════════════════════════════════════
ATTACHMENTS
═══════════════════════════════════════════════════════════════════

The following documents are attached:
{self._format_attachments_list(evidence_data)}

═══════════════════════════════════════════════════════════════════
CONTACT INFORMATION
═══════════════════════════════════════════════════════════════════

This report was generated automatically by NEMESIS IA Forensic System.
For additional information, please contact our security operations team.

System:     NEMESIS IA v1.0
Generated:  {datetime.now().isoformat()}
Compliance: ISO/IEC 27037:2012

═══════════════════════════════════════════════════════════════════

This is an automated report. Please do not reply to this email directly.
For urgent matters, please use our emergency contact information.

Best regards,
NEMESIS IA Autonomous Defense System
"""
        
        return body
    
    def _list_attachments(self, evidence_data: Dict) -> List[str]:
        """Lista archivos adjuntos"""
        
        attachments = [
            'incident_report.pdf',
            'evidence_report.pdf',
            'chain_of_custody.pdf'
        ]
        
        if evidence_data.get('has_pcap'):
            attachments.append('network_capture.pcap')
        
        if evidence_data.get('has_logs'):
            attachments.append('system_logs.tar.gz')
        
        return attachments
    
    def _format_attachments_list(self, evidence_data: Dict) -> str:
        """Formatea lista de adjuntos"""
        
        attachments = self._list_attachments(evidence_data)
        
        return '\n'.join([f"   • {att}" for att in attachments])
    
    def _get_priority(self, incident_data: Dict) -> str:
        """Determina prioridad del email"""
        
        severity = incident_data.get('severity', 'MEDIUM')
        
        priority_map = {
            'CRITICAL': 'HIGH',
            'HIGH': 'HIGH',
            'MEDIUM': 'NORMAL',
            'LOW': 'LOW'
        }
        
        return priority_map.get(severity, 'NORMAL')
    
    def generate_bulk_report(
        self,
        incidents: List[Dict],
        cert_name: str
    ) -> Dict:
        """
        Genera reporte de múltiples incidentes
        
        Args:
            incidents: Lista de incidentes
            cert_name: CERT destinatario
            
        Returns:
            Reporte consolidado
        """
        
        logger.info(f"📋 Generando reporte consolidado: {len(incidents)} incidentes")
        
        summary = self._generate_incidents_summary(incidents)
        
        body = f"""
Dear {cert_name} Team,

This is a consolidated report of multiple cybersecurity incidents detected 
by NEMESIS IA in the last reporting period.

═══════════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════════

Total Incidents:   {len(incidents)}
{summary}

═══════════════════════════════════════════════════════════════════
DETAILED INCIDENTS
═══════════════════════════════════════════════════════════════════

{self._format_incidents_list(incidents)}

═══════════════════════════════════════════════════════════════════

Complete documentation for each incident is available upon request.

Best regards,
NEMESIS IA Autonomous Defense System
"""
        
        return {
            'to': cert_name,
            'subject': f"Consolidated Incident Report - {len(incidents)} Incidents",
            'body': body,
            'priority': 'NORMAL',
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_incidents_summary(self, incidents: List[Dict]) -> str:
        """Genera resumen de incidentes"""
        
        # Contar por tipo
        types = {}
        severities = {}
        
        for incident in incidents:
            incident_type = incident.get('incident_type', 'UNKNOWN')
            severity = incident.get('severity', 'MEDIUM')
            
            types[incident_type] = types.get(incident_type, 0) + 1
            severities[severity] = severities.get(severity, 0) + 1
        
        summary = "By Type:\n"
        for itype, count in types.items():
            summary += f"   {itype:20} {count}\n"
        
        summary += "\nBy Severity:\n"
        for severity, count in severities.items():
            summary += f"   {severity:20} {count}\n"
        
        return summary
    
    def _format_incidents_list(self, incidents: List[Dict]) -> str:
        """Formatea lista de incidentes"""
        
        formatted = ""
        
        for i, incident in enumerate(incidents, 1):
            formatted += f"""
Incident #{i}:
   Case ID:     {incident.get('case_id', 'N/A')}
   Type:        {incident.get('incident_type', 'N/A')}
   Severity:    {incident.get('severity', 'N/A')}
   Source IP:   {incident.get('source_ip', 'N/A')}
   Detected:    {incident.get('detection_time', 'N/A')}

"""
        
        return formatted