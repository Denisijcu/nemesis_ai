#!/usr/bin/env python3
"""
Némesis IA - Email Alert System
Envía alertas por email usando SMTP
"""

import logging
import asyncio
from typing import Optional
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib

logger = logging.getLogger(__name__)


class EmailAlert:
    """Sistema de alertas por Email"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
        to_email: str
    ):
        """
        Inicializa el sistema de alertas Email
        
        Args:
            smtp_server: Servidor SMTP (ej: smtp.gmail.com)
            smtp_port: Puerto SMTP (ej: 587)
            username: Usuario SMTP
            password: Contraseña SMTP
            from_email: Email remitente
            to_email: Email destinatario
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.to_email = to_email
        
        self.enabled = all([smtp_server, username, password, from_email, to_email])
        
        if self.enabled:
            logger.info("📧 EmailAlert inicializado")
        else:
            logger.warning("⚠️  EmailAlert deshabilitado (falta config)")
    
    async def send_threat_alert(
        self,
        source_ip: str,
        attack_type: str,
        confidence: float,
        payload: str,
        action_taken: str
    ):
        """
        Envía alerta de amenaza por email
        
        Args:
            source_ip: IP del atacante
            attack_type: Tipo de ataque
            confidence: Nivel de confianza
            payload: Payload del ataque
            action_taken: Acción tomada
        """
        if not self.enabled:
            return
        
        try:
            subject = f"🚨 AMENAZA DETECTADA: {attack_type} desde {source_ip}"
            
            body = self._format_threat_html(
                source_ip, attack_type, confidence, payload, action_taken
            )
            
            await self._send_email(subject, body)
            
            logger.info(f"📧 Alerta Email enviada: {attack_type} desde {source_ip}")
        
        except Exception as e:
            logger.error(f"❌ Error enviando alerta Email: {e}")
    
    def _format_threat_html(
        self,
        source_ip: str,
        attack_type: str,
        confidence: float,
        payload: str,
        action_taken: str
    ) -> str:
        """Formatea el email en HTML"""
        
        color_map = {
            "SQL_INJECTION": "#e74c3c",
            "XSS": "#e67e22",
            "PATH_TRAVERSAL": "#f39c12",
            "COMMAND_INJECTION": "#c0392b",
            "UNKNOWN": "#95a5a6"
        }
        
        color = color_map.get(attack_type, "#e74c3c")
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: {color}; color: white; padding: 20px; border-radius: 5px; }}
        .content {{ background: #f4f4f4; padding: 20px; margin-top: 20px; border-radius: 5px; }}
        .field {{ margin: 10px 0; }}
        .label {{ font-weight: bold; }}
        .value {{ background: white; padding: 10px; border-radius: 3px; margin-top: 5px; }}
        .footer {{ text-align: center; margin-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚨 AMENAZA DETECTADA</h1>
            <p>Sistema Némesis IA - Alerta de Seguridad</p>
        </div>
        
        <div class="content">
            <div class="field">
                <div class="label">🎯 Tipo de Ataque:</div>
                <div class="value">{attack_type}</div>
            </div>
            
            <div class="field">
                <div class="label">🌐 IP Origen:</div>
                <div class="value">{source_ip}</div>
            </div>
            
            <div class="field">
                <div class="label">📊 Nivel de Confianza:</div>
                <div class="value">{confidence:.1%}</div>
            </div>
            
            <div class="field">
                <div class="label">⚙️ Acción Tomada:</div>
                <div class="value">{action_taken}</div>
            </div>
            
            <div class="field">
                <div class="label">📦 Payload:</div>
                <div class="value" style="font-family: monospace; word-break: break-all;">
                    {payload[:200]}{'...' if len(payload) > 200 else ''}
                </div>
            </div>
            
            <div class="field">
                <div class="label">🕐 Timestamp:</div>
                <div class="value">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Némesis IA - Sistema Autónomo de Defensa Cibernética</p>
            <p>Este es un mensaje automático. No responder.</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    async def _send_email(self, subject: str, html_body: str):
        """Envía email usando SMTP"""
        
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = self.from_email
        message['To'] = self.to_email
        
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)
        
        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            start_tls=True
        )
    
    async def send_daily_report(self, stats: dict):
        """Envía reporte diario por email"""
        if not self.enabled:
            return
        
        try:
            subject = f"📊 Reporte Diario - Némesis IA - {datetime.now().strftime('%Y-%m-%d')}"
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #3498db; color: white; padding: 20px; border-radius: 5px; }}
        .stats {{ background: #f4f4f4; padding: 20px; margin-top: 20px; border-radius: 5px; }}
        .stat-item {{ margin: 15px 0; padding: 10px; background: white; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 REPORTE DIARIO</h1>
            <p>Némesis IA - Estadísticas de Seguridad</p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <strong>🎯 Total de Amenazas:</strong> {stats.get('total_threats', 0)}
            </div>
            <div class="stat-item">
                <strong>🚫 IPs Bloqueadas:</strong> {stats.get('total_blocked_ips', 0)}
            </div>
            <div class="stat-item">
                <strong>📈 Últimas 24h:</strong> {stats.get('threats_last_24h', 0)}
            </div>
            
            <h3>Amenazas por Tipo:</h3>
            {"".join(f'<div class="stat-item">{k}: {v}</div>' for k, v in stats.get('threats_by_type', {}).items())}
        </div>
    </div>
</body>
</html>
            """
            
            await self._send_email(subject, html)
            
            logger.info("📧 Reporte diario enviado por Email")
        
        except Exception as e:
            logger.error(f"❌ Error enviando reporte: {e}")