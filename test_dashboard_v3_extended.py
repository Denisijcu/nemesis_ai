#!/usr/bin/env python3
"""Test Dashboard V3.5 Extended - THE BEAST V4.0"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_v3_extended import DashboardV3Extended


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 8 + "🎖️  THE BEAST V4.0 - EXTENDED  🎖️" + " " * 9 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    db = ThreatDatabase("data/nemesis_honeypot.db")
    dashboard = DashboardV3Extended(db, host="0.0.0.0", port=8080)
    
    print("✅ Dashboard THE BEAST V4.0 Extended")
    print("📊 Con todos los módulos nuevos integrados")
    print("🌐 http://localhost:8080")
    print()
    
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Dashboard detenido")