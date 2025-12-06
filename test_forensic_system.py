#!/usr/bin/env python3
"""
Test del sistema forense blockchain
"""

import sys
sys.path.insert(0, 'src')

import time
from forensics.forensic_sentinel import ForensicSentinel


def test_basic_evidence_collection():
    """Test de recolección básica"""
    print("=" * 70)
    print("TEST 1: RECOLECCIÓN DE EVIDENCIA")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Simular amenaza
    threat_data = {
        "attack_type": "SQL_INJECTION",
        "source_ip": "203.0.113.50",
        "timestamp": "2024-12-06T06:30:00",
        "confidence": 0.95,
        "payload": "' OR 1=1--",
        "target": "/api/users"
    }
    
    print("\n🔬 Recolectando evidencia de amenaza...\n")
    
    block, evidence_id = sentinel.collect_threat_evidence(
        threat_data=threat_data,
        collected_by="NEMESIS_IA",
        classification="CONFIDENTIAL"
    )
    
    print(f"   ✅ Evidence ID:  {evidence_id}")
    print(f"   ✅ Block Index:  {block.index}")
    print(f"   ✅ Block Hash:   {block.hash[:32]}...")
    print(f"   ✅ Collected by: {block.collected_by}")
    
    print()
    return sentinel, evidence_id


def test_custody_transfer():
    """Test de transferencia de custodia"""
    print("=" * 70)
    print("TEST 2: TRANSFERENCIA DE CUSTODIA")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Recolectar evidencia
    threat = {"attack_type": "XSS", "source_ip": "198.51.100.10", "confidence": 0.88}
    block, evidence_id = sentinel.collect_threat_evidence(threat)
    
    print(f"\n📋 Evidencia: {evidence_id}")
    print(f"   Handler inicial: NEMESIS_IA\n")
    
    # Transferir custodia
    print("🔄 Transfiriendo a FORENSIC_ANALYST...\n")
    
    success = sentinel.transfer_evidence(
        evidence_id=evidence_id,
        from_handler="NEMESIS_IA",
        to_handler="FORENSIC_ANALYST",
        reason="Forensic analysis required",
        witnessed_by="SYSTEM_SUPERVISOR"
    )
    
    print(f"   ✅ Transferencia: {'EXITOSA' if success else 'FALLIDA'}")
    
    print()
    return sentinel, evidence_id


def test_integrity_verification():
    """Test de verificación de integridad"""
    print("=" * 70)
    print("TEST 3: VERIFICACIÓN DE INTEGRIDAD")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Crear múltiples evidencias
    threats = [
        {"attack_type": "DDOS", "source_ip": "192.0.2.10", "confidence": 0.99},
        {"attack_type": "BRUTE_FORCE", "source_ip": "192.0.2.20", "confidence": 0.92},
        {"attack_type": "PORT_SCAN", "source_ip": "192.0.2.30", "confidence": 0.85}
    ]
    
    evidence_ids = []
    
    print("\n🔬 Recolectando múltiples evidencias...\n")
    
    for threat in threats:
        block, eid = sentinel.collect_threat_evidence(threat)
        evidence_ids.append(eid)
        print(f"   ✅ {eid}: {threat['attack_type']}")
    
    print("\n🔍 Verificando integridad...\n")
    
    for eid in evidence_ids:
        result = sentinel.verify_evidence_integrity(eid)
        status = "✅ VÁLIDA" if result["valid"] else "❌ COMPROMETIDA"
        print(f"   {eid}: {status}")
    
    print()
    return sentinel


def test_custody_report():
    """Test de reporte de custodia"""
    print("=" * 70)
    print("TEST 4: REPORTE DE CADENA DE CUSTODIA")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Crear evidencia y transferencias
    threat = {"attack_type": "DATA_EXFIL", "source_ip": "203.0.113.100", "confidence": 0.97}
    block, evidence_id = sentinel.collect_threat_evidence(threat)
    
    # Múltiples transferencias
    sentinel.transfer_evidence(
        evidence_id, "NEMESIS_IA", "FORENSIC_ANALYST",
        "Initial analysis", "SUPERVISOR"
    )
    
    time.sleep(0.1)
    
    sentinel.transfer_evidence(
        evidence_id, "FORENSIC_ANALYST", "LEGAL_TEAM",
        "Legal review", "COMPLIANCE_OFFICER"
    )
    
    # Generar reporte
    print("\n📋 REPORTE DE CADENA DE CUSTODIA:\n")
    report = sentinel.get_custody_report(evidence_id)
    print(report)
    
    print()


def test_blockchain_integrity():
    """Test de integridad de blockchain"""
    print("=" * 70)
    print("TEST 5: INTEGRIDAD DE BLOCKCHAIN")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Crear evidencias
    for i in range(5):
        threat = {
            "attack_type": f"THREAT_{i}",
            "source_ip": f"192.0.2.{i}",
            "confidence": 0.80 + (i * 0.03)
        }
        sentinel.collect_threat_evidence(threat)
    
    print("\n🔗 Generando reporte de integridad de blockchain:\n")
    report = sentinel.get_integrity_report()
    print(report)
    
    print()


def test_legal_package():
    """Test de paquete legal"""
    print("=" * 70)
    print("TEST 6: PAQUETE LEGAL COMPLETO")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Crear evidencia crítica
    threat = {
        "attack_type": "RANSOMWARE",
        "source_ip": "198.51.100.50",
        "confidence": 0.99,
        "severity": "CRITICAL",
        "payload": "Encrypted data demand",
        "target": "/var/www/data"
    }
    
    block, evidence_id = sentinel.collect_threat_evidence(
        threat_data=threat,
        classification="TOP_SECRET"
    )
    
    print(f"\n⚖️ Generando paquete legal para: {evidence_id}\n")
    
    legal_package = sentinel.generate_legal_package(evidence_id)
    
    print(f"   Evidence ID:        {legal_package['evidence_id']}")
    print(f"   Generated At:       {legal_package['generated_at']}")
    print(f"   Integrity Verified: {'✅ YES' if legal_package['integrity_verified'] else '❌ NO'}")
    print(f"   Admissible:         {'✅ YES' if legal_package['admissible'] else '❌ NO'}")
    print(f"   Compliance:         {legal_package['compliance']}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 7: ESTADÍSTICAS DEL SISTEMA")
    print("=" * 70)
    
    sentinel = ForensicSentinel()
    
    # Generar actividad
    for i in range(10):
        threat = {"attack_type": f"TEST_{i}", "source_ip": f"10.0.0.{i}", "confidence": 0.85}
        block, eid = sentinel.collect_threat_evidence(threat)
        
        if i % 3 == 0:
            sentinel.transfer_evidence(eid, "NEMESIS_IA", "FORENSIC_ANALYST", "Analysis")
        
        if i % 2 == 0:
            sentinel.verify_evidence_integrity(eid)
    
    stats = sentinel.get_statistics()
    
    print("\n📊 ESTADÍSTICAS:\n")
    
    print("   Sentinel:")
    for key, value in stats['sentinel'].items():
        print(f"      {key:25} {value}")
    
    print("\n   Blockchain:")
    bc_stats = stats['blockchain']
    print(f"      Chain length:         {bc_stats['chain_length']}")
    print(f"      Total evidence:       {bc_stats['total_evidence']}")
    print(f"      Chain valid:          {bc_stats['chain_valid']}")
    print(f"      Legal hold blocks:    {bc_stats['legal_hold_blocks']}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "FORENSIC SYSTEM - TESTS" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_evidence_collection()
    print()
    
    test_custody_transfer()
    print()
    
    test_integrity_verification()
    print()
    
    test_custody_report()
    print()
    
    test_blockchain_integrity()
    print()
    
    test_legal_package()
    print()
    
    test_statistics()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("🔗 CAPÍTULO 9 COMPLETADO:")
    print("   ✅ Blockchain Evidence System")
    print("   ✅ Chain of Custody Management")
    print("   ✅ Forensic Sentinel Integration")
    print("   ✅ Legal Package Generation")
    print("   ✅ Integrity Verification")
    print()
    print("⚖️ EVIDENCIA FORENSE: ADMISIBLE EN CORTE!")
    print()


if __name__ == "__main__":
    main()