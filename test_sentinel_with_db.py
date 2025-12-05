#!/usr/bin/env python3
"""
Test del Log Sentinel con Base de Datos
"""

import asyncio
import sys
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent
from logs.log_sentinel import LogSentinel
from database.threat_database import ThreatDatabase


async def test_sentinel_with_db():
    print("=" * 70)
    print("👁️💾 PROBANDO LOG SENTINEL CON BASE DE DATOS")
    print("=" * 70)
    print()
    
    # Crear archivo de logs de prueba
    test_log = "test_logs_db.txt"
    
    with open(test_log, 'w') as f:
        f.write('192.168.1.100 - - [04/Dec/2025:11:00:00] "GET /index.html HTTP/1.1" 200\n')
        f.write('192.168.1.101 - - [04/Dec/2025:11:00:05] "GET /api/users HTTP/1.1" 200\n')
        f.write('192.168.1.102 - - [04/Dec/2025:11:00:10] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403\n')
        f.write('192.168.1.103 - - [04/Dec/2025:11:00:15] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403\n')
        f.write('192.168.1.104 - - [04/Dec/2025:11:00:20] "GET /download?file=../../../etc/passwd HTTP/1.1" 403\n')
        f.write('192.168.1.102 - - [04/Dec/2025:11:00:25] "GET /admin?id=1 UNION SELECT * FROM users-- HTTP/1.1" 403\n')
    
    print(f"✅ Archivo de test creado: {test_log}")
    print()
    
    # Inicializar componentes
    agent = NemesisAgent()
    database = ThreatDatabase("data/nemesis_sentinel_test.db")
    sentinel = LogSentinel(agent, test_log, follow=False, database=database)
    
    print("🚀 Iniciando análisis de logs con persistencia...")
    print()
    
    # Procesar logs
    await sentinel.start()
    
    # Mostrar estadísticas del sentinel
    stats = sentinel.stats
    
    print()
    print("=" * 70)
    print("📊 ESTADÍSTICAS DEL SENTINEL")
    print("=" * 70)
    print(f"Logs procesados:     {stats['logs_processed']}")
    print(f"Amenazas detectadas: {stats['threats_detected']}")
    print(f"Tasa de detección:   {stats['detection_rate']:.1f}%")
    print()
    
    # Mostrar estadísticas de la BD
    print("=" * 70)
    print("📊 ESTADÍSTICAS DE LA BASE DE DATOS")
    print("=" * 70)
    
    db_stats = database.get_statistics()
    
    print(f"Total amenazas en BD: {db_stats['total_threats']}")
    print(f"IPs bloqueadas:       {db_stats['total_blocked_ips']}")
    print()
    
    print("Amenazas por tipo:")
    for attack_type, count in db_stats['threats_by_type'].items():
        print(f"  • {attack_type}: {count}")
    
    print()
    print("IPs más maliciosas:")
    for ip, count in db_stats['top_malicious_ips']:
        print(f"  • {ip}: {count} ataques")
    
    print()
    print("🚫 IPs Bloqueadas:")
    blocked = database.get_blocked_ips()
    for ip_info in blocked:
        print(f"  • {ip_info['ip']}: {ip_info['threat_count']} amenazas - {ip_info['reason']}")
    
    print()
    print("=" * 70)
    print("✅ Test completado con éxito")
    print("=" * 70)
    
    database.close()


asyncio.run(test_sentinel_with_db())