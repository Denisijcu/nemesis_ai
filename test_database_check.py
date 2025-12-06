#!/usr/bin/env python3
"""
Verifica el contenido de las bases de datos
ACTUALIZADO con Honeypot DB
"""

import sys
sys.path.insert(0, 'src')

from database.threat_database import ThreatDatabase
from pathlib import Path


def check_database(db_path: str, db_name: str):
    """Verifica una base de datos"""
    
    if not Path(db_path).exists():
        print(f"❌ {db_name}: No existe")
        print()
        return
    
    print("=" * 70)
    print(f"📊 {db_name}")
    print("=" * 70)
    
    try:
        db = ThreatDatabase(db_path)
        stats = db.get_statistics()
        
        print(f"Total amenazas:  {stats['total_threats']}")
        print(f"IPs bloqueadas:  {stats['total_blocked_ips']}")
        print(f"Últimas 24h:     {stats['threats_last_24h']}")
        print()
        
        if stats['total_threats'] > 0:
            print("Amenazas por tipo:")
            for attack_type, count in stats['threats_by_type'].items():
                print(f"  • {attack_type}: {count}")
            print()
            
            print("Top IPs maliciosas:")
            for ip, count in stats['top_malicious_ips'][:5]:
                print(f"  • {ip}: {count} ataques")
            print()
            
            threats = db.get_threats(limit=5)
            if threats:
                print("Últimas 5 amenazas:")
                for threat in threats:
                    print(f"  • {threat.attack_type} desde {threat.source_ip}")
                    print(f"    {threat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                    if "HONEYPOT" in threat.attack_type:
                        print(f"    🍯 Capturado por honeypot")
                    print()
        else:
            print("⚠️  No hay amenazas registradas")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "VERIFICACIÓN DE BASES DE DATOS" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    databases = [
        ("data/nemesis_complete_test.db", "Dashboard / LogSentinel"),
        ("data/nemesis_v2_test.db", "Dashboard V2"),
        ("data/nemesis_network_test.db", "NetworkSentinel"),
        ("data/nemesis_honeypot.db", "🍯 Honeypot System"),
        ("data/nemesis_sentinel_test.db", "LogSentinel con BD"),
        ("data/nemesis_test.db", "Tests generales"),
    ]
    
    found_databases = 0
    total_threats = 0
    honeypot_threats = 0
    
    for db_path, db_name in databases:
        if Path(db_path).exists():
            found_databases += 1
            
            try:
                db = ThreatDatabase(db_path)
                stats = db.get_statistics()
                threats = stats['total_threats']
                total_threats += threats
                
                if "honeypot" in db_path.lower():
                    honeypot_threats = threats
                
                db.close()
            except:
                pass
        
        check_database(db_path, db_name)
    
    print("=" * 70)
    print("📊 RESUMEN GLOBAL")
    print("=" * 70)
    print(f"Bases de datos encontradas:  {found_databases}/{len(databases)}")
    print(f"Total amenazas acumuladas:   {total_threats}")
    print(f"  • Honeypot:                {honeypot_threats}")
    print(f"  • Otros sistemas:          {total_threats - honeypot_threats}")
    print()
    print("=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("💡 NOTAS:")
    print("   • El Dashboard V2 puede ver CUALQUIERA de estas BDs")
    print("   • Solo cambia la ruta en test_dashboard_v2.py")
    print("   • Las amenazas de honeypot tienen tipo 'HONEYPOT_SSH'")
    print()
    print("🔧 PARA VER HONEYPOT EN DASHBOARD:")
    print("   1. Editar test_dashboard_v2.py")
    print("   2. Cambiar: ThreatDatabase('data/nemesis_honeypot.db')")
    print("   3. Ejecutar: python3 test_dashboard_v2.py")
    print()


if __name__ == "__main__":
    main()