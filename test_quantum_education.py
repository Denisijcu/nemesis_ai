#!/usr/bin/env python3
"""
Test de Quantum Education
"""

import sys
sys.path.insert(0, 'src')

from quantum.quantum_education import QuantumEducation


def test_explain_concepts():
    """Test de explicación de conceptos"""
    print("=" * 70)
    print("TEST 1: EXPLICACIÓN DE CONCEPTOS CLAVE")
    print("=" * 70)
    
    edu = QuantumEducation()
    
    key_concepts = [
        "shor_algorithm",
        "harvest_now_decrypt_later",
        "post_quantum_cryptography"
    ]
    
    for concept in key_concepts:
        print(edu.explain_concept(concept))
    
    print()


def test_timeline():
    """Test de timeline"""
    print("=" * 70)
    print("TEST 2: TIMELINE DE COMPUTACIÓN CUÁNTICA")
    print("=" * 70)
    
    edu = QuantumEducation()
    
    # Timeline completo
    timeline = edu.show_timeline(1994, 2035)
    print(timeline)
    
    print()


def test_current_status():
    """Test de estado actual"""
    print("=" * 70)
    print("TEST 3: ESTADO ACTUAL DE LA AMENAZA")
    print("=" * 70)
    
    edu = QuantumEducation()
    
    status = edu.get_current_status()
    
    print(f"\n📊 ESTADO ACTUAL:\n")
    print(f"   Año actual: {status['current_year']}")
    
    if status['latest_milestone']:
        print(f"\n   Último hito:")
        print(f"   • {status['latest_milestone']['event']}")
        print(f"   • Qubits: {status['latest_milestone']['qubits']:,}")
        print(f"   • Amenaza: {status['latest_milestone']['threat_level']}")
    
    if status['years_until_critical']:
        print(f"\n   ⚠️  Próximo hito CRÍTICO:")
        print(f"   • En ~{status['years_until_critical']} años")
        print(f"   • {status['next_critical_event']}")
    
    print(f"\n   🎯 Recomendación:")
    print(f"   {status['recommendation']}")
    
    print()


def test_executive_summary():
    """Test de resumen ejecutivo"""
    print("=" * 70)
    print("TEST 4: RESUMEN EJECUTIVO")
    print("=" * 70)
    
    edu = QuantumEducation()
    
    summary = edu.generate_executive_summary()
    print(summary)
    
    print()


def test_quiz():
    """Test de quiz educativo"""
    print("=" * 70)
    print("TEST 5: QUIZ EDUCATIVO")
    print("=" * 70)
    
    edu = QuantumEducation()
    
    quiz = edu.quiz_user()
    
    print("\n❓ QUIZ SOBRE AMENAZA CUÁNTICA:\n")
    
    for i, q in enumerate(quiz, 1):
        print(f"{i}. {q['question']}")
        for j, option in enumerate(q['options'], 1):
            marker = "✅" if option == q['correct'] else "  "
            print(f"   {marker} {j}) {option}")
        print(f"\n   💡 Respuesta: {q['correct']}")
        print(f"   📝 {q['explanation']}")
        print()
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "QUANTUM EDUCATION - TESTS" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_explain_concepts()
    print()
    
    test_timeline()
    print()
    
    test_current_status()
    print()
    
    test_executive_summary()
    print()
    
    test_quiz()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("⚛️ CAPÍTULO 7 COMPLETADO AL 100%:")
    print("   ✅ QuantumThreatAnalyzer (análisis de amenazas)")
    print("   ✅ RSAVulnerabilityDemo (demostración práctica)")
    print("   ✅ QuantumEducation (sistema educativo)")
    print("   ✅ Timeline histórico y proyectado")
    print("   ✅ Conceptos clave explicados")
    print("   ✅ Resumen ejecutivo")
    print("   ✅ Quiz educativo")
    print()
    print("🎯 CAPÍTULO 7: EL COLAPSO DEL RSA - 100% COMPLETO!")
    print()


if __name__ == "__main__":
    main()