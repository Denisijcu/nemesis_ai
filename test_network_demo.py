#!/usr/bin/env python3
"""
Demo del NetworkSentinel con paquetes simulados
NO requiere sudo, NO requiere tráfico real
"""

import sys
sys.path.insert(0, 'src')

import asyncio
from datetime import datetime
from network.protocol_analyzer import ProtocolAnalyzer
from network.packet_capture import PacketInfo


class NetworkSentinelDemo:
    """Versión demo que simula paquetes"""
    
    def __init__(self):
        self.analyzer = ProtocolAnalyzer()
        self.packets_processed = 0
        self.http_threats = 0
        self.dns_threats = 0
        self.port_scans = 0
    
    async def run_demo(self):
        """Ejecuta demo con paquetes simulados"""
        
        print("=" * 70)
        print("🎬 DEMO: NETWORK SENTINEL CON PAQUETES SIMULADOS")
        print("=" * 70)
        print()
        print("📝 Simulando captura de tráfico de red...")
        print("   (No requiere sudo ni tráfico real)")
        print()
        
        # Paquetes simulados
        demo_packets = [
            # Tráfico normal
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.100",
                dst_ip="93.184.216.34",
                src_port=54321,
                dst_port=80,
                protocol="TCP",
                length=580,
                payload="GET /index.html HTTP/1.1\r\nHost: example.com\r\n",
                flags="PA",
                http_method="GET",
                http_uri="/index.html",
                dns_query=None
            ),
            
            # SQL Injection
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.100",
                dst_ip="10.0.0.50",
                src_port=54322,
                dst_port=80,
                protocol="TCP",
                length=620,
                payload="GET /login?user=admin' OR '1'='1'-- HTTP/1.1\r\nHost: victim.com\r\n",
                flags="PA",
                http_method="GET",
                http_uri="/login?user=admin' OR '1'='1'--",
                dns_query=None
            ),
            
            # XSS
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.101",
                dst_ip="10.0.0.50",
                src_port=54323,
                dst_port=80,
                protocol="TCP",
                length=650,
                payload="GET /search?q=<script>alert(document.cookie)</script> HTTP/1.1\r\nHost: site.com\r\n",
                flags="PA",
                http_method="GET",
                http_uri="/search?q=<script>alert(document.cookie)</script>",
                dns_query=None
            ),
            
            # Path Traversal
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.102",
                dst_ip="10.0.0.50",
                src_port=54324,
                dst_port=80,
                protocol="TCP",
                length=600,
                payload="GET /download?file=../../../../etc/passwd HTTP/1.1\r\nHost: app.com\r\n",
                flags="PA",
                http_method="GET",
                http_uri="/download?file=../../../../etc/passwd",
                dns_query=None
            ),
            
            # Command Injection
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.103",
                dst_ip="10.0.0.50",
                src_port=54325,
                dst_port=80,
                protocol="TCP",
                length=590,
                payload="POST /api/exec?cmd=ls;cat /etc/shadow HTTP/1.1\r\nHost: api.com\r\n",
                flags="PA",
                http_method="POST",
                http_uri="/api/exec?cmd=ls;cat /etc/shadow",
                dns_query=None
            ),
            
            # DNS - Normal
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.100",
                dst_ip="8.8.8.8",
                src_port=53241,
                dst_port=53,
                protocol="DNS",
                length=60,
                payload=None,
                flags=None,
                http_method=None,
                http_uri=None,
                dns_query="google.com"
            ),
            
            # DNS - DGA (malware)
            PacketInfo(
                timestamp=datetime.now(),
                src_ip="192.168.1.104",
                dst_ip="8.8.8.8",
                src_port=53242,
                dst_port=53,
                protocol="DNS",
                length=75,
                payload=None,
                flags=None,
                http_method=None,
                http_uri=None,
                dns_query="xjkh3k4j5h6k7j8h9k0j1k2l3m4n5o6p7.com"
            ),
            
            # Port scan simulation (10 puertos)
            *[
                PacketInfo(
                    timestamp=datetime.now(),
                    src_ip="192.168.1.200",
                    dst_ip="10.0.0.100",
                    src_port=50000 + i,
                    dst_port=20 + i,
                    protocol="TCP",
                    length=40,
                    payload=None,
                    flags="S",
                    http_method=None,
                    http_uri=None,
                    dns_query=None
                )
                for i in range(10)
            ]
        ]
        
        print("🎯 Procesando paquetes simulados...")
        print()
        
        for i, packet in enumerate(demo_packets, 1):
            await asyncio.sleep(0.3)  # Simular delay
            
            self._process_packet(packet)
            
            if i % 5 == 0:
                print(f"   📦 Procesados: {i}/{len(demo_packets)}")
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS FINALES")
        print("=" * 70)
        print(f"📦 Paquetes procesados: {self.packets_processed}")
        print(f"🌐 Amenazas HTTP:       {self.http_threats}")
        print(f"🔍 Amenazas DNS:        {self.dns_threats}")
        print(f"🔍 Port scans:          {self.port_scans}")
        print(f"🚨 Total amenazas:      {self.http_threats + self.dns_threats + self.port_scans}")
        print("=" * 70)
        print()
        print("✅ DEMO COMPLETADO")
        print()
        print("💡 Este es el comportamiento esperado del NetworkSentinel")
        print("   en tráfico HTTP real (no HTTPS)")
        print("=" * 70)
    
    def _process_packet(self, packet: PacketInfo):
        """Procesa paquete (lógica simplificada)"""
        self.packets_processed += 1
        
        # HTTP
        if packet.http_method and packet.http_uri:
            analysis = self.analyzer.analyze_http(
                packet.http_method,
                packet.http_uri,
                packet.payload or ""
            )
            
            if analysis.suspicious_patterns:
                self.http_threats += 1
                print(f"   🚨 HTTP THREAT #{self.http_threats}: "
                      f"{analysis.suspicious_patterns[0].upper()} "
                      f"desde {packet.src_ip}")
        
        # DNS
        if packet.dns_query:
            analysis = self.analyzer.analyze_dns(packet.dns_query)
            
            if analysis.is_suspicious:
                self.dns_threats += 1
                print(f"   🚨 DNS THREAT #{self.dns_threats}: "
                      f"{analysis.suspicious_reasons[0]} "
                      f"desde {packet.src_ip}")
        
        # Port scan
        if packet.protocol == "TCP" and packet.flags:
            scan = self.analyzer.track_connection(
                packet.src_ip,
                packet.dst_ip,
                packet.dst_port,
                packet.flags
            )
            
            if scan:
                self.port_scans += 1
                print(f"   🚨 PORT SCAN #{self.port_scans}: "
                      f"{scan.scan_type} desde {scan.scanner_ip}")


async def main():
    demo = NetworkSentinelDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())