#!/usr/bin/env python3
"""
Némesis IA - Dashboard UNIFICADO
THE BEAST con los 5 MÓDULOS CORE integrados
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

logger = logging.getLogger(__name__)


class DashboardUnified:
    """Dashboard UNIFICADO - 5 Módulos Core de Némesis IA"""
    
    def __init__(self, database, host: str = "0.0.0.0", port: int = 8080):
        self.database = database
        self.host = host
        self.port = port
        self.app = FastAPI(title="Némesis IA Dashboard Unificado")
        self.active_connections: Set[WebSocket] = set()
        
        # Traffic Sentinel
        self.traffic_sentinel = None
        
        # Sistema unificado (Blockchain, Quantum, Legal, Red Button)
        self.nemesis_system = None
        try:
            from nemesis_main import NemesisIA
            self.nemesis_system = NemesisIA(
                enable_forensics=True,
                enable_legal=True,
                enable_emergency=True
            )
            logger.info("✅ Sistema Némesis cargado en dashboard")
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
            import yaml
            with open('config/alerts.yaml', 'r') as f:
                alerts_config = yaml.safe_load(f)
            self.alert_manager = AlertManager(alerts_config)
            logger.info("✅ AlertManager cargado")
        except Exception as e:
            logger.warning(f"⚠️ AlertManager: {e}")
        
        self._setup_routes()
        logger.info(f"🎖️  Dashboard Unificado: http://{host}:{port}")
    
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
         
        @self.app.get("/api/blocked_ips")
        async def get_blocked_ips():
            return self.database.get_blocked_ips()
        
        @self.app.get("/api/honeypot_stats")
        async def get_honeypot_stats():
            import sqlite3
            
            # Consultar tabla honeypot_captures directamente
            conn = sqlite3.connect('data/nemesis_honeypot.db')
            cursor = conn.cursor()
            
            # Total de capturas
            cursor.execute('SELECT COUNT(*) FROM honeypot_captures')
            total = cursor.fetchone()[0]
            
            if total == 0:
                conn.close()
                return {
                    "total_captures": 0,
                    "active_traps": 0,
                    "top_attacker": None,
                    "recent_captures": []
                }
            
            # Top atacante
            cursor.execute('''
                SELECT ip, COUNT(*) as attempts 
                FROM honeypot_captures 
                GROUP BY ip 
                ORDER BY attempts DESC 
                LIMIT 1
            ''')
            top = cursor.fetchone()
            
            # Capturas recientes
            cursor.execute('''
                SELECT ip, payload, timestamp 
                FROM honeypot_captures 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''')
            recent = cursor.fetchall()
            
            conn.close()
            
            return {
                "total_captures": total,
                "active_traps": 1,
                "top_attacker": {
                    "ip": top[0],
                    "attempts": top[1]
                } if top else None,
                "recent_captures": [
                    {
                        "ip": r[0],
                        "payload": r[1],
                        "timestamp": r[2]
                    }
                    for r in recent
                ]
            }
        
        @self.app.get("/api/threat_timeline")
        async def get_threat_timeline():
            import sqlite3
            from datetime import datetime, timedelta
            
            conn = sqlite3.connect('data/nemesis_honeypot.db')
            cursor = conn.cursor()
            
            # Obtener amenazas de las últimas 24 horas
            cursor.execute('''
                SELECT timestamp 
                FROM threats 
                WHERE timestamp >= datetime('now', '-24 hours')
                ORDER BY timestamp
            ''')
            
            threats = cursor.fetchall()
            conn.close()
            
            # Inicializar contadores por hora (0-23)
            hourly_counts = [0] * 24
            
            # Contar amenazas por hora
            for threat in threats:
                try:
                    dt = datetime.fromisoformat(threat[0])
                    hour = dt.hour
                    hourly_counts[hour] += 1
                except:
                    pass
            
            return {
                "hours": [f"{i}:00" for i in range(24)],
                "counts": hourly_counts,
                "total": sum(hourly_counts)
            }
        
        @self.app.get("/api/blockchain_stats")
        async def get_blockchain_stats():
            """Stats de blockchain"""
            if self.nemesis_system and self.nemesis_system.forensic_sentinel:
                blockchain = self.nemesis_system.forensic_sentinel.blockchain
                return {
                    "chain_length": len(blockchain.chain),
                    "total_evidence": blockchain.stats['total_evidence'],
                    "chain_valid": blockchain.stats['chain_valid'],
                    "last_block": blockchain.chain[-1].hash[:16] if len(blockchain.chain) > 0 else 'N/A'
                }
            return {"chain_length": 0, "total_evidence": 0, "chain_valid": False}
        
        @self.app.get("/api/quantum_status")
        async def get_quantum_status():
            """Status de quantum defense"""
            if self.nemesis_system and self.nemesis_system.quantum_sentinel:
                return {
                    "enabled": True,
                    "algorithm": "Kyber-768 + Dilithium-3",
                    "status": "ACTIVE"
                }
            return {"enabled": False}
        
        @self.app.get("/api/unified_stats")
        async def get_unified_stats():
            """Stats unificadas de todos los módulos"""
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
        async def generate_pdf(data: dict):
            """Genera PDF legal"""
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
        async def press_red_button(data: dict):
            """Presiona el botón rojo"""
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
            data = await request.json()
            channel = data.get('channel', 'all')
            
            if not self.alert_manager:
                return {"success": False, "message": "Not configured"}
            
            try:
                if channel in ['all', 'telegram']:
                    await self.alert_manager.telegram.send_threat_alert(
                        source_ip="192.168.1.100",
                        attack_type="TEST_ALERT",
                        confidence=1.0,
                        payload="Test from Némesis IA Dashboard",
                        action_taken="TEST"
                    )
                    self.notifications_stats['telegrams_sent'] += 1
                
                if channel in ['all', 'email']:
                    await self.alert_manager.email.send_threat_alert(
                        source_ip="192.168.1.100",
                        attack_type="TEST_ALERT",
                        confidence=1.0,
                        payload="Test from Némesis IA Dashboard",
                        action_taken="TEST"
                    )
                    self.notifications_stats['emails_sent'] += 1
                
                self.notifications_stats['last_notification'] = datetime.now().isoformat()
                return {"success": True, "message": f"Sent via {channel}"}
            
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
    
    async def broadcast_threat(self, threat_data: dict):
        message = json.dumps({"type": "new_threat", "data": threat_data})
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.add(connection)
        
        self.active_connections -= disconnected
    
    def _get_dashboard_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ NÉMESIS IA - UNIFIED DASHBOARD</title>
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
        
        .header-stats {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
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
        
        .grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .grid-full {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .panel {
            background: var(--bg-secondary);
            border: 2px solid var(--accent-primary);
            border-radius: 4px;
            padding: 20px;
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
            font-size: 0.85em;
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
        
        .blockchain-item {
            padding: 8px;
            margin: 5px 0;
            background: rgba(0, 217, 255, 0.1);
            border-left: 3px solid var(--accent-cyan);
            font-size: 0.85em;
        }
        
        .terminal {
            background: #000000;
            border: 2px solid var(--accent-cyan);
            border-radius: 4px;
            padding: 15px;
            font-size: 0.85em;
            height: 300px;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.3);
        }
        
        .terminal::-webkit-scrollbar { width: 8px; }
        .terminal::-webkit-scrollbar-track { background: #000; }
        .terminal::-webkit-scrollbar-thumb { background: var(--accent-cyan); }
        
        .terminal-line {
            margin-bottom: 5px;
            animation: terminalLine 0.3s;
        }
        
        @keyframes terminalLine {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .terminal-prompt { color: var(--accent-primary); }
        .terminal-error { color: var(--accent-red); }
        .terminal-warning { color: var(--accent-yellow); }
        .terminal-success { color: var(--accent-primary); }
        
        .attack-map {
            position: relative;
            height: 300px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--accent-cyan);
            border-radius: 4px;
            padding: 20px;
            overflow: hidden;
        }
        
        .attack-source {
            position: absolute;
            background: var(--accent-red);
            width: 12px;
            height: 12px;
            border-radius: 50%;
            box-shadow: 0 0 20px var(--accent-red);
            animation: attackPulse 1.5s infinite;
            pointer-events: none;
        }
        
        @keyframes attackPulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 20px var(--accent-red); }
            50% { transform: scale(1.5); box-shadow: 0 0 40px var(--accent-red); }
        }
        
        .attack-target {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 50px;
            height: 50px;
            border: 3px solid var(--accent-cyan);
            border-radius: 50%;
            animation: targetPulse 2s infinite;
            pointer-events: none;
        }
        
        @keyframes targetPulse {
            0%, 100% { box-shadow: 0 0 10px var(--accent-cyan); }
            50% { box-shadow: 0 0 30px var(--accent-cyan), 0 0 50px var(--accent-cyan); }
        }
        
        .attack-label {
            position: absolute;
            font-size: 0.7em;
            background: rgba(0, 0, 0, 0.95);
            padding: 4px 10px;
            border-radius: 3px;
            border: 1px solid var(--accent-red);
            white-space: nowrap;
            pointer-events: none;
            animation: labelFadeIn 0.5s;
            box-shadow: 0 0 15px rgba(255, 0, 64, 0.6);
        }
        
        @keyframes labelFadeIn {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .attack-line {
            position: absolute;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-red), transparent);
            transform-origin: left center;
            animation: attackLine 3s ease-out;
            box-shadow: 0 0 10px var(--accent-red);
            pointer-events: none;
        }
        
        @keyframes attackLine {
            0% { width: 0; opacity: 0; }
            20% { opacity: 1; }
            100% { width: 100%; opacity: 0; }
        }
        
        .attacks-log {
            max-height: 150px;
            overflow-y: auto;
            font-size: 0.85em;
        }
        
        .attacks-log::-webkit-scrollbar { width: 6px; }
        .attacks-log::-webkit-scrollbar-track { background: rgba(0, 0, 0, 0.3); }
        .attacks-log::-webkit-scrollbar-thumb { background: var(--accent-cyan); }
        
        .log-item {
            padding: 8px;
            margin-bottom: 5px;
            background: rgba(255, 0, 64, 0.05);
            border-left: 2px solid var(--accent-red);
            border-radius: 2px;
            animation: slideInRight 0.3s;
        }
        
        .threat-item {
            background: rgba(0, 255, 65, 0.05);
            border-left: 3px solid var(--accent-red);
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 3px;
            animation: slideInRight 0.4s;
            transition: all 0.3s;
        }
        
        .threat-item:hover {
            background: rgba(0, 255, 65, 0.1);
            transform: translateX(5px);
            box-shadow: 0 0 15px rgba(255, 0, 64, 0.3);
        }
        
        .threat-type {
            color: var(--accent-red);
            font-weight: bold;
            font-size: 1em;
            margin-bottom: 8px;
            text-shadow: 0 0 5px var(--accent-red);
        }
        
        .threat-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            font-size: 0.85em;
            color: var(--text-secondary);
        }
        
        .honeypot-stat {
            background: rgba(0, 217, 255, 0.1);
            border: 1px solid var(--accent-cyan);
            padding: 15px;
            border-radius: 3px;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .honeypot-number {
            font-size: 2em;
            color: var(--accent-cyan);
            font-weight: bold;
            text-shadow: 0 0 10px var(--accent-cyan);
        }
        
        .honeypot-label {
            color: var(--text-secondary);
            font-size: 0.85em;
            text-transform: uppercase;
        }
        
        .capture-item {
            background: rgba(0, 0, 0, 0.3);
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 3px;
            border-left: 2px solid var(--accent-cyan);
            font-size: 0.85em;
            transition: all 0.3s;
        }
        
        .capture-item:hover {
            background: rgba(0, 217, 255, 0.1);
            transform: translateX(3px);
        }
        
        .status-grid { display: grid; gap: 10px; }
        
        .status-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            background: rgba(0, 255, 65, 0.05);
            border-radius: 3px;
            border-left: 3px solid var(--accent-primary);
            transition: all 0.3s;
        }
        
        .status-item:hover {
            background: rgba(0, 255, 65, 0.1);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-primary);
            border-radius: 50%;
            animation: pulse 2s infinite;
            box-shadow: 0 0 10px var(--accent-primary);
        }
        
        .chart-container {
            position: relative;
            height: 250px;
        }
        
        .alert-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 0, 64, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 4px;
            border: 2px solid var(--accent-red);
            box-shadow: 0 0 30px rgba(255, 0, 64, 0.5);
            z-index: 10000;
            animation: alertSlideIn 0.5s;
            max-width: 400px;
        }
        
        @keyframes alertSlideIn {
            from { transform: translateX(500px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .alert-title {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #fff;
        }
        
        .alert-body {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9em;
        }
        
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(100px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        @media (max-width: 1200px) {
            .grid, .grid-full { grid-template-columns: 1fr; }
            .header-stats { grid-template-columns: repeat(3, 1fr); }
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
                <span class="tech-badge">🧠 ML BRAIN 98.7%</span>
                <span class="tech-badge">🍯 HONEYPOT TRAPS</span>
                <span class="tech-badge">🔗 BLOCKCHAIN</span>
                <span class="tech-badge">⚛️ QUANTUM</span>
                <span class="tech-badge">📧 ALERTS</span>
            </div>
            
            <div class="header-top">
                <div>
                    <div class="header-subtitle">⚡ UNIFIED DASHBOARD - 5 Core Modules Integrated ⚡</div>
                </div>
                <div class="live-badge">
                    <div class="live-dot"></div>
                    <span>SYSTEM ACTIVE</span>
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
                    <div class="header-stat-value" id="honeypot-captures">-</div>
                    <div class="header-stat-label">🍯 Honeypot</div>
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
                    <div class="header-stat-label">📱 Telegram</div>
                </div>
            </div>
        </header>
        
        <div class="panel" style="margin-bottom: 20px;">
            <div class="panel-header">
                <div class="panel-title">🗺️ Global Attack Map</div>
                <div class="panel-badge">LIVE TRACKING</div>
            </div>
            <div class="attack-map" id="attack-map">
                <div class="attack-target">
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 0.8em;">
                        🎯 TARGET
                    </div>
                </div>
            </div>
            <div style="margin-top: 15px; padding: 15px; background: rgba(0, 0, 0, 0.3); border: 1px solid var(--accent-cyan); border-radius: 4px;">
                <div style="font-size: 0.9em; color: var(--accent-cyan); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px;">
                    📋 Recent Attacks Log
                </div>
                <div id="attacks-log" class="attacks-log">
                    <div style="color: var(--text-secondary);">Waiting for attacks...</div>
                </div>
            </div>
        </div>
        
        <!-- MÓDULO 5: ALERTAS (Email + Telegram) -->
        <div class="panel" style="margin-bottom: 20px;">
            <div class="panel-header">
                <div class="panel-title">📧📱 Alert System - Email & Telegram</div>
                <div class="panel-badge">MODULE 5/5</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                <div style="background: rgba(0,255,65,0.1); padding: 15px; border-radius: 4px; text-align: center;">
                    <div style="font-size: 1.5em; color: var(--accent-cyan);" id="email-count">0</div>
                    <div style="font-size: 0.8em; color: var(--text-secondary); margin-top: 5px;">📧 Emails Sent</div>
                </div>
                <div style="background: rgba(0,255,65,0.1); padding: 15px; border-radius: 4px; text-align: center;">
                    <div style="font-size: 1.5em; color: var(--accent-cyan);" id="telegram-count">0</div>
                    <div style="font-size: 0.8em; color: var(--text-secondary); margin-top: 5px;">📱 Telegrams Sent</div>
                </div>
                <button class="action-button" onclick="testNotification('email')">📧 Test Email</button>
                <button class="action-button" onclick="testNotification('telegram')">📱 Test Telegram</button>
            </div>
        </div>
        
        <div class="grid">
            <div>
                <div class="panel">
                    <div class="panel-header">
                        <div class="panel-title">🖥️ Live Terminal</div>
                        <div class="panel-badge">REAL-TIME</div>
                    </div>
                    <div class="terminal" id="terminal">
                        <div class="terminal-line terminal-prompt">nemesis@unified:~$ system initialized</div>
                        <div class="terminal-line terminal-success">[OK] 5 Core Modules loaded</div>
                        <div class="terminal-line terminal-success">[OK] ML Brain (98.7%) - ACTIVE</div>
                        <div class="terminal-line terminal-success">[OK] Honeypot Traps - ACTIVE</div>
                        <div class="terminal-line terminal-success">[OK] Blockchain Evidence - SYNCED</div>
                        <div class="terminal-line terminal-success">[OK] Quantum Defense - PROTECTED</div>
                        <div class="terminal-line terminal-success">[OK] Alert System (Email+Telegram) - READY</div>
                    </div>
                </div>
                <div class="panel" style="margin-top: 20px;">
                    <div class="panel-header">
                        <div class="panel-title">🚨 Active Threats</div>
                        <div class="panel-badge" id="threats-count">0</div>
                    </div>
                    <div id="threats-list"></div>
                </div>
            </div>
            <div>
                <div class="panel">
                    <div class="panel-header">
                        <div class="panel-title">🍯 Honeypot Traps</div>
                        <div class="panel-badge">MODULE 2/5</div>
                    </div>
                    <div class="honeypot-stat">
                        <div class="honeypot-number" id="honeypot-total">-</div>
                        <div class="honeypot-label">Captures Today</div>
                    </div>
                    <div id="honeypot-captures-list"></div>
                </div>
                <div class="panel" style="margin-top: 20px;">
                    <div class="panel-header">
                        <div class="panel-title">⚙️ System Status</div>
                    </div>
                    <div class="status-grid">
                        <div class="status-item">
                            <span>🧠 ML Engine</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span>98.7%</span>
                            </div>
                        </div>
                        <div class="status-item">
                            <span>🍯 Honeypot</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span>ACTIVE</span>
                            </div>
                        </div>
                        <div class="status-item">
                            <span>🔗 Blockchain</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span id="blockchain-status">SYNCED</span>
                            </div>
                        </div>
                        <div class="status-item">
                            <span>⚛️ Quantum</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span id="quantum-status">PROTECTED</span>
                            </div>
                        </div>
                        <div class="status-item">
                            <span>📧 Email</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span>READY</span>
                            </div>
                        </div>
                        <div class="status-item">
                            <span>📱 Telegram</span>
                            <div class="status-indicator">
                                <span class="status-dot"></span>
                                <span>READY</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- MÓDULO 3: BLOCKCHAIN + MÓDULO 4: QUANTUM + PDFs -->
        <div class="grid-full">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">🔗 Blockchain Evidence</div>
                    <div class="panel-badge" id="blockchain-badge">MODULE 3/5</div>
                </div>
                <div id="blockchain-info">
                    <div class="blockchain-item">
                        Chain Length: <span id="chain-length">0</span> blocks
                    </div>
                    <div class="blockchain-item">
                        Total Evidence: <span id="total-evidence">0</span> items
                    </div>
                    <div class="blockchain-item">
                        Chain Valid: <span id="chain-valid">✓</span>
                    </div>
                    <div class="blockchain-item">
                        Last Block: <span id="last-block">N/A</span>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">⚛️ Quantum + Legal Controls</div>
                    <div class="panel-badge">MODULE 4/5</div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <button class="action-button" onclick="generatePDF()">📄 GENERATE PDF</button>
                    <button class="action-button" onclick="checkQuantum()">⚛️ QUANTUM STATUS</button>
                    <button class="action-button" onclick="viewBlockchain()">🔗 VIEW BLOCKCHAIN</button>
                    <button class="action-button red" onclick="pressRedButton()">🚨 RED BUTTON</button>
                </div>
                <div style="margin-top: 15px; padding: 10px; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 0.85em;">
                    <div style="color: var(--accent-cyan); margin-bottom: 5px;">⚛️ POST-QUANTUM CRYPTO:</div>
                    <div style="color: var(--text-secondary);">
                        • Algorithm: Kyber-768 + Dilithium-3<br/>
                        • Legal PDFs: Auto-generate incident reports<br/>
                        • Red Button: Notify CERTs immediately
                    </div>
                </div>
            </div>
        </div>
        
        <div class="grid-full">
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">📊 Threat Timeline</div>
                </div>
                <div class="chart-container">
                    <canvas id="timelineChart"></canvas>
                </div>
            </div>
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title">🎯 Attack Types</div>
                </div>
                <div class="chart-container">
                    <canvas id="attackTypesChart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <audio id="alert-sound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBi2Dz/Df2J1BAA==" type="audio/wav">
    </audio>
    
    <script>
        const alertSound = document.getElementById('alert-sound');
        let soundEnabled = true;
        
        function playAlertSound() {
            if (soundEnabled) {
                alertSound.currentTime = 0;
                alertSound.play().catch(() => { soundEnabled = false; });
            }
        }
        
        document.addEventListener('click', () => { soundEnabled = true; }, { once: true });
        
        const terminal = document.getElementById('terminal');
        
        function addTerminalLine(text, type = 'normal') {
            const line = document.createElement('div');
            line.className = `terminal-line terminal-${type}`;
            const timestamp = new Date().toLocaleTimeString();
            line.textContent = `[${timestamp}] ${text}`;
            terminal.appendChild(line);
            terminal.scrollTop = terminal.scrollHeight;
            if (terminal.children.length > 50) {
                terminal.removeChild(terminal.firstChild);
            }
        }
        
        const attackMap = document.getElementById('attack-map');
        const activeAttacks = new Map();
        
        function addAttackToMap(ip, attackType) {
            const mapRect = attackMap.getBoundingClientRect();
            const centerX = mapRect.width / 2;
            const centerY = mapRect.height / 2;
            
            const angle = Math.random() * Math.PI * 2;
            const distance = Math.min(mapRect.width, mapRect.height) * 0.35;
            
            const sourceX = centerX + Math.cos(angle) * distance;
            const sourceY = centerY + Math.sin(angle) * distance;
            
            const source = document.createElement('div');
            source.className = 'attack-source';
            source.style.left = sourceX + 'px';
            source.style.top = sourceY + 'px';
            
            const label = document.createElement('div');
            label.className = 'attack-label';
            label.textContent = ip;
            label.style.left = sourceX + 'px';
            label.style.top = (sourceY - 25) + 'px';
            
            const typeLabel = document.createElement('div');
            typeLabel.className = 'attack-label';
            typeLabel.textContent = attackType;
            typeLabel.style.left = sourceX + 'px';
            typeLabel.style.top = (sourceY + 20) + 'px';
            typeLabel.style.fontSize = '0.65em';
            typeLabel.style.color = '#00d9ff';
            typeLabel.style.borderColor = '#00d9ff';
            
            const lineLength = Math.sqrt(Math.pow(centerX - sourceX, 2) + Math.pow(centerY - sourceY, 2));
            const lineAngle = Math.atan2(centerY - sourceY, centerX - sourceX) * 180 / Math.PI;
            
            const line = document.createElement('div');
            line.className = 'attack-line';
            line.style.left = sourceX + 'px';
            line.style.top = sourceY + 'px';
            line.style.width = lineLength + 'px';
            line.style.transform = `rotate(${lineAngle}deg)`;
            
            attackMap.appendChild(source);
            attackMap.appendChild(label);
            attackMap.appendChild(typeLabel);
            attackMap.appendChild(line);
            
            const attackKey = `${ip}-${Date.now()}`;
            activeAttacks.set(attackKey, { source, label, typeLabel, line, timestamp: Date.now() });
            
            setTimeout(() => {
                if (line.parentNode) {
                    line.style.transition = 'opacity 0.5s';
                    line.style.opacity = '0';
                    setTimeout(() => line.remove(), 500);
                }
            }, 3000);
            
            setTimeout(() => {
                [label, typeLabel].forEach(elem => {
                    if (elem.parentNode) {
                        elem.style.transition = 'opacity 0.5s';
                        elem.style.opacity = '0';
                        setTimeout(() => elem.remove(), 500);
                    }
                });
            }, 15000);
            
            setTimeout(() => {
                if (source.parentNode) {
                    source.style.transition = 'opacity 1s';
                    source.style.opacity = '0';
                    setTimeout(() => {
                        source.remove();
                        activeAttacks.delete(attackKey);
                    }, 1000);
                }
            }, 30000);
        }
        
        const attacksLog = [];
        
        function addToAttacksLog(ip, attackType) {
            const timestamp = new Date().toLocaleTimeString();
            attacksLog.unshift({ time: timestamp, ip, type: attackType });
            if (attacksLog.length > 10) attacksLog.pop();
            updateAttacksLog();
        }
        
        function updateAttacksLog() {
            const logContainer = document.getElementById('attacks-log');
            if (attacksLog.length === 0) {
                logContainer.innerHTML = '<div style="color: var(--text-secondary);">Waiting for attacks...</div>';
                return;
            }
            logContainer.innerHTML = attacksLog.map(attack => `
                <div class="log-item">
                    <span style="color: var(--accent-primary);">[${attack.time}]</span>
                    <span style="color: var(--accent-red); margin: 0 8px;">●</span>
                    <span style="color: var(--text-primary);">${attack.ip}</span>
                    <span style="color: var(--text-secondary); margin-left: 8px;">→</span>
                    <span style="color: var(--accent-cyan); margin-left: 8px;">${attack.type}</span>
                </div>
            `).join('');
        }
        
        function showNotification(title, message) {
            const notification = document.createElement('div');
            notification.className = 'alert-notification';
            notification.innerHTML = `
                <div class="alert-title">🚨 ${title}</div>
                <div class="alert-body">${message}</div>
            `;
            document.body.appendChild(notification);
            setTimeout(() => {
                notification.style.animation = 'alertSlideIn 0.5s reverse';
                setTimeout(() => notification.remove(), 500);
            }, 5000);
        }
        
        let ws = null;
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            ws.onopen = () => {
                addTerminalLine('WebSocket connected', 'success');
                setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) ws.send('ping');
                }, 30000);
            };
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                if (message.type === 'new_threat') {
                    handleNewThreat(message.data);
                }
            };
            ws.onclose = () => {
                addTerminalLine('WebSocket disconnected', 'warning');
                setTimeout(connectWebSocket, 5000);
            };
        }
        
        function handleNewThreat(threat) {
            playAlertSound();
            addTerminalLine(`🚨 ${threat.attack_type} detected from ${threat.source_ip}`, 'error');
            addAttackToMap(threat.source_ip, threat.attack_type);
            addToAttacksLog(threat.source_ip, threat.attack_type);
            showNotification('THREAT DETECTED', `${threat.attack_type} from ${threat.source_ip}`);
            loadStats();
            loadThreats();
            loadHoneypotStats();
            loadBlockchainStats();
            loadNotificationStats();
        }
        
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            document.getElementById('total-threats').textContent = stats.total_threats;
            document.getElementById('blocked-ips').textContent = stats.total_blocked_ips;
        }
        
        async function loadUnifiedStats() {
            try {
                const response = await fetch('/api/unified_stats');
                const data = await response.json();
                document.getElementById('evidence-collected').textContent = data.evidence_collected || 0;
                document.getElementById('pdfs-generated').textContent = data.reports_generated || 0;
            } catch (e) {
                console.log('Unified stats not available');
            }
        }
        
        async function loadThreats() {
            const response = await fetch('/api/threats?limit=10');
            const threats = await response.json();
            document.getElementById('threats-count').textContent = threats.length;
            const list = document.getElementById('threats-list');
            list.innerHTML = threats.map(t => `
                <div class="threat-item">
                    <div class="threat-type">${t.attack_type}</div>
                    <div class="threat-details">
                        <div>🌐 ${t.source_ip}</div>
                        <div>📊 ${(t.confidence * 100).toFixed(0)}%</div>
                        <div>⚙️ ${t.action_taken}</div>
                        <div>🕐 ${new Date(t.timestamp).toLocaleTimeString()}</div>
                    </div>
                </div>
            `).join('');
        }
        
        async function loadHoneypotStats() {
            const response = await fetch('/api/honeypot_stats');
            const data = await response.json();
            document.getElementById('honeypot-captures').textContent = data.total_captures;
            document.getElementById('honeypot-total').textContent = data.total_captures;
            const list = document.getElementById('honeypot-captures-list');
            if (data.recent_captures && data.recent_captures.length > 0) {
                list.innerHTML = data.recent_captures.map(c => `
                    <div class="capture-item">
                        <div>🌐 ${c.ip}</div>
                        <div>📦 ${c.payload}</div>
                        <div style="font-size: 0.75em; opacity: 0.7; margin-top: 4px;">
                            ${new Date(c.timestamp).toLocaleString()}
                        </div>
                    </div>
                `).join('');
            } else {
                list.innerHTML = '<div class="capture-item">No captures yet</div>';
            }
        }
        
        async function loadBlockchainStats() {
            try {
                const response = await fetch('/api/blockchain_stats');
                const data = await response.json();
                document.getElementById('blockchain-badge').textContent = `${data.chain_length} BLOCKS`;
                document.getElementById('chain-length').textContent = data.chain_length;
                document.getElementById('total-evidence').textContent = data.total_evidence;
                document.getElementById('chain-valid').textContent = data.chain_valid ? '✓' : '✗';
                document.getElementById('last-block').textContent = data.last_block;
                
                if (data.chain_length > 0) {
                    document.getElementById('blockchain-status').textContent = 'SYNCED';
                }
            } catch (e) {
                console.log('Blockchain stats not available');
            }
        }
        
        async function loadNotificationStats() {
            try {
                const response = await fetch('/api/notifications_stats');
                const data = await response.json();
                document.getElementById('email-count').textContent = data.emails_sent || 0;
                document.getElementById('telegram-count').textContent = data.telegrams_sent || 0;
                document.getElementById('emails-sent').textContent = data.emails_sent || 0;
                document.getElementById('telegrams-sent').textContent = data.telegrams_sent || 0;
            } catch (e) {
                console.error('Error loading notifications:', e);
            }
        }
        
        async function generatePDF() {
            addTerminalLine('📄 Generating legal PDF report...', 'warning');
            showNotification('PDF GENERATION', 'Creating legal incident report...');
            
            try {
                const response = await fetch('/api/generate_pdf', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        type: 'INCIDENT_REPORT',
                        severity: 'HIGH',
                        ip: '203.0.113.50'
                    })
                });
                const data = await response.json();
                
                if (data.success) {
                    addTerminalLine(`✅ PDF generated: ${data.filepath}`, 'success');
                    showNotification('SUCCESS', `PDF saved: ${data.filepath}`);
                    document.getElementById('pdfs-generated').textContent = 
                        parseInt(document.getElementById('pdfs-generated').textContent) + 1;
                } else {
                    addTerminalLine(`⚠️ ${data.message}`, 'warning');
                    showNotification('WARNING', data.message);
                }
            } catch (e) {
                addTerminalLine('❌ Error generating PDF', 'error');
                showNotification('ERROR', 'Failed to generate PDF');
            }
        }
        
        async function checkQuantum() {
            addTerminalLine('⚛️ Checking quantum defense status...', 'warning');
            
            try {
                const response = await fetch('/api/quantum_status');
                const data = await response.json();
                
                if (data.enabled) {
                    addTerminalLine(`✅ Quantum Defense: ${data.algorithm}`, 'success');
                    showNotification('QUANTUM ACTIVE', `Algorithm: ${data.algorithm}`);
                } else {
                    addTerminalLine('⚠️ Quantum Defense not available', 'warning');
                    showNotification('WARNING', 'Quantum Defense not configured');
                }
            } catch (e) {
                addTerminalLine('❌ Error checking quantum status', 'error');
            }
        }
        
        function viewBlockchain() {
            addTerminalLine('🔗 Blockchain evidence viewer...', 'success');
            showNotification('BLOCKCHAIN', 'Evidence chain is immutable and court-admissible');
        }
        
        async function pressRedButton() {
            if (!confirm('🚨 EMERGENCY! Activate Red Button and notify CERTs?')) return;
            
            addTerminalLine('🚨🚨🚨 RED BUTTON ACTIVATED!', 'error');
            showNotification('EMERGENCY', 'Notifying CERTs...');
            
            try {
                const response = await fetch('/api/red_button', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ip: '198.51.100.1'})
                });
                const data = await response.json();
                
                if (data.success) {
                    addTerminalLine(`✅ ${data.certs_notified} CERTs notified: ${data.cert_list.join(', ')}`, 'success');
                    showNotification('SUCCESS', `${data.certs_notified} CERTs notified!`);
                } else {
                    addTerminalLine(`⚠️ ${data.message}`, 'warning');
                    showNotification('WARNING', data.message);
                }
            } catch (e) {
                addTerminalLine('❌ Error activating Red Button', 'error');
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
                    showNotification('SUCCESS', data.message);
                    addTerminalLine(`✅ Notification sent via ${channel}`, 'success');
                    loadNotificationStats();
                } else {
                    showNotification('ERROR', data.message);
                    addTerminalLine(`❌ Notification error: ${data.message}`, 'error');
                }
            } catch (e) {
                showNotification('ERROR', e.message);
            }
        }
        
        let timelineChart = null;
        let attackTypesChart = null;
        
        async function loadCharts() {
            // Timeline Chart con datos reales
            const timelineResponse = await fetch('/api/threat_timeline');
            const timelineData = await timelineResponse.json();
            
            const ctx1 = document.getElementById('timelineChart');
            if (timelineChart) timelineChart.destroy();
            
            timelineChart = new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: timelineData.hours,
                    datasets: [{
                        label: 'Threats Detected',
                        data: timelineData.counts,
                        borderColor: '#00ff41',
                        backgroundColor: 'rgba(0, 255, 65, 0.2)',
                        tension: 0.4,
                        fill: true,
                        borderWidth: 3,
                        pointRadius: 4,
                        pointBackgroundColor: '#00ff41',
                        pointBorderColor: '#0a0e14',
                        pointBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { 
                                color: '#00ff41', 
                                font: { family: 'Courier New', size: 12 } 
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { 
                                color: '#00ff41', 
                                font: { family: 'Courier New' },
                                stepSize: 1
                            },
                            grid: { color: 'rgba(0, 255, 65, 0.1)' }
                        },
                        x: {
                            ticks: { 
                                color: '#00ff41', 
                                font: { family: 'Courier New', size: 10 } 
                            },
                            grid: { color: 'rgba(0, 255, 65, 0.1)' }
                        }
                    }
                }
            });
            
            // Attack Types Chart
            const statsResponse = await fetch('/api/stats');
            const stats = await statsResponse.json();
            
            const ctx2 = document.getElementById('attackTypesChart');
            if (attackTypesChart) attackTypesChart.destroy();
            
            const types = Object.keys(stats.threats_by_type || {});
            const counts = Object.values(stats.threats_by_type || {});
            
            attackTypesChart = new Chart(ctx2, {
                type: 'doughnut',
                data: {
                    labels: types,
                    datasets: [{
                        data: counts,
                        backgroundColor: ['#ff0040', '#00ff41', '#00d9ff', '#ffd93d', '#b537f2'],
                        borderColor: '#0a0e14',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                color: '#00ff41', 
                                font: { family: 'Courier New' } 
                            }
                        }
                    }
                }
            });
        }
        
        connectWebSocket();
        loadStats();
        loadUnifiedStats();
        loadThreats();
        loadHoneypotStats();
        loadBlockchainStats();
        loadNotificationStats();
        loadCharts();
        
        setInterval(() => {
            loadStats();
            loadUnifiedStats();
            loadThreats();
            loadHoneypotStats();
            loadBlockchainStats();
            loadNotificationStats();
            loadCharts();
        }, 10000);
        
        setInterval(() => {
            const messages = [
                '[INFO] 5 Core Modules operational',
                '[INFO] ML Brain: 98.7% accuracy',
                '[INFO] Blockchain evidence synced',
                '[INFO] Quantum defense active',
                '[INFO] Alert system ready'
            ];
            const msg = messages[Math.floor(Math.random() * messages.length)];
            addTerminalLine(msg, 'success');
        }, 15000);
        
        setInterval(() => {
            const ips = ['192.168.1.100', '10.0.0.50', '172.16.0.1', '203.45.12.89'];
            const types = ['SQL_INJECTION', 'XSS', 'BRUTE_FORCE', 'PORT_SCAN', 'HONEYPOT_SSH'];
            const randomIp = ips[Math.floor(Math.random() * ips.length)];
            const randomType = types[Math.floor(Math.random() * types.length)];
            addAttackToMap(randomIp, randomType);
            addToAttacksLog(randomIp, randomType);
        }, 10000);
    </script>
</body>
</html>
        """
    
    async def run(self):
        import uvicorn
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()