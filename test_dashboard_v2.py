#!/usr/bin/env python3
"""
Test del Dashboard V2 con datos reales
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from database.threat_database import ThreatDatabase
from web.dashboard_v2 import DashboardV2


async def main():
    print("=" * 70)
    print("🌐 INICIANDO DASHBOARD V2")
    print("=" * 70)
    print()
    
    # Usar la BD con datos existentes
    db = ThreatDatabase("data/nemesis_honeypot.db")
    
    print("✅ Base de datos cargada")
    print()
    
    # Crear servidor V2
    dashboard = DashboardV2(db, host="0.0.0.0", port=8080)
    
    print("🚀 Dashboard V2 iniciado en: http://localhost:8080")
    print()
    print("✨ NUEVAS FEATURES:")
    print("   • 📊 Gráficas con Chart.js")
    print("   • ⚡ WebSocket real-time")
    print("   • 🎨 Animaciones mejoradas")
    print("   • 🔔 Notificaciones en vivo")
    print()
    print("📊 Presiona Ctrl+C para detener")
    print("=" * 70)
    print()
    
    # Iniciar servidor
    await dashboard.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Dashboard detenido")