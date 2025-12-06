#!/usr/bin/env python3
"""DEMO COMPLETO - Todo el flujo"""

from nemesis_main import NemesisIA
from datetime import datetime

print("="*70)
print("🔥 DÉMESIS IA - DEMO COMPLETO END-TO-END")
print("="*70)

# 1. Inicializar sistema
print("\n1️⃣ Inicializando sistema completo...")
nemesis = NemesisIA()

# 2. Simular detección
print("\n2️⃣ Detectando amenaza con ML...")
threat = {
    'case_id': 'DEMO-001',
    'incident_type': 'RANSOMWARE',
    'severity': 'CRITICAL',
    'confidence': 0.99,
    'source_ip': '203.0.113.50',
    'detection_time': datetime.now().isoformat(),
    'target': 'Production',
    'technical_analysis': 'Ransomware detected',
    'impact_assessment': 'Critical',
    'response_actions': 'Isolated'
}

# 3. Procesar incidente completo
print("\n3️⃣ Pipeline completo: Forensics → Legal → Intel → CERT...")
result = nemesis.process_incident_complete(threat)

# 4. Resultado
print("\n" + "="*70)
print("✅ RESULTADO:")
print(f"   Stages: {result['stages_completed']}")
print(f"   Evidence: {result.get('evidence', {}).get('evidence_id', 'N/A')}")
print(f"   CERTs: {result.get('emergency_response', {}).get('certs_notified', 0)}")
print("="*70)

print("\n✅ DEMO COMPLETADO - Sistema funcionando end-to-end!")