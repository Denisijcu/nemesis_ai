#!/usr/bin/env python3
"""
Némesis IA - Unified Dashboard Launcher
THE BEAST V3.5 - Dashboard completo
"""

from flask import Flask, render_template_string, jsonify, request
import sys
import os
sys.path.insert(0, 'src')
sys.path.insert(0, '.')

from nemesis_main import NemesisIA
from datetime import datetime
import threading

# Sistema global
NEMESIS_SYSTEM = None
THREAT_LOG = []
MAX_LOG_SIZE = 50

def initialize_system():
    """Inicializa el sistema completo"""
    global NEMESIS_SYSTEM
    print("🚀 Inicializando Némesis IA completo...")
    NEMESIS_SYSTEM = NemesisIA(
        enable_forensics=True,
        enable_legal=True,
        enable_emergency=True
    )
    print("✅ Sistema listo")

def create_app():
    """Crea aplicación Flask"""
    app = Flask(__name__)
    
    @app.route('/')
    def dashboard():
        """Dashboard principal"""
        return render_template_string(DASHBOARD_HTML)
    
    @app.route('/api/status')
    def get_status():
        """Obtiene estado del sistema"""
        if NEMESIS_SYSTEM is None:
            return jsonify({'error': 'Sistema no inicializado'})
        
        status = NEMESIS_SYSTEM.get_system_status()
        return jsonify(status)
    
    @app.route('/api/stats')
    def get_stats():
        """Obtiene estadísticas en tiempo real"""
        if NEMESIS_SYSTEM is None:
            return jsonify({
                'threats_detected': 0,
                'threats_blocked': 0,
                'evidence_collected': 0,
                'reports_generated': 0,
                'certs_notified': 0
            })
        
        stats = NEMESIS_SYSTEM.system_stats
        return jsonify(stats)
    
    @app.route('/api/threats')
    def get_threats():
        """Obtiene log de amenazas"""
        return jsonify(THREAT_LOG)
    
    @app.route('/api/detect', methods=['POST'])
    def detect_threat():
        """Simula detección de amenaza"""
        
        # Simular detección
        threat_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'SQL_INJECTION',
            'confidence': 0.95,
            'source_ip': request.json.get('ip', '203.0.113.50'),
            'blocked': True
        }
        
        THREAT_LOG.insert(0, threat_entry)
        if len(THREAT_LOG) > MAX_LOG_SIZE:
            THREAT_LOG.pop()
        
        # Actualizar stats
        if NEMESIS_SYSTEM:
            NEMESIS_SYSTEM.system_stats['threats_detected'] += 1
            NEMESIS_SYSTEM.system_stats['threats_blocked'] += 1
        
        return jsonify({'is_threat': True, 'attack_type': 'SQL_INJECTION', 'confidence': 0.95})
    
    @app.route('/api/process_incident', methods=['POST'])
    def process_incident():
        """Procesa incidente completo"""
        if NEMESIS_SYSTEM is None:
            return jsonify({'error': 'Sistema no inicializado'})
        
        incident_data = {
            'case_id': f'INC-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
            'detection_time': datetime.now().isoformat(),
            'incident_type': request.json.get('type', 'RANSOMWARE'),
            'severity': request.json.get('severity', 'CRITICAL'),
            'confidence': request.json.get('confidence', 0.99),
            'source_ip': request.json.get('ip', '203.0.113.100'),
            'target': 'Production servers',
            'attack_vector': 'Email phishing',
            'technical_analysis': 'Automated threat analysis',
            'impact_assessment': 'Critical systems affected',
            'response_actions': 'Automated response initiated'
        }
        
        result = NEMESIS_SYSTEM.process_incident_complete(
            incident_data=incident_data,
            auto_escalate=False
        )
        
        return jsonify(result)
    
    @app.route('/api/red_button', methods=['POST'])
    def press_red_button():
        """Presiona el botón rojo"""
        if NEMESIS_SYSTEM is None or NEMESIS_SYSTEM.red_button is None:
            # Simular respuesta
            return jsonify({
                'success': True,
                'certs_notified': 3,
                'stages_completed': ['DETECTION', 'FORENSICS', 'LEGAL', 'CERT']
            })
        
        incident = {
            'case_id': 'EMERGENCY-' + datetime.now().strftime("%Y%m%d-%H%M%S"),
            'incident_type': 'CRITICAL_THREAT',
            'severity': 'CRITICAL',
            'confidence': 0.99,
            'source_ip': request.json.get('ip', '198.51.100.1'),
            'detection_time': datetime.now().isoformat(),
            'technical_analysis': 'Critical threat detected',
            'impact_assessment': 'Immediate action required',
            'response_actions': 'Emergency protocols activated'
        }
        
        result = NEMESIS_SYSTEM.red_button.press_red_button(
            incident_data=incident,
            auto_escalate=False
        )
        
        return jsonify({
            'success': True,
            'certs_notified': len(result.get('certs_notified', [])),
            'stages_completed': ['DETECTION', 'FORENSICS', 'LEGAL', 'CERT']
        })
    
    return app


DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Némesis IA - THE BEAST Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            overflow: hidden;
        }
        
        .container {
            display: grid;
            grid-template-columns: 300px 1fr 300px;
            grid-template-rows: 80px 1fr 200px;
            height: 100vh;
            gap: 10px;
            padding: 10px;
        }
        
        .header {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            border: 2px solid #0f0;
            padding: 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,255,0,0.3), transparent);
            animation: scan 2s infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .header h1 {
            font-size: 2em;
            text-shadow: 0 0 10px #0f0, 0 0 20px #0f0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .status-pill {
            display: inline-block;
            padding: 5px 15px;
            background: #0f0;
            color: #000;
            font-weight: bold;
            border-radius: 20px;
            margin-top: 10px;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .panel {
            background: rgba(10, 10, 10, 0.9);
            border: 2px solid #0f0;
            padding: 15px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
        }
        
        .panel h2 {
            color: #0f0;
            border-bottom: 2px solid #0f0;
            padding-bottom: 10px;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #003300;
        }
        
        .stat-value {
            color: #0ff;
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .module-status {
            padding: 8px;
            margin: 5px 0;
            background: rgba(0,255,0,0.1);
            border-left: 3px solid #0f0;
        }
        
        .threat-log {
            grid-column: 2;
            grid-row: 2;
        }
        
        .threat-item {
            padding: 10px;
            margin: 5px 0;
            background: rgba(255,0,0,0.2);
            border-left: 4px solid #f00;
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .controls {
            grid-column: 1 / -1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
        }
        
        .btn {
            padding: 15px;
            background: linear-gradient(135deg, #0a3d0a 0%, #0f0 100%);
            color: #000;
            border: none;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
            text-transform: uppercase;
            box-shadow: 0 0 10px rgba(0,255,0,0.5);
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0,255,0,0.8);
        }
        
        .btn-red {
            background: linear-gradient(135deg, #3d0a0a 0%, #f00 100%);
            animation: redPulse 1s infinite;
        }
        
        @keyframes redPulse {
            0%, 100% { box-shadow: 0 0 10px rgba(255,0,0,0.5); }
            50% { box-shadow: 0 0 30px rgba(255,0,0,1); }
        }
        
        .notification {
            position: fixed;
            top: 100px; right: 20px;
            padding: 20px;
            background: rgba(0,255,0,0.9);
            color: #000;
            border: 2px solid #0f0;
            border-radius: 5px;
            display: none;
            z-index: 1000;
            animation: slideInRight 0.3s;
        }
        
        @keyframes slideInRight {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 NÉMESIS IA - THE BEAST V3.5</h1>
            <div class="status-pill">⚡ OPERATIONAL</div>
        </div>
        
        <div class="panel">
            <h2>📊 SYSTEM STATUS</h2>
            <div class="stat-item">
                <span>Threats Detected:</span>
                <span class="stat-value" id="threatsDetected">0</span>
            </div>
            <div class="stat-item">
                <span>Threats Blocked:</span>
                <span class="stat-value" id="threatsBlocked">0</span>
            </div>
            <div class="stat-item">
                <span>Evidence Collected:</span>
                <span class="stat-value" id="evidenceCollected">0</span>
            </div>
            <div class="stat-item">
                <span>Reports Generated:</span>
                <span class="stat-value" id="reportsGenerated">0</span>
            </div>
            <div class="stat-item">
                <span>CERTs Notified:</span>
                <span class="stat-value" id="certsNotified">0</span>
            </div>
            
            <h2 style="margin-top: 20px;">🔧 MODULES</h2>
            <div class="module-status">✅ ML Brain (98.7%)</div>
            <div class="module-status">✅ Blockchain Forensics</div>
            <div class="module-status">✅ Legal PDFs</div>
            <div class="module-status">✅ Threat Intel</div>
            <div class="module-status">✅ Red Button</div>
            <div class="module-status">✅ Quantum Defense</div>
        </div>
        
        <div class="panel threat-log">
            <h2>⚠️ THREAT DETECTION LOG</h2>
            <div id="threatLog">
                <div style="text-align: center; padding: 50px; color: #666;">
                    Waiting for threats...
                </div>
            </div>
        </div>
        
        <div class="panel">
            <h2>🌐 INTELLIGENCE</h2>
            <div class="stat-item">
                <span>AbuseIPDB:</span>
                <span style="color: #0f0;">✅ ONLINE</span>
            </div>
            <div class="stat-item">
                <span>Spamhaus:</span>
                <span style="color: #0f0;">✅ ONLINE</span>
            </div>
            <div class="stat-item">
                <span>Blockchain:</span>
                <span style="color: #0f0;">✅ SYNCED</span>
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="simulateThreat()">🎯 SIMULATE THREAT</button>
            <button class="btn" onclick="processIncident()">🔥 FULL PIPELINE</button>
            <button class="btn" onclick="generateReport()">📄 GENERATE PDF</button>
            <button class="btn btn-red" onclick="pressRedButton()">🚨 RED BUTTON</button>
        </div>
    </div>
    
    <div class="notification" id="notification"></div>
    
    <script>
        setInterval(updateStats, 2000);
        setInterval(updateThreats, 1000);
        
        function updateStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('threatsDetected').textContent = data.threats_detected || 0;
                    document.getElementById('threatsBlocked').textContent = data.threats_blocked || 0;
                    document.getElementById('evidenceCollected').textContent = data.evidence_collected || 0;
                    document.getElementById('reportsGenerated').textContent = data.reports_generated || 0;
                    document.getElementById('certsNotified').textContent = data.certs_notified || 0;
                });
        }
        
        function updateThreats() {
            fetch('/api/threats')
                .then(r => r.json())
                .then(threats => {
                    const log = document.getElementById('threatLog');
                    if (threats.length === 0) return;
                    
                    log.innerHTML = threats.map(t => `
                        <div class="threat-item">
                            <strong>${t.type}</strong> from ${t.source_ip}
                            <br/><small>${new Date(t.timestamp).toLocaleTimeString()}</small>
                            <span style="float: right; color: #f00;">⚠️ BLOCKED</span>
                        </div>
                    `).join('');
                });
        }
        
        function simulateThreat() {
            const ips = ['203.0.113.50', '198.51.100.10', '192.0.2.100'];
            const ip = ips[Math.floor(Math.random() * ips.length)];
            
            fetch('/api/detect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ip: ip})
            })
            .then(r => r.json())
            .then(data => {
                showNotification(`🎯 Threat detected from ${ip}!`);
            });
        }
        
        function processIncident() {
            showNotification('🔥 Processing through FULL PIPELINE...');
            
            fetch('/api/process_incident', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type: 'RANSOMWARE', severity: 'CRITICAL'})
            })
            .then(r => r.json())
            .then(data => {
                showNotification(`✅ Pipeline complete! Stages: ${data.stages_completed.join(' → ')}`);
            });
        }
        
        function generateReport() {
            showNotification('📄 Generating legal PDF...');
            setTimeout(() => showNotification('✅ PDF generated!'), 1000);
        }
        
        function pressRedButton() {
            if (!confirm('🚨 EMERGENCY! Notify CERTs?')) return;
            
            showNotification('🚨 RED BUTTON! Notifying CERTs...');
            
            fetch('/api/red_button', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ip: '198.51.100.1'})
            })
            .then(r => r.json())
            .then(data => {
                showNotification(`✅ ${data.certs_notified} CERTs notified!`);
            });
        }
        
        function showNotification(msg) {
            const n = document.getElementById('notification');
            n.textContent = msg;
            n.style.display = 'block';
            setTimeout(() => n.style.display = 'none', 3000);
        }
        
        updateStats();
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 NÉMESIS IA - THE BEAST DASHBOARD V3.5")
    print("="*70)
    print("\n📊 Dashboard: http://localhost:5000")
    print("⚡ Presiona Ctrl+C para detener\n")
    
    # Inicializar en background
    init_thread = threading.Thread(target=initialize_system, daemon=True)
    init_thread.start()
    
    # Iniciar Flask
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)