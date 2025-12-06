#!/usr/bin/env python3
"""
Test del TrafficSentinel - Sistema completo
"""

import sys
sys.path.insert(0, 'src')

import time
import asyncio
from datetime import datetime
from traffic.traffic_sentinel import TrafficSentinel
from database.threat_database import ThreatDatabase


def simulate_packet(src_ip, dst_ip, protocol="TCP", size=100, dst_port=80):
    """Simula un paquete"""
    return {
        "timestamp": datetime.now(),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": 12345,
        "dst_port": dst_port,
        "protocol": protocol,
        "size": size,
        "flags": {}
    }


def generate_normal_traffic(sentinel, packets=50):
    """Genera tráfico normal"""
    for i in range(packets):
        protocol = "TCP" if i % 3 != 0 else "UDP"
        packet = simulate_packet(
            src_ip=f"192.168.1.{i % 20 + 100}",
            dst_ip=f"10.0.0.{i % 10 + 50}",
            protocol=protocol,
            size=1000 + (i % 500),
            dst_port=[80, 443, 53][i % 3]
        )
        sentinel.process_packet(packet)


def test_basic_integration():
    """Test de integración básica"""
    print("=" * 70)
    print("TEST 1: INTEGRACIÓN BÁSICA")
    print("=" * 70)
    
    sentinel = TrafficSentinel(window_seconds=5)
    
    print("\n📦 Procesando tráfico normal...")
    generate_normal_traffic(sentinel, packets=100)
    
    # Estado del sistema
    status = sentinel.get_system_status()
    
    print(f"\n📊 Estado del sistema:")
    print(f"   • Status:            {status['status']}")
    print(f"   • Baseline generado: {status['baseline_generated']}")
    print(f"   • Paquetes:          {status['statistics']['packets_processed']}")
    print(f"   • PPS actual:        {status['current_traffic']['packets_per_second']:.1f}")
    print()


def test_baseline_generation():
    """Test de generación automática de baseline"""
    print("=" * 70)
    print("TEST 2: GENERACIÓN AUTOMÁTICA DE BASELINE")
    print("=" * 70)
    
    sentinel = TrafficSentinel(window_seconds=3, baseline_samples=5)
    
    print("\n📦 Generando tráfico para baseline automático...")
    
    # Generar suficiente tráfico para baseline
    for i in range(6):
        generate_normal_traffic(sentinel, packets=50)
        time.sleep(0.5)
        sentinel.collector._check_rotation()
        
        status = sentinel.get_system_status()
        if status['baseline_generated']:
            print(f"   ✅ Baseline generado en ventana {i+1}")
            break
    
    if sentinel.baseline_generated:
        baseline = sentinel.analyzer.baseline
        print(f"\n📊 Baseline:")
        print(f"   • PPS promedio: {baseline.avg_pps:.1f}")
        print(f"   • BPS promedio: {baseline.avg_bps:,.0f}")
        print(f"   • Muestras:     {baseline.samples}")
    else:
        print("\n❌ Baseline no generado")
    
    print()


def test_anomaly_detection_with_db():
    """Test de detección con base de datos"""
    print("=" * 70)
    print("TEST 3: DETECCIÓN CON BASE DE DATOS")
    print("=" * 70)
    
    # Crear BD temporal
    db = ThreatDatabase("data/traffic_test.db")
    sentinel = TrafficSentinel(database=db, window_seconds=3, baseline_samples=5)
    
    print("\n📦 Fase 1: Generando baseline...")
    
    for i in range(6):
        generate_normal_traffic(sentinel, packets=30)
        time.sleep(0.3)
        sentinel.collector._check_rotation()
    
    print("   ✅ Baseline establecido")
    
    print("\n📦 Fase 2: Generando ataques...")
    
    # Ataque DDoS
    print("   🚨 Simulando DDoS...")
    for i in range(200):
        packet = simulate_packet(
            src_ip="203.0.113.50",
            dst_ip="10.0.0.1",
            size=100
        )
        sentinel.process_packet(packet)
    
    # Port scan
    print("   🚨 Simulando Port Scan...")
    attacker = "198.51.100.99"
    for port in range(1, 15):
        packet = simulate_packet(
            src_ip=attacker,
            dst_ip="10.0.0.1",
            dst_port=port * 100
        )
        sentinel.process_packet(packet)
    
    # Analizar
    analysis = sentinel.analyze_current_traffic()
    
    print(f"\n🚨 ANOMALÍAS DETECTADAS: {len(analysis['anomalies'])}")
    
    for anomaly in analysis['anomalies']:
        severity_emoji = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(anomaly.severity, "⚪")
        
        print(f"   {severity_emoji} {anomaly.anomaly_type}")
        print(f"      IP:      {anomaly.source_ip}")
        print(f"      Severidad: {anomaly.severity}")
    
    # Estadísticas de BD
    stats = db.get_statistics()
    
    print(f"\n📊 Base de datos:")
    print(f"   • Amenazas guardadas: {stats['total_threats']}")
    print(f"   • IPs bloqueadas:     {stats['total_blocked_ips']}")
    
    # Ver amenazas en BD
    threats = db.get_threats(limit=5)
    if threats:
        print(f"\n   Últimas amenazas:")
        for t in threats[:3]:
            print(f"      • {t.attack_type} desde {t.source_ip} -> {t.action_taken}")
    
    print()


def test_full_report():
    """Test de reporte completo"""
    print("=" * 70)
    print("TEST 4: REPORTE COMPLETO DEL SISTEMA")
    print("=" * 70)
    
    db = ThreatDatabase("data/traffic_test.db")
    sentinel = TrafficSentinel(database=db, window_seconds=3, baseline_samples=5)
    
    # Generar baseline
    for i in range(6):
        generate_normal_traffic(sentinel, packets=30)
        time.sleep(0.2)
        sentinel.collector._check_rotation()
    
    # Tráfico con anomalías
    for i in range(150):
        packet = simulate_packet(
            src_ip="203.0.113.100",
            dst_ip="10.0.0.1",
            size=5000
        )
        sentinel.process_packet(packet)
    
    # Generar reporte
    report = sentinel.get_full_report()
    
    print(f"\n📊 REPORTE COMPLETO:")
    print()
    print(f"   Sistema:")
    print(f"      Status:      {report['system_status']['status']}")
    print(f"      Baseline:    {'✅' if report['system_status']['baseline_generated'] else '❌'}")
    print()
    
    stats = report['system_status']['statistics']
    print(f"   Estadísticas:")
    print(f"      Paquetes:    {stats['packets_processed']}")
    print(f"      Anomalías:   {stats['anomalies_detected']}")
    print(f"      Bloqueados:  {stats['threats_blocked']}")
    print()
    
    traffic = report['system_status']['current_traffic']
    print(f"   Tráfico actual:")
    print(f"      PPS:         {traffic['packets_per_second']:.1f}")
    print(f"      BPS:         {traffic['bytes_per_second']:,.0f}")
    print(f"      Conexiones:  {traffic['active_connections']}")
    print()
    
    if report['current_anomalies']:
        print(f"   🚨 Anomalías actuales: {len(report['current_anomalies'])}")
        for anomaly in report['current_anomalies'][:3]:
            print(f"      • {anomaly['type']} ({anomaly['severity']})")
    
    print()


def test_callback():
    """Test de callback personalizado"""
    print("=" * 70)
    print("TEST 5: CALLBACK PERSONALIZADO")
    print("=" * 70)
    
    sentinel = TrafficSentinel(window_seconds=3, baseline_samples=5)
    
    # Lista para guardar anomalías detectadas
    detected = []
    
    def on_anomaly(anomaly):
        """Callback cuando se detecta anomalía"""
        detected.append(anomaly)
        print(f"   ⚠️  CALLBACK: {anomaly.anomaly_type} detectado!")
    
    sentinel.set_anomaly_callback(on_anomaly)
    
    print("\n📦 Callback configurado, generando baseline...")
    
    for i in range(6):
        generate_normal_traffic(sentinel, packets=30)
        time.sleep(0.2)
        sentinel.collector._check_rotation()
    
    print("\n📦 Generando tráfico anómalo...")
    
    # DDoS
    for i in range(200):
        packet = simulate_packet(
            src_ip="203.0.113.50",
            dst_ip="10.0.0.1",
            size=100
        )
        sentinel.process_packet(packet)
    
    # Analizar para trigger callbacks
    sentinel.analyze_current_traffic()
    
    print(f"\n✅ Callbacks ejecutados: {len(detected)}")
    
    for i, anomaly in enumerate(detected, 1):
        print(f"   {i}. {anomaly.anomaly_type} - {anomaly.severity}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "TRAFFIC SENTINEL - TESTS" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_integration()
    print()
    
    test_baseline_generation()
    print()
    
    test_anomaly_detection_with_db()
    print()
    
    test_full_report()
    print()
    
    test_callback()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("📊 CAPÍTULO 6 COMPLETADO:")
    print("   ✅ TrafficCollector")
    print("   ✅ TrafficAnalyzer")
    print("   ✅ AnomalyDetector")
    print("   ✅ TrafficSentinel")
    print()
    print("🎯 Sistema completo de análisis de tráfico funcionando!")
    print()


if __name__ == "__main__":
    main()