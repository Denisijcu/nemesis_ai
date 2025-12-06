#!/usr/bin/env python3
"""Test THE BEAST V4.0 - Dashboard completo"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_beast import DashboardBeast


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 12 + "🎖️  THE BEAST V4.0 - COMPLETE SYSTEM  🎖️" + " " * 12 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    print("🚀 Inicializando THE BEAST V4.0...")
    print()
    
    # Database
    db = ThreatDatabase("data/nemesis_honeypot.db")
    
    # Dashboard BEAST
    dashboard = DashboardBeast(db, host="0.0.0.0", port=8080)
    
    print("=" * 70)
    print("✨ THE BEAST V4.0 - CARACTERÍSTICAS")
    print("=" * 70)
    print()
    print("📊 MÓDULOS INTEGRADOS:")
    print("   ✅ ML Brain (98.7%)")
    print("   ✅ Network Sentinel")
    print("   ✅ Honeypots")
    print("   ✅ Traffic Analyzer")
    print("   ✅ IP Reputation")
    print("   ✅ Auto Response")
    print("   ⚛️  Quantum Defense (Kyber + Dilithium)")
    print("   🔗 Blockchain Forensics")
    print("   📄 Legal PDF Generation")
    print("   🌐 Threat Intelligence")
    print("   🚨 Red Button (CERT)")
    print("   🤖 AI vs AI Defense")
    print("   🌐 Multi-Agent Network")
    print()
    print("🎮 CONTROLES DISPONIBLES:")
    print("   • Generate Legal PDF")
    print("   • View Blockchain Evidence")
    print("   • Check Quantum Status")
    print("   • 🚨 RED BUTTON (Emergency)")
    print()
    print("=" * 70)
    print("🌐 Dashboard: http://localhost:8080")
    print("=" * 70)
    print()
    
    # Run
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n✅ THE BEAST detenido")