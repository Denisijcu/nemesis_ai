#!/usr/bin/env python3
"""
Test del IP Reputation Checker
"""

import sys
sys.path.insert(0, 'src')

from reputation.ip_checker import IPReputationChecker


def test_basic_checking():
    """Test básico de checking"""
    print("=" * 70)
    print("TEST 1: VERIFICACIÓN BÁSICA DE IPs")
    print("=" * 70)
    
    checker = IPReputationChecker()
    
    # Lista de IPs para probar
    test_ips = [
        "8.8.8.8",           # Google DNS
        "192.168.1.100",     # IP privada
        "203.0.113.50",      # IP pública simulada
        "45.142.212.61",     # IP sospechosa simulada
        "127.0.0.1",         # Localhost
        "invalid.ip"         # IP inválida
    ]
    
    print()
    for ip in test_ips:
        rep = checker.check_ip(ip)
        
        threat_emoji = {
            "LOW": "🟢",
            "MEDIUM": "🟡",
            "HIGH": "🟠",
            "CRITICAL": "🔴",
            "UNKNOWN": "⚪"
        }.get(rep.threat_level, "⚪")
        
        print(f"{threat_emoji} {ip}")
        print(f"   Score:       {rep.reputation_score}/100")
        print(f"   Threat:      {rep.threat_level}")
        print(f"   Country:     {rep.country}")
        print(f"   ISP:         {rep.isp}")
        print(f"   Categories:  {', '.join(rep.categories)}")
        print(f"   Blacklisted: {'YES' if rep.is_blacklisted else 'NO'}")
        print(f"   Whitelisted: {'YES' if rep.is_whitelisted else 'NO'}")
        print()
    print()


def test_whitelist_blacklist():
    """Test de whitelist/blacklist"""
    print("=" * 70)
    print("TEST 2: WHITELIST Y BLACKLIST")
    print("=" * 70)
    
    checker = IPReputationChecker()
    
    test_ip = "203.0.113.100"
    
    # Verificación normal
    print(f"\n1. Verificación normal de {test_ip}:")
    rep = checker.check_ip(test_ip)
    print(f"   Score: {rep.reputation_score}/100")
    print(f"   Threat: {rep.threat_level}")
    
    # Añadir a blacklist
    print(f"\n2. Añadiendo a BLACKLIST...")
    checker.add_to_blacklist(test_ip)
    
    rep = checker.check_ip(test_ip)
    print(f"   Score: {rep.reputation_score}/100")
    print(f"   Threat: {rep.threat_level}")
    print(f"   Blacklisted: {rep.is_blacklisted}")
    
    # Remover de blacklist
    print(f"\n3. Removiendo de blacklist...")
    checker.remove_from_blacklist(test_ip)
    
    # Añadir a whitelist
    print(f"\n4. Añadiendo a WHITELIST...")
    checker.add_to_whitelist(test_ip)
    
    rep = checker.check_ip(test_ip)
    print(f"   Score: {rep.reputation_score}/100")
    print(f"   Threat: {rep.threat_level}")
    print(f"   Whitelisted: {rep.is_whitelisted}")
    
    print()


def test_cache():
    """Test de cache"""
    print("=" * 70)
    print("TEST 3: SISTEMA DE CACHE")
    print("=" * 70)
    
    checker = IPReputationChecker(cache_ttl=10)
    
    test_ip = "8.8.8.8"
    
    print(f"\n1. Primera verificación de {test_ip}:")
    import time
    start = time.time()
    rep1 = checker.check_ip(test_ip)
    time1 = time.time() - start
    print(f"   Tiempo: {time1*1000:.2f}ms")
    print(f"   Score: {rep1.reputation_score}")
    
    print(f"\n2. Segunda verificación (desde cache):")
    start = time.time()
    rep2 = checker.check_ip(test_ip)
    time2 = time.time() - start
    print(f"   Tiempo: {time2*1000:.2f}ms")
    print(f"   Score: {rep2.reputation_score}")
    print(f"   Cache hit: {'YES' if time2 < time1 else 'NO'}")
    
    # Stats de cache
    print(f"\n3. Estadísticas de cache:")
    stats = checker.get_cache_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print()


def test_geolocation():
    """Test de geolocalización"""
    print("=" * 70)
    print("TEST 4: GEOLOCALIZACIÓN Y CATEGORIZACIÓN")
    print("=" * 70)
    
    checker = IPReputationChecker()
    
    test_ips = {
        "25.100.50.10": "United States",
        "75.200.30.5": "China",
        "125.50.100.20": "Russia",
        "175.10.5.30": "Germany",
        "225.150.80.40": "Brazil"
    }
    
    print()
    for ip, expected_country in test_ips.items():
        rep = checker.check_ip(ip)
        
        match = "✅" if rep.country == expected_country else "❌"
        
        print(f"{match} {ip}")
        print(f"   Expected: {expected_country}")
        print(f"   Got:      {rep.country}")
        print(f"   ISP:      {rep.isp}")
        print(f"   ASN:      {rep.asn}")
        print(f"   Score:    {rep.reputation_score}/100")
        print()
    print()


def test_threat_scoring():
    """Test de scoring de amenazas"""
    print("=" * 70)
    print("TEST 5: SCORING DE AMENAZAS")
    print("=" * 70)
    
    checker = IPReputationChecker()
    
    print("\n📊 Scores por tipo de IP:\n")
    
    test_cases = [
        ("192.168.1.1", "IP Privada"),
        ("8.8.8.8", "Google DNS"),
        ("3.10.20.30", "Amazon AWS"),
        ("125.50.100.20", "Russia (High Risk)"),
        ("75.200.30.5", "China (High Risk)"),
    ]
    
    for ip, description in test_cases:
        rep = checker.check_ip(ip)
        
        bars = "█" * (rep.reputation_score // 5)
        spaces = "░" * (20 - len(bars))
        
        print(f"{description:30} [{bars}{spaces}] {rep.reputation_score}/100 - {rep.threat_level}")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 18 + "IP REPUTATION CHECKER - TESTS" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_basic_checking()
    print()
    
    test_whitelist_blacklist()
    print()
    
    test_cache()
    print()
    
    test_geolocation()
    print()
    
    test_threat_scoring()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()