#!/usr/bin/env python3
"""
Verifica el contenido de las bases de datos
"""

import sys
sys.path.insert(0, 'src')

from database.threat_database import ThreatDatabase
from pathlib import Path


def check_database(db_path: str, db_name: str):
    """Verifica una base de datos"""
    
    if not Path(db_path).exists():
        print(f"❌ {db_name}: No existe")
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
            
            # Últimas 5 amenazas
            threats = db.get_threats(limit=5)
            if threats:
                print("Últimas 5 amenazas:")
                for threat in threats:
                    print(f"  • {threat.attack_type} desde {threat.source_ip}")
                    print(f"    {threat.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("⚠️  No hay amenazas registradas")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "VERIFICACIÓN DE BASES DE DATOS" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    # Bases de datos a verificar
    databases = [
        ("data/nemesis_complete_test.db", "Dashboard / LogSentinel"),
        ("data/nemesis_v2_test.db", "Dashboard V2"),
        ("data/nemesis_network_test.db", "NetworkSentinel"),
        ("data/nemesis_sentinel_test.db", "LogSentinel con BD"),
        ("data/nemesis_test.db", "Tests generales"),
    ]
    
    for db_path, db_name in databases:
        check_database(db_path, db_name)
    
    print("=" * 70)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 70)
    print()
    print("💡 NOTA:")
    print("   El Dashboard V2 puede ver CUALQUIERA de estas bases de datos")
    print("   Solo necesitas cambiar la ruta en test_dashboard_v2.py")
    print()


if __name__ == "__main__":
    main()