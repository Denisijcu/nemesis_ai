#!/usr/bin/env python3
"""
Test de la base de datos
"""

import sys
sys.path.insert(0, 'src')

from datetime import datetime
from database.threat_database import ThreatDatabase, ThreatRecord


def test_database():
    print("=" * 70)
    print("💾 PROBANDO BASE DE DATOS")
    print("=" * 70)
    print()
    
    # Inicializar BD
    db = ThreatDatabase("data/nemesis_test.db")
    
    print("✅ Base de datos inicializada")
    print()
    
    # Crear amenazas de prueba
    threats = [
        ThreatRecord(
            id=None,
            timestamp=datetime.now(),
            source_ip="192.168.1.100",
            attack_type="SQL_INJECTION",
            payload="' OR '1'='1'--",
            confidence=0.95,
            action_taken="BLOCK",
            blocked=True
        ),
        ThreatRecord(
            id=None,
            timestamp=datetime.now(),
            source_ip="192.168.1.101",
            attack_type="XSS",
            payload="<script>alert(1)</script>",
            confidence=0.88,
            action_taken="BLOCK",
            blocked=True
        ),
        ThreatRecord(
            id=None,
            timestamp=datetime.now(),
            source_ip="192.168.1.100",
            attack_type="PATH_TRAVERSAL",
            payload="../../../etc/passwd",
            confidence=0.92,
            action_taken="BLOCK",
            blocked=True
        ),
    ]
    
    # Guardar amenazas
    print("💾 Guardando amenazas...")
    for threat in threats:
        threat_id = db.save_threat(threat)
        print(f"   ✅ Amenaza guardada: ID={threat_id}, Tipo={threat.attack_type}")
    
    print()
    
    # Bloquear IPs
    print("🚫 Bloqueando IPs...")
    db.block_ip("192.168.1.100", "SQL Injection + Path Traversal")
    db.block_ip("192.168.1.101", "XSS Attack")
    print("   ✅ IPs bloqueadas")
    print()
    
    # Obtener amenazas
    print("📊 Obteniendo amenazas...")
    all_threats = db.get_threats(limit=10)
    print(f"   Total recuperadas: {len(all_threats)}")
    
    for threat in all_threats:
        print(f"   • {threat.attack_type} desde {threat.source_ip} "
              f"({threat.confidence:.1%} confianza)")
    
    print()
    
    # IPs bloqueadas
    print("🚫 IPs Bloqueadas:")
    blocked = db.get_blocked_ips()
    for ip_info in blocked:
        print(f"   • {ip_info['ip']}: {ip_info['threat_count']} amenazas")
    
    print()
    
    # Estadísticas
    print("📊 Estadísticas Globales:")
    stats = db.get_statistics()
    
    print(f"   Total de amenazas:  {stats['total_threats']}")
    print(f"   IPs bloqueadas:     {stats['total_blocked_ips']}")
    print(f"   Últimas 24h:        {stats['threats_last_24h']}")
    print()
    print("   Amenazas por tipo:")
    for attack_type, count in stats['threats_by_type'].items():
        print(f"     • {attack_type}: {count}")
    
    print()
    print("   Top IPs maliciosas:")
    for ip, count in stats['top_malicious_ips']:
        print(f"     • {ip}: {count} ataques")
    
    print()
    print("=" * 70)
    print("✅ Test de base de datos completado")
    print("=" * 70)
    
    db.close()


if __name__ == "__main__":
    test_database()