#!/usr/bin/env python3
"""
Test del FakeSSH Honeypot
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from honeypot.fake_ssh import FakeSSH, SSHAttempt


async def attack_callback(attempt: SSHAttempt):
    """Callback cuando hay un intento de ataque"""
    print(f"\n{'='*70}")
    print(f"🚨 INTENTO DE ATAQUE DETECTADO")
    print(f"{'='*70}")
    print(f"🕐 Timestamp:  {attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 IP:         {attempt.attacker_ip}:{attempt.attacker_port}")
    print(f"👤 Username:   {attempt.username}")
    print(f"🔑 Password:   {attempt.password}")
    print(f"{'='*70}\n")


async def run_honeypot():
    """Ejecuta el honeypot"""
    print("=" * 70)
    print("🍯 FAKE SSH HONEYPOT - TEST")
    print("=" * 70)
    print()
    print("🎯 Honeypot SSH iniciando en puerto 2222...")
    print()
    print("💡 CÓMO PROBAR:")
    print("   En otra terminal ejecuta:")
    print("   ssh root@localhost -p 2222")
    print("   (Intenta cualquier password)")
    print()
    print("   O usa telnet:")
    print("   telnet localhost 2222")
    print()
    print("⚠️  Presiona Ctrl+C para detener")
    print("=" * 70)
    print()
    
    # Crear honeypot con callback
    honeypot = FakeSSH(
        host="0.0.0.0",
        port=2222,
        callback=attack_callback
    )
    
    try:
        # Iniciar servidor
        await honeypot.start()
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo honeypot...")
        await honeypot.stop()
        
        # Mostrar estadísticas
        stats = honeypot.stats
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS FINALES")
        print("=" * 70)
        print(f"📦 Total intentos:      {stats['total_attempts']}")
        print(f"🌐 IPs únicas:          {stats['unique_ips']}")
        print(f"👤 Usernames únicos:    {stats['unique_usernames']}")
        print(f"🔑 Passwords únicos:    {stats['unique_passwords']}")
        print("=" * 70)
        
        if honeypot.attempts:
            print()
            print("Últimos 5 intentos:")
            for attempt in honeypot.attempts[-5:]:
                print(f"  • {attempt.username}/{attempt.password} desde {attempt.attacker_ip}")
        
        print()
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "FAKE SSH HONEYPOT" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    asyncio.run(run_honeypot())


if __name__ == "__main__":
    main()