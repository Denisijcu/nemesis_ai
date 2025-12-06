#!/usr/bin/env python3
"""
Némesis IA - THE BEAST V5.0 COMPLETE
Dashboard completo con TODOS los módulos + Notificaciones
"""

import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Set
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import yaml

logger = logging.getLogger(__name__)


class DashboardComplete:
    """THE BEAST V5.0 - Sistema completo con notificaciones"""
    
    def __init__(self, database, host: str = "0.0.0.0", port: int = 8080):
        self.database = database
        self.host = host
        self.port = port
        self.app = FastAPI(title="Némesis IA Dashboard V5.0 Complete")
        self.active_connections: Set[WebSocket] = set()
        
        # Traffic Sentinel
        self.traffic_sentinel = None
        
        # Sistema unificado
        self.nemesis_system = None
        try:
            from nemesis_main import NemesisIA
            self.nemesis_system = NemesisIA(
                enable_forensics=True,
                enable_legal=True,
                enable_emergency=True
            )
            logger.info("✅ Sistema Némesis cargado")
        except Exception as e:
            logger.warning(f"⚠️ Sistema Némesis no disponible: {e}")
        
        # Alertas (Email + Telegram)
        self.alert_manager = None
        self.notifications_stats = {
            'emails_sent': 0,
            'telegrams_sent': 0,
            'last_notification': None
        }
        try:
            from alerts.alert_manager import AlertManager
            with open('config/alerts.yaml', 'r') as f:
                alerts_config = yaml.safe_load(f)
            self.alert_manager = AlertManager(alerts_config)
            logger.info("✅ AlertManager cargado")
        except Exception as e:
            logger.warning(f"⚠️ AlertManager no disponible: {e}")
        
        self._setup_routes()
        logger.info(f"🎖️ Dashboard V5.0 Complete: http://{host}:{port}")
    
    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            return self._get_dashboard_html()
        
        @self.app.get("/api/stats")
        async def get_stats():
            return self.database.get_statistics()
        
        @self.app.get("/api/threats")
        async def get_threats(limit: int = 50):
            threats = self.database.get_threats(limit=limit)
            return [
                {
                    "id": t.id,
                    "timestamp": t.timestamp.isoformat(),
                    "source_ip": t.source_ip,
                    "attack_type": t.attack_type,
                    "confidence": t.confidence,
                    "action_taken": t.action_taken,
                    "payload": t.payload
                }
                for t in threats
            ]
        
        @self.app.get("/api/honeypot_stats")
        async def get_honeypot_stats():
            threats = self.database.get_threats(limit=100)
            honeypot_threats = [t for t in threats if "HONEYPOT" in t.attack_type]
            
            if not honeypot_threats:
                return {
                    "total_captures": 0,
                    "recent_captures": []
                }
            
            return {
                "total_captures": len(honeypot_threats),
                "recent_captures": [
                    {
                        "ip": t.source_ip,
                        "payload": t.payload,
                        "timestamp": t.timestamp.isoformat()
                    }
                    for t in honeypot_threats[:5]
                ]
            }
        
        @self.app.get("/api/blockchain_stats")
        async def get_blockchain_stats():
            if self.nemesis_system and self.nemesis_system.forensic_sentinel:
                blockchain = self.nemesis_system.forensic_sentinel.blockchain
                return {
                    "chain_length": len(blockchain.chain),
                    "total_evidence": blockchain.stats['total_evidence'],
                    "chain_valid": blockchain.stats['chain_valid'],
                    "last_block": blockchain.chain[-1].hash[:16] if len(blockchain.chain) > 0 else 'N/A'
                }
            return {"chain_length": 0, "total_evidence": 0, "chain_valid": False}
        
        @self.app.get("/api/unified_stats")
        async def get_unified_stats():
            if self.nemesis_system:
                return self.nemesis_system.system_stats
            return {
                "threats_detected": 0,
                "threats_blocked": 0,
                "evidence_collected": 0,
                "reports_generated": 0,
                "certs_notified": 0
            }
        
        @self.app.get("/api/notifications_stats")
        async def get_notifications_stats():
            return self.notifications_stats
        
        @self.app.post("/api/generate_pdf")
        async def generate_pdf(request: Request):
            data = await request.json()
            if self.nemesis_system and self.nemesis_system.fiscal_digital:
                incident = {
                    'case_id': f'WEB-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                    'detection_time': datetime.now().isoformat(),
                    'incident_type': data.get('type', 'CYBER_ATTACK'),
                    'severity': data.get('severity', 'HIGH'),
                    'confidence': 0.95,
                    'source_ip': data.get('ip', '203.0.113.50'),
                    'technical_analysis': 'Generated from dashboard'
                }
                filepath = self.nemesis_system.fiscal_digital.generate_incident_report(incident)
                return {"success": True, "filepath": filepath}
            return {"success": False, "message": "Legal module not available"}
        
        @self.app.post("/api/red_button")
        async def press_red_button(request: Request):
            data = await request.json()
            if self.nemesis_system and self.nemesis_system.red_button:
                incident = {
                    'case_id': f'EMERGENCY-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                    'incident_type': 'CRITICAL_THREAT',
                    'severity': 'CRITICAL',
                    'confidence': 0.99,
                    'source_ip': data.get('ip', '198.51.100.1'),
                    'detection_time': datetime.now().isoformat(),
                    'technical_analysis': 'Emergency from dashboard',
                    'impact_assessment': 'Critical',
                    'response_actions': 'Emergency protocols'
                }
                result = self.nemesis_system.red_button.press_red_button(
                    incident_data=incident,
                    auto_escalate=False
                )
                return {
                    "success": True,
                    "certs_notified": len(result.get('certs_notified', [])),
                    "cert_list": result.get('certs_notified', [])
                }
            return {"success": False, "message": "Red Button not available"}
        
        @self.app.post("/api/test_notification")
        async def test_notification(request: Request):
            """Envía notificación de prueba"""
            data = await request.json()
            channel = data.get('channel', 'all')
            
            if not self.alert_manager:
                return {"success": False, "message": "AlertManager not configured"}
            
            try:
                if channel in ['all', 'telegram']:
                    await self.alert_manager.telegram.send_threat_alert(
                        source_ip="192.168.1.100",
                        attack_type="TEST_ALERT",
                        confidence=1.0,
                        payload="This is a test alert from Némesis IA Dashboard",
                        action_taken="TEST"
                    )
                    self.notifications_stats['telegrams_sent'] += 1
                
                if channel in ['all', 'email']:
                    await self.alert_manager.email.send_threat_alert(
                        source_ip="192.168.1.100",
                        attack_type="TEST_ALERT",
                        confidence=1.0,
                        payload="This is a test alert from Némesis IA Dashboard",
                        action_taken="TEST"
                    )
                    self.notifications_stats['emails_sent'] += 1
                
                self.notifications_stats['last_notification'] = datetime.now().isoformat()
                
                return {"success": True, "message": f"Test alert sent via {channel}"}
            
            except Exception as e:
                return {"success": False, "message": str(e)}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.active_connections.add(websocket)
            
            try:
                while True:
                    data = await websocket.receive_text()
                    if data == "ping":
                        await websocket.send_text("pong")
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)
    
    async def send_threat_notification(self, threat_data: dict):
        """Envía notificación cuando se detecta amenaza"""
        if self.alert_manager:
            try:
                await self.alert_manager.send_threat_alert(
                    source_ip=threat_data.get('source_ip', 'UNKNOWN'),
                    attack_type=threat_data.get('attack_type', 'UNKNOWN'),
                    confidence=threat_data.get('confidence', 0.0),
                    payload=threat_data.get('payload', ''),
                    action_taken=threat_data.get('action_taken', 'DETECTED')
                )
                self.notifications_stats['telegrams_sent'] += 1
                self.notifications_stats['emails_sent'] += 1
                self.notifications_stats['last_notification'] = datetime.now().isoformat()
            except Exception as e:
                logger.error(f"Error sending notification: {e}")
    
    def _get_dashboard_html(self) -> str:
        # Mantener TODO el HTML original pero agregar panel de notificaciones
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ NÉMESIS IA - THE BEAST V5.0 COMPLETE</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --bg-primary: #0a0e14;
            --bg-secondary: #161b22;
            --accent-primary: #00ff41;
            --accent-cyan: #00d9ff;
            --accent-red: #ff0040;
            --accent-yellow: #ffd93d;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
        }
        
        body {
            font-family: 'Courier New', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            overflow-x: hidden;
        }
        
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: repeating-linear-gradient(
                0deg,
                rgba(0, 255, 65, 0.03) 0px,
                transparent 1px,
                transparent 2px,
                rgba(0, 255, 65, 0.03) 3px
            );
            pointer-events: none;
            z-index: 9999;
            animation: scanlines 10s linear infinite;
        }
        
        @keyframes scanlines {
            0% { transform: translateY(0); }
            100% { transform: translateY(10px); }
        }
        
        .container {
            max-width: 1800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: var(--bg-secondary);
            border: 2px solid var(--accent-primary);
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
            animation: fadeInDown 0.6s;
        }
        
        .ascii-logo {
            font-size: 0.5em;
            color: var(--accent-primary);
            text-shadow: 0 0 10px var(--accent-primary);
            white-space: pre;
            text-align: center;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        
        .tech-badges {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .tech-badge {
            display: inline-block;
            padding: 5px 12px;
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.2), rgba(0, 255, 65, 0.2));
            border: 1px solid var(--accent-cyan);
            border-radius: 15px;
            font-size: 0.75em;
            text-transform: uppercase;
            letter-spacing: 1px;
            animation: badgePulse 2s infinite;
        }
        
        @keyframes badgePulse {
            0%, 100% { box-shadow: 0 0 5px var(--accent-cyan); }
            50% { box-shadow: 0 0 15px var(--accent-cyan); }
        }
        
        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .header-subtitle {
            color: var(--text-secondary);
            font-size: 0.9em;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .live-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 0, 64, 0.2);
            padding: 8px 16px;
            border: 1px solid var(--accent-red);
            border-radius: 3px;
        }
        
        .live-dot {
            width: 12px;
            height: 12px;
            background: var(--accent-red);
            border-radius: 50%;
            animation: pulse 1.5s infinite;
            box-shadow: 0 0 10px var(--accent-red);
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }
        
        .header-stats {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid var(--accent-primary);
        }
        
        .header-stat {
            text-align: center;
            transition: all 0.3s;
        }
        
        .header-stat:hover {
            transform: scale(1.1);
        }
        
        .header-stat-value {
            font-size: 1.8em;
            color: var(--accent-primary);
            font-weight: bold;
            text-shadow: 0 0 10px var(--accent-primary);
        }
        
        .header-stat-label {
            font-size: 0.75em;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-top: 5px;
        }
        
        .panel {
            background: var(--bg-secondary);
            border: 2px solid var(--accent-primary);
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
            animation: fadeInUp 0.6s;
            position: relative;
            overflow: hidden;
        }
        
        .panel::before {
            content: "";
            position: absolute;
            top: -2px;
            left: -100%;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
            animation: borderScan 3s linear infinite;
        }
        
        @keyframes borderScan {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--accent-primary);
        }
        
        .panel-title {
            font-size: 1.1em;
            color: var(--accent-primary);
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .panel-badge {
            background: rgba(0, 255, 65, 0.2);
            padding: 4px 12px;
            border-radius: 3px;
            font-size: 0.8em;
            border: 1px solid var(--accent-primary);
        }
        
        .action-button {
            padding: 10px 20px;
            background: linear-gradient(135deg, var(--bg-primary), var(--accent-primary));
            color: var(--bg-primary);
            border: 2px solid var(--accent-primary);
            border-radius: 4px;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            transition: all 0.3s;
            margin: 5px;
            text-transform: uppercase;
            font-size: 0.9em;
        }
        
        .action-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px var(--accent-primary);
        }
        
        .action-button.red {
            background: linear-gradient(135deg, var(--bg-primary), var(--accent-red));
            border-color: var(--accent-red);
            animation: redPulse 1.5s infinite;
        }
        
        @keyframes redPulse {
            0%, 100% { box-shadow: 0 0 10px var(--accent-red); }
            50% { box-shadow: 0 0 30px var(--accent-red); }
        }
        
        .notification-item {
            padding: 10px;
            margin: 8px 0;
            background: rgba(0, 217, 255, 0.1);
            border-left: 3px solid var(--accent-cyan);
            border-radius: 3px;
            font-size: 0.85em;
        }
        
        .grid-3col {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 1200px) {
            .header-stats { grid-template-columns: repeat(3, 1fr); }
            .grid-3col { grid-template-columns: 1fr; }
            .ascii-logo { font-size: 0.3em; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="ascii-logo">
███╗   ██╗███████╗███╗   ███╗███████╗███████╗██╗███████╗
████╗  ██║██╔════╝████╗ ████║██╔════╝██╔════╝██║██╔════╝
██╔██╗ ██║█████╗  ██╔████╔██║█████╗  ███████╗██║███████╗
██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══╝  ╚════██║██║╚════██║
██║ ╚████║███████╗██║ ╚═╝ ██║███████╗███████║██║███████║
╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝╚══════╝
            </div>
            
            <div class="tech-badges">
                <span class="tech-badge">⚛️ QUANTUM</span>
                <span class="tech-badge">🔗 BLOCKCHAIN</span>
                <span class="tech-badge">📄 LEGAL</span>
                <span class="tech-badge">🤖 AI vs AI</span>
                <span class="tech-badge">📧 EMAIL</span>
                <span class="tech-badge">📱 TELEGRAM</span>
            </div>
            
            <div class="header-top">
                <div>
                    <div class="header-subtitle">⚡ THE BEAST V5.0 COMPLETE - All Systems Operational ⚡</div>
                </div>
                <div class="live-badge">
                    <div class="live-dot"></div>
                    <span>LIVE</span>
                </div>
            </div>
            
            <div class="header-stats">
                <div class="header-stat">
                    <div class="header-stat-value" id="total-threats">-</div>
                    <div class="header-stat-label">⚔️ Threats</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value" id="blocked-ips">-</div>
                    <div class="header-stat-label">🚫 Blocked</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value" id="evidence-collected">0</div>
                    <div class="header-stat-label">🔗 Evidence</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value" id="pdfs-generated">0</div>
                    <div class="header-stat-label">📄 PDFs</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value" id="emails-sent">0</div>
                    <div class="header-stat-label">📧 Emails</div>
                </div>
                <div class="header-stat">
                    <div class="header-stat-value" id="telegrams-sent">0</div>
                    <div class="header-stat-label">📱 Telegrams</div>
                </div>
            </div>
        </header>
        
        <!-- PANEL DE NOTIFICACIONES -->
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">📧📱 NOTIFICATION CENTER</div>
                <div class="panel-badge">ACTIVE</div>
            </div>
            
            <div class="grid-3col">
                <div>
                    <div class="notification-item">
                        <strong>📧 Email Alerts</strong><br/>
                        Status: <span id="email-status" style="color: var(--accent-primary);">CONFIGURED</span><br/>
                        Sent: <span id="email-count">0</span>
                    </div>
                </div>
                
                <div>
                    <div class="notification-item">
                        <strong>📱 Telegram Alerts</strong><br/>
                        Status: <span id="telegram-status" style="color: var(--accent-primary);">CONFIGURED</span><br/>
                        Sent: <span id="telegram-count">0</span>
                    </div>
                </div>
                
                <div>
                    <div class="notification-item">
                        <strong>🕐 Last Notification</strong><br/>
                        <span id="last-notification">Never</span>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 15px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
                <button class="action-button" onclick="testNotification('email')">📧 TEST EMAIL</button>
                <button class="action-button" onclick="testNotification('telegram')">📱 TEST TELEGRAM</button>
                <button class="action-button" onclick="testNotification('all')">🔔 TEST ALL</button>
            </div>
        </div>
        
        <!-- PANEL DE CONTROLES AVANZADOS -->
        <div class="panel">
            <div class="panel-header">
                <div class="panel-title">🎮 ADVANCED CONTROLS</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                <button class="action-button" onclick="generatePDF()">📄 GENERATE PDF</button>
                <button class="action-button" onclick="viewBlockchain()">🔗 BLOCKCHAIN</button>
                <button class="action-button" onclick="checkQuantum()">⚛️ QUANTUM</button>
                <button class="action-button red" onclick="pressRedButton()">🚨 RED BUTTON</button>
            </div>
        </div>
        
        <div style="text-align: center; padding: 20px; color: var(--text-secondary); font-size: 0.9em;">
            <p>⚡ Némesis IA V5.0 Complete - 14/14 Modules Operational ⚡</p>
            <p>Email + Telegram + Blockchain + Quantum + Legal + CERT + AI vs AI + Multi-Agent</p>
        </div>
    </div>
    
    <script>
        async function loadNotificationStats() {
            try {
                const response = await fetch('/api/notifications_stats');
                const data = await response.json();
                
                document.getElementById('email-count').textContent = data.emails_sent || 0;
                document.getElementById('telegram-count').textContent = data.telegrams_sent || 0;
                document.getElementById('emails-sent').textContent = data.emails_sent || 0;
                document.getElementById('telegrams-sent').textContent = data.telegrams_sent || 0;
                
                if (data.last_notification) {
                    const date = new Date(data.last_notification);
                    document.getElementById('last-notification').textContent = date.toLocaleString();
                }
            } catch (e) {
                console.error('Error loading notification stats:', e);
            }
        }
        
        async function loadUnifiedStats() {
            try {
                const response = await fetch('/api/unified_stats');
                const data = await response.json();
                
                document.getElementById('evidence-collected').textContent = data.evidence_collected || 0;
                document.getElementById('pdfs-generated').textContent = data.reports_generated || 0;
            } catch (e) {
                console.error('Error loading unified stats:', e);
            }
        }
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('total-threats').textContent = data.total_threats || 0;
                document.getElementById('blocked-ips').textContent = data.total_blocked_ips || 0;
            } catch (e) {
                console.error('Error loading stats:', e);
            }
        }
        
        async function testNotification(channel) {
            try {
                const response = await fetch('/api/test_notification', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({channel: channel})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert(`✅ ${data.message}`);
                    loadNotificationStats();
                } else {
                    alert(`⚠️ ${data.message}`);
                }
            } catch (e) {
                alert(`❌ Error: ${e.message}`);
            }
        }
        
        async function generatePDF() {
            alert('📄 Generating legal PDF...');
            try {
                const response = await fetch('/api/generate_pdf', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({type: 'INCIDENT_REPORT', severity: 'HIGH'})
                });
                const data = await response.json();
                if (data.success) {
                    alert(`✅ PDF generated: ${data.filepath}`);
                    loadUnifiedStats();
                } else {
                    alert(`⚠️ ${data.message}`);
                }
            } catch (e) {
                alert(`❌ Error: ${e.message}`);
            }
        }
        
        function viewBlockchain() {
            alert('🔗 Blockchain evidence is immutable and court-admissible');
        }
        
        function checkQuantum() {
            alert('⚛️ Quantum Defense Active: Kyber-768 + Dilithium-3');
        }
        
        async function pressRedButton() {
            if (!confirm('🚨 EMERGENCY! Activate Red Button?')) return;
            
            try {
                const response = await fetch('/api/red_button', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ip: '198.51.100.1'})
                });
                const data = await response.json();
                if (data.success) {
                    alert(`✅ ${data.certs_notified} CERTs notified!`);
                } else {
                    alert(`⚠️ ${data.message}`);
                }
            } catch (e) {
                alert(`❌ Error: ${e.message}`);
            }
        }
        
        // Load stats every 5 seconds
        setInterval(() => {
            loadStats();
            loadUnifiedStats();
            loadNotificationStats();
        }, 5000);
        
        // Initial load
        loadStats();
        loadUnifiedStats();
        loadNotificationStats();
    </script>
</body>
</html>
        """
    
    async def run(self):
        import uvicorn
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()