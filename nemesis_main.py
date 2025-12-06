#!/usr/bin/env python3
"""
Némesis IA - Sistema Principal Unificado
Integración completa de todos los módulos
"""

import logging
import sys
import os
from datetime import datetime
from typing import Dict, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class NemesisIA:
    """Sistema Principal Unificado de Némesis IA"""
    
    def __init__(
        self,
        abuseipdb_api_key: Optional[str] = None,
        enable_forensics: bool = True,
        enable_legal: bool = True,
        enable_emergency: bool = True
    ):
        """Inicializa Némesis IA completo"""
        
        logger.info("="*70)
        logger.info("🚀 NÉMESIS IA - SISTEMA PRINCIPAL INICIANDO")
        logger.info("="*70)
        
        # Importar módulos dinámicamente
        try:
            # MÓDULO 1: DETECCIÓN
            logger.info("📡 Módulos de detección...")
            from agent.nemesis_agent import NemesisAgent
            from ml.ml_brain import MLBrain
            self.nemesis_agent = NemesisAgent()
            self.ml_brain = MLBrain()
            logger.info("   ✅ Agente Némesis + ML Brain")
            
        except Exception as e:
            logger.warning(f"   ⚠️ Detección: {e}")
            self.nemesis_agent = None
            self.ml_brain = None
        
        try:
            # MÓDULO 2: RESPUESTA
            logger.info("⚡ Sistema de respuesta...")
            from response.auto_response import ResponseSentinel
            self.response_sentinel = ResponseSentinel(
                threat_database=self.nemesis_agent.threat_db if self.nemesis_agent else None
            )
            logger.info("   ✅ Response Sentinel")
        except Exception as e:
            logger.warning(f"   ⚠️ Respuesta: {e}")
            self.response_sentinel = None
        
        # MÓDULO 3: FORENSE
        self.forensic_sentinel = None
        if enable_forensics:
            try:
                logger.info("🔗 Sistema forense (Blockchain)...")
                from forensics.forensic_sentinel import ForensicSentinel
                self.forensic_sentinel = ForensicSentinel(
                    threat_database=self.nemesis_agent.threat_db if self.nemesis_agent else None
                )
                logger.info("   ✅ Forensic Sentinel (Blockchain)")
            except Exception as e:
                logger.warning(f"   ⚠️ Forense: {e}")
        
        # MÓDULO 4: LEGAL
        self.fiscal_digital = None
        if enable_legal:
            try:
                logger.info("📄 Sistema legal (PDFs)...")
                from legal.fiscal_digital import FiscalDigital
                self.fiscal_digital = FiscalDigital(output_dir="legal_documents")
                logger.info("   ✅ Fiscal Digital")
            except Exception as e:
                logger.warning(f"   ⚠️ Legal: {e}")
        
        # MÓDULO 5: INTELIGENCIA
        self.law_enforcement = None
        try:
            logger.info("🌐 Threat intelligence...")
            from intel.law_enforcement_connector import LawEnforcementConnector
            self.law_enforcement = LawEnforcementConnector(abuseipdb_api_key)
            logger.info("   ✅ Law Enforcement Connector")
        except Exception as e:
            logger.warning(f"   ⚠️ Intelligence: {e}")
        
        # MÓDULO 6: EMERGENCIA
        self.red_button = None
        if enable_emergency:
            try:
                logger.info("🚨 Red Button System...")
                from emergency.red_button import RedButton
                self.red_button = RedButton(
                    forensic_sentinel=self.forensic_sentinel,
                    fiscal_digital=self.fiscal_digital,
                    law_enforcement=self.law_enforcement
                )
                logger.info("   ✅ Red Button")
            except Exception as e:
                logger.warning(f"   ⚠️ Emergency: {e}")
        
        # MÓDULO 7: QUANTUM (opcional)
        self.quantum_sentinel = None
        try:
            logger.info("⚛️ Quantum Defense...")
            from quantum.quantum_sentinel import QuantumSentinel
            self.quantum_sentinel = QuantumSentinel()
            self.quantum_sentinel.initialize_system()
            logger.info("   ✅ Quantum Sentinel")
        except Exception as e:
            logger.warning(f"   ⚠️ Quantum: {e}")
        
        # Estado del sistema
        self.system_stats = {
            "started_at": datetime.now().isoformat(),
            "threats_detected": 0,
            "threats_blocked": 0,
            "evidence_collected": 0,
            "reports_generated": 0,
            "certs_notified": 0
        }
        
        logger.info("="*70)
        logger.info("✅ NÉMESIS IA - SISTEMA OPERACIONAL")
        logger.info("="*70)
    
    def detect_threat(self, packet_data: Dict) -> Dict:
        """
        Detecta amenaza usando ML Brain
        
        Args:
            packet_data: Datos del paquete
            
        Returns:
            Predicción de amenaza
        """
        
        if not self.ml_brain:
            return {'is_threat': False, 'error': 'ML Brain no disponible'}
        
        try:
            prediction = self.ml_brain.predict(packet_data)
            
            if prediction.get('is_threat'):
                self.system_stats['threats_detected'] += 1
                logger.warning(
                    f"⚠️ AMENAZA: {prediction.get('attack_type')} "
                    f"({prediction.get('confidence', 0)*100:.1f}%)"
                )
            
            return prediction
        
        except Exception as e:
            logger.error(f"Error en detección: {e}")
            return {'is_threat': False, 'error': str(e)}
    
    def process_incident_complete(
        self,
        incident_data: Dict,
        auto_escalate: bool = False
    ) -> Dict:
        """
        Procesamiento COMPLETO de incidente:
        Detección → Evidencia → Legal → Intel → CERT
        """
        
        logger.info("="*70)
        logger.info("🔥 PROCESAMIENTO COMPLETO DE INCIDENTE")
        logger.info("="*70)
        
        result = {
            'incident_id': incident_data.get('case_id', 'UNKNOWN'),
            'timestamp': datetime.now().isoformat(),
            'stages_completed': []
        }
        
        # STAGE 1: Evidencia forense
        if self.forensic_sentinel:
            try:
                logger.info("🔗 Stage 1: Blockchain evidence...")
                block, evidence_id = self.forensic_sentinel.collect_threat_evidence(
                    threat_data=incident_data
                )
                result['evidence'] = {
                    'evidence_id': evidence_id,
                    'blockchain_block': block.index,
                    'hash': block.hash
                }
                result['stages_completed'].append('FORENSICS')
                self.system_stats['evidence_collected'] += 1
                logger.info(f"   ✅ Evidence: {evidence_id}")
            except Exception as e:
                logger.error(f"   ❌ Forensics error: {e}")
        
        # STAGE 2: Threat Intelligence
        if self.law_enforcement and incident_data.get('source_ip'):
            try:
                logger.info("🌐 Stage 2: Threat intel...")
                intel = self.law_enforcement.comprehensive_ip_check(
                    incident_data['source_ip']
                )
                result['threat_intelligence'] = {
                    'threat_score': intel.get('threat_score', 0),
                    'threat_level': intel.get('threat_level', 'UNKNOWN')
                }
                result['stages_completed'].append('INTELLIGENCE')
                logger.info(f"   ✅ Threat score: {intel.get('threat_score', 0)}")
            except Exception as e:
                logger.error(f"   ❌ Intel error: {e}")
        
        # STAGE 3: Documentos legales
        if self.fiscal_digital:
            try:
                logger.info("📄 Stage 3: Legal docs...")
                incident_report = self.fiscal_digital.generate_incident_report(
                    incident_data
                )
                result['legal_documents'] = {
                    'incident_report': incident_report
                }
                result['stages_completed'].append('LEGAL')
                self.system_stats['reports_generated'] += 1
                logger.info(f"   ✅ PDF: {os.path.basename(incident_report)}")
            except Exception as e:
                logger.error(f"   ❌ Legal error: {e}")
        
        # STAGE 4: Escalación CERT
        if self.red_button and (
            auto_escalate or 
            incident_data.get('severity') == 'CRITICAL'
        ):
            try:
                logger.info("🚨 Stage 4: CERT escalation...")
                escalation = self.red_button.press_red_button(
                    incident_data=incident_data,
                    evidence_id=result.get('evidence', {}).get('evidence_id'),
                    auto_escalate=False  # No enviar emails en demo
                )
                result['emergency_response'] = {
                    'escalated': True,
                    'certs_notified': len(escalation.get('certs_notified', [])),
                    'cert_list': escalation.get('certs_notified', [])
                }
                result['stages_completed'].append('EMERGENCY')
                self.system_stats['certs_notified'] += len(escalation.get('certs_notified', []))
                logger.info(f"   ✅ CERTs: {len(escalation.get('certs_notified', []))}")
            except Exception as e:
                logger.error(f"   ❌ Emergency error: {e}")
        
        logger.info("="*70)
        logger.info(f"✅ STAGES COMPLETED: {len(result['stages_completed'])}/4")
        logger.info("="*70)
        
        return result
    
    def get_system_status(self) -> Dict:
        """Estado completo del sistema"""
        
        return {
            'system': {
                'name': 'NÉMESIS IA',
                'version': '1.0.0',
                'status': 'OPERATIONAL',
                'started_at': self.system_stats['started_at']
            },
            'statistics': self.system_stats.copy(),
            'modules': {
                'ml_brain': self.ml_brain is not None,
                'forensics': self.forensic_sentinel is not None,
                'legal': self.fiscal_digital is not None,
                'intelligence': self.law_enforcement is not None,
                'emergency': self.red_button is not None,
                'quantum': self.quantum_sentinel is not None
            }
        }
    
    def generate_system_report(self) -> str:
        """Reporte completo del sistema"""
        
        status = self.get_system_status()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  NÉMESIS IA - SYSTEM REPORT                      ║
╚══════════════════════════════════════════════════════════════════╝

🚀 STATUS: {status['system']['status']}

📊 STATISTICS:

   Threats Detected:      {status['statistics']['threats_detected']}
   Threats Blocked:       {status['statistics']['threats_blocked']}
   Evidence Collected:    {status['statistics']['evidence_collected']}
   Reports Generated:     {status['statistics']['reports_generated']}
   CERTs Notified:        {status['statistics']['certs_notified']}

🔧 MODULES:

   ML Brain:              {'✅' if status['modules']['ml_brain'] else '❌'}
   Blockchain Forensics:  {'✅' if status['modules']['forensics'] else '❌'}
   Legal PDFs:            {'✅' if status['modules']['legal'] else '❌'}
   Threat Intel:          {'✅' if status['modules']['intelligence'] else '❌'}
   Red Button:            {'✅' if status['modules']['emergency'] else '❌'}
   Quantum Defense:       {'✅' if status['modules']['quantum'] else '❌'}

⚡ Online since: {status['system']['started_at']}

═══════════════════════════════════════════════════════════════════
"""
        
        return report


def main():
    """Demo de sistema unificado"""
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "NÉMESIS IA - SISTEMA UNIFICADO" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Inicializar
    nemesis = NemesisIA(
        enable_forensics=True,
        enable_legal=True,
        enable_emergency=True
    )
    
    print()
    print(nemesis.generate_system_report())
    
    # Demo: Incidente crítico
    print("\n" + "="*70)
    print("🔥 DEMO: PROCESAMIENTO COMPLETO DE INCIDENTE")
    print("="*70 + "\n")
    
    critical_incident = {
        'case_id': 'DEMO-CRITICAL-001',
        'detection_time': datetime.now().isoformat(),
        'incident_type': 'RANSOMWARE',
        'severity': 'CRITICAL',
        'confidence': 0.99,
        'source_ip': '203.0.113.100',
        'target': 'Production servers',
        'attack_vector': 'Email phishing',
        'technical_analysis': 'Ransomware detected.',
        'impact_assessment': 'Critical systems at risk.',
        'response_actions': 'Systems isolated.'
    }
    
    result = nemesis.process_incident_complete(
        incident_data=critical_incident,
        auto_escalate=False
    )
    
    print("\n📋 RESULTADO:\n")
    print(f"   Incident ID:  {result['incident_id']}")
    print(f"   Stages:       {len(result['stages_completed'])}/4")
    for stage in result['stages_completed']:
        print(f"      ✅ {stage}")
    
    if result.get('evidence'):
        print(f"\n   Evidence:     {result['evidence']['evidence_id']}")
        print(f"   Blockchain:   Block #{result['evidence']['blockchain_block']}")
    
    if result.get('emergency_response'):
        print(f"\n   CERTs:        {result['emergency_response']['certs_notified']} notified")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETADO - SISTEMA UNIFICADO FUNCIONAL")
    print("="*70)
    print()
    
    print(nemesis.generate_system_report())


if __name__ == "__main__":
    main()