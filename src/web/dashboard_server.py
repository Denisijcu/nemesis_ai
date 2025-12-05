#!/usr/bin/env python3
"""
Némesis IA - Dashboard Web Server
FastAPI server con WebSocket para real-time updates
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)


class DashboardServer:
    """Servidor web del dashboard"""
    
    def __init__(self, database, host: str = "0.0.0.0", port: int = 8080):
        """
        Inicializa el servidor
        
        Args:
            database: Instancia de ThreatDatabase
            host: Host del servidor
            port: Puerto del servidor
        """
        self.database = database
        self.host = host
        self.port = port
        
        # FastAPI app
        self.app = FastAPI(title="Némesis IA Dashboard")
        
        # WebSocket connections activas
        self.active_connections: List[WebSocket] = []
        
        # Setup routes
        self._setup_routes()
        
        logger.info(f"🌐 Dashboard inicializado: http://{host}:{port}")
    
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
                    "action_taken": t.action_taken
                }
                for t in threats
            ]
        
        @self.app.get("/api/blocked_ips")
        async def get_blocked_ips():
            """Obtiene IPs bloqueadas"""
            return self.database.get_blocked_ips()
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket para updates en tiempo real"""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    # Mantener conexión abierta
                    await websocket.receive_text()
            
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    async def broadcast_threat(self, threat_data: dict):
        """
        Envía una amenaza a todos los clientes conectados
        
        Args:
            threat_data: Datos de la amenaza
        """
        for connection in self.active_connections:
            try:
                await connection.send_json(threat_data)
            except:
                pass
    
    def _get_dashboard_html(self) -> str:
        """Genera el HTML del dashboard"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Némesis IA - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
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
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
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
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .panel {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .panel h2 {
            margin-bottom: 20px;
            font-size: 1.5em;
        }
        
        .threat-item, .ip-item {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 10px;
            border-left: 4px solid #ff6b6b;
        }
        
        .threat-type {
            font-weight: bold;
            color: #ff6b6b;
        }
        
        .timestamp {
            font-size: 0.85em;
            opacity: 0.7;
        }
        
        .live-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #51cf66;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-right: 5px;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        @media (max-width: 768px) {
            .content-grid {
                grid-template-columns: 1fr;
            }
            
            h1 {
                font-size: 2em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🛡️ NÉMESIS IA</h1>
            <p class="subtitle">Sistema Autónomo de Defensa Cibernética</p>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Amenazas</div>
                <div class="stat-value" id="total-threats">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">IPs Bloqueadas</div>
                <div class="stat-value" id="blocked-ips">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Últimas 24h</div>
                <div class="stat-value" id="last-24h">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label"><span class="live-indicator"></span>Estado</div>
                <div class="stat-value" style="font-size: 1.5em;">ACTIVO</div>
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
        // Cargar estadísticas
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            document.getElementById('total-threats').textContent = stats.total_threats;
            document.getElementById('blocked-ips').textContent = stats.total_blocked_ips;
            document.getElementById('last-24h').textContent = stats.threats_last_24h;
        }
        
        // Cargar amenazas
        async function loadThreats() {
            const response = await fetch('/api/threats?limit=10');
            const threats = await response.json();
            
            const list = document.getElementById('threats-list');
            list.innerHTML = threats.map(t => `
                <div class="threat-item">
                    <div class="threat-type">${t.attack_type}</div>
                    <div>IP: ${t.source_ip} | Confianza: ${(t.confidence * 100).toFixed(1)}%</div>
                    <div class="timestamp">${new Date(t.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }
        
        // Cargar IPs bloqueadas
        async function loadBlockedIPs() {
            const response = await fetch('/api/blocked_ips');
            const ips = await response.json();
            
            const list = document.getElementById('blocked-list');
            list.innerHTML = ips.slice(0, 10).map(ip => `
                <div class="ip-item">
                    <div style="font-weight: bold;">${ip.ip}</div>
                    <div>${ip.threat_count} amenazas</div>
                    <div class="timestamp">${ip.reason}</div>
                </div>
            `).join('');
        }
        
        // Inicializar
        loadStats();
        loadThreats();
        loadBlockedIPs();
        
        // Recargar cada 5 segundos
        setInterval(() => {
            loadStats();
            loadThreats();
            loadBlockedIPs();
        }, 5000);
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