#!/usr/bin/env python3
"""
Némesis IA - Honeypot Logger
Capítulo 5: Honeypots Inteligentes

Guarda intentos del honeypot en la base de datos
"""

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class HoneypotLogger:
    """Logger que guarda intentos en base de datos"""
    
    def __init__(self, database=None, alert_manager=None):
        """
        Inicializa el logger
        
        Args:
            database: Instancia de ThreatDatabase
            alert_manager: Instancia de AlertManager
        """
        self.database = database
        self.alert_manager = alert_manager
        
        self.attempts_logged = 0
        self.alerts_sent = 0
        
        logger.info("📝 HoneypotLogger inicializado")
        if database:
            logger.info("💾 Base de datos habilitada")
        if alert_manager:
            logger.info("📢 Alertas habilitadas")
    
    async def log_attempt(
        self,
        ip: str,
        username: str,
        password: str,
        service: str = "SSH",
        profile_data: Optional[dict] = None
    ):
        """
        Registra un intento de ataque
        
        Args:
            ip: IP del atacante
            username: Username intentado
            password: Password intentado
            service: Servicio atacado (SSH, HTTP, etc)
            profile_data: Datos del perfil del atacante
        """
        
        # Construir payload
        payload = f"Service: {service}, User: {username}, Pass: {password}"
        
        if profile_data:
            payload += f", Pattern: {profile_data.get('attack_pattern', 'UNKNOWN')}"
            payload += f", Score: {profile_data.get('threat_score', 0):.1f}"
        
        # Guardar en BD
        if self.database:
            try:
                from database.threat_database import ThreatRecord
                
                threat = ThreatRecord(
                    id=None,
                    timestamp=datetime.now(),
                    source_ip=ip,
                    attack_type=f"HONEYPOT_{service.upper()}",
                    payload=payload[:500],  # Limitar tamaño
                    confidence=0.99,  # Honeypot = alta confianza
                    action_taken="LOGGED",
                    blocked=False
                )
                
                threat_id = self.database.save_threat(threat)
                self.attempts_logged += 1
                
                logger.debug(f"💾 Intento guardado en BD: ID={threat_id}")
                
                # Si es un atacante peligroso, bloquearlo
                if profile_data and profile_data.get('threat_score', 0) > 50:
                    self.database.block_ip(
                        ip,
                        f"Honeypot attack: {profile_data.get('attack_pattern', 'UNKNOWN')}"
                    )
                    logger.warning(f"🚫 IP bloqueada: {ip}")
            
            except Exception as e:
                logger.error(f"❌ Error guardando en BD: {e}")
        
        # Enviar alerta
        if self.alert_manager:
            try:
                # Solo alertar si threat score > 30
                should_alert = False
                
                if profile_data:
                    threat_score = profile_data.get('threat_score', 0)
                    if threat_score > 30:
                        should_alert = True
                
                if should_alert:
                    await self.alert_manager.send_threat_alert(
                        source_ip=ip,
                        attack_type=f"HONEYPOT_{service.upper()}",
                        confidence=0.99,
                        payload=f"{username}/{password}",
                        action_taken="LOGGED"
                    )
                    
                    self.alerts_sent += 1
                    logger.info(f"📱 Alerta enviada para {ip}")
            
            except Exception as e:
                logger.error(f"❌ Error enviando alerta: {e}")
    
    def get_stats(self) -> dict:
        """Retorna estadísticas del logger"""
        return {
            "attempts_logged": self.attempts_logged,
            "alerts_sent": self.alerts_sent
        }