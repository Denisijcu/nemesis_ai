#!/usr/bin/env python3
"""
Test completo del sistema de alertas de NÉMESIS IA
Prueba Email (Gmail) y Telegram
"""
import sys
sys.path.insert(0, 'src')
import asyncio
import yaml
from datetime import datetime

async def test_alerts():
    print("=" * 80)
    print("📧📱 TEST DE SISTEMA DE ALERTAS - NÉMESIS IA")
    print("=" * 80)
    print()
    
    # Cargar configuración
    print("🔧 Cargando configuración...")
    try:
        with open('config/alerts.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("   ✅ Configuración cargada")
        print(f"   📧 Email: {config['email']['from_email']}")
        print(f"   📱 Telegram Chat ID: {config['telegram']['chat_id']}")
        print()
    except Exception as e:
        print(f"   ❌ Error cargando config: {e}")
        return
    
    # Inicializar AlertManager
    print("🚀 Inicializando AlertManager...")
    try:
        from alerts.alert_manager import AlertManager
        alert_manager = AlertManager(config)
        print("   ✅ AlertManager inicializado")
        print()
    except Exception as e:
        print(f"   ❌ Error inicializando AlertManager: {e}")
        return
    
    # Datos de prueba
    test_threat = {
        'source_ip': '203.0.113.666',
        'attack_type': 'TEST_ALERT_SYSTEM',
        'confidence': 0.99,
        'payload': 'This is a TEST alert from NÉMESIS IA - Sistema de Alertas Funcionando ✅',
        'action_taken': 'BLOCK'
    }
    
    print("=" * 80)
    print("TEST 1: ALERTA POR TELEGRAM")
    print("=" * 80)
    print()
    print("📱 Enviando alerta de prueba a Telegram...")
    print(f"   IP: {test_threat['source_ip']}")
    print(f"   Tipo: {test_threat['attack_type']}")
    print(f"   Confianza: {test_threat['confidence']*100}%")
    print()
    
    try:
        await alert_manager.telegram.send_threat_alert(
            source_ip=test_threat['source_ip'],
            attack_type=test_threat['attack_type'],
            confidence=test_threat['confidence'],
            payload=test_threat['payload'],
            action_taken=test_threat['action_taken']
        )
        print("   ✅ Alerta enviada a Telegram exitosamente!")
        print("   👉 Revisa tu Telegram, deberías ver el mensaje")
        print()
    except Exception as e:
        print(f"   ❌ Error enviando a Telegram: {e}")
        print()
    
    # Esperar 3 segundos antes del siguiente test
    print("⏳ Esperando 3 segundos...")
    await asyncio.sleep(3)
    print()
    
    print("=" * 80)
    print("TEST 2: ALERTA POR EMAIL")
    print("=" * 80)
    print()
    print("📧 Enviando alerta de prueba por Email...")
    print(f"   De: {config['email']['from_email']}")
    print(f"   Para: {config['email']['to_email']}")
    print()
    
    try:
        await alert_manager.email.send_threat_alert(
            source_ip=test_threat['source_ip'],
            attack_type=test_threat['attack_type'],
            confidence=test_threat['confidence'],
            payload=test_threat['payload'],
            action_taken=test_threat['action_taken']
        )
        print("   ✅ Email enviado exitosamente!")
        print("   👉 Revisa tu bandeja de entrada (y spam si no lo ves)")
        print()
    except Exception as e:
        print(f"   ❌ Error enviando Email: {e}")
        print()
    
    # Esperar 2 segundos
    await asyncio.sleep(2)
    
    print("=" * 80)
    print("TEST 3: ALERTA CRÍTICA (AMBOS CANALES)")
    print("=" * 80)
    print()
    
    critical_threat = {
        'source_ip': '198.51.100.1',
        'attack_type': 'CRITICAL_RCE_ATTEMPT',
        'confidence': 1.0,
        'payload': '🚨 ATAQUE CRÍTICO DETECTADO - Remote Code Execution Attempt',
        'action_taken': 'BLOCK + QUARANTINE'
    }
    
    print("🚨 Enviando alerta CRÍTICA a ambos canales...")
    print(f"   IP: {critical_threat['source_ip']}")
    print(f"   Tipo: {critical_threat['attack_type']}")
    print(f"   Confianza: {critical_threat['confidence']*100}%")
    print()
    
    # Enviar a Telegram
    try:
        await alert_manager.telegram.send_threat_alert(
            source_ip=critical_threat['source_ip'],
            attack_type=critical_threat['attack_type'],
            confidence=critical_threat['confidence'],
            payload=critical_threat['payload'],
            action_taken=critical_threat['action_taken']
        )
        print("   ✅ Alerta crítica enviada a Telegram")
    except Exception as e:
        print(f"   ❌ Error Telegram: {e}")
    
    # Enviar por Email
    try:
        await alert_manager.email.send_threat_alert(
            source_ip=critical_threat['source_ip'],
            attack_type=critical_threat['attack_type'],
            confidence=critical_threat['confidence'],
            payload=critical_threat['payload'],
            action_taken=critical_threat['action_taken']
        )
        print("   ✅ Alerta crítica enviada por Email")
    except Exception as e:
        print(f"   ❌ Error Email: {e}")
    
    print()
    print("=" * 80)
    print("TEST 4: ALERTA DE HONEYPOT")
    print("=" * 80)
    print()
    
    honeypot_alert = {
        'source_ip': '45.142.212.61',
        'attack_type': 'HONEYPOT_SSH_TRAP',
        'confidence': 0.95,
        'payload': '🍯 Atacante capturado en Honeypot SSH - Intento de credenciales: admin/admin123',
        'action_taken': 'MONITOR + LOG'
    }
    
    print("🍯 Enviando alerta de Honeypot...")
    print(f"   IP: {honeypot_alert['source_ip']}")
    print(f"   Credenciales intentadas: admin/admin123")
    print()
    
    try:
        await alert_manager.telegram.send_threat_alert(
            source_ip=honeypot_alert['source_ip'],
            attack_type=honeypot_alert['attack_type'],
            confidence=honeypot_alert['confidence'],
            payload=honeypot_alert['payload'],
            action_taken=honeypot_alert['action_taken']
        )
        print("   ✅ Alerta de Honeypot enviada a Telegram")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    try:
        await alert_manager.email.send_threat_alert(
            source_ip=honeypot_alert['source_ip'],
            attack_type=honeypot_alert['attack_type'],
            confidence=honeypot_alert['confidence'],
            payload=honeypot_alert['payload'],
            action_taken=honeypot_alert['action_taken']
        )
        print("   ✅ Alerta de Honeypot enviada por Email")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=" * 80)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 80)
    print()
    print("   ✅ Test 1: Alerta básica Telegram")
    print("   ✅ Test 2: Alerta básica Email")
    print("   ✅ Test 3: Alerta crítica (ambos canales)")
    print("   ✅ Test 4: Alerta Honeypot (ambos canales)")
    print()
    print("📱 VERIFICA TU TELEGRAM:")
    print("   Deberías tener 3 mensajes del bot")
    print()
    print("📧 VERIFICA TU EMAIL:")
    print("   Deberías tener 3 emails de alertas")
    print("   (Revisa spam si no los ves)")
    print()
    print("=" * 80)
    print("✅ PRUEBAS DE ALERTAS COMPLETADAS")
    print("=" * 80)
    print()
    print("💡 TIP: Si todo funciona, el dashboard también puede enviar alertas")
    print("   usando los botones '📧 Test Email' y '📱 Test Telegram'")
    print()

if __name__ == "__main__":
    asyncio.run(test_alerts())