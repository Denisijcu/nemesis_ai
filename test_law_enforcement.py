#!/usr/bin/env python3
"""
Test del sistema Law Enforcement Connector
"""

import sys
sys.path.insert(0, 'src')

from intel.law_enforcement_connector import LawEnforcementConnector


def test_ip_check():
    """Test de verificación de IP"""
    print("=" * 70)
    print("TEST 1: COMPREHENSIVE IP CHECK")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    # IPs de prueba (públicas conocidas)
    test_ips = [
        '8.8.8.8',      # Google DNS (limpia)
        '1.1.1.1',      # Cloudflare (limpia)
        '185.220.101.1' # Tor exit node (puede estar listada)
    ]
    
    print("\n🔍 Verificando IPs en todas las fuentes...\n")
    
    for ip in test_ips:
        result = connector.comprehensive_ip_check(ip)
        
        print(f"IP: {ip}")
        print(f"   Threat Score:  {result['threat_score']}/100")
        print(f"   Threat Level:  {result['threat_level']}")
        print(f"   AbuseIPDB:     Score {result['abuseipdb'].get('abuse_confidence_score', 0)}%")
        print(f"   Spamhaus:      Listed {result['spamhaus']['zones_listed']}/{result['spamhaus']['zones_checked']} zones")
        print(f"   Organization:  {result['whois'].get('organization', 'Unknown')}")
        print(f"   Recommendation: {result['recommendation']}")
        print()
    
    print()


def test_threat_report():
    """Test de reporte de amenaza"""
    print("=" * 70)
    print("TEST 2: THREAT REPORTING")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    # Simular amenaza detectada
    threat_ip = "203.0.113.50"  # TEST-NET-3 (documentación)
    threat_type = "SQL_INJECTION"
    evidence = "Multiple SQL injection attempts detected: ' OR 1=1--, UNION SELECT, etc."
    
    print(f"\n📝 Reportando amenaza: {threat_ip}\n")
    
    result = connector.report_threat(
        ip=threat_ip,
        threat_type=threat_type,
        evidence=evidence,
        auto_report=False  # Deshabilitado para testing
    )
    
    print(f"   IP:           {result['ip']}")
    print(f"   Threat Type:  {result['threat_type']}")
    print(f"   Reported:     {result.get('reported', False)}")
    print(f"   Reason:       {result.get('reason', 'N/A')}")
    
    print()


def test_bulk_report():
    """Test de reporte en lote"""
    print("=" * 70)
    print("TEST 3: BULK THREAT REPORTING")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    # Múltiples amenazas
    threats = [
        {
            'ip': '198.51.100.10',
            'threat_type': 'BRUTE_FORCE',
            'evidence': 'SSH brute force - 500 failed attempts'
        },
        {
            'ip': '198.51.100.20',
            'threat_type': 'PORT_SCAN',
            'evidence': 'Port scan detected - scanned 1000+ ports'
        },
        {
            'ip': '198.51.100.30',
            'threat_type': 'DDOS',
            'evidence': 'DDoS attack - 10k requests/second'
        }
    ]
    
    print(f"\n📋 Reportando {len(threats)} amenazas...\n")
    
    result = connector.bulk_threat_report(threats, auto_report=False)
    
    print(f"   Total:       {result['total']}")
    print(f"   Successful:  {result['successful']}")
    print(f"   Failed:      {result['failed']}")
    
    print()


def test_abuse_contact():
    """Test de búsqueda de contacto abuse"""
    print("=" * 70)
    print("TEST 4: ABUSE CONTACT LOOKUP")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    test_ip = "1.1.1.1"
    
    print(f"\n📧 Buscando contacto abuse para: {test_ip}\n")
    
    result = connector.find_abuse_contact(test_ip)
    
    print(f"   IP:              {result['ip']}")
    print(f"   Organization:    {result['organization']}")
    print(f"   Abuse Email:     {result['abuse_email']}")
    print(f"   Country:         {result['country']}")
    print(f"   Threat Level:    {result['threat_level']}")
    print(f"   Threat Score:    {result['threat_score']}")
    print(f"   Recommendation:  {result['recommended_action']}")
    
    print()


def test_threat_intel_report():
    """Test de reporte de threat intelligence"""
    print("=" * 70)
    print("TEST 5: THREAT INTELLIGENCE REPORT")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    # IPs para análisis
    ips = [
        '8.8.8.8',
        '1.1.1.1',
        '192.0.2.10',
        '192.0.2.20',
        '198.51.100.10'
    ]
    
    print(f"\n📊 Generando reporte de threat intel para {len(ips)} IPs...\n")
    
    report = connector.generate_threat_intel_report(ips)
    
    print(f"   Total IPs:        {report['total_ips_analyzed']}")
    print(f"   Avg Threat Score: {report['average_threat_score']:.1f}")
    print()
    
    print("   Threat Distribution:")
    for level, count in report['threat_distribution'].items():
        print(f"      {level:10} {count}")
    print()
    
    print("   Top Threats:")
    for i, threat in enumerate(report['top_threats'][:3], 1):
        print(f"      {i}. {threat['ip']:15} Score: {threat['threat_score']}")
    print()
    
    print("   Recommendations:")
    for rec in report['recommendations']:
        print(f"      • {rec}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 6: STATISTICS")
    print("=" * 70)
    
    connector = LawEnforcementConnector()
    
    # Generar actividad
    test_ips = ['8.8.8.8', '1.1.1.1', '192.0.2.1']
    
    for ip in test_ips:
        connector.comprehensive_ip_check(ip)
    
    connector.report_threat(
        '198.51.100.50',
        'SQL_INJECTION',
        'Test',
        auto_report=False
    )
    
    connector.find_abuse_contact('1.1.1.1')
    
    print("\n📊 Estadísticas del sistema:\n")
    print(connector.generate_summary_report())
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "LAW ENFORCEMENT CONNECTOR - TESTS" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_ip_check()
    print()
    
    test_threat_report()
    print()
    
    test_bulk_report()
    print()
    
    test_abuse_contact()
    print()
    
    test_threat_intel_report()
    print()
    
    test_statistics()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("🌐 CAPÍTULO 11 COMPLETADO:")
    print("   ✅ AbuseIPDB Integration")
    print("   ✅ Spamhaus DNSBL")
    print("   ✅ WHOIS Lookups")
    print("   ✅ Law Enforcement Connector")
    print("   ✅ Threat Intelligence Reports")
    print("   ✅ Abuse Contact Finder")
    print("   ✅ Bulk Reporting")
    print()
    print("⚖️ INTELIGENCIA Y REPORTE: AUTOMATIZADO!")
    print()
    
    print("💡 NOTA: Para producción:")
    print("   • Obtener API key de AbuseIPDB en https://www.abuseipdb.com")
    print("   • Configurar límites de rate limiting")
    print("   • Implementar retry logic robusto")
    print()


if __name__ == "__main__":
    main()