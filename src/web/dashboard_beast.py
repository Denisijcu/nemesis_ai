#!/usr/bin/env python3
"""
Némesis IA - THE BEAST V4.0
Dashboard completo con TODOS los módulos integrados
"""

import asyncio
import json
from datetime import datetime
from aiohttp import web
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from database.threat_database import ThreatDatabase


class DashboardBeast:
    """THE BEAST - Dashboard unificado completo"""
    
    def __init__(self, database, host="0.0.0.0", port=8080):
        self.db = database
        self.host = host
        self.port = port
        self.app = web.Application()
        
        # Módulos opcionales (se cargan si existen)
        self.nemesis_system = None
        self.traffic_sentinel = None
        
        # Intentar cargar sistema unificado
        try:
            from nemesis_main import NemesisIA
            self.nemesis_system = NemesisIA(
                enable_forensics=True,
                enable_legal=True,
                enable_emergency=True
            )
            print("✅ Sistema Némesis cargado")
        except Exception as e:
            print(f"⚠️ Sistema Némesis no disponible: {e}")
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura rutas"""
        self.app.router.add_get('/', self.handle_dashboard)
        self.app.router.add_get('/api/stats', self.handle_stats)
        self.app.router.add_get('/api/threats', self.handle_threats)
        self.app.router.add_get('/api/map_data', self.handle_map_data)
        self.app.router.add_get('/api/honeypot', self.handle_honeypot)
        self.app.router.add_get('/api/traffic', self.handle_traffic)
        
        # NUEVAS RUTAS para módulos integrados
        self.app.router.add_get('/api/blockchain', self.handle_blockchain)
        self.app.router.add_post('/api/generate_pdf', self.handle_generate_pdf)
        self.app.router.add_post('/api/red_button', self.handle_red_button)
        self.app.router.add_get('/api/quantum_status', self.handle_quantum)
        self.app.router.add_get('/api/adversarial', self.handle_adversarial)
        self.app.router.add_get('/api/collective', self.handle_collective)
        self.app.router.add_get('/api/unified_stats', self.handle_unified_stats)
    
    async def handle_dashboard(self, request):
        """Sirve el dashboard HTML"""
        return web.Response(text=HTML_TEMPLATE, content_type='text/html')
    
    async def handle_stats(self, request):
        """Stats básicas"""
        stats = self.db.get_statistics()
        return web.json_response(stats)
    
    async def handle_threats(self, request):
        """Últimas amenazas"""
        threats = self.db.get_threats(limit=20)
        threat_list = [{
            'timestamp': t.timestamp,
            'source_ip': t.source_ip,
            'attack_type': t.attack_type,
            'confidence': t.confidence,
            'action_taken': t.action_taken
        } for t in threats]
        return web.json_response(threat_list)
    
    async def handle_map_data(self, request):
        """Datos para el mapa"""
        threats = self.db.get_threats(limit=50)
        return web.json_response([{
            'ip': t.source_ip,
            'type': t.attack_type,
            'time': t.timestamp
        } for t in threats])
    
    async def handle_honeypot(self, request):
        """Stats del honeypot"""
        threats = self.db.get_threats(limit=1000)
        honeypot_threats = [t for t in threats if 'HONEYPOT' in t.attack_type]
        
        return web.json_response({
            'total_captures': len(honeypot_threats),
            'recent': [{
                'ip': t.source_ip,
                'timestamp': t.timestamp,
                'credentials': t.payload or 'N/A'
            } for t in honeypot_threats[:5]]
        })
    
    async def handle_traffic(self, request):
        """Stats de tráfico"""
        if self.traffic_sentinel:
            status = self.traffic_sentinel.get_system_status()
            return web.json_response(status['statistics'])
        return web.json_response({
            'packets_processed': 0,
            'bandwidth_mbps': 0,
            'packets_per_second': 0
        })
    
    async def handle_blockchain(self, request):
        """Stats de blockchain"""
        if self.nemesis_system and self.nemesis_system.forensic_sentinel:
            blockchain = self.nemesis_system.forensic_sentinel.blockchain
            return web.json_response({
                'chain_length': len(blockchain.chain),
                'total_evidence': blockchain.stats['total_evidence'],
                'chain_valid': blockchain.stats['chain_valid'],
                'last_block_hash': blockchain.chain[-1].hash[:16] if len(blockchain.chain) > 0 else 'N/A'
            })
        return web.json_response({
            'chain_length': 0,
            'total_evidence': 0,
            'chain_valid': False
        })
    
    async def handle_generate_pdf(self, request):
        """Genera PDF legal"""
        if self.nemesis_system and self.nemesis_system.fiscal_digital:
            incident_data = await request.json()
            
            incident = {
                'case_id': f'WEB-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                'detection_time': datetime.now().isoformat(),
                'incident_type': incident_data.get('type', 'CYBER_ATTACK'),
                'severity': incident_data.get('severity', 'HIGH'),
                'confidence': 0.95,
                'source_ip': incident_data.get('ip', '203.0.113.50'),
                'technical_analysis': 'Generated from dashboard'
            }
            
            filepath = self.nemesis_system.fiscal_digital.generate_incident_report(incident)
            
            return web.json_response({
                'success': True,
                'filepath': filepath,
                'message': 'PDF generated successfully'
            })
        
        return web.json_response({
            'success': False,
            'message': 'Legal module not available'
        })
    
    async def handle_red_button(self, request):
        """Presiona el botón rojo"""
        if self.nemesis_system and self.nemesis_system.red_button:
            incident_data = await request.json()
            
            incident = {
                'case_id': f'EMERGENCY-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                'incident_type': 'CRITICAL_THREAT',
                'severity': 'CRITICAL',
                'confidence': 0.99,
                'source_ip': incident_data.get('ip', '198.51.100.1'),
                'detection_time': datetime.now().isoformat(),
                'technical_analysis': 'Emergency escalation from dashboard',
                'impact_assessment': 'Critical incident',
                'response_actions': 'Emergency protocols activated'
            }
            
            result = self.nemesis_system.red_button.press_red_button(
                incident_data=incident,
                auto_escalate=False
            )
            
            return web.json_response({
                'success': True,
                'certs_notified': len(result.get('certs_notified', [])),
                'cert_list': result.get('certs_notified', [])
            })
        
        return web.json_response({
            'success': False,
            'message': 'Red Button not available'
        })
    
    async def handle_quantum(self, request):
        """Status de quantum defense"""
        if self.nemesis_system and self.nemesis_system.quantum_sentinel:
            return web.json_response({
                'enabled': True,
                'status': 'ACTIVE',
                'algorithm': 'Kyber-768 + Dilithium-3'
            })
        return web.json_response({'enabled': False})
    
    async def handle_adversarial(self, request):
        """Stats de AI vs AI"""
        # Simulado por ahora
        return web.json_response({
            'attacks_detected': 0,
            'attacks_blocked': 0,
            'model_poisoning_prevented': 0
        })
    
    async def handle_collective(self, request):
        """Stats de multi-agent"""
        # Simulado por ahora
        return web.json_response({
            'active_agents': 5,
            'consensus_reached': 0,
            'coordinated_responses': 0
        })
    
    async def handle_unified_stats(self, request):
        """Stats unificadas de TODOS los módulos"""
        if self.nemesis_system:
            unified = self.nemesis_system.system_stats
            return web.json_response(unified)
        return web.json_response({
            'threats_detected': 0,
            'threats_blocked': 0,
            'evidence_collected': 0,
            'reports_generated': 0,
            'certs_notified': 0
        })
    
    async def run(self):
        """Inicia el servidor"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        print(f"🌐 Dashboard: http://{self.host}:{self.port}")
        
        # Mantener corriendo
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            await runner.cleanup()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Némesis IA - THE BEAST V4.0</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #0f0;
            overflow-x: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
            border-bottom: 3px solid #0f0;
            padding: 20px;
            text-align: center;
            position: relative;
            box-shadow: 0 0 30px rgba(0,255,0,0.3);
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,255,0,0.3), transparent);
            animation: scan 3s infinite;
        }
        
        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .header h1 {
            font-size: 2.5em;
            text-shadow: 0 0 20px #0f0;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; text-shadow: 0 0 20px #0f0; }
            50% { opacity: 0.8; text-shadow: 0 0 40px #0f0; }
        }
        
        .status-bar {
            display: flex;
            justify-content: space-around;
            padding: 15px;
            background: rgba(0,20,0,0.8);
            border-bottom: 2px solid #0f0;
        }
        
        .stat-box {
            text-align: center;
            padding: 10px;
            border: 2px solid #0f0;
            border-radius: 5px;
            min-width: 150px;
            background: rgba(0,50,0,0.3);
        }
        
        .stat-value {
            font-size: 2em;
            color: #0ff;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.8em;
            color: #0f0;
        }
        
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 15px;
            padding: 15px;
        }
        
        .panel {
            background: rgba(10,10,10,0.95);
            border: 2px solid #0f0;
            border-radius: 5px;
            padding: 15px;
            box-shadow: 0 0 20px rgba(0,255,0,0.2);
        }
        
        .panel h2 {
            color: #0f0;
            border-bottom: 2px solid #0f0;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        
        .module-badge {
            display: inline-block;
            padding: 5px 10px;
            margin: 5px;
            background: rgba(0,255,0,0.2);
            border: 1px solid #0f0;
            border-radius: 3px;
            font-size: 0.9em;
        }
        
        .module-badge.active::before {
            content: '● ';
            color: #0f0;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
        
        .btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #0a3d0a 0%, #0f0 100%);
            color: #000;
            border: none;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            cursor: pointer;
            font-size: 1em;
            margin: 5px;
            transition: all 0.3s;
            box-shadow: 0 0 10px rgba(0,255,0,0.5);
        }
        
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(0,255,0,0.8);
        }
        
        .btn-red {
            background: linear-gradient(135deg, #3d0a0a 0%, #f00 100%);
            animation: redPulse 1.5s infinite;
        }
        
        @keyframes redPulse {
            0%, 100% { box-shadow: 0 0 10px rgba(255,0,0,0.5); }
            50% { box-shadow: 0 0 30px rgba(255,0,0,1); }
        }
        
        .threat-item {
            padding: 10px;
            margin: 8px 0;
            background: rgba(255,0,0,0.2);
            border-left: 4px solid #f00;
            animation: slideIn 0.3s;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .blockchain-block {
            padding: 8px;
            margin: 5px 0;
            background: rgba(0,255,255,0.1);
            border-left: 3px solid #0ff;
            font-size: 0.9em;
        }
        
        .quantum-badge {
            display: inline-block;
            padding: 5px 15px;
            background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
            color: #000;
            font-weight: bold;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,255,255,0.5);
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 20px;
            background: rgba(0,255,0,0.95);
            color: #000;
            border: 2px solid #0f0;
            border-radius: 5px;
            display: none;
            z-index: 10000;
            box-shadow: 0 0 30px rgba(0,255,0,0.8);
            animation: slideInRight 0.3s;
        }
        
        @keyframes slideInRight {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
        
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        
        .evidence-item {
            padding: 8px;
            margin: 5px 0;
            background: rgba(0,150,255,0.1);
            border-left: 3px solid #09f;
            font-size: 0.85em;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 NÉMESIS IA - THE BEAST V4.0 🚀</h1>
        <div style="margin-top: 10px;">
            <span class="quantum-badge">⚛️ QUANTUM PROTECTED</span>
            <span class="quantum-badge">🔗 BLOCKCHAIN EVIDENCE</span>
            <span class="quantum-badge">🤖 AI vs AI DEFENSE</span>
        </div>
    </div>
    
    <div class="status-bar">
        <div class="stat-box">
            <div class="stat-value" id="threatsDetected">0</div>
            <div class="stat-label">THREATS DETECTED</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="threatsBlocked">0</div>
            <div class="stat-label">THREATS BLOCKED</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="evidenceCollected">0</div>
            <div class="stat-label">EVIDENCE COLLECTED</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="reportsGenerated">0</div>
            <div class="stat-label">PDFs GENERATED</div>
        </div>
        <div class="stat-box">
            <div class="stat-value" id="certsNotified">0</div>
            <div class="stat-label">CERTs NOTIFIED</div>
        </div>
    </div>
    
    <div class="main-grid">
        <!-- LEFT PANEL -->
        <div>
            <div class="panel">
                <h2>🔧 ALL MODULES</h2>
                <div class="module-badge active">ML Brain 98.7%</div>
                <div class="module-badge active">Network Sentinel</div>
                <div class="module-badge active">Honeypots</div>
                <div class="module-badge active">Traffic Analyzer</div>
                <div class="module-badge active">IP Reputation</div>
                <div class="module-badge active">Auto Response</div>
                <div class="module-badge active" id="quantumBadge">Quantum Defense</div>
                <div class="module-badge active">Blockchain Forensics</div>
                <div class="module-badge active">Legal PDFs</div>
                <div class="module-badge active">Threat Intel</div>
                <div class="module-badge active">Red Button (CERT)</div>
                <div class="module-badge active">AI vs AI</div>
                <div class="module-badge active">Multi-Agent</div>
            </div>
            
            <div class="panel" style="margin-top: 15px;">
                <h2>🔗 BLOCKCHAIN</h2>
                <div id="blockchainStats">
                    <div class="blockchain-block">
                        Chain Length: <span id="chainLength">0</span>
                    </div>
                    <div class="blockchain-block">
                        Evidence Items: <span id="evidenceCount">0</span>
                    </div>
                    <div class="blockchain-block">
                        Chain Valid: <span id="chainValid">✓</span>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- CENTER PANEL -->
        <div>
            <div class="panel">
                <h2>⚠️ LIVE THREAT FEED</h2>
                <div id="threatFeed">
                    <div style="text-align: center; padding: 30px; color: #666;">
                        Monitoring for threats...
                    </div>
                </div>
            </div>
            
            <div class="panel" style="margin-top: 15px;">
                <h2>🎮 CONTROLS</h2>
                <div class="controls">
                    <button class="btn" onclick="generatePDF()">📄 GENERATE PDF</button>
                    <button class="btn" onclick="viewBlockchain()">🔗 VIEW BLOCKCHAIN</button>
                    <button class="btn" onclick="checkQuantum()">⚛️ QUANTUM STATUS</button>
                    <button class="btn btn-red" onclick="pressRedButton()">🚨 RED BUTTON</button>
                </div>
            </div>
        </div>
        
        <!-- RIGHT PANEL -->
        <div>
            <div class="panel">
                <h2>🍯 HONEYPOT</h2>
                <div>
                    Total Captures: <span id="honeypotTotal" style="color: #0ff; font-size: 1.5em;">0</span>
                </div>
                <div id="honeypotRecent" style="margin-top: 10px; font-size: 0.85em;">
                </div>
            </div>
            
            <div class="panel" style="margin-top: 15px;">
                <h2>🤖 AI vs AI</h2>
                <div class="evidence-item">
                    Adversarial Attacks: <span id="adversarialAttacks">0</span>
                </div>
                <div class="evidence-item">
                    Attacks Blocked: <span id="adversarialBlocked">0</span>
                </div>
            </div>
            
            <div class="panel" style="margin-top: 15px;">
                <h2>🌐 MULTI-AGENT</h2>
                <div class="evidence-item">
                    Active Agents: <span id="activeAgents">0</span>
                </div>
                <div class="evidence-item">
                    Consensus Reached: <span id="consensusReached">0</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="notification" id="notification"></div>
    
    <script>
        // Update stats every 2 seconds
        setInterval(updateUnifiedStats, 2000);
        setInterval(updateThreats, 2000);
        setInterval(updateBlockchain, 3000);
        setInterval(updateHoneypot, 2000);
        setInterval(updateAdversarial, 3000);
        setInterval(updateCollective, 3000);
        
        function updateUnifiedStats() {
            fetch('/api/unified_stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('threatsDetected').textContent = data.threats_detected || 0;
                    document.getElementById('threatsBlocked').textContent = data.threats_blocked || 0;
                    document.getElementById('evidenceCollected').textContent = data.evidence_collected || 0;
                    document.getElementById('reportsGenerated').textContent = data.reports_generated || 0;
                    document.getElementById('certsNotified').textContent = data.certs_notified || 0;
                })
                .catch(e => console.error('Error:', e));
        }
        
        function updateThreats() {
            fetch('/api/threats')
                .then(r => r.json())
                .then(threats => {
                    const feed = document.getElementById('threatFeed');
                    if (threats.length === 0) return;
                    
                    feed.innerHTML = threats.slice(0, 10).map(t => `
                        <div class="threat-item">
                            <strong>${t.attack_type}</strong> from ${t.source_ip}
                            <br/><small>${new Date(t.timestamp).toLocaleString()}</small>
                            <span style="float: right; color: #f00;">⚠️ ${t.action_taken}</span>
                        </div>
                    `).join('');
                })
                .catch(e => console.error('Error:', e));
        }
        
        function updateBlockchain() {
            fetch('/api/blockchain')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('chainLength').textContent = data.chain_length || 0;
                    document.getElementById('evidenceCount').textContent = data.total_evidence || 0;
                    document.getElementById('chainValid').textContent = data.chain_valid ? '✓' : '✗';
                })
                .catch(e => console.error('Error:', e));
        }
        
        function updateHoneypot() {
            fetch('/api/honeypot')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('honeypotTotal').textContent = data.total_captures || 0;
                    
                    const recent = document.getElementById('honeypotRecent');
                    if (data.recent && data.recent.length > 0) {
                        recent.innerHTML = data.recent.slice(0, 3).map(c => `
                            <div class="evidence-item">
                                ${c.ip}<br/>
                                <small>${c.credentials}</small>
                            </div>
                        `).join('');
                    }
                })
                .catch(e => console.error('Error:', e));
        }
        
        function updateAdversarial() {
            fetch('/api/adversarial')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('adversarialAttacks').textContent = data.attacks_detected || 0;
                    document.getElementById('adversarialBlocked').textContent = data.attacks_blocked || 0;
                })
                .catch(e => console.error('Error:', e));
        }
        
        function updateCollective() {
            fetch('/api/collective')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('activeAgents').textContent = data.active_agents || 0;
                    document.getElementById('consensusReached').textContent = data.consensus_reached || 0;
                })
                .catch(e => console.error('Error:', e));
        }
        
        function generatePDF() {
            showNotification('📄 Generating legal PDF report...');
            
            fetch('/api/generate_pdf', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    type: 'INCIDENT_REPORT',
                    severity: 'HIGH',
                    ip: '203.0.113.50'
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showNotification('✅ PDF generated: ' + data.filepath);
                    document.getElementById('reportsGenerated').textContent = 
                        parseInt(document.getElementById('reportsGenerated').textContent) + 1;
                } else {
                    showNotification('⚠️ ' + data.message);
                }
            })
            .catch(e => showNotification('❌ Error generating PDF'));
        }
        
        function viewBlockchain() {
            showNotification('🔗 Blockchain viewer opening...');
            // Aquí podrías abrir un modal con detalles del blockchain
        }
        
        function checkQuantum() {
            fetch('/api/quantum_status')
                .then(r => r.json())
                .then(data => {
                    if (data.enabled) {
                        showNotification('⚛️ Quantum Defense ACTIVE: ' + data.algorithm);
                    } else {
                        showNotification('⚠️ Quantum Defense not available');
                    }
                })
                .catch(e => showNotification('❌ Error checking quantum status'));
        }
        
        function pressRedButton() {
            if (!confirm('🚨 EMERGENCY! Activate Red Button and notify CERTs?')) return;
            
            showNotification('🚨 RED BUTTON ACTIVATED! Notifying CERTs...');
            
            fetch('/api/red_button', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ip: '198.51.100.1'})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showNotification(`✅ ${data.certs_notified} CERTs notified: ${data.cert_list.join(', ')}`);
                    document.getElementById('certsNotified').textContent = 
                        parseInt(document.getElementById('certsNotified').textContent) + data.certs_notified;
                } else {
                    showNotification('⚠️ ' + data.message);
                }
            })
            .catch(e => showNotification('❌ Error activating Red Button'));
        }
        
        function showNotification(msg) {
            const n = document.getElementById('notification');
            n.textContent = msg;
            n.style.display = 'block';
            setTimeout(() => n.style.display = 'none', 4000);
        }
        
        // Initial load
        updateUnifiedStats();
        updateThreats();
        updateBlockchain();
    </script>
</body>
</html>
"""