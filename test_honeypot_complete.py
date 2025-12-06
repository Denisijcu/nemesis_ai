#!/usr/bin/env python3
"""
Test del Honeypot COMPLETO
Con profiler + BD + alertas
"""

import sys
sys.path.insert(0, 'src')

import asyncio
import yaml
from honeypot.fake_ssh import FakeSSH, SSHAttempt
from honeypot.attacker_profiler import AttackerProfiler
from honeypot.honeypot_logger import HoneypotLogger
from database.threat_database import ThreatDatabase
from alerts.alert_manager import AlertManager


class HoneypotSystem:
    """Sistema de Honeypot Completo"""
    
    def __init__(self, use_database: bool = True, use_alerts: bool = False):
        """
        Inicializa el sistema completo
        
        Args:
            use_database: Si True, guarda en BD
            use_alerts: Si True, envía alertas
        """
        # Componentes base
        self.profiler = AttackerProfiler()
        
        # Base de datos
        self.database = None
        if use_database:
            self.database = ThreatDatabase("data/nemesis_honeypot.db")
        
        # Alertas
        self.alert_manager = None
        if use_alerts:
            try:
                with open('config/alerts.yaml', 'r') as f:
                    config = yaml.safe_load(f)
                self.alert_manager = AlertManager(config)
            except:
                print("⚠️  No se pudo cargar config de alertas")
        
        # Logger
        self.logger = HoneypotLogger(
            database=self.database,
            alert_manager=self.alert_manager
        )
        
        # Honeypot
        self.honeypot = FakeSSH(
            host="0.0.0.0",
            port=2222,
            callback=self._on_attack
        )
    
    async def _on_attack(self, attempt: SSHAttempt):
        """Callback cuando hay ataque"""
        
        # 1. Actualizar perfil
        profile = self.profiler.process_attempt(
            ip=attempt.attacker_ip,
            username=attempt.username,
            password=attempt.password,
            timestamp=attempt.timestamp
        )
        
        # 2. Mostrar en consola
        print(f"\n{'='*70}")
        print(f"🚨 ATAQUE #{profile.total_attempts} desde {attempt.attacker_ip}")
        print(f"{'='*70}")
        print(f"👤 Username:        {attempt.username}")
        print(f"🔑 Password:        {attempt.password}")
        print(f"🎯 Patrón:          {profile.attack_pattern}")
        print(f"📊 Sofisticación:   {profile.sophistication_level}")
        print(f"⚠️  Threat Score:    {profile.threat_score:.1f}/100")
        
        # 3. Guardar en BD y enviar alertas
        await self.logger.log_attempt(
            ip=attempt.attacker_ip,
            username=attempt.username,
            password=attempt.password,
            service="SSH",
            profile_data=profile.to_dict()
        )
        
        # 4. Alertas especiales
        if profile.threat_score > 50:
            print(f"🔴 ALERTA: Atacante peligroso!")
            print(f"   💾 Guardado en BD")
            if profile.threat_score > 60:
                print(f"   📱 Alerta enviada")
                print(f"   🚫 IP bloqueada")
        
        print(f"{'='*70}\n")
    
    async def start(self):
        """Inicia el sistema"""
        try:
            await self.honeypot.start()
        except KeyboardInterrupt:
            await self.stop()
    
    async def stop(self):
        """Detiene y muestra estadísticas"""
        print("\n\n⏹️  Deteniendo sistema...")
        await self.honeypot.stop()
        
        # Stats del profiler
        profiler_stats = self.profiler.get_statistics()
        
        # Stats del logger
        logger_stats = self.logger.get_stats()
        
        # Stats del honeypot
        honeypot_stats = self.honeypot.stats
        
        # Stats de la BD
        db_stats = None
        if self.database:
            db_stats = self.database.get_statistics()
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS FINALES DEL SISTEMA")
        print("=" * 70)
        print()
        
        print("🍯 Honeypot:")
        print(f"   Total intentos:   {honeypot_stats['total_attempts']}")
        print(f"   IPs únicas:       {honeypot_stats['unique_ips']}")
        print()
        
        print("🔍 Profiler:")
        print(f"   Atacantes:        {profiler_stats['total_attackers']}")
        print(f"   Promedio/IP:      {profiler_stats['avg_attempts_per_ip']}")
        print(f"   Threat promedio:  {profiler_stats.get('avg_threat_score', 0):.1f}/100")
        print()
        
        if profiler_stats['patterns']:
            print("   Patrones:")
            for pattern, count in profiler_stats['patterns'].items():
                print(f"     • {pattern}: {count}")
            print()
        
        print("📝 Logger:")
        print(f"   Guardados en BD:  {logger_stats['attempts_logged']}")
        print(f"   Alertas enviadas: {logger_stats['alerts_sent']}")
        print()
        
        if db_stats:
            print("💾 Base de Datos:")
            print(f"   Total amenazas:   {db_stats['total_threats']}")
            print(f"   IPs bloqueadas:   {db_stats['total_blocked_ips']}")
            print()
        
        # Top atacantes
        top = self.profiler.get_top_attackers(limit=3)
        if top:
            print("🔴 Top 3 Atacantes:")
            for i, profile in enumerate(top, 1):
                print(f"   {i}. {profile.ip}")
                print(f"      Intentos: {profile.total_attempts}")
                print(f"      Patrón: {profile.attack_pattern}")
                print(f"      Score: {profile.threat_score:.1f}/100")
            print()
        
        print("=" * 70)
        
        if self.database:
            self.database.close()


async def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "HONEYPOT SYSTEM - COMPLETO" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("=" * 70)
    print("🍯 SISTEMA DE HONEYPOT COMPLETO")
    print("=" * 70)
    print()
    print("✨ CARACTERÍSTICAS:")
    print("   ✅ FakeSSH activo")
    print("   ✅ Profiler de atacantes")
    print("   ✅ Logger a base de datos")
    print("   ✅ Alertas automáticas (si configurado)")
    print("   ✅ Bloqueo de IPs peligrosas")
    print()
    print("🎯 Puerto: 2222")
    print()
    print("💡 PROBAR:")
    print("   Terminal 2: python3 simulate_attacks.py")
    print()
    print("=" * 70)
    print()
    
    # Crear sistema (con BD, sin alertas por defecto)
    system = HoneypotSystem(
        use_database=True,
        use_alerts=False  # Cambiar a True si quieres alertas
    )
    
    await system.start()


if __name__ == "__main__":
    asyncio.run(main())