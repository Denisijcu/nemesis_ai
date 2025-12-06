#!/usr/bin/env python3
"""
Némesis IA - Response Sentinel
Capítulo 8: Sistema de Respuesta Automática

Integración completa del sistema de respuesta automática
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Callable

from .response_engine import ResponseEngine, Response, ResponseAction
from .action_executor import ActionExecutor

logger = logging.getLogger(__name__)


class ResponseSentinel:
    """Sistema completo de respuesta automática"""
    
    def __init__(
        self,
        database=None,
        alert_manager=None,
        dry_run: bool = False,
        auto_respond: bool = True
    ):
        """
        Inicializa el Response Sentinel
        
        Args:
            database: ThreatDatabase instance
            alert_manager: AlertManager instance
            dry_run: Modo simulación
            auto_respond: Responder automáticamente
        """
        
        # Componentes
        self.engine = ResponseEngine(database=database, dry_run=dry_run)
        self.executor = ActionExecutor(dry_run=dry_run, simulation=True)
        
        # Referencias externas
        self.database = database
        self.alert_manager = alert_manager
        
        # Configuración
        self.auto_respond = auto_respond
        
        # Callbacks
        self.on_response_executed: Optional[Callable] = None
        
        # Estadísticas
        self.stats = {
            "threats_processed": 0,
            "responses_executed": 0,
            "auto_responses": 0,
            "manual_responses": 0
        }
        
        logger.info(
            f"🎖️  ResponseSentinel inicializado "
            f"(auto_respond: {auto_respond}, dry_run: {dry_run})"
        )
    
    def process_threat(
        self,
        source_ip: str,
        threat_type: str,
        severity: str,
        confidence: float = 1.0,
        threat_id: Optional[int] = None
    ) -> Response:
        """
        Procesa una amenaza y ejecuta respuesta automática
        
        Args:
            source_ip: IP de origen
            threat_type: Tipo de amenaza
            severity: Severidad
            confidence: Confianza de detección
            threat_id: ID de amenaza en BD
            
        Returns:
            Response ejecutada
        """
        
        self.stats["threats_processed"] += 1
        
        # 1. Decidir respuesta
        response = self.engine.decide_response(
            source_ip=source_ip,
            threat_type=threat_type,
            severity=severity,
            confidence=confidence,
            threat_id=threat_id
        )
        
        # 2. Ejecutar si auto_respond está activado
        if self.auto_respond:
            success = self.execute_response(response)
            
            if success:
                self.stats["auto_responses"] += 1
        
        return response
    
    def execute_response(self, response: Response) -> bool:
        """
        Ejecuta una respuesta completa
        
        Args:
            response: Response a ejecutar
            
        Returns:
            True si exitoso
        """
        
        self.stats["responses_executed"] += 1
        
        logger.info(
            f"⚡ Ejecutando respuesta para {response.source_ip} "
            f"({response.severity})"
        )
        
        # 1. Ejecutar en el engine
        engine_success = self.engine.execute_response(response)
        
        if not engine_success:
            logger.error("Engine execution failed")
            return False
        
        # 2. Ejecutar acciones concretas
        for action in response.actions:
            self._execute_concrete_action(action, response)
        
        # 3. Enviar alertas si corresponde
        if ResponseAction.SEND_ALERT in response.actions:
            self._send_alert(response)
        
        # 4. Callback
        if self.on_response_executed:
            try:
                self.on_response_executed(response)
            except Exception as e:
                logger.error(f"Error en callback: {e}")
        
        logger.info(f"✅ Respuesta ejecutada: {response.id}")
        
        return True
    
    def _execute_concrete_action(self, action: ResponseAction, response: Response):
        """Ejecuta acción concreta usando el executor"""
        
        if action == ResponseAction.BLOCK_IP:
            # Calcular duración
            duration = None
            if response.expires_at:
                duration = int((response.expires_at - datetime.now()).total_seconds())
            
            self.executor.block_ip_firewall(response.source_ip, duration)
        
        elif action == ResponseAction.RATE_LIMIT:
            self.executor.apply_rate_limit(response.source_ip)
        
        elif action == ResponseAction.CLOSE_PORT:
            # Determinar puerto basándose en threat_type
            port_map = {
                "PORT_SCAN": 22,
                "HONEYPOT_SSH": 2222,
                "SQL_INJECTION": 3306,
                "HTTP_ATTACK": 80
            }
            port = port_map.get(response.threat_type, 22)
            self.executor.close_port(port, response.source_ip)
        
        elif action == ResponseAction.THROTTLE_TRAFFIC:
            self.executor.throttle_bandwidth(response.source_ip)
        
        elif action == ResponseAction.QUARANTINE:
            self.executor.quarantine_ip(response.source_ip)
        
        elif action == ResponseAction.RESTART_SERVICE:
            # Solo en casos críticos
            if response.severity == "CRITICAL":
                self.executor.restart_service("nginx")
    
    def _send_alert(self, response: Response):
        """Envía alerta para una respuesta"""
        
        if not self.alert_manager:
            logger.debug("AlertManager no disponible")
            return
        
        try:
            severity_emoji = {
                "LOW": "🟢",
                "MEDIUM": "🟡",
                "HIGH": "🟠",
                "CRITICAL": "🔴"
            }.get(response.severity, "⚪")
            
            actions_str = ", ".join([a.value for a in response.actions])
            
            self.alert_manager.send_alert(
                title=f"{severity_emoji} Automated Response Executed",
                message=(
                    f"Threat: {response.threat_type}\n"
                    f"Source: {response.source_ip}\n"
                    f"Severity: {response.severity}\n"
                    f"Actions: {actions_str}\n"
                    f"Time: {response.executed_at}"
                ),
                severity=response.severity
            )
        
        except Exception as e:
            logger.error(f"Error enviando alerta: {e}")
    
    def rollback_response(self, response_id: int) -> bool:
        """
        Hace rollback de una respuesta
        
        Args:
            response_id: ID de la respuesta
            
        Returns:
            True si exitoso
        """
        
        # Rollback en engine
        success = self.engine.rollback_response(response_id)
        
        if success:
            # Rollback de acciones concretas
            # (desbloquear IP, remover rate limits, etc.)
            
            # Buscar la respuesta
            for response in self.engine.response_history:
                if response.id == response_id:
                    if ResponseAction.BLOCK_IP in response.actions:
                        self.executor.unblock_ip_firewall(response.source_ip)
                    
                    if ResponseAction.RATE_LIMIT in response.actions:
                        self.executor.remove_rate_limit(response.source_ip)
                    
                    break
        
        return success
    
    def whitelist_ip(self, ip: str):
        """Añade IP a whitelist (nunca será bloqueada)"""
        self.engine.add_to_whitelist(ip)
    
    def get_full_statistics(self) -> Dict:
        """Obtiene estadísticas completas del sistema"""
        
        engine_stats = self.engine.get_statistics()
        executor_stats = self.executor.get_statistics()
        
        return {
            "sentinel": self.stats,
            "engine": engine_stats,
            "executor": executor_stats
        }
    
    def get_active_blocks(self) -> Dict:
        """Obtiene información de bloqueos activos"""
        
        return {
            "blocked_ips": self.executor.get_blocked_ips(),
            "rate_limited_ips": self.executor.get_rate_limited_ips()
        }
    
    def generate_report(self) -> Dict:
        """Genera reporte completo del sistema"""
        
        stats = self.get_full_statistics()
        active = self.get_active_blocks()
        history = self.engine.get_response_history(20)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "active_blocks": active,
            "recent_responses": [
                {
                    "id": r.id,
                    "ip": r.source_ip,
                    "threat_type": r.threat_type,
                    "severity": r.severity,
                    "actions": [a.value for a in r.actions],
                    "status": r.status.value,
                    "executed_at": r.executed_at.isoformat() if r.executed_at else None
                }
                for r in history
            ]
        }