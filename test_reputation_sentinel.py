#!/usr/bin/env python3
"""
Test del Reputation Sentinel - Sistema completo
"""

import sys
sys.path.insert(0, 'src')

import time
from reputation.reputation_sentinel import ReputationSentinel
from database.threat_database import ThreatDatabase


def test_basic_integration():
    """Test de integración básica"""
    print("=" * 70)
    print("TEST 1: INTEGRACIÓN BÁSICA")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    test_ips = [
        "8.8.8.8",           # Google DNS
        "203.0.113.50",      # IP pública
        "192.168.1.100",     # IP privada
        "125.50.100.20",     # Russia (high risk)
    ]
    
    print("\n🔍 Verificando IPs...\n")
    
    for ip in test_ips:
        rep = sentinel.check_ip(ip)
        
        threat_emoji = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "CRITICAL": "🔴"
        }.get(rep.threat_level, "⚪")
        
        print(f"{threat_emoji} {ip}")
        print(f"   Score:   {rep.reputation_score}/100")
        print(f"   Threat:  {rep.threat_level}")
        print(f"   Country: {rep.country}")
        print()
    
    print()


def test_with_threat_database():
    """Test con ThreatDatabase integrada"""
    print("=" * 70)
    print("TEST 2: INTEGRACIÓN CON THREAT DATABASE")
    print("=" * 70)
    
    threat_db = ThreatDatabase("data/test_reputation_threats.db")
    sentinel = ReputationSentinel(threat_database=threat_db)
    
    # IPs maliciosas
    malicious_ips = [
        "125.50.100.20",  # Russia - baja reputación
        "75.200.30.5",    # China - baja reputación
        "100.150.75.10",  # Russia
    ]
    
    print("\n🚨 Verificando IPs maliciosas...\n")
    
    for ip in malicious_ips:
        rep = sentinel.check_ip(ip)
        print(f"🔴 {ip}: {rep.reputation_score}/100 ({rep.threat_level})")
    
    # Ver amenazas guardadas
    stats = threat_db.get_statistics()
    
    print(f"\n📊 Amenazas en ThreatDatabase: {stats['total_threats']}")
    
    threats = threat_db.get_threats(limit=5)
    if threats:
        print(f"\n   Últimas amenazas:")
        for t in threats[:3]:
            print(f"      • {t.attack_type} desde {t.source_ip}")
    
    print()


def test_whitelist_blacklist():
    """Test de whitelist/blacklist"""
    print("=" * 70)
    print("TEST 3: WHITELIST Y BLACKLIST")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    good_ip = "8.8.8.8"
    bad_ip = "203.0.113.666"
    
    print(f"\n✅ Añadiendo {good_ip} a WHITELIST...")
    sentinel.whitelist_ip(good_ip, reason="Trusted DNS server")
    
    print(f"🚫 Añadiendo {bad_ip} a BLACKLIST...")
    sentinel.blacklist_ip(bad_ip, reason="Known attacker", severity="CRITICAL")
    
    print("\n📋 Verificando reputaciones...\n")
    
    rep_good = sentinel.check_ip(good_ip)
    rep_bad = sentinel.check_ip(bad_ip)
    
    print(f"   {good_ip}:")
    print(f"      Score:       {rep_good.reputation_score}/100")
    print(f"      Whitelisted: {rep_good.is_whitelisted}")
    
    print(f"\n   {bad_ip}:")
    print(f"      Score:       {rep_bad.reputation_score}/100")
    print(f"      Blacklisted: {rep_bad.is_blacklisted}")
    
    print()


def test_bulk_check():
    """Test de verificación en masa"""
    print("=" * 70)
    print("TEST 4: VERIFICACIÓN EN MASA")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    ips_to_check = [
        "8.8.8.8",
        "1.1.1.1",
        "203.0.113.1",
        "203.0.113.2",
        "203.0.113.3",
        "125.50.100.20",
        "192.168.1.1",
        "10.0.0.1"
    ]
    
    print(f"\n🔍 Verificando {len(ips_to_check)} IPs en bulk...\n")
    
    start = time.time()
    results = sentinel.bulk_check(ips_to_check)
    elapsed = time.time() - start
    
    print(f"⏱️  Tiempo: {elapsed:.3f}s ({len(results)/elapsed:.1f} IPs/s)\n")
    
    # Agrupar por threat level
    by_threat = {}
    for ip, rep in results.items():
        level = rep.threat_level
        if level not in by_threat:
            by_threat[level] = []
        by_threat[level].append(ip)
    
    print("📊 Resultados por Threat Level:\n")
    for level in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        if level in by_threat:
            print(f"   {level:10} {len(by_threat[level])} IPs")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 5: ESTADÍSTICAS DEL SISTEMA")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    # Generar actividad
    test_ips = ["8.8.8.8", "203.0.113.50", "125.50.100.20", "192.168.1.1"]
    
    for ip in test_ips:
        sentinel.check_ip(ip)
    
    # Obtener stats
    stats = sentinel.get_reputation_stats()
    
    print("\n📊 ESTADÍSTICAS COMPLETAS:\n")
    
    print("   Sentinel:")
    for key, value in stats['sentinel_stats'].items():
        print(f"      {key:20} {value}")
    
    print("\n   Database:")
    db_stats = stats['database_stats']
    print(f"      Total IPs tracked:   {db_stats['total_ips_tracked']}")
    print(f"      Whitelisted:         {db_stats['whitelisted']}")
    print(f"      Blacklisted:         {db_stats['blacklisted']}")
    print(f"      Average score:       {db_stats['average_score']:.2f}/100")
    
    print("\n   Cache:")
    for key, value in stats['cache_stats'].items():
        print(f"      {key:20} {value}")
    
    print()


def test_top_malicious():
    """Test de top IPs maliciosas"""
    print("=" * 70)
    print("TEST 6: TOP IPs MALICIOSAS")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    # Generar IPs maliciosas
    malicious = ["125.50.100.20", "75.200.30.5", "100.150.75.10"]
    
    for ip in malicious:
        sentinel.check_ip(ip)
    
    # Obtener top
    top = sentinel.get_top_malicious(5)
    
    print(f"\n🔴 TOP {len(top)} IPs MALICIOSAS:\n")
    
    for i, (ip, score, threat, country, isp, checks) in enumerate(top, 1):
        print(f"   {i}. {ip}")
        print(f"      Score:   {score}/100")
        print(f"      Threat:  {threat}")
        print(f"      Country: {country}")
        print(f"      Checks:  {checks}")
        print()


def test_enrichment():
    """Test de enriquecimiento de amenazas"""
    print("=" * 70)
    print("TEST 7: ENRIQUECIMIENTO DE AMENAZAS")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    threat_ip = "203.0.113.50"
    
    print(f"\n🔍 Enriqueciendo información de {threat_ip}...\n")
    
    enriched = sentinel.enrich_threat(threat_ip)
    
    print("📋 Información enriquecida:")
    for key, value in enriched.items():
        print(f"   {key:20} {value}")
    
    print()


def test_full_report():
    """Test de reporte completo"""
    print("=" * 70)
    print("TEST 8: REPORTE COMPLETO")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    # Generar actividad
    test_ips = [
        "8.8.8.8", "203.0.113.50", "125.50.100.20",
        "192.168.1.1", "75.200.30.5", "100.150.75.10"
    ]
    
    for ip in test_ips:
        sentinel.check_ip(ip)
    
    # Generar reporte
    report = sentinel.generate_report()
    
    print(f"\n📊 REPORTE COMPLETO:\n")
    print(f"   Timestamp: {report['timestamp']}")
    
    sentinel_stats = report['statistics']['sentinel_stats']
    print(f"\n   IPs verificadas:     {sentinel_stats['ips_checked']}")
    print(f"   Maliciosas:          {sentinel_stats['malicious_found']}")
    print(f"   Whitelist hits:      {sentinel_stats['whitelist_hits']}")
    print(f"   Blacklist hits:      {sentinel_stats['blacklist_hits']}")
    
    if report['top_malicious_ips']:
        print(f"\n   Top IPs maliciosas:")
        for i, ip_data in enumerate(report['top_malicious_ips'][:3], 1):
            print(f"      {i}. {ip_data['ip']} ({ip_data['score']}/100)")
    
    if report['threat_distribution']:
        print(f"\n   Distribución de amenazas:")
        for level, count in report['threat_distribution'].items():
            print(f"      {level:10} {count}")
    
    print()


def test_callback():
    """Test de callbacks"""
    print("=" * 70)
    print("TEST 9: CALLBACKS PERSONALIZADOS")
    print("=" * 70)
    
    sentinel = ReputationSentinel()
    
    malicious_detected = []
    
    def on_malicious(reputation):
        """Callback cuando se detecta IP maliciosa"""
        malicious_detected.append(reputation.ip)
        print(f"   ⚠️  CALLBACK: IP maliciosa {reputation.ip} detectada!")
    
    sentinel.set_malicious_callback(on_malicious)
    
    print("\n📊 Callback configurado, verificando IPs...\n")
    
    # Verificar IPs (algunas maliciosas)
    test_ips = ["8.8.8.8", "125.50.100.20", "75.200.30.5"]
    
    for ip in test_ips:
        sentinel.check_ip(ip)
    
    print(f"\n✅ Callbacks ejecutados: {len(malicious_detected)}")
    print(f"   IPs maliciosas detectadas: {malicious_detected}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "REPUTATION SENTINEL - TESTS" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_integration()
    print()
    
    test_with_threat_database()
    print()
    
    test_whitelist_blacklist()
    print()
    
    test_bulk_check()
    print()
    
    test_statistics()
    print()
    
    test_top_malicious()
    print()
    
    test_enrichment()
    print()
    
    test_full_report()
    print()
    
    test_callback()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("📊 CAPÍTULO 7 COMPLETADO:")
    print("   ✅ IPReputationChecker")
    print("   ✅ ReputationDatabase")
    print("   ✅ ReputationSentinel")
    print()
    print("🎯 Sistema completo de reputación de IPs funcionando!")
    print()


if __name__ == "__main__":
    main()