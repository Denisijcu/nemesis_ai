#!/usr/bin/env python3
"""
Test del sistema de alertas
"""

import sys
sys.path.insert(0, 'src')

import asyncio
import yaml
from alerts.alert_manager import AlertManager


async def test_alerts():
    print("=" * 70)
    print("📢 PROBANDO SISTEMA DE ALERTAS")
    print("=" * 70)
    print()
    
    # Cargar configuración
    try:
        with open('config/alerts.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✅ Configuración cargada")
    except:
        print("⚠️  No se encontró config/alerts.yaml")
        print("   Usando configuración de prueba (alertas deshabilitadas)")
        config = {}
    
    print()
    
    # Inicializar manager
    manager = AlertManager(config)
    
    print("📢 Enviando alerta de prueba...")
    print()
    
    # Enviar alerta de prueba
    await manager.send_threat_alert(
        source_ip="192.168.1.100",
        attack_type="SQL_INJECTION",
        confidence=0.95,
        payload="' OR '1'='1'-- admin",
        action_taken="BLOCK"
    )
    
    print("✅ Alerta enviada (si estaba configurado)")
    print()
    
    # Enviar reporte
    print("📊 Enviando reporte de prueba...")
    print()
    
    test_stats = {
        'total_threats': 42,
        'total_blocked_ips': 15,
        'threats_last_24h': 8,
        'threats_by_type': {
            'SQL_INJECTION': 12,
            'XSS': 18,
            'PATH_TRAVERSAL': 7,
            'COMMAND_INJECTION': 5
        }
    }
    
    await manager.send_daily_report(test_stats)
    
    print("✅ Reporte enviado (si estaba configurado)")
    print()
    print("=" * 70)
    print("📢 Test de alertas completado")
    print("=" * 70)
    print()
    print("💡 NOTA:")
    print("   Para habilitar alertas, edita: config/alerts.yaml")
    print("   - Telegram: Crea bot con @BotFather")
    print("   - Email: Usa App Password de Gmail")
    print("=" * 70)


asyncio.run(test_alerts())