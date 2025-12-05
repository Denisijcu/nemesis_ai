#!/usr/bin/env python3
"""
Test del Protocol Analyzer
"""

import sys
sys.path.insert(0, 'src')

from network.protocol_analyzer import ProtocolAnalyzer


def test_http_analysis():
    """Test de análisis HTTP"""
    print("=" * 70)
    print("🌐 TEST: ANÁLISIS HTTP")
    print("=" * 70)
    print()
    
    analyzer = ProtocolAnalyzer()
    
    # Test 1: Request normal
    print("Test 1: Request legítimo")
    result = analyzer.analyze_http(
        "GET",
        "/index.html",
        "GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0\r\n"
    )
    print(f"   URI: {result.uri}")
    print(f"   Host: {result.host}")
    print(f"   Patrones sospechosos: {result.suspicious_patterns or 'Ninguno'}")
    print(f"   ✅ Resultado: {'LIMPIO' if not result.suspicious_patterns else 'SOSPECHOSO'}")
    print()
    
    # Test 2: SQL Injection
    print("Test 2: SQL Injection")
    result = analyzer.analyze_http(
        "GET",
        "/login?user=admin' OR '1'='1'--",
        "GET /login?user=admin' OR '1'='1'-- HTTP/1.1\r\nHost: evil.com\r\n"
    )
    print(f"   URI: {result.uri}")
    print(f"   Patrones detectados: {result.suspicious_patterns}")
    print(f"   🚨 Resultado: {'ATAQUE DETECTADO' if result.suspicious_patterns else 'LIMPIO'}")
    print()
    
    # Test 3: XSS
    print("Test 3: Cross-Site Scripting (XSS)")
    result = analyzer.analyze_http(
        "GET",
        "/search?q=<script>alert(1)</script>",
        "GET /search?q=<script>alert(1)</script> HTTP/1.1\r\nHost: victim.com\r\n"
    )
    print(f"   URI: {result.uri}")
    print(f"   Patrones detectados: {result.suspicious_patterns}")
    print(f"   🚨 Resultado: {'ATAQUE DETECTADO' if result.suspicious_patterns else 'LIMPIO'}")
    print()
    
    # Test 4: Path Traversal
    print("Test 4: Path Traversal")
    result = analyzer.analyze_http(
        "GET",
        "/download?file=../../../etc/passwd",
        "GET /download?file=../../../etc/passwd HTTP/1.1\r\nHost: target.com\r\n"
    )
    print(f"   URI: {result.uri}")
    print(f"   Patrones detectados: {result.suspicious_patterns}")
    print(f"   🚨 Resultado: {'ATAQUE DETECTADO' if result.suspicious_patterns else 'LIMPIO'}")
    print()


def test_dns_analysis():
    """Test de análisis DNS"""
    print("=" * 70)
    print("🔍 TEST: ANÁLISIS DNS")
    print("=" * 70)
    print()
    
    analyzer = ProtocolAnalyzer()
    
    # Test 1: Dominio normal
    print("Test 1: Dominio legítimo")
    result = analyzer.analyze_dns("google.com")
    print(f"   Dominio: {result.domain}")
    print(f"   Sospechoso: {result.is_suspicious}")
    print(f"   Razones: {result.suspicious_reasons or 'Ninguna'}")
    print(f"   ✅ Resultado: {'LIMPIO' if not result.is_suspicious else 'SOSPECHOSO'}")
    print()
    
    # Test 2: DGA (Domain Generation Algorithm)
    print("Test 2: Dominio DGA (malware)")
    result = analyzer.analyze_dns("xjkh3kjh4k5jh6k7jh8k9jhk0j.com")
    print(f"   Dominio: {result.domain}")
    print(f"   Sospechoso: {result.is_suspicious}")
    print(f"   Razones: {result.suspicious_reasons}")
    print(f"   🚨 Resultado: {'DGA DETECTADO' if result.is_suspicious else 'LIMPIO'}")
    print()
    
    # Test 3: Dominio con muchos subdominios
    print("Test 3: Demasiados subdominios")
    result = analyzer.analyze_dns("a.b.c.d.e.f.g.example.com")
    print(f"   Dominio: {result.domain}")
    print(f"   Sospechoso: {result.is_suspicious}")
    print(f"   Razones: {result.suspicious_reasons}")
    print(f"   🚨 Resultado: {'SOSPECHOSO' if result.is_suspicious else 'LIMPIO'}")
    print()


def test_port_scan_detection():
    """Test de detección de port scanning"""
    print("=" * 70)
    print("🔍 TEST: DETECCIÓN DE PORT SCANNING")
    print("=" * 70)
    print()
    
    analyzer = ProtocolAnalyzer()
    
    print("Simulando port scan de 192.168.1.100 → 192.168.1.200")
    print()
    
    # Simular scan de 15 puertos
    for port in range(20, 35):
        result = analyzer.track_connection(
            src_ip="192.168.1.100",
            dst_ip="192.168.1.200",
            dst_port=port,
            flags="S"  # SYN flag
        )
        
        if result:
            print(f"🚨 PORT SCAN DETECTADO!")
            print(f"   Escáner: {result.scanner_ip}")
            print(f"   Objetivo: {result.target_ip}")
            print(f"   Puertos escaneados: {len(result.ports_scanned)}")
            print(f"   Tipo de scan: {result.scan_type}")
            print(f"   Duración: {result.scan_duration:.2f}s")
            break
    else:
        print("❌ No se detectó port scan (esperado después de 10+ puertos)")
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PROTOCOL ANALYZER - TEST SUITE" + " " * 23 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_http_analysis()
    test_dns_analysis()
    test_port_scan_detection()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)


if __name__ == "__main__":
    main()