#!/usr/bin/env python3
"""
Test del Response System - Sistema completo
"""

import sys
sys.path.insert(0, 'src')

from response.response_sentinel import ResponseSentinel
from database.threat_database import ThreatDatabase


def test_basic_response():
    """Test de respuesta básica"""
    print("=" * 70)
    print("TEST 1: RESPUESTAS BÁSICAS POR SEVERIDAD")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True)
    
    test_cases = [
        ("203.0.113.1", "SQL_INJECTION", "CRITICAL", 0.95),
        ("203.0.113.2", "PORT_SCAN", "HIGH", 0.90),
        ("203.0.113.3", "BRUTE_FORCE", "MEDIUM", 0.85),
        ("203.0.113.4", "SUSPICIOUS", "LOW", 0.70),
    ]
    
    print("\n🎯 Procesando amenazas...\n")
    
    for ip, threat_type, severity, confidence in test_cases:
        response = sentinel.process_threat(
            source_ip=ip,
            threat_type=threat_type,
            severity=severity,
            confidence=confidence
        )
        
        severity_emoji = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "CRITICAL": "🔴"
        }.get(severity, "⚪")
        
        actions_str = ", ".join([a.value for a in response.actions])
        
        print(f"{severity_emoji} {ip} - {threat_type}")
        print(f"   Severidad: {severity}")
        print(f"   Acciones:  {actions_str}")
        print(f"   Status:    {response.status.value}")
        print()
    
    print()


def test_with_database():
    """Test con ThreatDatabase integrada"""
    print("=" * 70)
    print("TEST 2: INTEGRACIÓN CON THREAT DATABASE")
    print("=" * 70)
    
    db = ThreatDatabase("data/test_response.db")
    sentinel = ResponseSentinel(database=db, dry_run=True, auto_respond=True)
    
    print("\n🚨 Simulando amenazas con auto-response...\n")
    
    # Amenazas críticas - SIN usar la base de datos directamente
    # El ResponseSentinel ya maneja el guardado automáticamente
    critical_threats = [
        ("45.142.212.61", "DDOS", "CRITICAL"),
        ("198.51.100.88", "DATA_EXFILTRATION", "CRITICAL"),
    ]
    
    for ip, threat_type, severity in critical_threats:
        # Procesar con ResponseSentinel
        # (el engine ya guarda en BD automáticamente si tiene database)
        response = sentinel.process_threat(
            source_ip=ip,
            threat_type=threat_type,
            severity=severity,
            confidence=0.95
        )
        
        print(f"🔴 {ip} - {threat_type}")
        print(f"   Response ID: {response.id}")
        print(f"   Acciones:    {[a.value for a in response.actions]}")
        print(f"   Status:      {response.status.value}")
        print(f"   Blocked:     {ip in sentinel.executor.get_blocked_ips()}")
        print()
    
    # Estadísticas
    stats = db.get_statistics()
    print(f"📊 Estadísticas BD:")
    print(f"   Total amenazas: {stats['total_threats']}")
    print(f"   IPs bloqueadas: {stats['total_blocked_ips']}")
    
    print()


def test_strikes_system():
    """Test del sistema de strikes"""
    print("=" * 70)
    print("TEST 3: SISTEMA DE STRIKES (3 STRIKES = BLOCK)")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True)
    
    attacker_ip = "203.0.113.100"
    
    print(f"\n⚠️  Simulando amenazas MEDIUM desde {attacker_ip}...\n")
    
    # Generar 3 amenazas MEDIUM (activa strikes)
    for i in range(1, 4):
        response = sentinel.process_threat(
            source_ip=attacker_ip,
            threat_type="SUSPICIOUS_ACTIVITY",
            severity="MEDIUM",
            confidence=0.80
        )
        
        strikes = sentinel.engine.get_strikes(attacker_ip)
        actions = [a.value for a in response.actions]
        
        print(f"   Strike {i}/3")
        print(f"      Strikes actuales: {strikes}")
        print(f"      Acciones:         {actions}")
        
        if "BLOCK_IP" in actions:
            print(f"      ⚠️  ESCALADO: IP bloqueada después de 3 strikes!")
        
        print()
    
    print()


def test_whitelist():
    """Test de whitelist"""
    print("=" * 70)
    print("TEST 4: WHITELIST (IPs PROTEGIDAS)")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True)
    
    trusted_ip = "8.8.8.8"
    
    print(f"\n✅ Añadiendo {trusted_ip} a whitelist...\n")
    sentinel.whitelist_ip(trusted_ip)
    
    # Intentar bloquear IP en whitelist
    print(f"🚨 Procesando amenaza CRITICAL desde IP whitelisted...\n")
    
    response = sentinel.process_threat(
        source_ip=trusted_ip,
        threat_type="DDOS",
        severity="CRITICAL",
        confidence=0.95
    )
    
    print(f"   IP:       {trusted_ip}")
    print(f"   Acciones: {[a.value for a in response.actions]}")
    print(f"   Blocked:  {trusted_ip in sentinel.executor.get_blocked_ips()}")
    
    # Verificar que solo fue LOG_ONLY
    from response.response_engine import ResponseAction
    if response.actions == [ResponseAction.LOG_ONLY]:
        print(f"\n   ✅ IP protegida: Solo LOG, sin bloqueo")
    
    print()


def test_rollback():
    """Test de rollback"""
    print("=" * 70)
    print("TEST 5: ROLLBACK DE RESPUESTAS")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True)
    
    test_ip = "203.0.113.50"
    
    print(f"\n1. Bloqueando {test_ip}...\n")
    
    response = sentinel.process_threat(
        source_ip=test_ip,
        threat_type="PORT_SCAN",
        severity="HIGH",
        confidence=0.90
    )
    
    print(f"   Response ID: {response.id}")
    print(f"   Acciones:    {[a.value for a in response.actions]}")
    print(f"   Bloqueada:   {test_ip in sentinel.executor.get_blocked_ips()}")
    
    print(f"\n2. Haciendo rollback de respuesta #{response.id}...\n")
    
    success = sentinel.rollback_response(response.id)
    
    print(f"   Rollback exitoso: {success}")
    print(f"   Bloqueada:        {test_ip in sentinel.executor.get_blocked_ips()}")
    print(f"   Status:           {response.status.value}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 6: ESTADÍSTICAS DEL SISTEMA")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True, auto_respond=True)
    
    # Generar actividad
    test_threats = [
        ("203.0.113.1", "DDOS", "CRITICAL"),
        ("203.0.113.2", "PORT_SCAN", "HIGH"),
        ("203.0.113.3", "BRUTE_FORCE", "MEDIUM"),
        ("203.0.113.4", "SQL_INJECTION", "HIGH"),
        ("203.0.113.5", "XSS", "MEDIUM"),
    ]
    
    for ip, threat_type, severity in test_threats:
        sentinel.process_threat(ip, threat_type, severity, 0.90)
    
    # Obtener estadísticas
    stats = sentinel.get_full_statistics()
    
    print("\n📊 ESTADÍSTICAS COMPLETAS:\n")
    
    print("   Sentinel:")
    for key, value in stats['sentinel'].items():
        print(f"      {key:25} {value}")
    
    print("\n   Engine:")
    for key, value in stats['engine'].items():
        print(f"      {key:25} {value}")
    
    print("\n   Executor:")
    for key, value in stats['executor'].items():
        if key != "by_action_type":
            print(f"      {key:25} {value}")
    
    if stats['executor']['by_action_type']:
        print("\n   Acciones ejecutadas:")
        for action, count in stats['executor']['by_action_type'].items():
            print(f"      {action:25} {count}")
    
    print()


def test_full_report():
    """Test de reporte completo"""
    print("=" * 70)
    print("TEST 7: REPORTE COMPLETO")
    print("=" * 70)
    
    sentinel = ResponseSentinel(dry_run=True, auto_respond=True)
    
    # Generar actividad
    for i in range(5):
        sentinel.process_threat(
            source_ip=f"203.0.113.{i}",
            threat_type="ATTACK",
            severity=["LOW", "MEDIUM", "HIGH", "CRITICAL"][i % 4],
            confidence=0.90
        )
    
    # Generar reporte
    report = sentinel.generate_report()
    
    print(f"\n📊 REPORTE COMPLETO:\n")
    print(f"   Timestamp: {report['timestamp']}")
    
    print(f"\n   Amenazas procesadas:    {report['statistics']['sentinel']['threats_processed']}")
    print(f"   Respuestas ejecutadas:  {report['statistics']['sentinel']['responses_executed']}")
    print(f"   Respuestas automáticas: {report['statistics']['sentinel']['auto_responses']}")
    
    print(f"\n   IPs bloqueadas:      {len(report['active_blocks']['blocked_ips'])}")
    print(f"   Rate limited:        {len(report['active_blocks']['rate_limited_ips'])}")
    
    if report['recent_responses']:
        print(f"\n   Últimas 3 respuestas:")
        for resp in report['recent_responses'][:3]:
            print(f"      • {resp['ip']} - {resp['threat_type']} ({resp['severity']})")
            print(f"        Acciones: {', '.join(resp['actions'])}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "AUTOMATED RESPONSE SYSTEM - TESTS" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_response()
    print()
    
    test_with_database()
    print()
    
    test_strikes_system()
    print()
    
    test_whitelist()
    print()
    
    test_rollback()
    print()
    
    test_statistics()
    print()
    
    test_full_report()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("📊 CAPÍTULO 8 COMPLETADO:")
    print("   ✅ ResponseEngine (políticas + strikes)")
    print("   ✅ ActionExecutor (firewall + rate limit)")
    print("   ✅ ResponseSentinel (integración total)")
    print()
    print("🎯 Sistema completo de respuesta automática funcionando!")
    print()


if __name__ == "__main__":
    main()