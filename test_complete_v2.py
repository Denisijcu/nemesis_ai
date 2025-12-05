#!/usr/bin/env python3
"""
Test completo V2: Sentinel + BD + Alertas + Dashboard Real-time
"""

import asyncio
import sys
import yaml
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent
from logs.log_sentinel import LogSentinel
from database.threat_database import ThreatDatabase
from alerts.alert_manager import AlertManager
from web.dashboard_v2 import DashboardV2


async def write_logs_continuously(log_file: str, dashboard: DashboardV2):
    """Escribe logs cada 3 segundos para simular tráfico real"""
    
    logs = [
        '192.168.1.100 - - [04/Dec/2025:14:00:00] "GET /index.html HTTP/1.1" 200\n',
        '192.168.1.101 - - [04/Dec/2025:14:00:03] "GET /api/products HTTP/1.1" 200\n',
        '192.168.1.102 - - [04/Dec/2025:14:00:06] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403\n',
        '192.168.1.103 - - [04/Dec/2025:14:00:09] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403\n',
        '192.168.1.104 - - [04/Dec/2025:14:00:12] "GET /api/users HTTP/1.1" 200\n',
        '192.168.1.105 - - [04/Dec/2025:14:00:15] "GET /download?file=../../../etc/passwd HTTP/1.1" 403\n',
        '192.168.1.106 - - [04/Dec/2025:14:00:18] "GET /admin?id=1; DROP TABLE users-- HTTP/1.1" 403\n',
    ]
    
    await asyncio.sleep(5)  # Esperar a que todo inicie
    
    print("📝 Iniciando generación de logs (cada 3 segundos)...")
    print()
    
    for i, log in enumerate(logs, 1):
        with open(log_file, 'a') as f:
            f.write(log)
        print(f"✅ Log {i}/{len(logs)} escrito")
        await asyncio.sleep(3)  # Cada 3 segundos
    
    print()
    print("✅ Todos los logs escritos")
    print("💡 El dashboard debería mostrar las amenazas en tiempo real")


async def test_complete_v2():
    print("=" * 70)
    print("🚀 SISTEMA COMPLETO V2 CON DASHBOARD REAL-TIME")
    print("=" * 70)
    print()
    
    # Crear archivo de logs vacío
    test_log = "test_realtime_v2.txt"
    with open(test_log, 'w') as f:
        f.write("")
    
    print(f"✅ Archivo de logs creado: {test_log}")
    print()
    
    # Cargar config de alertas
    try:
        with open('config/alerts.yaml', 'r') as f:
            alerts_config = yaml.safe_load(f)
        print("✅ Configuración de alertas cargada")
    except:
        print("⚠️  Sin config de alertas")
        alerts_config = {}
    
    print()
    
    # Inicializar componentes
    print("📦 Inicializando componentes...")
    agent = NemesisAgent()
    database = ThreatDatabase("data/nemesis_v2_test.db")
    alert_manager = AlertManager(alerts_config)
    dashboard = DashboardV2(database, host="0.0.0.0", port=8080)
    sentinel = LogSentinel(
        agent, 
        test_log, 
        follow=True,  # ← IMPORTANTE: tail -f para tiempo real
        database=database, 
        alert_manager=alert_manager,
        dashboard=dashboard  # ← Nuevo parámetro
    )
    
    print()
    print("=" * 70)
    print("✨ SISTEMA V2 INICIADO")
    print("=" * 70)
    print()
    print("🌐 Dashboard: http://localhost:8080")
    print("📱 Alertas: Telegram + Email")
    print("💾 Base de datos: SQLite")
    print("⚡ WebSocket: Real-time")
    print()
    print("📝 Los logs se generarán cada 3 segundos")
    print("🔴 Abre el dashboard en tu navegador AHORA")
    print()
    print("⏰ El sistema se ejecutará por 30 segundos")
    print("   Presiona Ctrl+C para detener antes")
    print("=" * 70)
    print()
    
    # Ejecutar todo en paralelo
    try:
        await asyncio.wait_for(
            asyncio.gather(
                dashboard.run(),
                sentinel.start(),
                write_logs_continuously(test_log, dashboard)
            ),
            timeout=30.0
        )
    except asyncio.TimeoutError:
        print("\n⏰ Timeout alcanzado, deteniendo...")
        await sentinel.stop()
    except KeyboardInterrupt:
        print("\n\n⏹️  Detenido manualmente")
        await sentinel.stop()
    
    # Mostrar estadísticas finales
    stats = sentinel.stats
    db_stats = database.get_statistics()
    
    print()
    print("=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    print(f"📄 Logs procesados:     {stats['logs_processed']}")
    print(f"🚨 Amenazas detectadas: {stats['threats_detected']}")
    print(f"💾 Guardadas en BD:     {db_stats['total_threats']}")
    print(f"📱 Alertas enviadas:    {stats['threats_detected']}")
    print(f"🌐 Broadcasts:          {stats['threats_detected']}")
    print()
    
    if stats['threats_detected'] > 0:
        print("Amenazas por tipo:")
        for attack_type, count in db_stats['threats_by_type'].items():
            print(f"  • {attack_type}: {count}")
    
    print()
    print("=" * 70)
    print("✅ TEST COMPLETADO")
    print("=" * 70)
    
    database.close()


asyncio.run(test_complete_v2())