#!/usr/bin/env python3
"""
Test del RED BUTTON - Botón de Emergencia de NÉMESIS IA
Simula un ataque crítico que requiere notificación inmediata a CERTs
"""
import sys
sys.path.insert(0, 'src')
from datetime import datetime

def test_red_button():
    print("=" * 80)
    print("🚨 TEST DEL RED BUTTON - BOTÓN DE EMERGENCIA NÉMESIS IA")
    print("=" * 80)
    print()
    
    print("⚠️  ADVERTENCIA:")
    print("   El RED BUTTON es para EMERGENCIAS REALES de ciberseguridad")
    print("   Este es un TEST controlado con datos simulados")
    print()
    
    # Importar sistema
    print("🔧 Inicializando sistema NÉMESIS...")
    try:
        from nemesis_main import NemesisIA
        nemesis = NemesisIA(
            enable_forensics=True,
            enable_legal=True,
            enable_emergency=True
        )
        print("   ✅ Sistema NÉMESIS inicializado")
        print("   ✅ Módulo forense activado")
        print("   ✅ Módulo legal activado")
        print("   ✅ Módulo de emergencia activado")
        print()
    except Exception as e:
        print(f"   ❌ Error inicializando NÉMESIS: {e}")
        print()
        print("💡 Verifica que nemesis_main.py existe y tiene NemesisIA class")
        return
    
    # Verificar componentes
    print("🔍 Verificando componentes del RED BUTTON...")
    components = []
    
    if hasattr(nemesis, 'forensic_sentinel') and nemesis.forensic_sentinel:
        print("   ✅ ForensicSentinel (Blockchain) - DISPONIBLE")
        components.append('forensic')
    else:
        print("   ⚠️  ForensicSentinel - NO DISPONIBLE")
    
    if hasattr(nemesis, 'fiscal_digital') and nemesis.fiscal_digital:
        print("   ✅ FiscalDigital (PDFs legales) - DISPONIBLE")
        components.append('legal')
    else:
        print("   ⚠️  FiscalDigital - NO DISPONIBLE")
    
    if hasattr(nemesis, 'red_button') and nemesis.red_button:
        print("   ✅ RedButton (Notificación CERTs) - DISPONIBLE")
        components.append('emergency')
    else:
        print("   ⚠️  RedButton - NO DISPONIBLE")
    
    print()
    
    if 'emergency' not in components:
        print("❌ RED BUTTON NO ESTÁ DISPONIBLE")
        print("   El sistema no tiene el módulo de emergencia configurado")
        return
    
    # Datos del incidente crítico
    print("=" * 80)
    print("🎯 SIMULANDO INCIDENTE CRÍTICO")
    print("=" * 80)
    print()
    
    incident_data = {
        'case_id': f'EMERGENCY-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
        'incident_type': 'CRITICAL_INFRASTRUCTURE_ATTACK',
        'severity': 'CRITICAL',
        'confidence': 0.99,
        'source_ip': '45.142.212.61',
        'target_system': 'Production Database Server',
        'detection_time': datetime.now().isoformat(),
        'attack_vector': 'SQL Injection + Remote Code Execution',
        'technical_analysis': '''
ANÁLISIS TÉCNICO DEL INCIDENTE:

1. VECTOR DE ATAQUE:
   - SQL Injection en endpoint /api/users
   - Escalación a Remote Code Execution
   - Intento de exfiltración de base de datos

2. IMPACTO DETECTADO:
   - Acceso no autorizado a base de datos de producción
   - 150,000 registros de usuarios en riesgo
   - Intento de lateral movement hacia servidores internos

3. EVIDENCIA RECOLECTADA:
   - Logs de firewall (200+ peticiones maliciosas)
   - Capturas de tráfico (PCAP files)
   - Volcados de memoria del proceso comprometido
   - Blockchain evidence hash: a3f5b2c8d9e1...

4. RESPUESTA INMEDIATA:
   - IP 45.142.212.61 bloqueada en firewall
   - Servidor de producción aislado de red
   - Snapshot de sistema comprometido creado
   - Notificación a equipo de respuesta a incidentes
        ''',
        'impact_assessment': 'CRÍTICO - Datos sensibles en riesgo',
        'response_actions': '''
ACCIONES TOMADAS:
1. ✅ Aislamiento inmediato del servidor comprometido
2. ✅ Bloqueo de IP atacante en perímetro
3. ✅ Recolección de evidencia forense
4. ✅ Notificación a equipo de seguridad
5. ✅ Activación de plan de respuesta a incidentes
6. 🚨 NOTIFICACIÓN A CERTS REQUERIDA
        ''',
        'affected_systems': [
            'db-prod-01.company.com',
            'web-frontend-03.company.com'
        ],
        'data_at_risk': '150,000 user records (PII)',
        'estimated_cost': '$500,000 USD'
    }
    
    print("📋 DETALLES DEL INCIDENTE:")
    print(f"   Case ID: {incident_data['case_id']}")
    print(f"   Tipo: {incident_data['incident_type']}")
    print(f"   Severidad: {incident_data['severity']}")
    print(f"   Confianza: {incident_data['confidence']*100}%")
    print(f"   IP Atacante: {incident_data['source_ip']}")
    print(f"   Sistema Objetivo: {incident_data['target_system']}")
    print(f"   Datos en riesgo: {incident_data['data_at_risk']}")
    print(f"   Costo estimado: {incident_data['estimated_cost']}")
    print()
    
    # Confirmar presionar RED BUTTON
    print("=" * 80)
    print("⚠️  CONFIRMACIÓN REQUERIDA")
    print("=" * 80)
    print()
    print("Al presionar el RED BUTTON se ejecutará:")
    print("   1. 📄 Generación de PDFs legales")
    print("   2. 🔗 Registro en blockchain inmutable")
    print("   3. 📧 Notificación a CERTs configurados")
    print("   4. 🚨 Escalación automática de incidente")
    print()
    
    confirm = input("¿Deseas presionar el RED BUTTON? (si/no): ").strip().lower()
    
    if confirm not in ['si', 's', 'yes', 'y']:
        print()
        print("❌ RED BUTTON NO PRESIONADO - Test cancelado")
        return
    
    print()
    print("=" * 80)
    print("🚨🚨🚨 PRESIONANDO RED BUTTON 🚨🚨🚨")
    print("=" * 80)
    print()
    
    # Presionar RED BUTTON
    try:
        result = nemesis.red_button.press_red_button(
            incident_data=incident_data,
            auto_escalate=False  # No escalar automáticamente en test
        )
        
        print("✅ RED BUTTON PRESIONADO EXITOSAMENTE")
        print()
        
        # Mostrar resultados
        print("=" * 80)
        print("📊 RESULTADO DE LA OPERACIÓN")
        print("=" * 80)
        print()
        
        if 'legal_package' in result:
            print("📄 PAQUETE LEGAL GENERADO:")
            package = result['legal_package']
            print(f"   Ruta: {package.get('package_dir', 'N/A')}")
            print(f"   Archivos generados: {len(package.get('files', []))}")
            if package.get('files'):
                for file in package['files']:
                    print(f"      • {file}")
            print()
        
        if 'blockchain_record' in result:
            print("🔗 EVIDENCIA EN BLOCKCHAIN:")
            blockchain = result['blockchain_record']
            print(f"   Evidence ID: {blockchain.get('evidence_id', 'N/A')}")
            print(f"   Block Hash: {blockchain.get('block_hash', 'N/A')[:32]}...")
            print(f"   Chain válida: {'✅' if blockchain.get('chain_valid') else '❌'}")
            print()
        
        if 'certs_notified' in result:
            print("📧 CERTs NOTIFICADOS:")
            certs = result['certs_notified']
            if certs:
                for cert in certs:
                    print(f"   • {cert}")
            else:
                print("   ⚠️  No hay CERTs configurados (esto es normal en test)")
            print()
        
        if 'timestamp' in result:
            print(f"⏰ Timestamp: {result['timestamp']}")
            print()
        
        print("=" * 80)
        print("✅ OPERACIÓN DE EMERGENCIA COMPLETADA")
        print("=" * 80)
        print()
        
        # Verificar archivos generados
        if 'legal_package' in result and result['legal_package'].get('package_dir'):
            package_dir = result['legal_package']['package_dir']
            print("📁 Archivos generados en:")
            print(f"   {package_dir}")
            print()
            print("Puedes revisarlos con:")
            print(f"   ls -lh {package_dir}")
            print()
        
        # Stats del sistema
        print("📊 ESTADÍSTICAS DEL SISTEMA NÉMESIS:")
        if hasattr(nemesis, 'system_stats'):
            stats = nemesis.system_stats
            print(f"   Amenazas detectadas: {stats.get('threats_detected', 0)}")
            print(f"   Amenazas bloqueadas: {stats.get('threats_blocked', 0)}")
            print(f"   Evidencia recolectada: {stats.get('evidence_collected', 0)}")
            print(f"   Reportes generados: {stats.get('reports_generated', 0)}")
            print(f"   CERTs notificados: {stats.get('certs_notified', 0)}")
        print()
        
    except Exception as e:
        print(f"❌ ERROR al presionar RED BUTTON: {e}")
        print()
        import traceback
        print("Stack trace:")
        traceback.print_exc()
        return
    
    print("=" * 80)
    print("🎯 TEST DEL RED BUTTON COMPLETADO")
    print("=" * 80)
    print()
    print("✅ Verificaciones recomendadas:")
    print("   1. Revisar PDFs generados en legal_documents/")
    print("   2. Verificar blockchain con test_forensic_system.py")
    print("   3. Comprobar que la evidencia es admisible en corte")
    print()
    print("💡 En producción, esto notificaría a:")
    print("   • CERT Nacional (INCIBE en España)")
    print("   • US-CERT (si aplica)")
    print("   • Autoridades locales de ciberseguridad")
    print("   • Equipo interno de respuesta a incidentes")
    print()

if __name__ == "__main__":
    test_red_button()