#!/usr/bin/env python3
"""
Generador de capturas demo para el honeypot
"""
import sys
sys.path.insert(0, 'src')
import sqlite3
from datetime import datetime, timedelta
import random

# Conectar a BD
conn = sqlite3.connect('data/nemesis_honeypot.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
    CREATE TABLE IF NOT EXISTS honeypot_captures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        ip TEXT NOT NULL,
        port INTEGER NOT NULL,
        protocol TEXT NOT NULL,
        payload TEXT,
        threat_score INTEGER DEFAULT 0
    )
""")

print("✅ Tabla honeypot_captures creada/verificada")
print("🎯 Generando capturas demo...\n")

# IPs de atacantes conocidos
attacker_ips = [
    '45.142.212.61',
    '185.220.101.3',
    '91.219.236.232',
    '89.248.172.16',
    '192.42.116.15',
    '167.99.173.45',
    '203.0.113.50',
    '198.51.100.42'
]

# Payloads típicos
payloads = [
    'SSH-2.0-libssh_0.8.1',
    'admin:admin',
    'root:password',
    'root:12345678',
    'admin:123456',
    'user:password',
    'test:test',
    'admin:root'
]

# Generar 20 capturas
captures = []
base_time = datetime.now() - timedelta(hours=2)

for i in range(20):
    ip = random.choice(attacker_ips)
    payload = random.choice(payloads)
    timestamp = base_time + timedelta(minutes=i*5)
    threat_score = random.randint(20, 85)
    
    cursor.execute("""
        INSERT INTO honeypot_captures 
        (timestamp, ip, port, protocol, payload, threat_score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        timestamp.isoformat(),
        ip,
        2222,
        'SSH',
        payload,
        threat_score
    ))
    
    print(f"🐝 {ip:18s} | SSH:2222 | {payload:25s} | Score: {threat_score}")
    captures.append(cursor.lastrowid)

conn.commit()

# Verificar
cursor.execute('SELECT COUNT(*) FROM honeypot_captures')
total = cursor.fetchone()[0]

print()
print("=" * 70)
print(f"✅ {total} capturas guardadas en honeypot_captures")
print("=" * 70)
print()
print("SIGUIENTE PASO:")
print("1. Reinicia el dashboard: python test_dashboard_unified.py")
print("2. Refresca el navegador")
print("3. Deberías ver las capturas en la sección Honeypot")
print("=" * 70)

conn.close()