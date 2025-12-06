#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')
import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_final import DashboardFinal

async def main():
    print("\n🚀 NÉMESIS IA - THE BEAST FINAL")
    print("✅ Email + Telegram + Mapa + Terminal + Todo\n")
    
    db = ThreatDatabase("data/nemesis_honeypot.db")
    dashboard = DashboardFinal(db, host="0.0.0.0", port=8080)
    
    print("🌐 http://localhost:8080\n")
    await dashboard.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n✅ Detenido")