#!/usr/bin/env python3
"""Test THE BEAST V5.0 COMPLETE con notificaciones"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_complete import DashboardComplete


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "🎖️  THE BEAST V5.0 COMPLETE  🎖️" + " " * 9 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    db = ThreatDatabase("data/nemesis_honeypot.db")
    dashboard = DashboardComplete(db, host="0.0.0.0", port=8080)
    
    print("✅ THE BEAST V5.0 COMPLETE")
    print()
    print("📦 MÓDULOS INTEGRADOS:")
    print("   ✅ Caps 1-6:  ML + Network + Honeypots + Logs")
    print("   ✅ Caps 7-8:  Quantum Defense (Kyber + Dilithium)")
    print("   ✅ Caps 9-10: Blockchain + Legal PDFs")
    print("   ✅ Caps 11-12: Threat Intel + Red Button")
    print("   ✅ Caps 13-14: AI vs AI + Multi-Agent")
    print("   ✅ NUEVO: Email + Telegram Notifications")
    print()
    print("🌐 Dashboard: http://localhost:8080")
    print()
    print("📧 NOTIFICACIONES:")
    print("   • Email configurado: denisijcu266@gmail.com")
    print("   • Telegram bot activo")
    print("   • Test buttons disponibles en dashboard")
    print()
    print("=" * 70)
    
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Dashboard detenido")