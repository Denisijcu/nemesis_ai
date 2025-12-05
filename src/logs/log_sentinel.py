#!/usr/bin/env python3
"""
Némesis IA - Log Sentinel
Con integración a Dashboard V2
"""

import asyncio
import logging
from typing import Optional
from datetime import datetime

from .log_reader import LogReader
from .log_parser import LogParser

logger = logging.getLogger(__name__)


class LogSentinel:
    """Centinela de Logs que monitorea y analiza en tiempo real"""
    
    def __init__(self, agent, log_file: str, follow: bool = True, database=None, alert_manager=None, dashboard=None):
        """
        Inicializa el Centinela
        
        Args:
            agent: Instancia de NemesisAgent
            log_file: Archivo de log a monitorear
            follow: Si True, hace tail -f
            database: Instancia de ThreatDatabase (opcional)
            alert_manager: Instancia de AlertManager (opcional)
            dashboard: Instancia de DashboardV2 (opcional)
        """
        self.agent = agent
        self.reader = LogReader(log_file, follow=follow)
        self.parser = LogParser()
        self.database = database
        self.alert_manager = alert_manager
        self.dashboard = dashboard  # ← NUEVO
        
        self._is_running = False
        self._logs_processed = 0
        self._threats_detected = 0
        
        logger.info(f"👁️  LogSentinel inicializado")
        if self.database:
            logger.info("💾 Base de datos habilitada")
        if self.alert_manager:
            logger.info("📢 Sistema de alertas habilitado")
        if self.dashboard:  # ← NUEVO
            logger.info("🌐 Dashboard real-time habilitado")
    
    async def start(self):
        """Inicia el monitoreo de logs"""
        logger.info("🚀 LogSentinel iniciando...")
        self._is_running = True
        
        try:
            async for log_line in self.reader.start():
                if not self._is_running:
                    break
                
                # Procesar línea
                await self._process_log_line(log_line)
        
        except Exception as e:
            logger.error(f"❌ Error en LogSentinel: {e}")
        
        finally:
            logger.info("⏹️  Deteniendo LogSentinel...")
            self._is_running = False
            
            logger.info(
                f"📊 LogSentinel detenido - "
                f"Logs procesados: {self._logs_processed}, "
                f"Amenazas: {self._threats_detected}"
            )
    
    async def _process_log_line(self, log_line: str):
        """Procesa una línea de log"""
        self._logs_processed += 1
        
        # Parsear log
        parsed = self.parser.parse(log_line)
        
        if not parsed:
            return
        
        # Analizar con Agente Némesis
        verdict = await self.agent.process_log_line(log_line)
        
        if verdict and verdict.is_malicious:
            self._threats_detected += 1
            
            logger.warning(
                f"🚨 AMENAZA #{self._threats_detected}: "
                f"{verdict.attack_type} desde {parsed.source_ip}"
            )
            
            # Guardar en base de datos, enviar alertas y actualizar dashboard
            if self.database or self.alert_manager or self.dashboard:
                await self._save_and_alert(parsed, verdict)
    
    async def _save_and_alert(self, parsed, verdict):
        """Guarda amenaza en BD, envía alertas y actualiza dashboard"""
        try:
            threat_data = {
                "timestamp": datetime.now().isoformat(),
                "source_ip": parsed.source_ip,
                "attack_type": verdict.attack_type,
                "payload": parsed.path,
                "confidence": verdict.confidence,
                "action_taken": verdict.recommended_action
            }
            
            # Guardar en base de datos
            if self.database:
                from database.threat_database import ThreatRecord
                
                threat = ThreatRecord(
                    id=None,
                    timestamp=datetime.now(),
                    source_ip=parsed.source_ip,
                    attack_type=verdict.attack_type,
                    payload=parsed.path,
                    confidence=verdict.confidence,
                    action_taken=verdict.recommended_action,
                    blocked=(verdict.recommended_action == "BLOCK")
                )
                
                threat_id = self.database.save_threat(threat)
                
                # Registrar IP bloqueada
                if verdict.recommended_action == "BLOCK":
                    self.database.block_ip(
                        parsed.source_ip,
                        f"{verdict.attack_type} attack"
                    )
                
                logger.debug(f"💾 Amenaza guardada en BD: ID={threat_id}")
            
            # Enviar alerta
            if self.alert_manager:
                await self.alert_manager.send_threat_alert(
                    source_ip=parsed.source_ip,
                    attack_type=verdict.attack_type,
                    confidence=verdict.confidence,
                    payload=parsed.path,
                    action_taken=verdict.recommended_action
                )
            
            # Broadcast a dashboard (NUEVO)
            if self.dashboard:
                await self.dashboard.broadcast_threat(threat_data)
                logger.debug("🌐 Amenaza enviada al dashboard")
        
        except Exception as e:
            logger.error(f"❌ Error en save_and_alert: {e}")
    
    async def stop(self):
        """Detiene el Centinela manualmente"""
        self._is_running = False
        await self.reader.stop()
    
    @property
    def stats(self):
        """Retorna estadísticas"""
        return {
            "logs_processed": self._logs_processed,
            "threats_detected": self._threats_detected,
            "detection_rate": (
                (self._threats_detected / self._logs_processed * 100)
                if self._logs_processed > 0 else 0
            )
        }