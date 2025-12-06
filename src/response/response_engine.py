#!/usr/bin/env python3
"""
Némesis IA - Response Engine
Capítulo 8: Sistema de Respuesta Automática

Motor de decisión y ejecución de respuestas automáticas
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ResponseAction(Enum):
    """Tipos de acciones de respuesta"""
    BLOCK_IP = "BLOCK_IP"
    UNBLOCK_IP = "UNBLOCK_IP"
    CLOSE_PORT = "CLOSE_PORT"
    RATE_LIMIT = "RATE_LIMIT"
    THROTTLE_TRAFFIC = "THROTTLE_TRAFFIC"
    RESTART_SERVICE = "RESTART_SERVICE"
    SEND_ALERT = "SEND_ALERT"
    ESCALATE = "ESCALATE"
    LOG_ONLY = "LOG_ONLY"
    QUARANTINE = "QUARANTINE"


class ResponseStatus(Enum):
    """Estado de una respuesta"""
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


@dataclass
class Response:
    """Representa una respuesta automática"""
    id: int
    threat_id: Optional[int]
    source_ip: str
    threat_type: str
    severity: str
    
    # Acciones
    actions: List[ResponseAction]
    
    # Estado
    status: ResponseStatus
    
    # Timing
    created_at: datetime
    executed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    
    # Resultados
    success: bool = False
    error_message: Optional[str] = None
    
    # Metadata
    auto_generated: bool = True
    rollback_possible: bool = True
    rolled_back: bool = False


class ResponseEngine:
    """Motor de respuesta automática"""
    
    def __init__(self, database=None, dry_run: bool = False):
        """
        Inicializa el Response Engine
        
        Args:
            database: ThreatDatabase instance
            dry_run: Si True, solo simula sin ejecutar
        """
        
        self.database = database
        self.dry_run = dry_run
        
        # Políticas de respuesta
        self.policies = self._init_default_policies()
        
        # Historial de respuestas
        self.response_history: List[Response] = []
        self.response_counter = 0
        
        # Whitelist (IPs que NUNCA se bloquean)
        self.whitelist: set = {
            "127.0.0.1",
            "::1",
            "localhost"
        }
        
        # Strike system (3 strikes = block)
        self.strikes: Dict[str, int] = {}
        self.strike_threshold = 3
        
        # Estadísticas
        self.stats = {
            "total_responses": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "ips_blocked": 0,
            "false_positives": 0,
            "rollbacks": 0
        }
        
        logger.info(f"⚙️  ResponseEngine inicializado (dry_run: {dry_run})")
    
    def _init_default_policies(self) -> Dict:
        """Inicializa políticas por defecto"""
        
        return {
            "CRITICAL": {
                "actions": [
                    ResponseAction.BLOCK_IP,
                    ResponseAction.SEND_ALERT,
                    ResponseAction.ESCALATE
                ],
                "duration_hours": None,  # Permanente
                "immediate": True
            },
            "HIGH": {
                "actions": [
                    ResponseAction.BLOCK_IP,
                    ResponseAction.SEND_ALERT
                ],
                "duration_hours": 24,
                "immediate": True
            },
            "MEDIUM": {
                "actions": [
                    ResponseAction.RATE_LIMIT,
                    ResponseAction.LOG_ONLY
                ],
                "duration_hours": 6,
                "immediate": False,
                "strike_based": True
            },
            "LOW": {
                "actions": [
                    ResponseAction.LOG_ONLY
                ],
                "duration_hours": 1,
                "immediate": False
            }
        }
    
    def decide_response(
        self,
        source_ip: str,
        threat_type: str,
        severity: str,
        confidence: float = 1.0,
        threat_id: Optional[int] = None
    ) -> Response:
        """
        Decide qué respuesta tomar basándose en la amenaza
        
        Args:
            source_ip: IP de origen
            threat_type: Tipo de amenaza
            severity: Severidad (LOW, MEDIUM, HIGH, CRITICAL)
            confidence: Confianza de la detección (0-1)
            threat_id: ID de la amenaza en BD
            
        Returns:
            Response con acciones decididas
        """
        
        # Verificar whitelist
        if source_ip in self.whitelist:
            logger.info(f"✅ IP en whitelist, ignorando: {source_ip}")
            return self._create_log_only_response(
                source_ip, threat_type, severity, threat_id
            )
        
        # Obtener política
        policy = self.policies.get(severity, self.policies["LOW"])
        
        # Determinar acciones
        actions = self._determine_actions(
            source_ip, threat_type, severity, confidence, policy
        )
        
        # Calcular expiración
        expires_at = None
        if policy.get("duration_hours"):
            expires_at = datetime.now() + timedelta(hours=policy["duration_hours"])
        
        # Crear respuesta
        self.response_counter += 1
        response = Response(
            id=self.response_counter,
            threat_id=threat_id,
            source_ip=source_ip,
            threat_type=threat_type,
            severity=severity,
            actions=actions,
            status=ResponseStatus.PENDING,
            created_at=datetime.now(),
            expires_at=expires_at
        )
        
        logger.info(
            f"📋 Respuesta decidida para {source_ip}: "
            f"{[a.value for a in actions]} (severity: {severity})"
        )
        
        return response
    
    def _determine_actions(
        self,
        source_ip: str,
        threat_type: str,
        severity: str,
        confidence: float,
        policy: Dict
    ) -> List[ResponseAction]:
        """Determina acciones específicas basándose en política y contexto"""
        
        actions = policy["actions"].copy()
        
        # Strike system para MEDIUM
        if policy.get("strike_based"):
            self.strikes[source_ip] = self.strikes.get(source_ip, 0) + 1
            
            if self.strikes[source_ip] >= self.strike_threshold:
                logger.warning(
                    f"⚠️  {source_ip} alcanzó {self.strike_threshold} strikes, escalando"
                )
                actions = [ResponseAction.BLOCK_IP, ResponseAction.SEND_ALERT]
                # Reset strikes
                self.strikes[source_ip] = 0
        
        # Baja confianza = solo log
        if confidence < 0.7:
            logger.info(f"Baja confianza ({confidence:.2f}), solo logging")
            return [ResponseAction.LOG_ONLY]
        
        # Tipos específicos de amenaza
        if threat_type in ["DDOS", "DDOS_ATTACK"]:
            # DDoS requiere rate limiting además de block
            if ResponseAction.BLOCK_IP in actions:
                actions.append(ResponseAction.RATE_LIMIT)
        
        if threat_type in ["PORT_SCAN"]:
            # Port scan = close ports específicos
            if ResponseAction.BLOCK_IP in actions:
                actions.append(ResponseAction.CLOSE_PORT)
        
        return actions
    
    def execute_response(self, response: Response) -> bool:
        """
        Ejecuta una respuesta
        
        Args:
            response: Response a ejecutar
            
        Returns:
            True si exitoso, False si falla
        """
        
        self.stats["total_responses"] += 1
        
        response.status = ResponseStatus.EXECUTING
        response.executed_at = datetime.now()
        
        logger.info(
            f"⚡ Ejecutando respuesta #{response.id} para {response.source_ip}"
        )
        
        if self.dry_run:
            logger.info("   [DRY RUN] Simulando ejecución...")
            response.status = ResponseStatus.SUCCESS
            response.success = True
            self.stats["successful_responses"] += 1
            self.response_history.append(response)
            return True
        
        try:
            # Ejecutar cada acción
            for action in response.actions:
                success = self._execute_action(action, response)
                
                if not success:
                    raise Exception(f"Acción {action.value} falló")
            
            # Éxito
            response.status = ResponseStatus.SUCCESS
            response.success = True
            self.stats["successful_responses"] += 1
            
            # Actualizar estadísticas específicas
            if ResponseAction.BLOCK_IP in response.actions:
                self.stats["ips_blocked"] += 1
            
            logger.info(f"✅ Respuesta #{response.id} ejecutada exitosamente")
            
            self.response_history.append(response)
            return True
        
        except Exception as e:
            # Fallo
            response.status = ResponseStatus.FAILED
            response.success = False
            response.error_message = str(e)
            self.stats["failed_responses"] += 1
            
            logger.error(f"❌ Respuesta #{response.id} falló: {e}")
            
            self.response_history.append(response)
            return False
    
    def _execute_action(self, action: ResponseAction, response: Response) -> bool:
        """Ejecuta una acción específica"""
        
        logger.info(f"   Ejecutando: {action.value} para {response.source_ip}")
        
        if action == ResponseAction.BLOCK_IP:
            return self._block_ip(response.source_ip, response.expires_at)
        
        elif action == ResponseAction.RATE_LIMIT:
            return self._apply_rate_limit(response.source_ip)
        
        elif action == ResponseAction.CLOSE_PORT:
            return self._close_port(response.source_ip, response.threat_type)
        
        elif action == ResponseAction.SEND_ALERT:
            return self._send_alert(response)
        
        elif action == ResponseAction.LOG_ONLY:
            return self._log_threat(response)
        
        elif action == ResponseAction.ESCALATE:
            return self._escalate_threat(response)
        
        else:
            logger.warning(f"Acción no implementada: {action.value}")
            return True
    
    def _block_ip(self, ip: str, expires_at: Optional[datetime]) -> bool:
        """Bloquea una IP (simulación de iptables)"""
        
        # En producción, esto ejecutaría:
        # subprocess.run(['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'])
        
        duration = "permanente" if not expires_at else f"hasta {expires_at}"
        logger.info(f"   🚫 IP bloqueada: {ip} ({duration})")
        
        # Guardar en database si está disponible
        if self.database:
            self.database.block_ip(ip, reason="Automated response")
        
        return True
    
    def _apply_rate_limit(self, ip: str) -> bool:
        """Aplica rate limiting a una IP"""
        
        # En producción:
        # - tc (traffic control) en Linux
        # - nginx rate limiting
        # - fail2ban
        
        logger.info(f"   ⏱️  Rate limit aplicado a {ip}")
        return True
    
    def _close_port(self, ip: str, threat_type: str) -> bool:
        """Cierra puerto específico"""
        
        # Determinar puerto basándose en tipo de amenaza
        port_map = {
            "PORT_SCAN": 22,  # SSH
            "HONEYPOT_SSH": 2222,
            "SQL_INJECTION": 3306,  # MySQL
            "HTTP_ATTACK": 80
        }
        
        port = port_map.get(threat_type, 0)
        
        if port:
            logger.info(f"   🔒 Puerto {port} cerrado para {ip}")
        
        return True
    
    def _send_alert(self, response: Response) -> bool:
        """Envía alerta"""
        
        logger.info(f"   🚨 Alerta enviada para {response.source_ip}")
        return True
    
    def _log_threat(self, response: Response) -> bool:
        """Registra amenaza en logs"""
        
        logger.info(f"   📝 Amenaza registrada: {response.threat_type}")
        return True
    
    def _escalate_threat(self, response: Response) -> bool:
        """Escala amenaza a nivel superior"""
        
        logger.warning(
            f"   ⬆️  ESCALADO: {response.threat_type} desde {response.source_ip}"
        )
        return True
    
    def _create_log_only_response(
        self,
        source_ip: str,
        threat_type: str,
        severity: str,
        threat_id: Optional[int]
    ) -> Response:
        """Crea respuesta de solo logging"""
        
        self.response_counter += 1
        return Response(
            id=self.response_counter,
            threat_id=threat_id,
            source_ip=source_ip,
            threat_type=threat_type,
            severity=severity,
            actions=[ResponseAction.LOG_ONLY],
            status=ResponseStatus.PENDING,
            created_at=datetime.now()
        )
    
    def rollback_response(self, response_id: int) -> bool:
        """
        Hace rollback de una respuesta
        
        Args:
            response_id: ID de la respuesta
            
        Returns:
            True si exitoso
        """
        
        # Buscar respuesta
        response = None
        for r in self.response_history:
            if r.id == response_id:
                response = r
                break
        
        if not response:
            logger.error(f"Respuesta #{response_id} no encontrada")
            return False
        
        if not response.rollback_possible:
            logger.error(f"Respuesta #{response_id} no permite rollback")
            return False
        
        if response.rolled_back:
            logger.warning(f"Respuesta #{response_id} ya tiene rollback")
            return False
        
        logger.info(f"🔄 Haciendo rollback de respuesta #{response_id}")
        
        # Revertir acciones
        if ResponseAction.BLOCK_IP in response.actions:
            logger.info(f"   Desbloqueando {response.source_ip}")
            if self.database:
                # En producción: ejecutar iptables -D
                pass
        
        response.rolled_back = True
        response.status = ResponseStatus.ROLLED_BACK
        self.stats["rollbacks"] += 1
        
        logger.info(f"✅ Rollback completado para #{response_id}")
        return True
    
    def add_to_whitelist(self, ip: str):
        """Añade IP a whitelist"""
        self.whitelist.add(ip)
        logger.info(f"✅ {ip} añadida a whitelist")
    
    def remove_from_whitelist(self, ip: str):
        """Remueve IP de whitelist"""
        self.whitelist.discard(ip)
        logger.info(f"Removida de whitelist: {ip}")
    
    def get_response_history(self, limit: int = 50) -> List[Response]:
        """Obtiene historial de respuestas"""
        return self.response_history[-limit:]
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del motor"""
        
        # Calcular success rate
        total = self.stats["total_responses"]
        success_rate = 0
        if total > 0:
            success_rate = (self.stats["successful_responses"] / total) * 100
        
        return {
            **self.stats,
            "success_rate": round(success_rate, 2),
            "active_strikes": len(self.strikes),
            "whitelist_size": len(self.whitelist)
        }
    
    def get_strikes(self, ip: str) -> int:
        """Obtiene strikes de una IP"""
        return self.strikes.get(ip, 0)
    
    def reset_strikes(self, ip: str):
        """Resetea strikes de una IP"""
        if ip in self.strikes:
            del self.strikes[ip]
            logger.info(f"Strikes reseteados para {ip}")