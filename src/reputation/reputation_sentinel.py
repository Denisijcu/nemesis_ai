#!/usr/bin/env python3
"""
Némesis IA - Reputation Sentinel
Capítulo 7: Sistema de Reputación de IPs

Integración completa del sistema de reputación
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional, Dict, Callable

from .ip_checker import IPReputationChecker, IPReputation
from .reputation_database import ReputationDatabase

logger = logging.getLogger(__name__)


class ReputationSentinel:
    """Sistema completo de reputación de IPs"""
    
    def __init__(
        self,
        database=None,
        threat_database=None,
        cache_ttl: int = 3600
    ):
        """
        Inicializa el Reputation Sentinel
        
        Args:
            database: ReputationDatabase instance
            threat_database: ThreatDatabase instance (opcional)
            cache_ttl: Tiempo de vida del cache
        """
        
        # Componentes del sistema
        self.checker = IPReputationChecker(cache_ttl=cache_ttl)
        self.database = database or ReputationDatabase()
        self.threat_database = threat_database
        
        # Cargar whitelist/blacklist desde BD
        self._load_lists_from_db()
        
        # Callbacks
        self.on_malicious_ip_callback: Optional[Callable] = None
        self.on_reputation_change_callback: Optional[Callable] = None
        
        # Estadísticas
        self.stats = {
            "ips_checked": 0,
            "malicious_found": 0,
            "whitelist_hits": 0,
            "blacklist_hits": 0,
            "cache_hits": 0
        }
        
        logger.info("🎖️  ReputationSentinel inicializado")
    
    def _load_lists_from_db(self):
        """Carga whitelist/blacklist desde base de datos al checker"""
        
        # Esta función sincroniza las listas de la BD con el checker en memoria
        # En una implementación real, podrías cargar todas las IPs
        # Por ahora, las listas se manejan en tiempo real
        
        logger.debug("Listas cargadas desde BD")
    
    def set_malicious_callback(self, callback: Callable):
        """Callback para cuando se detecta IP maliciosa"""
        self.on_malicious_ip_callback = callback
    
    def set_reputation_change_callback(self, callback: Callable):
        """Callback para cambios de reputación"""
        self.on_reputation_change_callback = callback
    
    def check_ip(self, ip: str, force_refresh: bool = False) -> IPReputation:
        """
        Verifica reputación de una IP (pipeline completo)
        
        Args:
            ip: Dirección IP
            force_refresh: Forzar actualización
            
        Returns:
            IPReputation completa
        """
        
        self.stats["ips_checked"] += 1
        
        # 1. Verificar en BD primero (si no es force_refresh)
        if not force_refresh:
            db_rep = self.database.get_reputation(ip)
            if db_rep:
                # Verificar si no es muy vieja (usando cache_ttl)
                age = (datetime.now() - db_rep.checked_at).total_seconds()
                if age < self.checker.cache_ttl:
                    logger.debug(f"BD hit para {ip}")
                    self.stats["cache_hits"] += 1
                    return db_rep
        
        # 2. Verificar whitelist/blacklist en BD
        is_whitelisted = self.database.is_whitelisted(ip)
        is_blacklisted = self.database.is_blacklisted(ip)
        
        if is_whitelisted:
            self.stats["whitelist_hits"] += 1
            # Actualizar checker
            self.checker.add_to_whitelist(ip)
        
        if is_blacklisted:
            self.stats["blacklist_hits"] += 1
            # Actualizar checker
            self.checker.add_to_blacklist(ip)
        
        # 3. Obtener reputación del checker
        reputation = self.checker.check_ip(ip, force_refresh=force_refresh)
        
        # 4. Guardar en BD
        self.database.save_reputation(reputation)
        
        # 5. Verificar si es maliciosa
        if self._is_malicious(reputation):
            self._handle_malicious_ip(reputation)
        
        # 6. Integración con ThreatDatabase si está disponible
        if self.threat_database and reputation.reputation_score < 40:
            self._update_threat_database(reputation)
        
        return reputation
    
    def _is_malicious(self, reputation: IPReputation) -> bool:
        """Determina si una IP es maliciosa"""
        
        # Criterios:
        # - Score bajo (<40)
        # - En blacklist
        # - Threat level CRITICAL o HIGH
        
        if reputation.is_blacklisted:
            return True
        
        if reputation.reputation_score < 40:
            return True
        
        if reputation.threat_level in ["CRITICAL", "HIGH"]:
            return True
        
        return False
    
    def _handle_malicious_ip(self, reputation: IPReputation):
        """Maneja detección de IP maliciosa"""
        
        self.stats["malicious_found"] += 1
        
        logger.warning(
            f"🚨 IP maliciosa detectada: {reputation.ip} "
            f"(Score: {reputation.reputation_score}, Threat: {reputation.threat_level})"
        )
        
        # Añadir automáticamente a blacklist si no está
        if not reputation.is_blacklisted:
            self.database.add_to_blacklist(
                reputation.ip,
                reason=f"Auto-blacklisted: Score {reputation.reputation_score}",
                severity=reputation.threat_level
            )
            self.checker.add_to_blacklist(reputation.ip)
        
        # Callback
        if self.on_malicious_ip_callback:
            try:
                self.on_malicious_ip_callback(reputation)
            except Exception as e:
                logger.error(f"Error en callback malicious IP: {e}")
    
    def _update_threat_database(self, reputation: IPReputation):
        """Actualiza ThreatDatabase con información de reputación"""
        
        try:
            # Añadir como amenaza de baja reputación
            self.threat_database.add_threat(
                source_ip=reputation.ip,
                attack_type="LOW_REPUTATION",
                confidence=1.0 - (reputation.reputation_score / 100),
                action_taken="LOGGED",
                payload=f"Score: {reputation.reputation_score}, Country: {reputation.country}"
            )
            
            # Bloquear si es muy maliciosa
            if reputation.reputation_score < 20:
                self.threat_database.block_ip(
                    ip=reputation.ip,
                    reason=f"Critical reputation: {reputation.reputation_score}/100"
                )
        
        except Exception as e:
            logger.error(f"Error actualizando ThreatDatabase: {e}")
    
    def whitelist_ip(self, ip: str, reason: str = None):
        """
        Añade IP a whitelist
        
        Args:
            ip: Dirección IP
            reason: Razón para whitelist
        """
        
        self.database.add_to_whitelist(ip, reason=reason)
        self.checker.add_to_whitelist(ip)
        
        logger.info(f"✅ IP whitelisted: {ip}")
    
    def blacklist_ip(self, ip: str, reason: str = None, severity: str = "HIGH"):
        """
        Añade IP a blacklist
        
        Args:
            ip: Dirección IP
            reason: Razón para blacklist
            severity: Severidad (LOW, MEDIUM, HIGH, CRITICAL)
        """
        
        self.database.add_to_blacklist(ip, reason=reason, severity=severity)
        self.checker.add_to_blacklist(ip)
        
        logger.info(f"🚫 IP blacklisted: {ip} ({severity})")
    
    def bulk_check(self, ips: list) -> Dict[str, IPReputation]:
        """
        Verifica múltiples IPs
        
        Args:
            ips: Lista de IPs
            
        Returns:
            Diccionario {ip: IPReputation}
        """
        
        results = {}
        
        for ip in ips:
            try:
                results[ip] = self.check_ip(ip)
            except Exception as e:
                logger.error(f"Error verificando {ip}: {e}")
        
        logger.info(f"Verificadas {len(results)} IPs en bulk")
        
        return results
    
    def get_top_malicious(self, limit: int = 10) -> list:
        """Obtiene las IPs más maliciosas"""
        return self.database.get_top_malicious_ips(limit)
    
    def get_reputation_stats(self) -> Dict:
        """Obtiene estadísticas completas del sistema"""
        
        db_stats = self.database.get_statistics()
        cache_stats = self.checker.get_cache_stats()
        
        return {
            "sentinel_stats": self.stats,
            "database_stats": db_stats,
            "cache_stats": cache_stats
        }
    
    def cleanup_and_maintain(self):
        """Ejecuta tareas de mantenimiento"""
        
        logger.info("🧹 Ejecutando mantenimiento...")
        
        # Limpiar expirados
        expired = self.database.cleanup_expired()
        
        # Aplicar decay
        decayed = self.database.decay_reputations(days_old=30, decay_amount=5)
        
        # Limpiar cache
        self.checker.clear_cache()
        
        logger.info(
            f"Mantenimiento completado: "
            f"{expired} expirados, {decayed} decayed"
        )
        
        return {
            "expired_removed": expired,
            "reputations_decayed": decayed
        }
    
    async def start_monitoring(self, interval: int = 3600):
        """
        Inicia monitoreo automático de mantenimiento
        
        Args:
            interval: Intervalo en segundos (default: 1 hora)
        """
        
        logger.info(f"🚀 Iniciando monitoreo automático (cada {interval}s)")
        
        try:
            while True:
                await asyncio.sleep(interval)
                
                # Ejecutar mantenimiento
                self.cleanup_and_maintain()
        
        except asyncio.CancelledError:
            logger.info("⏹️  Monitoreo detenido")
    
    def enrich_threat(self, ip: str) -> Dict:
        """
        Enriquece información de una amenaza con datos de reputación
        
        Args:
            ip: IP de la amenaza
            
        Returns:
            Diccionario con información enriquecida
        """
        
        reputation = self.check_ip(ip)
        
        return {
            "ip": ip,
            "reputation_score": reputation.reputation_score,
            "threat_level": reputation.threat_level,
            "country": reputation.country,
            "city": reputation.city,
            "isp": reputation.isp,
            "asn": reputation.asn,
            "is_blacklisted": reputation.is_blacklisted,
            "is_whitelisted": reputation.is_whitelisted,
            "categories": reputation.categories
        }
    
    def get_country_statistics(self) -> Dict:
        """Obtiene estadísticas por país"""
        
        stats = self.database.get_statistics()
        return stats.get('top_countries', {})
    
    def get_threat_level_distribution(self) -> Dict:
        """Obtiene distribución de threat levels"""
        
        stats = self.database.get_statistics()
        return stats.get('by_threat_level', {})
    
    def generate_report(self) -> Dict:
        """Genera reporte completo del sistema"""
        
        stats = self.get_reputation_stats()
        top_malicious = self.get_top_malicious(10)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "top_malicious_ips": [
                {
                    "ip": ip,
                    "score": score,
                    "threat_level": threat,
                    "country": country,
                    "isp": isp,
                    "checks": checks
                }
                for ip, score, threat, country, isp, checks in top_malicious
            ],
            "country_stats": self.get_country_statistics(),
            "threat_distribution": self.get_threat_level_distribution()
        }