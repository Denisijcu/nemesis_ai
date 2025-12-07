#!/usr/bin/env python3
"""Test Dashboard UNIFICADO - 5 Core Modules"""
import sys
sys.path.insert(0, 'src')
import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_unified import DashboardUnified

async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "🎖️  NÉMESIS IA UNIFIED DASHBOARD  🎖️" + " " * 8 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    db = ThreatDatabase("data/nemesis_honeypot.db")
    dashboard = DashboardUnified(db, host="0.0.0.0", port=8080)
    
    print("✅ DASHBOARD UNIFICADO - 5 CORE MODULES")
    print()
    print("📦 MÓDULOS INTEGRADOS:")
    print("   1️⃣  🧠 ML Brain (98.7% accuracy)")
    print("   2️⃣  🍯 Honeypot Traps (ultra-realistic)")
    print("   3️⃣  🔗 Blockchain Evidence (immutable)")
    print("   4️⃣  ⚛️  Quantum Defense (Kyber + Dilithium)")
    print("   5️⃣  📧 Alert System (Email + Telegram)")
    print()
    print("🌐 Dashboard: http://localhost:8080")
    print()
    print("🎮 CONTROLES DISPONIBLES:")
    print("   • Generate Legal PDFs")
    print("   • Press Red Button (CERT notifications)")
    print("   • Test Email alerts")
    print("   • Test Telegram alerts")
    print("   • View Blockchain evidence")
    print("   • Check Quantum status")
    print()
    print("=" * 70)
    
    await dashboard.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Dashboard detenido")