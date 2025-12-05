import asyncio
import sys
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent

async def test_detection():
    print("=" * 70)
    print("🧪 PRUEBA COMPLETA DEL AGENTE NÉMESIS")
    print("=" * 70)
    print()
    
    agent = NemesisAgent()
    
    tests = [
        {
            "name": "Tráfico Legítimo 1",
            "log": '192.168.1.100 - - [04/Dec/2025:10:00:00] "GET /index.html HTTP/1.1" 200',
            "expected": "LEGÍTIMO"
        },
        {
            "name": "Tráfico Legítimo 2",
            "log": '192.168.1.101 - - [04/Dec/2025:10:00:05] "GET /api/users?page=1&limit=10 HTTP/1.1" 200',
            "expected": "LEGÍTIMO"
        },
        {
            "name": "Búsqueda Legítima (V2 fix)",
            "log": '192.168.1.102 - - [04/Dec/2025:10:00:10] "GET /search?q=python+tutorial HTTP/1.1" 200',
            "expected": "LEGÍTIMO"
        },
        {
            "name": "SQL Injection Clásico",
            "log": '192.168.1.103 - - [04/Dec/2025:10:00:15] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
        {
            "name": "SQL Injection UNION",
            "log": '192.168.1.104 - - [04/Dec/2025:10:00:20] "GET /products?id=1\' UNION SELECT * FROM users-- HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
        {
            "name": "XSS con <script>",
            "log": '192.168.1.105 - - [04/Dec/2025:10:00:25] "GET /search?q=<script>alert(\'XSS\')</script> HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
        {
            "name": "XSS con onerror",
            "log": '192.168.1.106 - - [04/Dec/2025:10:00:30] "GET /comment?text=<img src=x onerror=alert(1)> HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
        {
            "name": "Path Traversal",
            "log": '192.168.1.107 - - [04/Dec/2025:10:00:35] "GET /download?file=../../../etc/passwd HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
        {
            "name": "Command Injection (V2 fix)",
            "log": '192.168.1.108 - - [04/Dec/2025:10:00:40] "GET /ping?host=127.0.0.1; cat /etc/passwd HTTP/1.1" 403',
            "expected": "MALICIOSO"
        },
    ]
    
    correct = 0
    total = len(tests)
    
    for i, test in enumerate(tests, 1):
        print(f"{'─' * 70}")
        print(f"Test {i}/{total}: {test['name']}")
        print(f"Log: {test['log'][:65]}...")
        print(f"Esperado: {test['expected']}")
        
        try:
            verdict = await agent.process_log_line(test['log'])
            
            if verdict:
                actual = "MALICIOSO" if verdict.is_malicious else "LEGÍTIMO"
                is_correct = (actual == test['expected'])
                
                if is_correct:
                    correct += 1
                    status = "✅"
                else:
                    status = "❌"
                
                print(f"{status} Resultado: {actual}")
                print(f"   Confianza: {verdict.confidence:.2%}")
                print(f"   Tipo: {verdict.attack_type}")
                print(f"   Acción: {verdict.recommended_action}")
                
                if verdict.is_malicious:
                    print(f"   🎯 Source IP: {verdict.threat_event.source_ip}")
                    print(f"   📦 Payload: {verdict.threat_event.payload[:50]}...")
            else:
                print("⚠️  Sin veredicto")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
    
    accuracy = (correct / total) * 100
    print("=" * 70)
    print(f"📊 RESUMEN FINAL")
    print("=" * 70)
    print(f"Total de tests: {total}")
    print(f"Correctos: {correct}")
    print(f"Incorrectos: {total - correct}")
    print(f"Accuracy: {accuracy:.1f}%")
    
    if accuracy == 100:
        print("\n🌟 ¡PERFECTO! El agente detecta todo correctamente")
    elif accuracy >= 90:
        print("\n✅ Excelente performance del agente")
    else:
        print("\n⚠️  El agente necesita mejoras")
    
    print("=" * 70)

asyncio.run(test_detection())