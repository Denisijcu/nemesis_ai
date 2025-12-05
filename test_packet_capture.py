#!/usr/bin/env python3
"""
Test básico de PacketCapture
REQUIERE: sudo/root
"""

import sys
sys.path.insert(0, 'src')

from network.packet_capture import PacketCapture, PacketInfo


def packet_handler(packet: PacketInfo):
    """Maneja cada paquete capturado"""
    
    # Información básica
    print(f"\n{'='*70}")
    print(f"📦 Paquete capturado:")
    print(f"   🕐 Timestamp: {packet.timestamp.strftime('%H:%M:%S')}")
    print(f"   🌐 {packet.src_ip}:{packet.src_port} → {packet.dst_ip}:{packet.dst_port}")
    print(f"   📡 Protocolo: {packet.protocol}")
    print(f"   📏 Tamaño: {packet.length} bytes")
    
    # HTTP
    if packet.http_method:
        print(f"   🌐 HTTP: {packet.http_method} {packet.http_uri}")
    
    # DNS
    if packet.dns_query:
        print(f"   🔍 DNS Query: {packet.dns_query}")
    
    # TCP Flags
    if packet.flags:
        print(f"   🚩 Flags: {packet.flags}")
    
    # Payload (primeros 100 chars)
    if packet.payload:
        preview = packet.payload[:100].replace('\n', ' ')
        print(f"   📦 Payload: {preview}...")


def main():
    print("=" * 70)
    print("📡 PROBANDO PACKET CAPTURE")
    print("=" * 70)
    print()
    print("⚠️  NOTA: Este script requiere permisos root/sudo")
    print()
    print("🎯 Capturando paquetes HTTP...")
    print("   Abre un navegador y visita cualquier sitio")
    print("   Presiona Ctrl+C para detener")
    print()
    print("=" * 70)
    print()
    
    try:
        # Capturar solo tráfico HTTP (puerto 80)
        capture = PacketCapture(
            interface="eth0",  # Cambiar según tu interface
            filter_str="tcp port 80"
        )
        
        # Capturar 10 paquetes
        capture.start_capture(
            packet_callback=packet_handler,
            count=10
        )
        
        print()
        print("=" * 70)
        print(f"✅ Captura completada: {capture.packet_count} paquetes")
        print("=" * 70)
    
    except PermissionError:
        print("\n❌ ERROR: Se requieren permisos root")
        print("   Ejecuta: sudo python3 test_packet_capture.py")
    except KeyboardInterrupt:
        print("\n\n⏹️  Captura detenida por usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()