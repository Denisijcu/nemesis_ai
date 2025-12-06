#!/usr/bin/env python3
"""
Test del Dashboard V3.5 - THE BEAST MODE
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_v3 import DashboardV3


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "⚡ NÉMESIS IA DASHBOARD V3.5 - THE BEAST ⚡" + " " * 9 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    print("=" * 70)
    print("🎖️  INICIANDO THE BEAST MODE")
    print("=" * 70)
    print()
    
    # Usar BD del honeypot
    db = ThreatDatabase("data/nemesis_honeypot.db")
    
    print("✅ Base de datos cargada: nemesis_honeypot.db")
    
    # Stats
    stats = db.get_statistics()
    print(f"📊 Amenazas en BD: {stats['total_threats']}")
    print()
    
    # Crear dashboard V3.5
    dashboard = DashboardV3(db, host="0.0.0.0", port=8080)
    
    print("=" * 70)
    print("✨ DASHBOARD V3.5 - THE BEAST MODE")
    print("=" * 70)
    print()
    print("🌐 ACCEDE AL DASHBOARD:")
    print("   http://localhost:8080")
    print()
    print("🎖️  Presiona Ctrl+C para detener")
    print("=" * 70)
    print()
    
    # Iniciar servidor
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Dashboard detenido")