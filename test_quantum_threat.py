#!/usr/bin/env python3
"""
Test del Quantum Threat Analyzer
"""

import sys
sys.path.insert(0, 'src')

from quantum.quantum_threat_analyzer import QuantumThreatAnalyzer


def test_basic_analysis():
    """Test de análisis básico"""
    print("=" * 70)
    print("TEST 1: ANÁLISIS DE ALGORITMOS COMUNES")
    print("=" * 70)
    
    analyzer = QuantumThreatAnalyzer()
    
    test_algos = [
        ("RSA", 2048),
        ("RSA", 4096),
        ("ECC", 256),
        ("AES", 256),
    ]
    
    print("\n⚛️ Analizando vulnerabilidad cuántica...\n")
    
    for algo, key_size in test_algos:
        threat = analyzer.analyze_algorithm(algo, key_size)
        
        risk_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(threat.risk_level, "⚪")
        
        print(f"{risk_emoji} {threat.algorithm}")
        print(f"   Seguro ahora:        {'✅ SÍ' if threat.currently_secure else '❌ NO'}")
        print(f"   Vulnerable en:       ~{threat.years_until_vulnerable} años")
        print(f"   Ataque cuántico:     {threat.quantum_attack}")
        print(f"   Nivel de riesgo:     {threat.risk_level}")
        print(f"   Recomendación:       {threat.recommendation}")
        print()
    
    print()


def test_threat_report():
    """Test de reporte completo"""
    print("=" * 70)
    print("TEST 2: REPORTE COMPLETO DE AMENAZAS")
    print("=" * 70)
    
    analyzer = QuantumThreatAnalyzer()
    
    report = analyzer.generate_threat_report()
    
    print(f"\n📊 REPORTE DE AMENAZAS CUÁNTICAS")
    print(f"   Timestamp: {report['timestamp']}")
    print()
    
    print(f"   📈 Estadísticas:")
    print(f"      Algoritmos analizados:       {report['total_algorithms_analyzed']}")
    print(f"      Actualmente seguros:         {report['currently_safe']}")
    print(f"      Vulnerables en <10 años:     {report['vulnerable_within_10_years']}")
    print()
    
    print(f"   🎯 Por Nivel de Riesgo:")
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        threats = report['threats_by_risk'][level]
        if threats:
            print(f"\n      {level}: {len(threats)} algoritmos")
            for t in threats:
                print(f"         • {t['algorithm']}: {t['years_until_vulnerable']} años")
    
    print(f"\n   📋 Resumen:")
    print(f"      {report['summary']}")
    
    print()


def test_timeline():
    """Test de timeline cuántico"""
    print("=" * 70)
    print("TEST 3: TIMELINE DE COMPUTACIÓN CUÁNTICA")
    print("=" * 70)
    
    analyzer = QuantumThreatAnalyzer()
    
    print("\n⏰ Timeline Estimado:\n")
    
    for year, specs in sorted(analyzer.quantum_timeline.items()):
        print(f"   {year}:")
        print(f"      Qubits:      {specs['qubits']:,}")
        print(f"      Error rate:  {specs['error_rate']}")
        print()
    
    # Mostrar qué se puede romper cada año
    print("   🔓 Capacidades de Romper Algoritmos:\n")
    
    for year, specs in sorted(analyzer.quantum_timeline.items()):
        qubits = specs['qubits']
        print(f"   {year} ({qubits:,} qubits):")
        
        breakable = []
        for algo, required in analyzer.breaking_requirements.items():
            if required <= qubits:
                breakable.append(algo)
        
        if breakable:
            for algo in breakable:
                print(f"      ❌ Puede romper: {algo}")
        else:
            print(f"      ✅ Ningún algoritmo rompible aún")
        
        print()
    
    print()


def test_data_lifetime_risk():
    """Test de riesgo por tiempo de vida de datos"""
    print("=" * 70)
    print("TEST 4: RIESGO POR TIEMPO DE VIDA DE DATOS")
    print("=" * 70)
    
    analyzer = QuantumThreatAnalyzer()
    
    scenarios = [
        (5, "Datos médicos (5 años de protección)"),
        (10, "Secretos corporativos (10 años)"),
        (25, "Datos gubernamentales (25 años)"),
        (50, "Secretos de estado (50 años)")
    ]
    
    print("\n⏳ Análisis 'Harvest Now, Decrypt Later':\n")
    
    for years, description in scenarios:
        risk = analyzer.calculate_data_lifetime_risk(years)
        
        risk_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(risk['risk_level'], "⚪")
        
        print(f"{risk_emoji} {description}")
        print(f"   Riesgo:          {risk['risk_level']}")
        print(f"   Algoritmos en riesgo: {len(risk['at_risk_algorithms'])}")
        
        if risk['at_risk_algorithms']:
            print(f"   Vulnerables:")
            for algo in risk['at_risk_algorithms'][:3]:
                print(f"      • {algo['algorithm']}: datos expuestos en {algo['data_will_be_exposed_in']} años")
        
        print(f"   Recomendación:   {risk['recommendation']}")
        print()
    
    print()


def test_migration_priority():
    """Test de prioridades de migración"""
    print("=" * 70)
    print("TEST 5: PRIORIDADES DE MIGRACIÓN")
    print("=" * 70)
    
    analyzer = QuantumThreatAnalyzer()
    
    priorities = analyzer.get_migration_priority()
    
    print("\n🎯 Lista Priorizada de Migraciones:\n")
    
    urgent = [p for p in priorities if p[1] == "URGENT"]
    high = [p for p in priorities if p[1] == "HIGH"]
    
    if urgent:
        print(f"   🔴 URGENTE ({len(urgent)}):")
        for algo, _ in urgent:
            print(f"      • {algo}")
        print()
    
    if high:
        print(f"   🟠 ALTA PRIORIDAD ({len(high)}):")
        for algo, _ in high:
            print(f"      • {algo}")
        print()
    
    if not urgent and not high:
        print("   ✅ No hay migraciones urgentes en este momento")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "QUANTUM THREAT ANALYZER - TESTS" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_analysis()
    print()
    
    test_threat_report()
    print()
    
    test_timeline()
    print()
    
    test_data_lifetime_risk()
    print()
    
    test_migration_priority()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("⚛️ CAPÍTULO 7 - PARTE 1 COMPLETADA:")
    print("   ✅ QuantumThreatAnalyzer")
    print("   ✅ Timeline de amenazas cuánticas")
    print("   ✅ Análisis de riesgo por algoritmo")
    print("   ✅ Prioridades de migración")
    print()
    print("🎯 La amenaza es REAL. La migración a PQC es necesaria!")
    print()


if __name__ == "__main__":
    main()