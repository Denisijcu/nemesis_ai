#!/usr/bin/env python3
"""
Test del Log Sentinel en tiempo real
"""

import asyncio
import sys
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent
from logs.log_sentinel import LogSentinel


async def test_sentinel():
    print("=" * 70)
    print("👁️  PROBANDO LOG SENTINEL")
    print("=" * 70)
    print()
    
    # Crear archivo de logs de prueba
    test_log = "test_logs.txt"
    
    with open(test_log, 'w') as f:
        f.write('192.168.1.100 - - [04/Dec/2025:10:00:00] "GET /index.html HTTP/1.1" 200\n')
        f.write('192.168.1.101 - - [04/Dec/2025:10:00:05] "GET /api/users HTTP/1.1" 200\n')
        f.write('192.168.1.102 - - [04/Dec/2025:10:00:10] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403\n')
        f.write('192.168.1.103 - - [04/Dec/2025:10:00:15] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403\n')
        f.write('192.168.1.104 - - [04/Dec/2025:10:00:20] "GET /download?file=../../../etc/passwd HTTP/1.1" 403\n')
    
    print(f"✅ Archivo de test creado: {test_log}")
    print()
    
    # Inicializar agente
    agent = NemesisAgent()
    
    # Inicializar sentinel
    sentinel = LogSentinel(agent, test_log, follow=False)
    
    print("🚀 Iniciando análisis de logs...")
    print()
    
    # Procesar logs
    await sentinel.start()
    
    # Mostrar estadísticas
    stats = sentinel.stats
    
    print()
    print("=" * 70)
    print("📊 ESTADÍSTICAS FINALES")
    print("=" * 70)
    print(f"Logs procesados:   {stats['logs_processed']}")
    print(f"Amenazas detectadas: {stats['threats_detected']}")
    print(f"Tasa de detección:  {stats['detection_rate']:.1f}%")
    print("=" * 70)


asyncio.run(test_sentinel())