#!/usr/bin/env python3
"""
Test del TrafficAnalyzer
"""

import sys
sys.path.insert(0, 'src')

import time
from datetime import datetime
from traffic.traffic_collector import TrafficCollector
from traffic.traffic_analyzer import TrafficAnalyzer


def simulate_packet(src_ip, dst_ip, protocol="TCP", size=100, src_port=None, dst_port=None):
    """Simula un paquete"""
    return {
        "timestamp": datetime.now(),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port or 12345,
        "dst_port": dst_port or 80,
        "protocol": protocol,
        "size": size,
        "flags": {}
    }


def generate_normal_traffic(collector, packets=100):
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
        collector.process_packet(packet)


def test_baseline_generation():
    """Test de generación de baseline"""
    print("=" * 70)
    print("TEST 1: GENERACIÓN DE BASELINE")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    analyzer = TrafficAnalyzer(collector)
    
    print("\n📦 Generando tráfico normal para baseline...")
    
    # Simular varias ventanas de tráfico normal
    for window in range(15):
        generate_normal_traffic(collector, packets=50)
        time.sleep(0.5)
        
        # Forzar rotación
        collector._check_rotation()
    
    print(f"   Ventanas generadas: {len(collector.get_stats_history())}")
    
    # Generar baseline
    baseline = analyzer.generate_baseline(min_samples=10)
    
    if baseline:
        print(f"\n✅ Baseline generado:")
        print(f"   • PPS promedio:  {baseline.avg_pps:.1f} ± {baseline.std_pps:.1f}")
        print(f"   • BPS promedio:  {baseline.avg_bps:,.0f} ± {baseline.std_bps:,.0f}")
        print(f"   • CPM promedio:  {baseline.avg_cpm:.1f} ± {baseline.std_cpm:.1f}")
        print(f"   • Muestras:      {baseline.samples}")
        print()
        print("   Protocolos:")
        for proto, pct in baseline.protocol_distribution.items():
            print(f"      {proto}: {pct:.1f}%")
        print()
    else:
        print("❌ No se pudo generar baseline")
    print()


def test_traffic_report():
    """Test de reporte de tráfico"""
    print("=" * 70)
    print("TEST 2: REPORTE DE TRÁFICO")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    analyzer = TrafficAnalyzer(collector)
    
    print("\n📦 Generando tráfico...")
    generate_normal_traffic(collector, packets=100)
    
    # Generar reporte
    report = analyzer.analyze_current_traffic()
    
    print(f"\n📊 REPORTE DE TRÁFICO:")
    print(f"   • Timestamp:     {report.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   • PPS:           {report.current_pps:.1f}")
    print(f"   • BPS:           {report.current_bps:,.0f}")
    print(f"   • Conexiones:    {report.current_connections}")
    print()
    
    print("   🔝 Top 5 emisores:")
    for i, (ip, bytes_sent) in enumerate(report.top_senders[:5], 1):
        print(f"      {i}. {ip}: {bytes_sent:,} bytes")
    print()
    
    print("   📊 Protocolos:")
    for proto, pct in report.protocol_breakdown.items():
        print(f"      {proto}: {pct:.1f}%")
    print()
    
    print("   🔌 Top 5 puertos:")
    for i, (port, count) in enumerate(report.top_ports[:5], 1):
        print(f"      {i}. Puerto {port}: {count} usos")
    print()


def test_anomaly_detection():
    """Test de detección de anomalías"""
    print("=" * 70)
    print("TEST 3: DETECCIÓN DE ANOMALÍAS")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    analyzer = TrafficAnalyzer(collector)
    
    print("\n📦 Fase 1: Generando baseline con tráfico normal...")
    
    # Generar baseline
    for window in range(15):
        generate_normal_traffic(collector, packets=50)
        time.sleep(0.3)
        collector._check_rotation()
    
    analyzer.generate_baseline(min_samples=10)
    print("   ✅ Baseline establecido")
    
    print("\n📦 Fase 2: Generando tráfico anómalo...")
    
    # Simular ataque DDoS (muchos paquetes)
    for i in range(500):
        packet = simulate_packet(
            src_ip="203.0.113.50",  # IP atacante
            dst_ip="10.0.0.1",
            size=100,
            dst_port=80
        )
        collector.process_packet(packet)
    
    # Simular puerto inusual
    for i in range(50):
        packet = simulate_packet(
            src_ip="192.168.1.100",
            dst_ip="10.0.0.1",
            dst_port=31337,  # Puerto inusual
            size=5000
        )
        collector.process_packet(packet)
    
    # Analizar
    report = analyzer.analyze_current_traffic()
    anomalies = analyzer.detect_traffic_anomalies(report)
    
    print(f"\n🚨 ANOMALÍAS DETECTADAS: {len(anomalies)}")
    print()
    
    for i, anomaly in enumerate(anomalies, 1):
        severity_emoji = {
            "HIGH": "🔴",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(anomaly['severity'], "⚪")
        
        print(f"   {i}. {severity_emoji} {anomaly['type']}")
        print(f"      {anomaly['description']}")
        print()


def test_summary_report():
    """Test de reporte resumen"""
    print("=" * 70)
    print("TEST 4: REPORTE RESUMEN COMPLETO")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    analyzer = TrafficAnalyzer(collector)
    
    # Generar baseline
    for window in range(15):
        generate_normal_traffic(collector, packets=50)
        time.sleep(0.2)
        collector._check_rotation()
    
    analyzer.generate_baseline(min_samples=10)
    
    # Tráfico anómalo
    for i in range(200):
        packet = simulate_packet(
            src_ip="203.0.113.99",
            dst_ip="10.0.0.1",
            size=10000
        )
        collector.process_packet(packet)
    
    # Generar resumen
    summary = analyzer.generate_summary_report()
    
    print(f"\n📊 REPORTE RESUMEN:")
    print()
    print("   Métricas:")
    for key, value in summary['metrics'].items():
        print(f"      {key}: {value}")
    print()
    
    print("   Top Talkers:")
    print("      Emisores:")
    for ip, bytes in summary['top_talkers']['senders'][:3]:
        print(f"         {ip}: {bytes:,} bytes")
    print()
    
    print("   Protocolos:")
    for proto, pct in summary['protocols'].items():
        print(f"      {proto}: {pct:.1f}%")
    print()
    
    if summary['anomalies']:
        print(f"   🚨 Anomalías: {len(summary['anomalies'])}")
        for anomaly in summary['anomalies']:
            print(f"      • {anomaly['type']}: {anomaly['severity']}")
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "TRAFFIC ANALYZER - TESTS" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_baseline_generation()
    print()
    
    test_traffic_report()
    print()
    
    test_anomaly_detection()
    print()
    
    test_summary_report()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()