#!/usr/bin/env python3
"""
Test de Reputation Database
"""

import sys
sys.path.insert(0, 'src')

import time
from reputation.ip_checker import IPReputationChecker, IPReputation
from reputation.reputation_database import ReputationDatabase


def test_basic_operations():
    """Test de operaciones básicas"""
    print("=" * 70)
    print("TEST 1: OPERACIONES BÁSICAS")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    checker = IPReputationChecker()
    
    # Verificar varias IPs y guardar
    test_ips = [
        "8.8.8.8",
        "203.0.113.50",
        "45.142.212.61",
        "192.168.1.100"
    ]
    
    print("\n📊 Guardando reputaciones...\n")
    
    for ip in test_ips:
        rep = checker.check_ip(ip)
        db.save_reputation(rep)
        print(f"✅ {ip}: Score {rep.reputation_score}/100 ({rep.threat_level})")
    
    print("\n📖 Recuperando desde BD...\n")
    
    for ip in test_ips:
        rep = db.get_reputation(ip)
        if rep:
            print(f"💾 {ip}: Score {rep.reputation_score}/100 ({rep.threat_level})")
    
    print()


def test_whitelist_blacklist():
    """Test de whitelist/blacklist persistente"""
    print("=" * 70)
    print("TEST 2: WHITELIST Y BLACKLIST PERSISTENTE")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    
    whitelist_ip = "8.8.8.8"
    blacklist_ip = "203.0.113.666"
    
    print(f"\n✅ Añadiendo {whitelist_ip} a WHITELIST...")
    db.add_to_whitelist(whitelist_ip, reason="Trusted Google DNS")
    
    print(f"🚫 Añadiendo {blacklist_ip} a BLACKLIST...")
    db.add_to_blacklist(blacklist_ip, reason="Known botnet", severity="CRITICAL")
    
    print("\n📋 Verificando...\n")
    print(f"   {whitelist_ip} en whitelist: {db.is_whitelisted(whitelist_ip)}")
    print(f"   {blacklist_ip} en blacklist: {db.is_blacklisted(blacklist_ip)}")
    
    # Recuperar reputación (debe reflejar whitelist/blacklist)
    rep_white = db.get_reputation(whitelist_ip)
    rep_black = db.get_reputation(blacklist_ip)
    
    if rep_white:
        print(f"\n   Whitelist - Whitelisted: {rep_white.is_whitelisted}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 3: ESTADÍSTICAS")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    
    stats = db.get_statistics()
    
    print("\n📊 ESTADÍSTICAS DE REPUTACIÓN:\n")
    print(f"   Total IPs tracked:     {stats['total_ips_tracked']}")
    print(f"   Whitelisted:           {stats['whitelisted']}")
    print(f"   Blacklisted:           {stats['blacklisted']}")
    print(f"   Score promedio:        {stats['average_score']:.2f}/100")
    
    print(f"\n   Por Threat Level:")
    for level, count in stats['by_threat_level'].items():
        print(f"      {level:12} {count}")
    
    if stats['top_countries']:
        print(f"\n   Top Countries:")
        for country, count in stats['top_countries'].items():
            print(f"      {country:20} {count}")
    
    print()


def test_top_malicious():
    """Test de IPs más maliciosas"""
    print("=" * 70)
    print("TEST 4: TOP IPs MALICIOSAS")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    checker = IPReputationChecker()
    
    # Generar algunas IPs maliciosas
    malicious_ips = [
        "125.50.100.20",  # Russia
        "75.200.30.5",    # China
        "100.150.75.10",  # Russia
    ]
    
    for ip in malicious_ips:
        rep = checker.check_ip(ip)
        db.save_reputation(rep)
    
    # Obtener top maliciosas
    top = db.get_top_malicious_ips(5)
    
    print("\n🔴 TOP 5 IPs MALICIOSAS:\n")
    
    for i, (ip, score, threat, country, isp, checks) in enumerate(top, 1):
        print(f"   {i}. {ip}")
        print(f"      Score:   {score}/100")
        print(f"      Threat:  {threat}")
        print(f"      Country: {country}")
        print(f"      ISP:     {isp}")
        print(f"      Checks:  {checks}")
        print()


def test_history():
    """Test de historial"""
    print("=" * 70)
    print("TEST 5: HISTORIAL DE REPUTACIÓN")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    checker = IPReputationChecker()
    
    test_ip = "203.0.113.100"
    
    print(f"\n📊 Verificando {test_ip} varias veces...\n")
    
    # Verificar varias veces
    for i in range(3):
        rep = checker.check_ip(test_ip)
        db.save_reputation(rep)
        time.sleep(0.1)
    
    # Añadir a blacklist
    db.add_to_blacklist(test_ip, reason="Testing", severity="HIGH")
    
    # Obtener historial
    history = db.get_reputation_history(test_ip)
    
    print(f"📜 Historial de {test_ip} ({len(history)} eventos):\n")
    
    for event in history:
        print(f"   [{event['timestamp']}]")
        print(f"      Event:  {event['event']}")
        print(f"      Score:  {event['score']}/100")
        print(f"      Threat: {event['threat_level']}")
        print()


def test_cleanup_decay():
    """Test de limpieza y decay"""
    print("=" * 70)
    print("TEST 6: CLEANUP Y DECAY")
    print("=" * 70)
    
    db = ReputationDatabase("data/test_reputation.db")
    
    print("\n🧹 Limpiando entradas expiradas...")
    expired = db.cleanup_expired()
    print(f"   Removidas: {expired}")
    
    print("\n📉 Aplicando decay a reputaciones viejas...")
    decayed = db.decay_reputations(days_old=1, decay_amount=5)
    print(f"   Actualizadas: {decayed}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "REPUTATION DATABASE - TESTS" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_operations()
    print()
    
    test_whitelist_blacklist()
    print()
    
    test_statistics()
    print()
    
    test_top_malicious()
    print()
    
    test_history()
    print()
    
    test_cleanup_decay()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("💾 Base de datos creada: data/test_reputation.db")
    print()


if __name__ == "__main__":
    main()