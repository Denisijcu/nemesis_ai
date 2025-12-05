#!/usr/bin/env python3
"""
Test offline del Protocol Analyzer
No requiere captura real de red
"""

import sys
sys.path.insert(0, 'src')

from network.protocol_analyzer import ProtocolAnalyzer
from network.packet_capture import PacketInfo
from datetime import datetime


def test_offline():
    print("=" * 70)
    print("🧪 TEST OFFLINE - PROTOCOL ANALYZER")
    print("=" * 70)
    print()
    
    analyzer = ProtocolAnalyzer()
    
    # Simular paquetes maliciosos
    test_packets = [
        {
            "name": "SQL Injection",
            "http_method": "GET",
            "uri": "/login?user=admin' OR '1'='1'--",
            "payload": "GET /login?user=admin' OR '1'='1'-- HTTP/1.1\r\nHost: victim.com\r\n"
        },
        {
            "name": "XSS",
            "http_method": "GET",
            "uri": "/search?q=<script>alert(document.cookie)</script>",
            "payload": "GET /search?q=<script>alert(1)</script> HTTP/1.1\r\nHost: site.com\r\n"
        },
        {
            "name": "Path Traversal",
            "http_method": "GET",
            "uri": "/download?file=../../../../etc/passwd",
            "payload": "GET /download?file=../../../../etc/passwd HTTP/1.1\r\nHost: app.com\r\n"
        },
        {
            "name": "Command Injection",
            "http_method": "POST",
            "uri": "/api/exec?cmd=ls;cat /etc/shadow",
            "payload": "POST /api/exec?cmd=ls;cat /etc/shadow HTTP/1.1\r\nHost: api.com\r\n"
        },
        {
            "name": "LFI",
            "http_method": "GET",
            "uri": "/view?page=php://filter/convert.base64-encode/resource=index",
            "payload": "GET /view?page=php://filter/ HTTP/1.1\r\nHost: web.com\r\n"
        }
    ]
    
    detected = 0
    
    for i, test in enumerate(test_packets, 1):
        print(f"Test {i}: {test['name']}")
        
        result = analyzer.analyze_http(
            test['http_method'],
            test['uri'],
            test['payload']
        )
        
        if result.suspicious_patterns:
            detected += 1
            print(f"   ✅ DETECTADO: {result.suspicious_patterns}")
        else:
            print(f"   ❌ NO DETECTADO")
        
        print()
    
    # DNS Tests
    print("=" * 70)
    print("🔍 DNS ANALYSIS")
    print("=" * 70)
    print()
    
    dns_tests = [
        ("google.com", False),
        ("xjkh3k4j5h6k7j8h9k0j1k2l3m4n5o6p7.com", True),  # DGA
        ("a.b.c.d.e.f.g.h.example.com", True),  # Muchos subdominios
    ]
    
    dns_detected = 0
    
    for domain, should_detect in dns_tests:
        result = analyzer.analyze_dns(domain)
        
        print(f"Dominio: {domain}")
        
        if result.is_suspicious:
            dns_detected += 1
            print(f"   🚨 SOSPECHOSO: {result.suspicious_reasons}")
        else:
            print(f"   ✅ LIMPIO")
        
        if result.is_suspicious == should_detect:
            print(f"   ✓ Correcto")
        else:
            print(f"   ✗ Falló")
        
        print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESULTADOS FINALES")
    print("=" * 70)
    print(f"HTTP: {detected}/{len(test_packets)} detectados")
    print(f"DNS:  {dns_detected}/2 detectados (esperados)")
    print()
    
    if detected == len(test_packets):
        print("✅ TODOS LOS ATAQUES HTTP DETECTADOS")
    else:
        print(f"⚠️  Faltan {len(test_packets) - detected} detecciones")
    
    print("=" * 70)


if __name__ == "__main__":
    test_offline()