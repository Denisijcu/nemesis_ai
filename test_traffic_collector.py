#!/usr/bin/env python3
"""
Test del TrafficCollector
"""

import sys
sys.path.insert(0, 'src')

import time
from datetime import datetime
from traffic.traffic_collector import TrafficCollector


def simulate_packet(src_ip, dst_ip, protocol="TCP", size=100, src_port=None, dst_port=None, flags=None):
    """Simula un paquete"""
    return {
        "timestamp": datetime.now(),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port or 12345,
        "dst_port": dst_port or 80,
        "protocol": protocol,
        "size": size,
        "flags": flags or {}
    }


def test_basic_stats():
    """Test de estadísticas básicas"""
    print("=" * 70)
    print("TEST 1: ESTADÍSTICAS BÁSICAS")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    
    # Simular tráfico variado
    print("\n📦 Simulando 100 paquetes...")
    
    for i in range(100):
        protocol = "TCP" if i % 2 == 0 else "UDP"
        src_ip = f"192.168.1.{i % 10 + 100}"
        dst_ip = f"10.0.0.{i % 5 + 50}"
        
        packet = simulate_packet(
            src_ip=src_ip,
            dst_ip=dst_ip,
            protocol=protocol,
            size=500 + (i * 10),
            dst_port=80 if protocol == "TCP" else 53
        )
        
        collector.process_packet(packet)
    
    # Obtener estadísticas
    stats = collector.get_current_stats()
    
    print(f"\n✅ Total paquetes:  {stats.total_packets}")
    print(f"✅ Total bytes:     {stats.total_bytes:,}")
    print(f"✅ Conexiones:      {stats.active_connections}")
    print()
    
    # Distribución de protocolos
    print("📊 Distribución de protocolos:")
    dist = collector.get_protocol_distribution()
    for protocol, percentage in dist.items():
        print(f"   • {protocol}: {percentage:.1f}%")
    print()


def test_top_talkers():
    """Test de top talkers"""
    print("=" * 70)
    print("TEST 2: TOP TALKERS")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    
    # Simular una IP muy activa
    print("\n📦 Simulando tráfico con IP muy activa...")
    
    # IP normal
    for i in range(20):
        packet = simulate_packet(
            src_ip="192.168.1.100",
            dst_ip="10.0.0.50",
            size=1000
        )
        collector.process_packet(packet)
    
    # IP muy activa (attacker)
    for i in range(80):
        packet = simulate_packet(
            src_ip="203.0.113.50",  # IP sospechosa
            dst_ip="10.0.0.50",
            size=5000  # Paquetes grandes
        )
        collector.process_packet(packet)
    
    # Top talkers
    print("\n🔝 Top 5 IPs por tráfico enviado:")
    top = collector.get_top_talkers(5)
    for i, (ip, bytes_sent) in enumerate(top, 1):
        print(f"   {i}. {ip}: {bytes_sent:,} bytes")
    print()


def test_bandwidth():
    """Test de uso de bandwidth"""
    print("=" * 70)
    print("TEST 3: BANDWIDTH USAGE")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    
    print("\n📦 Simulando tráfico intenso...")
    
    start = time.time()
    
    # Simular tráfico pesado por 2 segundos
    while time.time() - start < 2:
        for i in range(10):
            packet = simulate_packet(
                src_ip=f"192.168.1.{i % 10}",
                dst_ip="10.0.0.1",
                size=10000  # 10KB por paquete
            )
            collector.process_packet(packet)
        
        time.sleep(0.1)
    
    # Bandwidth
    bandwidth = collector.get_bandwidth_usage()
    
    print(f"\n📊 Bandwidth:")
    print(f"   • Bytes/second:   {bandwidth['bytes_per_second']:,.0f}")
    print(f"   • Packets/second: {bandwidth['packets_per_second']:.1f}")
    print(f"   • Total bytes:    {bandwidth['total_bytes']:,}")
    print()


def test_connections():
    """Test de tracking de conexiones"""
    print("=" * 70)
    print("TEST 4: CONNECTION TRACKING")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    
    print("\n📦 Simulando conexiones TCP...")
    
    # Nueva conexión (SYN)
    packet = simulate_packet(
        src_ip="192.168.1.100",
        dst_ip="10.0.0.50",
        src_port=54321,
        dst_port=80,
        flags={'S': True}  # SYN
    )
    collector.process_packet(packet)
    
    # Más paquetes de la misma conexión
    for i in range(10):
        packet = simulate_packet(
            src_ip="192.168.1.100",
            dst_ip="10.0.0.50",
            src_port=54321,
            dst_port=80,
            flags={'A': True}  # ACK
        )
        collector.process_packet(packet)
    
    # Cerrar conexión (FIN)
    packet = simulate_packet(
        src_ip="192.168.1.100",
        dst_ip="10.0.0.50",
        src_port=54321,
        dst_port=80,
        flags={'F': True}  # FIN
    )
    collector.process_packet(packet)
    
    # Estadísticas de conexiones
    conn_stats = collector.get_connection_stats()
    
    print(f"\n📊 Conexiones:")
    print(f"   • Activas:  {conn_stats['active']}")
    print(f"   • Nuevas:   {conn_stats['new']}")
    print(f"   • Cerradas: {conn_stats['closed']}")
    print(f"   • Tracked:  {conn_stats['total_tracked']}")
    print()


def test_summary():
    """Test de resumen completo"""
    print("=" * 70)
    print("TEST 5: RESUMEN COMPLETO")
    print("=" * 70)
    
    collector = TrafficCollector(window_seconds=5)
    
    print("\n📦 Simulando tráfico mixto...")
    
    # Tráfico variado
    for i in range(50):
        protocol = ["TCP", "UDP", "ICMP"][i % 3]
        packet = simulate_packet(
            src_ip=f"192.168.1.{i % 20}",
            dst_ip=f"10.0.0.{i % 10}",
            protocol=protocol,
            size=1000 + (i * 50),
            dst_port=[80, 443, 53, 22][i % 4]
        )
        collector.process_packet(packet)
    
    # Resumen
    summary = collector.get_summary()
    
    print(f"\n📊 RESUMEN:")
    print(f"   General:")
    print(f"      Paquetes: {summary['general']['total_packets']}")
    print(f"      Bytes:    {summary['general']['total_bytes']:,}")
    print()
    print(f"   Bandwidth:")
    print(f"      Bytes/s:  {summary['bandwidth']['bytes_per_second']:,.0f}")
    print()
    print(f"   Protocolos:")
    for proto, count in summary['protocols'].items():
        print(f"      {proto}: {count}")
    print()
    print(f"   Conexiones:")
    for key, value in summary['connections'].items():
        print(f"      {key}: {value}")
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "TRAFFIC COLLECTOR - TESTS" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_stats()
    print()
    
    test_top_talkers()
    print()
    
    test_bandwidth()
    print()
    
    test_connections()
    print()
    
    test_summary()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()