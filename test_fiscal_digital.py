#!/usr/bin/env python3
"""
Test del sistema Fiscal Digital
"""

import sys
sys.path.insert(0, 'src')

import os
from datetime import datetime
from legal.fiscal_digital import FiscalDigital


def test_incident_report():
    """Test de reporte de incidente"""
    print("=" * 70)
    print("TEST 1: INCIDENT REPORT GENERATION")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    incident_data = {
        'case_id': 'INC-2024-001',
        'severity': 'HIGH',
        'status': 'OPEN',
        'incident_type': 'SQL_INJECTION',
        'detection_time': datetime.now().isoformat(),
        'source_ip': '203.0.113.50',
        'target': '/api/users',
        'confidence': 0.95,
        'attack_vector': 'Web Application',
        'evidence_id': 'EVD-123456789ABC',
        'evidence_hash': 'a' * 64,
        'blockchain_hash': 'b' * 64,
        'evidence_count': 3,
        'classification': 'CONFIDENTIAL',
        'executive_summary': 'Critical SQL injection attack detected targeting user database.',
        'technical_analysis': 'Attack used malformed SQL queries with OR 1=1 patterns.',
        'impact_assessment': 'Potential data breach prevented. No data exfiltration detected.',
        'response_actions': 'IP blocked, WAF rules updated, evidence preserved.',
        'recommendations': 'Implement input validation, update WAF rules, security training.'
    }
    
    print("\n📋 Generando reporte de incidente...\n")
    
    filepath = fiscal.generate_incident_report(incident_data)
    
    print(f"   ✅ Documento generado:")
    print(f"      {filepath}")
    print(f"      Tamaño: {os.path.getsize(filepath)} bytes")
    
    print()


def test_evidence_report():
    """Test de reporte de evidencia"""
    print("=" * 70)
    print("TEST 2: EVIDENCE REPORT GENERATION")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    evidence_data = {
        'evidence_id': 'EVD-A1B2C3D4E5F6',
        'evidence_type': 'NETWORK_TRAFFIC',
        'classification': 'TOP_SECRET',
        'collected_by': 'NEMESIS_IA',
        'collection_time': datetime.now().isoformat(),
        'collection_method': 'Automated packet capture',
        'hash': 'f' * 64,
        'block_index': 42,
        'previous_hash': 'e' * 64,
        'custody_events': [
            {'index': 1, 'handler': 'NEMESIS_IA', 'timestamp': '2024-12-06T07:00:00', 'action': 'COLLECTED'},
            {'index': 2, 'handler': 'FORENSIC_ANALYST', 'timestamp': '2024-12-06T07:30:00', 'action': 'ANALYZED'},
            {'index': 3, 'handler': 'LEGAL_TEAM', 'timestamp': '2024-12-06T08:00:00', 'action': 'REVIEWED'}
        ],
        'current_handler': 'LEGAL_TEAM',
        'location': 'LEGAL_VAULT',
        'technical_details': 'Captured malicious payload with SQL injection patterns and evasion techniques.'
    }
    
    print("\n🔬 Generando reporte de evidencia...\n")
    
    filepath = fiscal.generate_evidence_report(evidence_data)
    
    print(f"   ✅ Documento generado:")
    print(f"      {filepath}")
    print(f"      Tamaño: {os.path.getsize(filepath)} bytes")
    
    print()


def test_legal_complaint():
    """Test de denuncia legal"""
    print("=" * 70)
    print("TEST 3: LEGAL COMPLAINT GENERATION")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    complaint_data = {
        'case_id': 'COMPLAINT-2024-001',
        'entity': 'TechCorp Industries',
        'incident_date': '2024-12-06',
        'incident_datetime': '2024-12-06 06:30:00 UTC',
        'incident_type': 'UNAUTHORIZED_ACCESS',
        'source_ip': '198.51.100.50',
        'target_systems': 'Production database servers',
        'damage_estimate': '$50,000 - Investigation and remediation costs',
        'evidence_count': 5,
        'evidence_ids': ['EVD-001', 'EVD-002', 'EVD-003', 'EVD-004', 'EVD-005'],
        'summary': 'Sophisticated cyber attack targeting our database infrastructure.',
        'requested_action': 'Full criminal investigation and prosecution of perpetrators.',
        'complainant_name': 'John Doe',
        'complainant_title': 'Chief Information Security Officer'
    }
    
    print("\n⚖️ Generando denuncia legal...\n")
    
    filepath = fiscal.generate_legal_complaint(complaint_data)
    
    print(f"   ✅ Documento generado:")
    print(f"      {filepath}")
    print(f"      Tamaño: {os.path.getsize(filepath)} bytes")
    
    print()


def test_custody_report():
    """Test de reporte de cadena de custodia"""
    print("=" * 70)
    print("TEST 4: CHAIN OF CUSTODY REPORT")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    custody_data = {
        'evidence_id': 'EVD-CUSTODY-TEST',
        'valid': True,
        'blockchain_valid': True,
        'current_handler': 'LEGAL_TEAM',
        'events': [
            {
                'timestamp': '2024-12-06T06:00:00',
                'action': 'COLLECTED',
                'handler': 'NEMESIS_IA',
                'hash_after': 'a' * 32
            },
            {
                'timestamp': '2024-12-06T06:30:00',
                'action': 'TRANSFERRED',
                'handler': 'FORENSIC_ANALYST',
                'hash_after': 'a' * 32
            },
            {
                'timestamp': '2024-12-06T07:00:00',
                'action': 'ANALYZED',
                'handler': 'FORENSIC_ANALYST',
                'hash_after': 'a' * 32
            },
            {
                'timestamp': '2024-12-06T07:30:00',
                'action': 'TRANSFERRED',
                'handler': 'LEGAL_TEAM',
                'hash_after': 'a' * 32
            }
        ]
    }
    
    print("\n🔗 Generando reporte de custody...\n")
    
    filepath = fiscal.generate_chain_of_custody_report(custody_data)
    
    print(f"   ✅ Documento generado:")
    print(f"      {filepath}")
    print(f"      Tamaño: {os.path.getsize(filepath)} bytes")
    
    print()


def test_complete_package():
    """Test de paquete legal completo"""
    print("=" * 70)
    print("TEST 5: COMPLETE LEGAL PACKAGE")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    # Datos completos
    incident_data = {
        'case_id': 'PKG-2024-001',
        'severity': 'CRITICAL',
        'incident_type': 'RANSOMWARE',
        'detection_time': datetime.now().isoformat(),
        'source_ip': '192.0.2.100',
        'target': 'File servers',
        'confidence': 0.99,
        'evidence_id': 'EVD-PKG-001',
        'evidence_hash': 'c' * 64,
        'classification': 'TOP_SECRET'
    }
    
    evidence_data = {
        'evidence_id': 'EVD-PKG-001',
        'evidence_type': 'MALWARE_SAMPLE',
        'classification': 'TOP_SECRET',
        'collected_by': 'NEMESIS_IA',
        'collection_time': datetime.now().isoformat(),
        'hash': 'd' * 64,
        'block_index': 100
    }
    
    custody_data = {
        'evidence_id': 'EVD-PKG-001',
        'valid': True,
        'events': [
            {'timestamp': '2024-12-06T06:00:00', 'action': 'COLLECTED', 'handler': 'NEMESIS_IA', 'hash_after': 'd' * 32}
        ]
    }
    
    print("\n📦 Generando paquete legal completo...\n")
    
    documents = fiscal.generate_complete_legal_package(
        incident_data,
        evidence_data,
        custody_data
    )
    
    print(f"   ✅ Paquete generado con {len(documents)} documentos:")
    for doc_type, filepath in documents.items():
        print(f"      • {doc_type}: {os.path.basename(filepath)}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 6: STATISTICS")
    print("=" * 70)
    
    fiscal = FiscalDigital(output_dir="test_legal_docs")
    
    # Generar varios documentos
    for i in range(3):
        incident = {'case_id': f'STAT-{i}', 'incident_type': 'TEST', 'confidence': 0.8}
        fiscal.generate_incident_report(incident)
    
    for i in range(2):
        evidence = {'evidence_id': f'EVD-STAT-{i}', 'evidence_type': 'TEST', 'hash': 'x' * 64}
        fiscal.generate_evidence_report(evidence)
    
    print("\n📊 Estadísticas:\n")
    print(fiscal.generate_summary_report())
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 19 + "FISCAL DIGITAL - TESTS" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_incident_report()
    print()
    
    test_evidence_report()
    print()
    
    test_legal_complaint()
    print()
    
    test_custody_report()
    print()
    
    test_complete_package()
    print()
    
    test_statistics()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("📄 CAPÍTULO 10 COMPLETADO:")
    print("   ✅ PDF Generator")
    print("   ✅ Document Templates")
    print("   ✅ Fiscal Digital System")
    print("   ✅ Incident Reports")
    print("   ✅ Evidence Reports")
    print("   ✅ Legal Complaints")
    print("   ✅ Chain of Custody Reports")
    print("   ✅ Complete Legal Packages")
    print()
    print("⚖️ DOCUMENTOS LEGALES: LISTOS PARA CORTE!")
    print()
    
    print("💡 Documentos generados en: test_legal_docs/")
    print("   Puedes abrirlos con cualquier lector de PDF")
    print()


if __name__ == "__main__":
    main()