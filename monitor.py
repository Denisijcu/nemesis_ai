import asyncio
import sys
from datetime import datetime
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent

async def monitor():
    agent = NemesisAgent()
    
    print("=" * 60)
    print("🛡️  NÉMESIS - MONITOR EN TIEMPO REAL")
    print("=" * 60)
    print()
    
    logs = [
        '192.168.1.100 - - [04/Dec/2025:10:20:00] "GET /index.html HTTP/1.1" 200',
        '192.168.1.101 - - [04/Dec/2025:10:20:02] "GET /api/products HTTP/1.1" 200',
        '192.168.1.102 - - [04/Dec/2025:10:20:04] "GET /login?user=admin\' OR \'1\'=\'1\'-- HTTP/1.1" 403',
        '192.168.1.103 - - [04/Dec/2025:10:20:06] "GET /search?q=<script>alert(1)</script> HTTP/1.1" 403',
        '192.168.1.104 - - [04/Dec/2025:10:20:08] "GET /api/users?page=1 HTTP/1.1" 200',
        '192.168.1.105 - - [04/Dec/2025:10:20:10] "GET /download?file=../../../etc/passwd HTTP/1.1" 403',
    ]
    
    threats = 0
    
    for log in logs:
        timestamp = datetime.now().strftime("%H:%M:%S")
        verdict = await agent.process_log_line(log)
        
        if verdict and verdict.is_malicious:
            threats += 1
            print(f"[{timestamp}] 🚨 AMENAZA #{threats} DETECTADA")
            print(f"  Tipo: {verdict.attack_type}")
            print(f"  Confianza: {verdict.confidence:.1%}")
            print(f"  Acción: {verdict.recommended_action}")
            print()
        else:
            print(f"[{timestamp}] ✅ Tráfico legítimo")
        
        await asyncio.sleep(2)
    
    print("=" * 60)
    print(f"📊 Total amenazas detectadas: {threats}")
    print("=" * 60)

asyncio.run(monitor())