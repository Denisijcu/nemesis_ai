#!/usr/bin/env python3
"""
Test del AttackerProfiler con FakeSSH
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from honeypot.fake_ssh import FakeSSH, SSHAttempt
from honeypot.attacker_profiler import AttackerProfiler


class HoneypotWithProfiler:
    """Honeypot integrado con Profiler"""
    
    def __init__(self):
        self.profiler = AttackerProfiler()
        self.honeypot = FakeSSH(
            host="0.0.0.0",
            port=2222,
            callback=self._on_attack
        )
    
    async def _on_attack(self, attempt: SSHAttempt):
        """Callback cuando hay ataque"""
        
        # Actualizar perfil
        profile = self.profiler.process_attempt(
            ip=attempt.attacker_ip,
            username=attempt.username,
            password=attempt.password,
            timestamp=attempt.timestamp
        )
        
        # Mostrar información
        print(f"\n{'='*70}")
        print(f"🚨 ATAQUE #{profile.total_attempts} desde {attempt.attacker_ip}")
        print(f"{'='*70}")
        print(f"👤 Username:        {attempt.username}")
        print(f"🔑 Password:        {attempt.password}")
        print(f"🎯 Patrón:          {profile.attack_pattern}")
        print(f"📊 Sofisticación:   {profile.sophistication_level}")
        print(f"⚠️  Threat Score:    {profile.threat_score:.1f}/100")
        print(f"{'='*70}\n")
        
        # Alerta si threat score alto
        if profile.threat_score > 50:
            print(f"🔴 ALERTA: Atacante peligroso detectado!")
            print(f"   IP: {profile.ip}")
            print(f"   Intentos: {profile.total_attempts}")
            print(f"   Score: {profile.threat_score:.1f}")
            print()
    
    async def start(self):
        """Inicia el honeypot"""
        try:
            await self.honeypot.start()
        except KeyboardInterrupt:
            await self.stop()
    
    async def stop(self):
        """Detiene y muestra estadísticas"""
        print("\n\n⏹️  Deteniendo honeypot...")
        await self.honeypot.stop()
        
        # Estadísticas del profiler
        stats = self.profiler.get_statistics()
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS DE PERFILADO")
        print("=" * 70)
        print(f"🌐 Total atacantes:       {stats['total_attackers']}")
        print(f"📦 Total intentos:        {stats['total_attempts']}")
        print(f"📈 Promedio por IP:       {stats['avg_attempts_per_ip']}")
        print(f"⚠️  Threat score promedio: {stats.get('avg_threat_score', 0):.1f}")
        print()
        
        if stats['patterns']:
            print("Patrones de ataque:")
            for pattern, count in stats['patterns'].items():
                print(f"  • {pattern}: {count}")
            print()
        
        if stats['sophistication']:
            print("Nivel de sofisticación:")
            for level, count in stats['sophistication'].items():
                print(f"  • {level}: {count}")
            print()
        
        # Top atacantes
        top = self.profiler.get_top_attackers(limit=5)
        if top:
            print("🔴 Top 5 Atacantes más peligrosos:")
            for i, profile in enumerate(top, 1):
                print(f"  {i}. {profile.ip}")
                print(f"     Intentos: {profile.total_attempts}")
                print(f"     Patrón: {profile.attack_pattern}")
                print(f"     Score: {profile.threat_score:.1f}/100")
                print()
        
        print("=" * 70)


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "HONEYPOT CON ATTACKER PROFILER" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("=" * 70)
    print("🍯 HONEYPOT + PROFILER")
    print("=" * 70)
    print()
    print("🎯 Iniciando honeypot con perfilado de atacantes...")
    print()
    print("💡 PROBAR:")
    print("   ssh admin@localhost -p 2222")
    print("   (Intenta varios usuarios/passwords para ver el perfil)")
    print()
    print("=" * 70)
    print()
    
    system = HoneypotWithProfiler()
    await system.start()


if __name__ == "__main__":
    asyncio.run(main())