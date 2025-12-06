#!/usr/bin/env python3
"""
Test del AnomalyDetector
"""

import sys
sys.path.insert(0, 'src')

import time
from datetime import datetime
from traffic.anomaly_detector import AnomalyDetector


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


def test_ddos_detection():
    """Test de detección de DDoS"""
    print("=" * 70)
    print("TEST 1: DETECCIÓN DE DDoS")
    print("=" * 70)
    
    detector = AnomalyDetector()
    
    # Simular ataque DDoS
    print("\n🚨 Simulando ataque DDoS...")
    
    stats = {
        "packets_per_second": 1500,  # Muy alto
        "new_connections": 150,       # Muchas conexiones
        "top_senders": [("203.0.113.50", 1000000)]
    }
    
    anomaly = detector.detect_ddos(stats)
    
    if anomaly:
        print(f"\n✅ DDoS detectado:")
        print(f"   • Tipo:        {anomaly.anomaly_type}")
        print(f"   • Severidad:   {anomaly.severity}")
        print(f"   • IP:          {anomaly.source_ip}")
        print(f"   • Descripción: {anomaly.description}")
        print(f"   • Confianza:   {anomaly.confidence * 100:.0f}%")
        print(f"   • Detalles:    {anomaly.details}")
    else:
        print("❌ No se detectó DDoS")
    
    print()


def test_port_scan_detection():
    """Test de detección de port scanning"""
    print("=" * 70)
    print("TEST 2: DETECCIÓN DE PORT SCANNING")
    print("=" * 70)
    
    detector = AnomalyDetector()
    attacker_ip = "192.168.1.100"
    
    print(f"\n🔍 Simulando port scan desde {attacker_ip}...")
    
    # Simular escaneo de 15 puertos en 30 segundos
    for port in range(1, 16):
        packet = simulate_packet(
            src_ip=attacker_ip,
            dst_ip="10.0.0.50",
            dst_port=port * 100
        )
        detector.update_tracking(packet)
        time.sleep(0.05)
    
    # Detectar
    anomaly = detector.detect_port_scan(attacker_ip)
    
    if anomaly:
        print(f"\n✅ Port scan detectado:")
        print(f"   • Tipo:        {anomaly.anomaly_type}")
        print(f"   • Severidad:   {anomaly.severity}")
        print(f"   • IP:          {anomaly.source_ip}")
        print(f"   • Descripción: {anomaly.description}")
        print(f"   • Confianza:   {anomaly.confidence * 100:.0f}%")
        print(f"   • Scan type:   {anomaly.details['scan_type']}")
        print(f"   • Puertos:     {len(anomaly.details['ports'])}")
    else:
        print("❌ No se detectó port scan")
    
    print()


def test_data_exfiltration():
    """Test de detección de exfiltración"""
    print("=" * 70)
    print("TEST 3: DETECCIÓN DE DATA EXFILTRATION")
    print("=" * 70)
    
    detector = AnomalyDetector()
    
    print("\n📤 Simulando exfiltración de datos...")
    
    # Upload rate de 15 MB/s (muy alto)
    anomaly = detector.detect_data_exfiltration(
        source_ip="192.168.1.100",
        upload_rate=15_000_000  # 15 MB/s
    )
    
    if anomaly:
        print(f"\n✅ Exfiltración detectada:")
        print(f"   • Tipo:        {anomaly.anomaly_type}")
        print(f"   • Severidad:   {anomaly.severity}")
        print(f"   • IP:          {anomaly.source_ip}")
        print(f"   • Descripción: {anomaly.description}")
        print(f"   • Confianza:   {anomaly.confidence * 100:.0f}%")
        print(f"   • Rate:        {anomaly.details['upload_rate_mbps']:.2f} MB/s")
    else:
        print("❌ No se detectó exfiltración")
    
    print()


def test_suspicious_ports():
    """Test de detección de puertos sospechosos"""
    print("=" * 70)
    print("TEST 4: DETECCIÓN DE PUERTOS SOSPECHOSOS")
    print("=" * 70)
    
    detector = AnomalyDetector()
    
    print("\n🔌 Simulando uso de puertos sospechosos...")
    
    port_usage = {
        80: 100,      # Normal
        443: 80,      # Normal
        31337: 10,    # Back Orifice - SOSPECHOSO
        12345: 8,     # NetBus - SOSPECHOSO
        4444: 6       # Metasploit - SOSPECHOSO
    }
    
    anomalies = detector.detect_suspicious_ports(port_usage)
    
    print(f"\n✅ Puertos sospechosos detectados: {len(anomalies)}")
    
    for i, anomaly in enumerate(anomalies, 1):
        print(f"\n   {i}. {anomaly.details['port_description']}")
        print(f"      Puerto:      {anomaly.details['port']}")
        print(f"      Usos:        {anomaly.details['count']}")
        print(f"      Severidad:   {anomaly.severity}")
        print(f"      Confianza:   {anomaly.confidence * 100:.0f}%")
    
    print()


def test_complete_analysis():
    """Test de análisis completo"""
    print("=" * 70)
    print("TEST 5: ANÁLISIS COMPLETO")
    print("=" * 70)
    
    detector = AnomalyDetector()
    
    print("\n🔍 Simulando tráfico con múltiples anomalías...")
    
    # Simular port scan
    attacker_ip = "203.0.113.99"
    for port in range(1, 12):
        packet = simulate_packet(
            src_ip=attacker_ip,
            dst_ip="10.0.0.1",
            dst_port=port * 100
        )
        detector.update_tracking(packet)
    
    # Preparar datos de tráfico
    traffic_data = {
        "packets_per_second": 1200,  # DDoS
        "bytes_per_second": 5_000_000,
        "new_connections": 120,
        "top_senders": [(attacker_ip, 10_000_000)],
        "port_usage": {
            80: 50,
            31337: 8,  # Sospechoso
            4444: 6    # Sospechoso
        },
        "protocols": {
            "TCP": 70.0,
            "UDP": 20.0,
            "ICMP": 10.0
        }
    }
    
    # Analizar
    anomalies = detector.analyze_traffic(traffic_data)
    
    print(f"\n🚨 ANOMALÍAS DETECTADAS: {len(anomalies)}")
    print()
    
    # Agrupar por severidad
    critical = [a for a in anomalies if a.severity == "CRITICAL"]
    high = [a for a in anomalies if a.severity == "HIGH"]
    medium = [a for a in anomalies if a.severity == "MEDIUM"]
    
    if critical:
        print(f"   🔴 CRITICAL ({len(critical)}):")
        for a in critical:
            print(f"      • {a.anomaly_type}: {a.description}")
    
    if high:
        print(f"\n   🟠 HIGH ({len(high)}):")
        for a in high:
            print(f"      • {a.anomaly_type}: {a.description}")
    
    if medium:
        print(f"\n   🟡 MEDIUM ({len(medium)}):")
        for a in medium:
            print(f"      • {a.anomaly_type}: {a.description}")
    
    # Resumen
    print()
    summary = detector.get_anomaly_summary()
    
    print("   📊 RESUMEN:")
    print(f"      Total anomalías: {summary['total_anomalies']}")
    print()
    print("      Por tipo:")
    for atype, count in summary['by_type'].items():
        print(f"         {atype}: {count}")
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "ANOMALY DETECTOR - TESTS" + " " * 24 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_ddos_detection()
    print()
    
    test_port_scan_detection()
    print()
    
    test_data_exfiltration()
    print()
    
    test_suspicious_ports()
    print()
    
    test_complete_analysis()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()