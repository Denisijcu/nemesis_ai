#!/usr/bin/env python3
"""
Test del Dashboard V3.5 con Traffic Analytics integrado
Sistema completo: Network + Honeypot + Traffic
"""

import sys
sys.path.insert(0, 'src')

import asyncio
import time
from datetime import datetime
from database.threat_database import ThreatDatabase
from web.dashboard_v3 import DashboardV3
from traffic.traffic_sentinel import TrafficSentinel


def simulate_packet(src_ip, dst_ip, protocol="TCP", size=100, dst_port=80):
    """Simula un paquete de red"""
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


def simulate_honeypot_attack(db):
    """Simula capturas del honeypot guardándolas directamente en BD"""
    attackers = [
        ("45.142.212.61", "root:toor"),
        ("185.220.101.23", "admin:admin"),
        ("192.241.234.142", "ubuntu:ubuntu"),
        ("203.0.113.50", "admin:password123"),
        ("198.51.100.88", "root:12345")
    ]
    
    import random
    attacker = random.choice(attackers)
    
    # Guardar en BD como amenaza HONEYPOT_SSH
    db.add_threat(
        source_ip=attacker[0],
        attack_type="HONEYPOT_SSH",
        confidence=1.0,
        action_taken="LOGGED",
        payload=attacker[1]
    )
    
    return attacker


async def simulate_traffic(sentinel, db, duration=300):
    """Simula tráfico de red + honeypot en background"""
    print("📊 Simulador de tráfico iniciado...")
    
    start_time = time.time()
    packet_count = 0
    honeypot_count = 0
    
    try:
        while time.time() - start_time < duration:
            # Tráfico normal
            for i in range(10):
                protocol = ["TCP", "UDP", "ICMP"][i % 3]
                packet = simulate_packet(
                    src_ip=f"192.168.1.{(packet_count + i) % 50 + 100}",
                    dst_ip=f"10.0.0.{(packet_count + i) % 20 + 50}",
                    protocol=protocol,
                    size=1000 + ((packet_count + i) % 5000),
                    dst_port=[80, 443, 53, 22, 3306][i % 5]
                )
                sentinel.process_packet(packet)
                packet_count += 1
            
            # Cada 20 segundos, simular honeypot capture
            if int(time.time() - start_time) % 20 == 0 and honeypot_count < 50:
                print(f"   🍯 Simulando captura honeypot... ({honeypot_count + 1})")
                attacker = simulate_honeypot_attack(db)
                honeypot_count += 1
            
            # Cada 30 segundos, simular un ataque de red
            if int(time.time() - start_time) % 30 == 0:
                print(f"   🚨 Simulando ataque de red... ({packet_count} paquetes)")
                
                # Mini DDoS
                attacker_ip = f"203.0.113.{(int(time.time()) % 255)}"
                for i in range(50):
                    packet = simulate_packet(
                        src_ip=attacker_ip,
                        dst_ip="10.0.0.1",
                        size=100,
                        dst_port=80
                    )
                    sentinel.process_packet(packet)
                    packet_count += 1
                
                # Guardar como amenaza en BD
                db.add_threat(
                    source_ip=attacker_ip,
                    attack_type="DDOS",
                    confidence=0.95,
                    action_taken="BLOCKED",
                    payload="High packet rate detected"
                )
            
            await asyncio.sleep(1)
    
    except asyncio.CancelledError:
        print(f"📊 Simulador detenido.")
        print(f"   • Paquetes procesados: {packet_count}")
        print(f"   • Capturas honeypot: {honeypot_count}")


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "🎖️  DASHBOARD V3.5 + TRAFFIC ANALYTICS  🎖️" + " " * 8 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    print("=" * 70)
    print("🚀 INICIANDO SISTEMA COMPLETO")
    print("=" * 70)
    print()
    
    # Base de datos (usar la del honeypot que tiene datos)
    db = ThreatDatabase("data/nemesis_honeypot.db")
    print("✅ Base de datos: nemesis_honeypot.db")
    
    # Traffic Sentinel
    sentinel = TrafficSentinel(database=db, window_seconds=10, baseline_samples=5)
    print("✅ Traffic Sentinel inicializado")
    
    # Dashboard
    dashboard = DashboardV3(db, host="0.0.0.0", port=8080)
    
    # Guardar referencia al sentinel en el dashboard
    dashboard.traffic_sentinel = sentinel
    
    print("✅ Dashboard V3.5 inicializado")
    print()
    
    # Stats de BD
    stats = db.get_statistics()
    print(f"📊 Amenazas en BD: {stats['total_threats']}")
    print(f"🚫 IPs bloqueadas: {stats['total_blocked_ips']}")
    
    # Contar honeypot captures existentes
    threats = db.get_threats(limit=1000)
    honeypot_threats = [t for t in threats if "HONEYPOT" in t.attack_type]
    print(f"🍯 Capturas honeypot existentes: {len(honeypot_threats)}")
    print()
    
    print("=" * 70)
    print("✨ FEATURES DEL DASHBOARD COMPLETO")
    print("=" * 70)
    print()
    print("🎨 VISUALIZACIÓN:")
    print("   • ASCII Art Logo")
    print("   • Header con 5 stats principales")
    print("   • Live badge pulsante")
    print()
    print("🗺️ MAPA DE ATAQUES:")
    print("   • Puntos rojos pulsantes (30s)")
    print("   • Líneas rojas animadas (3s)")
    print("   • Labels con IP y tipo (15s)")
    print("   • Tabla de log permanente")
    print()
    print("🖥️ TERMINAL:")
    print("   • Logs en tiempo real")
    print("   • Colores por tipo")
    print("   • Auto-scroll")
    print()
    print("🍯 HONEYPOT PANEL:")
    print("   • Total capturas (ACTUALIZÁNDOSE)")
    print("   • Últimas 5 capturas")
    print("   • Nueva captura cada 20 segundos")
    print()
    print("📊 TRAFFIC ANALYTICS:")
    print("   • Bandwidth en tiempo real")
    print("   • Packets/second meter")
    print("   • Traffic status indicator")
    print("   • Baseline learning")
    print()
    print("🚨 THREAT MONITOR:")
    print("   • Lista de amenazas")
    print("   • Animaciones slide-in")
    print("   • Confidence scores")
    print()
    print("⚙️ SYSTEM STATUS:")
    print("   • 6 módulos monitoreados")
    print("   • Dots pulsantes verdes")
    print("   • Status indicators")
    print()
    print("📈 GRÁFICAS:")
    print("   • Timeline de amenazas")
    print("   • Attack types distribution")
    print()
    print("🔊 EFECTOS:")
    print("   • Sonido de alerta")
    print("   • Notificaciones popup")
    print("   • Scanlines CRT")
    print("   • Border scan animado")
    print()
    print("=" * 70)
    print("🌐 ACCEDE AL DASHBOARD:")
    print("   http://localhost:8080")
    print()
    print("💡 LO QUE VERÁS:")
    print()
    print("   1. Dashboard se abrirá con datos existentes")
    print("   2. Cada 20 segundos: Nueva captura honeypot 🍯")
    print("   3. Cada 30 segundos: Ataque de red simulado 🚨")
    print("   4. Tráfico continuo generándose 📊")
    print("   5. Todos los paneles actualizándose en vivo ⚡")
    print()
    print("=" * 70)
    print("🎖️  THE BEAST MODE - SISTEMA COMPLETO")
    print("   Presiona Ctrl+C para detener")
    print("=" * 70)
    print()
    
    # Iniciar simulador de tráfico en background
    traffic_task = asyncio.create_task(simulate_traffic(sentinel, db, duration=3600))
    
    # Iniciar dashboard
    try:
        await dashboard.run()
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo sistema...")
        traffic_task.cancel()
        try:
            await traffic_task
        except asyncio.CancelledError:
            pass
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS FINALES")
        print("=" * 70)
        
        # Stats del sentinel
        status = sentinel.get_system_status()
        print()
        print(f"Traffic Sentinel:")
        print(f"   • Paquetes procesados: {status['statistics']['packets_processed']}")
        print(f"   • Anomalías detectadas: {status['statistics']['anomalies_detected']}")
        print(f"   • Amenazas bloqueadas:  {status['statistics']['threats_blocked']}")
        
        # Stats de BD
        final_stats = db.get_statistics()
        print()
        print(f"Base de datos:")
        print(f"   • Total amenazas:    {final_stats['total_threats']}")
        print(f"   • IPs bloqueadas:    {final_stats['total_blocked_ips']}")
        print(f"   • Última 24h:        {final_stats['threats_last_24h']}")
        
        # Contar honeypot final
        final_threats = db.get_threats(limit=1000)
        final_honeypot = [t for t in final_threats if "HONEYPOT" in t.attack_type]
        print(f"   • Capturas honeypot: {len(final_honeypot)}")
        
        print()
        print("✅ Sistema detenido correctamente")
        print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n💎 Dashboard cerrado")