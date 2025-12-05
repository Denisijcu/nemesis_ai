#!/usr/bin/env python3
"""
Test del Log Sentinel en tiempo real con tail -f
"""

import asyncio
import sys
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent
from logs.log_sentinel import LogSentinel


async def write_logs_continuously(log_file: str):
    """Escribe logs cada 2 segundos para simular tráfico real"""
    
    logs = [
        '192.168.1.100 - - [04/Dec/2025:11:00:00] "GET /index.html HTTP/1.1" 200\n',
        '192.168.1.101 - - [04/Dec/2025:11:00:02] "GET /api/products HTTP/1.1" 200\n',
        '192.168.1.102 - - [04/Dec/2025:11:00:04] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403\n',
        '192.168.1.103 - - [04/Dec/2025:11:00:06] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403\n',
        '192.168.1.104 - - [04/Dec/2025:11:00:08] "GET /api/users HTTP/1.1" 200\n',
        '192.168.1.105 - - [04/Dec/2025:11:00:10] "GET /download?file=../../../etc/passwd HTTP/1.1" 403\n',
    ]
    
    await asyncio.sleep(2)  # Esperar a que el sentinel inicie
    
    for i, log in enumerate(logs, 1):
        with open(log_file, 'a') as f:
            f.write(log)
        print(f"📝 Log {i}/{len(logs)} escrito")
        await asyncio.sleep(2)
    
    print("✅ Todos los logs escritos")


async def test_realtime():
    print("=" * 70)
    print("👁️  PROBANDO LOG SENTINEL EN TIEMPO REAL (tail -f)")
    print("=" * 70)
    print()
    
    test_log = "test_logs_realtime.txt"
    
    # Crear archivo vacío
    with open(test_log, 'w') as f:
        f.write("")
    
    print(f"✅ Archivo de test creado: {test_log}")
    print()
    
    # Inicializar agente
    agent = NemesisAgent()
    
    # Inicializar sentinel con follow=True
    sentinel = LogSentinel(agent, test_log, follow=True)
    
    print("🚀 Iniciando monitoreo en tiempo real...")
    print("   (Los logs se escribirán cada 2 segundos)")
    print()
    
    # Ejecutar ambos en paralelo
    try:
        await asyncio.wait_for(
            asyncio.gather(
                sentinel.start(),
                write_logs_continuously(test_log)
            ),
            timeout=20.0
        )
    except asyncio.TimeoutError:
        print("\n⏰ Timeout alcanzado, deteniendo...")
        await sentinel.stop()
    
    # Mostrar estadísticas
    stats = sentinel.stats
    
    print()
    print("=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    print(f"Logs procesados:     {stats['logs_processed']}")
    print(f"Amenazas detectadas: {stats['threats_detected']}")
    print(f"Tasa de detección:   {stats['detection_rate']:.1f}%")
    print("=" * 70)


asyncio.run(test_realtime())