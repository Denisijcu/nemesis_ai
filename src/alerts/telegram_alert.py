#!/usr/bin/env python3
"""
Némesis IA - Telegram Alert System
Envía alertas de amenazas por Telegram
"""

import logging
import asyncio
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class TelegramAlert:
    """Sistema de alertas por Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Inicializa el sistema de alertas Telegram
        
        Args:
            bot_token: Token del bot de Telegram
            chat_id: ID del chat donde enviar alertas
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = bool(bot_token and chat_id)
        
        if self.enabled:
            logger.info("📱 TelegramAlert inicializado")
        else:
            logger.warning("⚠️  TelegramAlert deshabilitado (falta config)")
    
    async def send_threat_alert(
        self, 
        source_ip: str,
        attack_type: str,
        confidence: float,
        payload: str,
        action_taken: str
    ):
        """
        Envía alerta de amenaza por Telegram
        
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
            # Formatear mensaje
            message = self._format_threat_message(
                source_ip, attack_type, confidence, payload, action_taken
            )
            
            # Enviar mensaje
            await self._send_message(message)
            
            logger.info(f"📱 Alerta Telegram enviada: {attack_type} desde {source_ip}")
        
        except Exception as e:
            logger.error(f"❌ Error enviando alerta Telegram: {e}")
    
    def _format_threat_message(
        self,
        source_ip: str,
        attack_type: str,
        confidence: float,
        payload: str,
        action_taken: str
    ) -> str:
        """Formatea el mensaje de alerta (SIN Markdown)"""
        
        # Emoji según tipo de ataque
        emoji_map = {
            "SQL_INJECTION": "💉",
            "XSS": "🔴",
            "PATH_TRAVERSAL": "📂",
            "COMMAND_INJECTION": "⚡",
            "UNKNOWN": "❓"
        }
        
        emoji = emoji_map.get(attack_type, "🚨")
        
        # Truncar payload si es muy largo
        if len(payload) > 100:
            payload = payload[:97] + "..."
        
        # Mensaje simple sin formato especial
        message = f"""{emoji} AMENAZA DETECTADA

🎯 Tipo: {attack_type}
🌐 IP: {source_ip}
📊 Confianza: {confidence:.1%}
⚙️ Acción: {action_taken}

📦 Payload:
{payload}

🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return message.strip()
    
    async def _send_message(self, message: str):
        """Envía mensaje a Telegram usando la API"""
        import aiohttp
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Telegram API error: {error_text}")
    
    async def send_daily_report(self, stats: dict):
        """
        Envía reporte diario
        
        Args:
            stats: Estadísticas del día
        """
        if not self.enabled:
            return
        
        try:
            message = f"""📊 REPORTE DIARIO - NÉMESIS IA

🎯 Amenazas detectadas: {stats.get('total_threats', 0)}
🚫 IPs bloqueadas: {stats.get('total_blocked_ips', 0)}
📈 Últimas 24h: {stats.get('threats_last_24h', 0)}

Amenazas por tipo:"""
            
            threats_by_type = stats.get('threats_by_type', {})
            for attack_type, count in threats_by_type.items():
                message += f"\n  • {attack_type}: {count}"
            
            message += f"\n\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            await self._send_message(message)
            
            logger.info("📱 Reporte diario enviado por Telegram")
        
        except Exception as e:
            logger.error(f"❌ Error enviando reporte: {e}")