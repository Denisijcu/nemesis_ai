#!/usr/bin/env python3
"""
Némesis IA - Action Executor
Capítulo 8: Sistema de Respuesta Automática

Ejecutor de acciones concretas del sistema
"""

import logging
import subprocess
import time
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Ejecutor de acciones de respuesta"""
    
    def __init__(self, dry_run: bool = False, simulation: bool = True):
        """
        Inicializa el executor
        
        Args:
            dry_run: Solo simular, no ejecutar
            simulation: Usar comandos simulados (seguro)
        """
        
        self.dry_run = dry_run
        self.simulation = simulation
        
        # Tracking de acciones ejecutadas
        self.executed_actions: List[Dict] = []
        
        # Comandos bloqueados (IPs actualmente bloqueadas)
        self.blocked_ips: Dict[str, datetime] = {}
        
        # Rate limits activos
        self.rate_limits: Dict[str, Dict] = {}
        
        logger.info(f"⚙️  ActionExecutor inicializado (simulation: {simulation})")
    
    def block_ip_firewall(self, ip: str, duration_seconds: Optional[int] = None) -> bool:
        """
        Bloquea IP usando firewall (iptables)
        
        Args:
            ip: IP a bloquear
            duration_seconds: Duración del bloqueo (None = permanente)
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            logger.info(f"   [DRY RUN] Bloqueando IP en firewall: {ip}")
            return True
        
        if self.simulation:
            # Simulación - NO ejecuta comandos reales
            logger.info(f"   [SIMULATION] IP bloqueada en firewall: {ip}")
            self.blocked_ips[ip] = datetime.now()
            
            # Registrar acción
            self._log_action("BLOCK_IP_FIREWALL", ip, {
                "duration": duration_seconds,
                "command": f"iptables -A INPUT -s {ip} -j DROP"
            })
            
            return True
        
        try:
            # PRODUCCIÓN - Ejecutar iptables real
            # ⚠️ SOLO USAR EN SISTEMAS LINUX CON PERMISOS
            
            cmd = ['iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                logger.info(f"   ✅ IP bloqueada en firewall: {ip}")
                self.blocked_ips[ip] = datetime.now()
                self._log_action("BLOCK_IP_FIREWALL", ip, {"command": ' '.join(cmd)})
                return True
            else:
                logger.error(f"   ❌ Error bloqueando IP: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"   ❌ Timeout ejecutando iptables para {ip}")
            return False
        except Exception as e:
            logger.error(f"   ❌ Error ejecutando iptables: {e}")
            return False
    
    def unblock_ip_firewall(self, ip: str) -> bool:
        """
        Desbloquea IP del firewall
        
        Args:
            ip: IP a desbloquear
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            logger.info(f"   [DRY RUN] Desbloqueando IP: {ip}")
            return True
        
        if self.simulation:
            logger.info(f"   [SIMULATION] IP desbloqueada: {ip}")
            
            if ip in self.blocked_ips:
                del self.blocked_ips[ip]
            
            self._log_action("UNBLOCK_IP_FIREWALL", ip, {
                "command": f"iptables -D INPUT -s {ip} -j DROP"
            })
            
            return True
        
        try:
            # PRODUCCIÓN
            cmd = ['iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP']
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                logger.info(f"   ✅ IP desbloqueada: {ip}")
                if ip in self.blocked_ips:
                    del self.blocked_ips[ip]
                self._log_action("UNBLOCK_IP_FIREWALL", ip, {"command": ' '.join(cmd)})
                return True
            else:
                logger.error(f"   ❌ Error desbloqueando IP: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"   ❌ Error ejecutando iptables: {e}")
            return False
    
    def apply_rate_limit(self, ip: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        """
        Aplica rate limiting a una IP
        
        Args:
            ip: IP a limitar
            max_requests: Máximo de requests permitidos
            window_seconds: Ventana de tiempo en segundos
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            logger.info(f"   [DRY RUN] Rate limit: {ip} ({max_requests}/{window_seconds}s)")
            return True
        
        # Guardar configuración de rate limit
        self.rate_limits[ip] = {
            "max_requests": max_requests,
            "window_seconds": window_seconds,
            "applied_at": datetime.now()
        }
        
        logger.info(
            f"   ⏱️  Rate limit aplicado: {ip} "
            f"({max_requests} req/{window_seconds}s)"
        )
        
        self._log_action("RATE_LIMIT", ip, {
            "max_requests": max_requests,
            "window": window_seconds
        })
        
        # En producción, esto configuraría:
        # - nginx rate limiting
        # - tc (traffic control)
        # - fail2ban
        
        return True
    
    def remove_rate_limit(self, ip: str) -> bool:
        """Remueve rate limiting de una IP"""
        
        if ip in self.rate_limits:
            del self.rate_limits[ip]
            logger.info(f"   Rate limit removido: {ip}")
            self._log_action("REMOVE_RATE_LIMIT", ip, {})
            return True
        
        return False
    
    def close_port(self, port: int, ip: Optional[str] = None) -> bool:
        """
        Cierra puerto específico (opcionalmente solo para una IP)
        
        Args:
            port: Puerto a cerrar
            ip: IP específica (None = todas las IPs)
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            target = ip if ip else "TODAS"
            logger.info(f"   [DRY RUN] Cerrando puerto {port} para {target}")
            return True
        
        if self.simulation:
            target = ip if ip else "TODAS"
            logger.info(f"   [SIMULATION] Puerto {port} cerrado para {target}")
            
            self._log_action("CLOSE_PORT", ip or "ALL", {
                "port": port,
                "command": f"iptables -A INPUT -p tcp --dport {port} -j DROP"
            })
            
            return True
        
        try:
            # PRODUCCIÓN
            if ip:
                cmd = ['iptables', '-A', 'INPUT', '-s', ip, '-p', 'tcp', '--dport', str(port), '-j', 'DROP']
            else:
                cmd = ['iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', str(port), '-j', 'DROP']
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                target = ip if ip else "todas las IPs"
                logger.info(f"   ✅ Puerto {port} cerrado para {target}")
                self._log_action("CLOSE_PORT", ip or "ALL", {"port": port})
                return True
            else:
                logger.error(f"   ❌ Error cerrando puerto: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"   ❌ Error ejecutando iptables: {e}")
            return False
    
    def throttle_bandwidth(self, ip: str, rate_kbps: int = 128) -> bool:
        """
        Limita ancho de banda de una IP
        
        Args:
            ip: IP a throttlear
            rate_kbps: Tasa en KB/s
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            logger.info(f"   [DRY RUN] Throttling {ip}: {rate_kbps} KB/s")
            return True
        
        logger.info(f"   🔻 Bandwidth throttled: {ip} → {rate_kbps} KB/s")
        
        self._log_action("THROTTLE_BANDWIDTH", ip, {
            "rate_kbps": rate_kbps
        })
        
        # En producción:
        # - tc qdisc (Linux Traffic Control)
        # - iptables + hashlimit
        
        return True
    
    def restart_service(self, service_name: str) -> bool:
        """
        Reinicia un servicio del sistema
        
        Args:
            service_name: Nombre del servicio
            
        Returns:
            True si exitoso
        """
        
        if self.dry_run:
            logger.info(f"   [DRY RUN] Reiniciando servicio: {service_name}")
            return True
        
        if self.simulation:
            logger.info(f"   [SIMULATION] Servicio reiniciado: {service_name}")
            self._log_action("RESTART_SERVICE", service_name, {})
            return True
        
        try:
            # PRODUCCIÓN
            cmd = ['systemctl', 'restart', service_name]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"   ✅ Servicio reiniciado: {service_name}")
                self._log_action("RESTART_SERVICE", service_name, {})
                return True
            else:
                logger.error(f"   ❌ Error reiniciando servicio: {result.stderr}")
                return False
        
        except Exception as e:
            logger.error(f"   ❌ Error reiniciando servicio: {e}")
            return False
    
    def quarantine_ip(self, ip: str) -> bool:
        """
        Pone IP en cuarentena (permite solo tráfico mínimo)
        
        Args:
            ip: IP a poner en cuarentena
            
        Returns:
            True si exitoso
        """
        
        logger.info(f"   🔒 IP en cuarentena: {ip}")
        
        # Cuarentena = rate limit muy bajo + logging
        self.apply_rate_limit(ip, max_requests=10, window_seconds=60)
        
        self._log_action("QUARANTINE", ip, {
            "rate_limit": "10 req/min"
        })
        
        return True
    
    def _log_action(self, action_type: str, target: str, details: Dict):
        """Registra acción ejecutada"""
        
        self.executed_actions.append({
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "target": target,
            "details": details
        })
    
    def get_blocked_ips(self) -> List[str]:
        """Retorna lista de IPs bloqueadas"""
        return list(self.blocked_ips.keys())
    
    def get_rate_limited_ips(self) -> Dict[str, Dict]:
        """Retorna IPs con rate limit activo"""
        return self.rate_limits.copy()
    
    def get_action_history(self, limit: int = 50) -> List[Dict]:
        """Retorna historial de acciones"""
        return self.executed_actions[-limit:]
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas del executor"""
        
        action_types = {}
        for action in self.executed_actions:
            atype = action["action"]
            action_types[atype] = action_types.get(atype, 0) + 1
        
        return {
            "total_actions": len(self.executed_actions),
            "blocked_ips": len(self.blocked_ips),
            "rate_limited_ips": len(self.rate_limits),
            "by_action_type": action_types
        }