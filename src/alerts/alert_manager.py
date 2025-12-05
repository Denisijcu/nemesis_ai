#!/usr/bin/env python3
"""
Némesis IA - Alert Manager
Gestiona múltiples canales de alertas
"""

import logging
from typing import Optional
from .telegram_alert import TelegramAlert
from .email_alert import EmailAlert

logger = logging.getLogger(__name__)


class AlertManager:
    """Gestor central de alertas multicanal"""
    
    def __init__(self, config: dict):
        """
        Inicializa el gestor de alertas
        
        Args:
            config: Diccionario con configuración de alertas
        """
        # Telegram
        telegram_config = config.get('telegram', {})
        self.telegram = TelegramAlert(
            bot_token=telegram_config.get('bot_token', ''),
            chat_id=telegram_config.get('chat_id', '')
        )
        
        # Email
        email_config = config.get('email', {})
        self.email = EmailAlert(
            smtp_server=email_config.get('smtp_server', ''),
            smtp_port=email_config.get('smtp_port', 587),
            username=email_config.get('username', ''),
            password=email_config.get('password', ''),
            from_email=email_config.get('from_email', ''),
            to_email=email_config.get('to_email', '')
        )
        
        logger.info("📢 AlertManager inicializado")
    
    async def send_threat_alert(
        self,
        source_ip: str,
        attack_type: str,
        confidence: float,
        payload: str,
        action_taken: str
    ):
        """
        Envía alerta de amenaza por todos los canales habilitados
        
        Args:
            source_ip: IP del atacante
            attack_type: Tipo de ataque
            confidence: Nivel de confianza
            payload: Payload del ataque
            action_taken: Acción tomada
        """
        # Enviar por Telegram
        await self.telegram.send_threat_alert(
            source_ip, attack_type, confidence, payload, action_taken
        )
        
        # Enviar por Email
        await self.email.send_threat_alert(
            source_ip, attack_type, confidence, payload, action_taken
        )
    
    async def send_daily_report(self, stats: dict):
        """
        Envía reporte diario por todos los canales
        
        Args:
            stats: Estadísticas del sistema
        """
        await self.telegram.send_daily_report(stats)
        await self.email.send_daily_report(stats)