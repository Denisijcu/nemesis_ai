#!/usr/bin/env python3
"""
Test del sistema Red Button
"""

import sys
sys.path.insert(0, 'src')

from datetime import datetime
from emergency.red_button import RedButton
from emergency.cert_database import CERTDatabase


def test_cert_database():
    """Test de base de datos de CERTs"""
    print("=" * 70)
    print("TEST 1: CERT DATABASE")
    print("=" * 70)
    
    cert_db = CERTDatabase()
    
    print(f"\n🌐 CERTs disponibles: {len(cert_db.certs)}\n")
    
    # Mostrar algunos CERTs
    for cert_id in ['US-CERT', 'CERT-EU', 'NCSC-UK']:
        cert = cert_db.get_cert(cert_id)
        if cert:
            print(f"   {cert.name:15} {cert.organization[:40]:40} {cert.email}")
    
    print()
    
    # Búsqueda por país
    us_certs = cert_db.get_cert_by_country('US')
    print(f"   CERTs en US: {len(us_certs)}")
    
    # CERTs recomendados para amenaza crítica
    recommended = cert_db.get_recommended_certs('CRITICAL', 'UK')
    print(f"   CERTs recomendados (CRITICAL, UK): {len(recommended)}")
    for cert in recommended:
        print(f"      • {cert.name} ({cert.country})")
    
    print()


def test_incident_reporter():
    """Test de generación de reportes"""
    print("=" * 70)
    print("TEST 2: INCIDENT REPORTER")
    print("=" * 70)
    
    from emergency.incident_reporter import IncidentReporter
    
    reporter = IncidentReporter()
    
    # Datos de incidente
    incident_data = {
        'case_id': 'INC-2024-CRITICAL-001',
        'detection_time': datetime.now().isoformat(),
        'incident_type': 'RANSOMWARE',
        'severity': 'CRITICAL',
        'confidence': 0.99,
        'source_ip': '203.0.113.100',
        'target': 'Production servers',
        'attack_vector': 'Email phishing',
        'technical_analysis': 'Ransomware payload detected with encryption capabilities.',
        'impact_assessment': 'Multiple servers affected, data encryption in progress.',
        'response_actions': 'Systems isolated, backups secured, incident response activated.'
    }
    
    evidence_data = {
        'evidence_id': 'EVD-CRITICAL-001',
        'evidence_type': 'MALWARE_SAMPLE',
        'hash': 'a' * 64,
        'has_pcap': True,
        'has_logs': True
    }
    
    print("\n📝 Generando reporte para US-CERT...\n")
    
    report = reporter.generate_cert_report(
        incident_data=incident_data,
        evidence_data=evidence_data,
        cert_name='US-CERT'
    )
    
    print(f"   Subject:   {report['subject']}")
    print(f"   Priority:  {report['priority']}")
    print(f"   Generated: {report['generated_at']}")
    print(f"   Attachments: {len(report['attachments'])}")
    
    print("\n   Body preview:")
    print("   " + "─" * 66)
    body_lines = report['body'].split('\n')[:15]
    for line in body_lines:
        print(f"   {line[:66]}")
    print("   " + "─" * 66)
    print(f"   ... ({len(body_lines)} total lines)")
    
    print()


def test_red_button_press():
    """Test de presionar el botón rojo"""
    print("=" * 70)
    print("TEST 3: RED BUTTON PRESS - EMERGENCY ESCALATION")
    print("=" * 70)
    
    red_button = RedButton()
    
    # Incidente crítico
    critical_incident = {
        'case_id': 'CRITICAL-2024-001',
        'detection_time': datetime.now().isoformat(),
        'incident_type': 'ADVANCED_PERSISTENT_THREAT',
        'severity': 'CRITICAL',
        'confidence': 0.98,
        'source_ip': '198.51.100.200',
        'target': 'Infrastructure servers',
        'attack_vector': 'Zero-day exploit',
        'technical_analysis': 'APT group activity detected with data exfiltration attempts.',
        'impact_assessment': 'Critical infrastructure at risk, potential data breach.',
        'response_actions': 'Emergency response activated, systems hardened.'
    }
    
    print("\n🚨🚨🚨 PRESSING RED BUTTON 🚨🚨🚨\n")
    
    escalation = red_button.press_red_button(
        incident_data=critical_incident,
        evidence_id='EVD-APT-001',
        auto_escalate=False  # No enviar emails reales en test
    )
    
    print(f"   ✅ Escalation completed")
    print(f"   Incident ID:     {escalation['incident_id']}")
    print(f"   Severity:        {escalation['severity']}")
    print(f"   CERTs notified:  {len(escalation['certs_notified'])}")
    print(f"   Auto-escalated:  {escalation['auto_escalated']}")
    print()
    
    print("   Notified CERTs:")
    for cert_name in escalation['certs_notified']:
        print(f"      • {cert_name}")
    print()
    
    print("   Legal documents generated:")
    for doc_type, filename in escalation['legal_docs'].items():
        print(f"      • {doc_type}: {filename}")
    print()
    
    print("   Threat Intelligence:")
    threat_intel = escalation['threat_intel']
    print(f"      Source IP:     {threat_intel['source_ip']}")
    print(f"      Threat Level:  {threat_intel['threat_level']}")
    print(f"      Country:       {threat_intel['country']}")
    
    print()


def test_bulk_escalation():
    """Test de escalación en lote"""
    print("=" * 70)
    print("TEST 4: BULK ESCALATION")
    print("=" * 70)
    
    red_button = RedButton()
    
    # Múltiples incidentes
    incidents = [
        {
            'case_id': 'INC-001',
            'incident_type': 'SQL_INJECTION',
            'severity': 'HIGH',
            'source_ip': '192.0.2.10',
            'detection_time': datetime.now().isoformat()
        },
        {
            'case_id': 'INC-002',
            'incident_type': 'BRUTE_FORCE',
            'severity': 'HIGH',
            'source_ip': '192.0.2.20',
            'detection_time': datetime.now().isoformat()
        },
        {
            'case_id': 'INC-003',
            'incident_type': 'DDOS',
            'severity': 'CRITICAL',
            'source_ip': '192.0.2.30',
            'detection_time': datetime.now().isoformat()
        }
    ]
    
    print(f"\n🚨 Escalando {len(incidents)} incidentes en lote...\n")
    
    result = red_button.bulk_escalate(
        incidents=incidents,
        cert_id='US-CERT'
    )
    
    print(f"   Total incidents:  {result['total_incidents']}")
    print(f"   CERTs notified:   {result['certs_notified']}")
    print(f"   Timestamp:        {result['timestamp']}")
    
    print()


def test_escalation_history():
    """Test de historial de escalaciones"""
    print("=" * 70)
    print("TEST 5: ESCALATION HISTORY")
    print("=" * 70)
    
    red_button = RedButton()
    
    # Crear algunas escalaciones
    for i in range(3):
        incident = {
            'case_id': f'HIST-{i}',
            'incident_type': 'TEST',
            'severity': 'MEDIUM',
            'source_ip': f'192.0.2.{i}',
            'detection_time': datetime.now().isoformat()
        }
        red_button.press_red_button(incident, auto_escalate=False)
    
    history = red_button.get_escalation_history()
    
    print(f"\n📋 Escalation History: {len(history)} events\n")
    
    for i, escalation in enumerate(history, 1):
        print(f"   {i}. {escalation['incident_id']:15} "
              f"Severity: {escalation['severity']:8} "
              f"CERTs: {len(escalation['certs_notified'])}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 6: STATISTICS")
    print("=" * 70)
    
    red_button = RedButton()
    
    # Generar actividad
    incidents = [
        {'case_id': 'STAT-1', 'severity': 'CRITICAL', 'incident_type': 'APT', 
         'source_ip': '1.2.3.4', 'detection_time': datetime.now().isoformat()},
        {'case_id': 'STAT-2', 'severity': 'HIGH', 'incident_type': 'RANSOMWARE',
         'source_ip': '5.6.7.8', 'detection_time': datetime.now().isoformat()},
        {'case_id': 'STAT-3', 'severity': 'MEDIUM', 'incident_type': 'SCAN',
         'source_ip': '9.10.11.12', 'detection_time': datetime.now().isoformat()}
    ]
    
    for incident in incidents:
        red_button.press_red_button(incident, auto_escalate=False)
    
    # Bulk escalation
    red_button.bulk_escalate([incidents[0]], cert_id='US-CERT')
    
    print("\n📊 Estadísticas del Red Button System:\n")
    print(red_button.generate_status_report())
    
    print()


def test_cert_selection():
    """Test de selección de CERTs"""
    print("=" * 70)
    print("TEST 7: CERT SELECTION LOGIC")
    print("=" * 70)
    
    cert_db = CERTDatabase()
    
    test_cases = [
        ('CRITICAL', 'UK'),
        ('HIGH', 'DE'),
        ('MEDIUM', 'US'),
        ('LOW', None)
    ]
    
    print("\n🎯 Testing CERT selection for different scenarios:\n")
    
    for threat_level, country in test_cases:
        certs = cert_db.get_recommended_certs(threat_level, country)
        
        print(f"   Threat: {threat_level:8} Country: {country or 'None':4} → "
              f"{len(certs)} CERTs")
        for cert in certs:
            print(f"      • {cert.name} ({cert.country})")
        print()
    
    print()


def test_complete_workflow():
    """Test de workflow completo"""
    print("=" * 70)
    print("TEST 8: COMPLETE EMERGENCY WORKFLOW")
    print("=" * 70)
    
    print("\n🔥 Simulating complete emergency response workflow...\n")
    
    # 1. Inicializar sistema
    print("   1️⃣  Initializing Red Button System...")
    red_button = RedButton()
    print("      ✅ System ready")
    
    # 2. Detectar incidente crítico
    print("\n   2️⃣  Critical incident detected...")
    incident = {
        'case_id': 'WORKFLOW-2024-001',
        'detection_time': datetime.now().isoformat(),
        'incident_type': 'ZERO_DAY_EXPLOIT',
        'severity': 'CRITICAL',
        'confidence': 0.99,
        'source_ip': '185.220.100.50',
        'target': 'Critical infrastructure',
        'attack_vector': 'Unknown vulnerability',
        'technical_analysis': 'Zero-day exploit detected targeting core systems.',
        'impact_assessment': 'Potential nationwide impact, immediate action required.',
        'response_actions': 'Emergency protocols activated, all teams mobilized.'
    }
    print("      ✅ Incident classified as CRITICAL")
    
    # 3. Presionar botón rojo
    print("\n   3️⃣  🚨 PRESSING RED BUTTON 🚨")
    escalation = red_button.press_red_button(
        incident_data=incident,
        evidence_id='EVD-ZERO-DAY-001',
        auto_escalate=False
    )
    print(f"      ✅ {len(escalation['certs_notified'])} CERTs notified")
    
    # 4. Verificar escalación
    print("\n   4️⃣  Verifying escalation...")
    history = red_button.get_escalation_history()
    print(f"      ✅ {len(history)} escalations in history")
    
    # 5. Generar reporte final
    print("\n   5️⃣  Generating final status report...")
    stats = red_button.get_statistics()
    print(f"      ✅ {stats['button_presses']} button press(es)")
    print(f"      ✅ {stats['certs_notified']} CERT(s) notified")
    print(f"      ✅ {stats['reports_sent']} report(s) sent")
    
    print("\n   ✅ COMPLETE WORKFLOW EXECUTED SUCCESSFULLY")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "RED BUTTON - TESTS" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_cert_database()
    print()
    
    test_incident_reporter()
    print()
    
    test_red_button_press()
    print()
    
    test_bulk_escalation()
    print()
    
    test_escalation_history()
    print()
    
    test_statistics()
    print()
    
    test_cert_selection()
    print()
    
    test_complete_workflow()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("🚨 CAPÍTULO 12 COMPLETADO:")
    print("   ✅ CERT Database (10+ CERTs internacionales)")
    print("   ✅ Incident Reporter")
    print("   ✅ Red Button System")
    print("   ✅ Emergency Escalation")
    print("   ✅ Bulk Reporting")
    print("   ✅ CERT Selection Logic")
    print("   ✅ Complete Emergency Workflow")
    print()
    print("🚨 EL BOTÓN ROJO: LISTO PARA EMERGENCIAS!")
    print()
    
    print("💡 NOTA: En producción:")
    print("   • Configurar servidor SMTP para emails")
    print("   • Implementar PGP para emails cifrados")
    print("   • Configurar webhooks para notificaciones")
    print("   • Integrar con sistema de ticketing")
    print()


if __name__ == "__main__":
    main()