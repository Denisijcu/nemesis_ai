#!/usr/bin/env python3
"""
Test del Network Sentinel con MÁS TIEMPO
REQUIERE: sudo/root
"""

import sys
import asyncio
sys.path.insert(0, 'src')

from network.network_sentinel import NetworkSentinel


async def test_basic_monitoring():
    """Test básico de monitoreo de red - 5 MINUTOS"""
    print("=" * 70)
    print("🌐 TEST: NETWORK SENTINEL - MONITOREO EXTENDIDO")
    print("=" * 70)
    print()
    print("⚠️  NOTA: Este script requiere permisos root/sudo")
    print()
    print("🎯 Monitoreando tráfico de red por 5 MINUTOS...")
    print("   O hasta capturar 200 paquetes")
    print()
    print("💡 AHORA GENERA TRÁFICO EN OTRA TERMINAL:")
    print()
    print("   # Tráfico normal")
    print("   curl http://neverssl.com")
    print("   curl http://example.com")
    print()
    print("   # Ataques (serán detectados)")
    print("   curl \"http://httpbin.org/get?id=1' OR '1'='1'--\"")
    print("   curl \"http://httpbin.org/get?q=<script>alert(1)</script>\"")
    print("   curl \"http://httpbin.org/get?file=../../../etc/passwd\"")
    print()
    print("=" * 70)
    print()
    
    try:
        sentinel = NetworkSentinel(
            interface="eth0",
            database=None,
            alert_manager=None
        )
        
        print("🚀 Captura iniciada... GENERA TRÁFICO AHORA!")
        print("   (Presiona Ctrl+C para detener antes)")
        print()
        
        # 5 minutos O 200 paquetes
        await asyncio.wait_for(
            sentinel.start(packet_count=200),
            timeout=300.0  # 5 minutos
        )
        
        stats = sentinel.stats
        
        print()
        print("=" * 70)
        print("📊 ESTADÍSTICAS FINALES")
        print("=" * 70)
        print(f"📦 Paquetes procesados: {stats['packets_processed']}")
        print(f"🌐 Amenazas HTTP:       {stats['http_threats']}")
        print(f"🔍 Amenazas DNS:        {stats['dns_threats']}")
        print(f"🔍 Port scans:          {stats['port_scans']}")
        print(f"🚨 Total amenazas:      {stats['total_threats']}")
        print("=" * 70)
        
        if stats['total_threats'] == 0:
            print()
            print("⚠️  NO SE DETECTARON AMENAZAS")
            print("   Razones posibles:")
            print("   • No generaste tráfico malicioso")
            print("   • El tráfico fue por HTTPS (encriptado)")
            print("   • La interface es incorrecta")
            print()
            print("💡 Prueba ejecutar: python3 test_network_offline.py")
            print("   Ese test no requiere tráfico real")
    
    except PermissionError:
        print("\n❌ ERROR: Se requieren permisos root")
        print("   Ejecuta: sudo python3 test_network_sentinel.py")
    except asyncio.TimeoutError:
        print("\n⏰ Timeout de 5 minutos alcanzado")
        stats = sentinel.stats
        print(f"\n📊 Capturados: {stats['packets_processed']} paquetes")
        print(f"🚨 Amenazas: {stats['total_threats']}")
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoreo detenido por usuario")
        stats = sentinel.stats
        print(f"\n📊 Capturados: {stats['packets_processed']} paquetes")
        print(f"🚨 Amenazas: {stats['total_threats']}")
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def test_continuous():
    """Test continuo - se ejecuta hasta Ctrl+C"""
    print("=" * 70)
    print("🌐 NETWORK SENTINEL - MODO CONTINUO")
    print("=" * 70)
    print()
    print("⚠️  Se ejecutará hasta que presiones Ctrl+C")
    print()
    print("💡 Genera tráfico en otra terminal:")
    print("   curl \"http://httpbin.org/get?id=1' OR '1'='1'--\"")
    print()
    print("=" * 70)
    print()
    
    try:
        sentinel = NetworkSentinel(
            interface="eth0",
            database=None,
            alert_manager=None
        )
        
        print("🚀 Modo continuo activado... (Ctrl+C para detener)")
        print()
        
        # Sin timeout, sin límite de paquetes
        await sentinel.start(packet_count=0)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Detenido")
        stats = sentinel.stats
        print(f"\n📊 Paquetes: {stats['packets_processed']}")
        print(f"🚨 Amenazas: {stats['total_threats']}")


def main():
    import sys
    
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "NETWORK SENTINEL - TEST EXTENDIDO" + " " * 20 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--continuous":
            asyncio.run(test_continuous())
        else:
            print("Opciones:")
            print("  (sin args)     - Test de 5 minutos")
            print("  --continuous   - Modo continuo (Ctrl+C para parar)")
    else:
        asyncio.run(test_basic_monitoring())


if __name__ == "__main__":
    main()