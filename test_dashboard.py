#!/usr/bin/env python3
"""
Test del Dashboard Web
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_server import DashboardServer


async def main():
    print("=" * 70)
    print("🌐 INICIANDO DASHBOARD WEB")
    print("=" * 70)
    print()
    
    # Usar la BD que ya tiene datos
    db = ThreatDatabase("data/nemesis_sentinel_test.db")
    
    print("✅ Base de datos cargada")
    print()
    
    # Crear servidor
    server = DashboardServer(db, host="0.0.0.0", port=8080)
    
    print("🚀 Dashboard iniciado en: http://localhost:8080")
    print()
    print("📊 Presiona Ctrl+C para detener")
    print("=" * 70)
    print()
    
    # Iniciar servidor
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Dashboard detenido")