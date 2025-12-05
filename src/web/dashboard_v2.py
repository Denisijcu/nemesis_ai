#!/usr/bin/env python3
"""
Némesis IA - Dashboard V2
Dashboard mejorado con WebSocket, Chart.js y notificaciones real-time
"""

import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

logger = logging.getLogger(__name__)


class DashboardV2:
    """Dashboard mejorado con real-time updates"""
    
    def __init__(self, database, host: str = "0.0.0.0", port: int = 8080):
        """
        Inicializa el dashboard V2
        
        Args:
            database: Instancia de ThreatDatabase
            host: Host del servidor
            port: Puerto del servidor
        """
        self.database = database
        self.host = host
        self.port = port
        
        # FastAPI app
        self.app = FastAPI(title="Némesis IA Dashboard V2")
        
        # WebSocket connections activas
        self.active_connections: Set[WebSocket] = set()
        
        # Setup routes
        self._setup_routes()
        
        logger.info(f"🌐 Dashboard V2 inicializado: http://{host}:{port}")
    
    def _setup_routes(self):
        """Configura las rutas de la API"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            """Página principal del dashboard"""
            return self._get_dashboard_html()
        
        @self.app.get("/api/stats")
        async def get_stats():
            """Obtiene estadísticas globales"""
            return self.database.get_statistics()
        
        @self.app.get("/api/threats")
        async def get_threats(limit: int = 50):
            """Obtiene lista de amenazas"""
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
            """Obtiene IPs bloqueadas"""
            return self.database.get_blocked_ips()
        
        @self.app.get("/api/chart_data")
        async def get_chart_data():
            """Obtiene datos para gráficas"""
            stats = self.database.get_statistics()
            threats = self.database.get_threats(limit=100)
            
            # Timeline data (últimas 24 horas)
            timeline = {}
            for threat in threats:
                hour = threat.timestamp.strftime('%H:00')
                timeline[hour] = timeline.get(hour, 0) + 1
            
            # Top IPs
            top_ips = stats.get('top_malicious_ips', [])[:10]
            
            return {
                "timeline": timeline,
                "attack_types": stats.get('threats_by_type', {}),
                "top_ips": {ip: count for ip, count in top_ips}
            }
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket para updates en tiempo real"""
            await websocket.accept()
            self.active_connections.add(websocket)
            
            try:
                while True:
                    # Mantener conexión abierta
                    data = await websocket.receive_text()
                    
                    # Si recibe "ping", responde "pong"
                    if data == "ping":
                        await websocket.send_text("pong")
            
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)
    
    async def broadcast_threat(self, threat_data: dict):
        """
        Envía una amenaza a todos los clientes conectados
        
        Args:
            threat_data: Datos de la amenaza
        """
        message = json.dumps({
            "type": "new_threat",
            "data": threat_data
        })
        
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting: {e}")
                disconnected.add(connection)
        
        # Limpiar conexiones muertas
        self.active_connections -= disconnected
    
    def _get_dashboard_html(self) -> str:
        """Genera el HTML del dashboard V2"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Némesis IA - Dashboard V2</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #51cf66;
            --danger: #ff6b6b;
            --warning: #ffd93d;
            --dark: #1a1a2e;
            --light: #f8f9fa;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: #fff;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            animation: fadeInDown 0.6s;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            animation: pulse 2s infinite;
        }
        
        .live-indicator {
            width: 10px;
            height: 10px;
            background: var(--success);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--success);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: all 0.3s;
            animation: fadeInUp 0.6s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
        }
        
        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .stat-label {
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .charts-section {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            animation: fadeInUp 0.6s;
        }
        
        .panel h2 {
            margin-bottom: 20px;
            font-size: 1.5em;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .chart-container {
            position: relative;
            height: 300px;
        }
        
        .threat-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid var(--danger);
            animation: slideInRight 0.4s;
            transition: all 0.3s;
        }
        
        .threat-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(5px);
        }
        
        .threat-item.new {
            animation: newThreatPulse 1s;
        }
        
        .threat-type {
            font-weight: bold;
            color: var(--danger);
            font-size: 1.1em;
        }
        
        .threat-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .timestamp {
            font-size: 0.85em;
            opacity: 0.7;
            margin-top: 8px;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 107, 107, 0.95);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            z-index: 1000;
            animation: slideInRight 0.4s;
            max-width: 400px;
        }
        
        .notification.success {
            background: rgba(81, 207, 102, 0.95);
        }
        
        .notification-title {
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
        }
        
        @keyframes newThreatPulse {
            0% {
                background: rgba(255, 107, 107, 0.3);
                transform: scale(1.05);
            }
            100% {
                background: rgba(255, 255, 255, 0.05);
                transform: scale(1);
            }
        }
        
        @media (max-width: 1200px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            .charts-section {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            
            .charts-section {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ NÉMESIS IA</h1>
            <p class="subtitle">Sistema Autónomo de Defensa Cibernética V2</p>
            <div class="status-badge">
                <span class="live-indicator"></span>
                <span>Sistema Activo - Real-time Monitoring</span>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">🎯 Total Amenazas</div>
                <div class="stat-value" id="total-threats">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">🚫 IPs Bloqueadas</div>
                <div class="stat-value" id="blocked-ips">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">📈 Últimas 24h</div>
                <div class="stat-value" id="last-24h">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">⚡ Detecciones/min</div>
                <div class="stat-value" id="rate">0</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="panel">
                <h2>📊 Timeline de Amenazas</h2>
                <div class="chart-container">
                    <canvas id="timelineChart"></canvas>
                </div>
            </div>
            
            <div class="panel">
                <h2>🎯 Tipos de Ataque</h2>
                <div class="chart-container">
                    <canvas id="attackTypesChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="content-grid">
            <div class="panel">
                <h2>🚨 Amenazas Recientes</h2>
                <div id="threats-list"></div>
            </div>
            
            <div class="panel">
                <h2>🚫 IPs Bloqueadas</h2>
                <div id="blocked-list"></div>
            </div>
        </div>
    </div>
    
    <script>
        // WebSocket connection
        let ws = null;
        let reconnectInterval = null;
        
        // Charts
        let timelineChart = null;
        let attackTypesChart = null;
        
        // Connect to WebSocket
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);
            
            ws.onopen = () => {
                console.log('✅ WebSocket connected');
                if (reconnectInterval) {
                    clearInterval(reconnectInterval);
                    reconnectInterval = null;
                }
                
                // Send ping every 30 seconds
                setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send('ping');
                    }
                }, 30000);
            };
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                
                if (message.type === 'new_threat') {
                    handleNewThreat(message.data);
                }
            };
            
            ws.onclose = () => {
                console.log('❌ WebSocket disconnected');
                // Reconnect after 5 seconds
                if (!reconnectInterval) {
                    reconnectInterval = setInterval(connectWebSocket, 5000);
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }
        
        // Handle new threat
        function handleNewThreat(threat) {
            // Show notification
            showNotification('🚨 Nueva Amenaza Detectada', 
                `${threat.attack_type} desde ${threat.source_ip}`);
            
            // Play sound (optional)
            // playAlertSound();
            
            // Reload data
            loadStats();
            loadThreats();
            loadChartData();
        }
        
        // Show notification
        function showNotification(title, message) {
            const notification = document.createElement('div');
            notification.className = 'notification';
            notification.innerHTML = `
                <div class="notification-title">${title}</div>
                <div>${message}</div>
            `;
            
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.animation = 'slideInRight 0.4s reverse';
                setTimeout(() => notification.remove(), 400);
            }, 5000);
        }
        
        // Load statistics
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            document.getElementById('total-threats').textContent = stats.total_threats;
            document.getElementById('blocked-ips').textContent = stats.total_blocked_ips;
            document.getElementById('last-24h').textContent = stats.threats_last_24h;
        }
        
        // Load threats
        async function loadThreats() {
            const response = await fetch('/api/threats?limit=10');
            const threats = await response.json();
            
            const list = document.getElementById('threats-list');
            list.innerHTML = threats.map(t => `
                <div class="threat-item">
                    <div class="threat-type">${t.attack_type}</div>
                    <div class="threat-details">
                        <div>🌐 IP: ${t.source_ip}</div>
                        <div>📊 Confianza: ${(t.confidence * 100).toFixed(1)}%</div>
                    </div>
                    <div class="timestamp">🕐 ${new Date(t.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }
        
        // Load blocked IPs
        async function loadBlockedIPs() {
            const response = await fetch('/api/blocked_ips');
            const ips = await response.json();
            
            const list = document.getElementById('blocked-list');
            list.innerHTML = ips.slice(0, 10).map(ip => `
                <div class="threat-item">
                    <div style="font-weight: bold;">🚫 ${ip.ip}</div>
                    <div>${ip.threat_count} amenazas</div>
                    <div class="timestamp">${ip.reason}</div>
                </div>
            `).join('');
        }
        
        // Load chart data
        async function loadChartData() {
            const response = await fetch('/api/chart_data');
            const data = await response.json();
            
            updateTimelineChart(data.timeline);
            updateAttackTypesChart(data.attack_types);
        }
        
        // Update timeline chart
        function updateTimelineChart(timeline) {
            const ctx = document.getElementById('timelineChart');
            
            if (timelineChart) {
                timelineChart.destroy();
            }
            
            const hours = Object.keys(timeline).sort();
            const values = hours.map(h => timeline[h]);
            
            timelineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: hours,
                    datasets: [{
                        label: 'Amenazas',
                        data: values,
                        borderColor: 'rgb(255, 107, 107)',
                        backgroundColor: 'rgba(255, 107, 107, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: '#fff' }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#fff' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        },
                        x: {
                            ticks: { color: '#fff' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' }
                        }
                    }
                }
            });
        }
        
        // Update attack types chart
        function updateAttackTypesChart(attackTypes) {
            const ctx = document.getElementById('attackTypesChart');
            
            if (attackTypesChart) {
                attackTypesChart.destroy();
            }
            
            const labels = Object.keys(attackTypes);
            const values = Object.values(attackTypes);
            
            attackTypesChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            'rgb(255, 107, 107)',
                            'rgb(255, 209, 61)',
                            'rgb(102, 126, 234)',
                            'rgb(81, 207, 102)',
                            'rgb(118, 75, 162)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#fff' }
                        }
                    }
                }
            });
        }
        
        // Initialize
        connectWebSocket();
        loadStats();
        loadThreats();
        loadBlockedIPs();
        loadChartData();
        
        // Refresh every 10 seconds
        setInterval(() => {
            loadStats();
            loadThreats();
            loadBlockedIPs();
            loadChartData();
        }, 10000);
    </script>
</body>
</html>
        """
    
    async def run(self):
        """Inicia el servidor"""
        import uvicorn
        
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )
        
        server = uvicorn.Server(config)
        await server.serve()