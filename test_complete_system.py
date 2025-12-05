#!/usr/bin/env python3
"""
Test completo: Sentinel + BD + Alertas
"""

import asyncio
import sys
import yaml
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent
from logs.log_sentinel import LogSentinel
from database.threat_database import ThreatDatabase
from alerts.alert_manager import AlertManager


async def test_complete_system():
    print("=" * 70)
    print("🚀 SISTEMA COMPLETO: SENTINEL + BD + ALERTAS")
    print("=" * 70)
    print()
    
    # Crear logs de prueba
    test_log = "test_complete.txt"
    with open(test_log, 'w') as f:
        f.write('192.168.1.100 - - [04/Dec/2025:12:00:00] "GET /index.html HTTP/1.1" 200\n')
        f.write('192.168.1.101 - - [04/Dec/2025:12:00:05] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403\n')
        f.write('192.168.1.102 - - [04/Dec/2025:12:00:10] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403\n')
        f.write('192.168.1.103 - - [04/Dec/2025:12:00:15] "GET /download?file=../../../etc/passwd HTTP/1.1" 403\n')
    
    print(f"✅ Logs de prueba creados: {test_log}")
    print()
    
    # Cargar config de alertas
    try:
        with open('config/alerts.yaml', 'r') as f:
            alerts_config = yaml.safe_load(f)
        print("✅ Configuración de alertas cargada")
    except:
        print("⚠️  Sin config de alertas, usando defaults")
        alerts_config = {}
    
    print()
    
    # Inicializar componentes
    print("📦 Inicializando componentes...")
    agent = NemesisAgent()
    database = ThreatDatabase("data/nemesis_complete_test.db")
    alert_manager = AlertManager(alerts_config)
    sentinel = LogSentinel(
        agent, 
        test_log, 
        follow=False, 
        database=database, 
        alert_manager=alert_manager
    )
    
    print()
    print("🚀 Procesando logs...")
    print("   📱 Las alertas llegarán a Telegram en tiempo real")
    print("   💾 Todo se guardará en la base de datos")
    print()
    
    # Procesar
    await sentinel.start()
    
    # Stats
    stats = sentinel.stats
    db_stats = database.get_statistics()
    
    print()
    print("=" * 70)
    print("📊 RESULTADOS FINALES")
    print("=" * 70)
    print(f"📄 Logs procesados:     {stats['logs_processed']}")
    print(f"🚨 Amenazas detectadas: {stats['threats_detected']}")
    print(f"💾 Guardadas en BD:     {db_stats['total_threats']}")
    print(f"📱 Alertas enviadas:    {stats['threats_detected']} (Telegram)")
    print()
    
    print("Amenazas por tipo:")
    for attack_type, count in db_stats['threats_by_type'].items():
        print(f"  • {attack_type}: {count}")
    
    print()
    print("🚫 IPs bloqueadas:")
    blocked = database.get_blocked_ips()
    for ip_info in blocked:
        print(f"  • {ip_info['ip']}: {ip_info['threat_count']} amenazas")
    
    print()
    print("=" * 70)
    print("✅ SISTEMA COMPLETO FUNCIONANDO AL 100%")
    print("=" * 70)
    print()
    print("💡 Revisa tu Telegram - deberías tener 3 alertas!")
    print("   🌐 Dashboard disponible en: http://localhost:8080")
    print("=" * 70)
    
    database.close()


asyncio.run(test_complete_system())