#!/usr/bin/env python3
"""
Némesis IA - Attacker Profiler
Capítulo 5: Honeypots Inteligentes

Perfila atacantes basándose en sus patrones de comportamiento
"""

import logging
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field
from collections import Counter

logger = logging.getLogger(__name__)


@dataclass
class AttackerProfile:
    """Perfil completo de un atacante"""
    ip: str
    first_seen: datetime
    last_seen: datetime
    
    # Estadísticas de intentos
    total_attempts: int = 0
    usernames_tried: List[str] = field(default_factory=list)
    passwords_tried: List[str] = field(default_factory=list)
    
    # Análisis de patrones
    attack_pattern: str = "UNKNOWN"  # BRUTE_FORCE, CREDENTIAL_STUFFING, DICTIONARY, etc
    sophistication_level: str = "LOW"  # LOW, MEDIUM, HIGH
    
    # Características
    common_usernames: List[tuple] = field(default_factory=list)  # [(username, count), ...]
    common_passwords: List[tuple] = field(default_factory=list)  # [(password, count), ...]
    
    # Timing
    average_attempt_interval: float = 0.0  # Segundos entre intentos
    
    # Threat level
    threat_score: float = 0.0  # 0-100
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        return {
            "ip": self.ip,
            "first_seen": self.first_seen.isoformat(),
            "last_seen": self.last_seen.isoformat(),
            "total_attempts": self.total_attempts,
            "attack_pattern": self.attack_pattern,
            "sophistication_level": self.sophistication_level,
            "threat_score": self.threat_score,
            "top_usernames": self.common_usernames[:5],
            "top_passwords": self.common_passwords[:5],
            "avg_interval": round(self.average_attempt_interval, 2)
        }


class AttackerProfiler:
    """Analizador y perfilador de atacantes"""
    
    def __init__(self):
        """Inicializa el profiler"""
        self.profiles: Dict[str, AttackerProfile] = {}
        logger.info("🔍 AttackerProfiler inicializado")
    
    def process_attempt(self, ip: str, username: str, password: str, timestamp: datetime) -> AttackerProfile:
        """
        Procesa un intento de ataque y actualiza el perfil
        
        Args:
            ip: IP del atacante
            username: Username intentado
            password: Password intentado
            timestamp: Momento del intento
            
        Returns:
            Perfil actualizado del atacante
        """
        
        # Crear perfil si no existe
        if ip not in self.profiles:
            self.profiles[ip] = AttackerProfile(
                ip=ip,
                first_seen=timestamp,
                last_seen=timestamp
            )
            logger.info(f"🆕 Nuevo atacante detectado: {ip}")
        
        profile = self.profiles[ip]
        
        # Actualizar estadísticas básicas
        profile.total_attempts += 1
        profile.last_seen = timestamp
        profile.usernames_tried.append(username)
        profile.passwords_tried.append(password)
        
        # Analizar patrón de ataque
        profile.attack_pattern = self._identify_attack_pattern(profile)
        
        # Calcular nivel de sofisticación
        profile.sophistication_level = self._calculate_sophistication(profile)
        
        # Calcular threat score
        profile.threat_score = self._calculate_threat_score(profile)
        
        # Análisis de frecuencias
        profile.common_usernames = Counter(profile.usernames_tried).most_common(10)
        profile.common_passwords = Counter(profile.passwords_tried).most_common(10)
        
        # Calcular intervalo entre intentos
        if profile.total_attempts > 1:
            time_diff = (profile.last_seen - profile.first_seen).total_seconds()
            profile.average_attempt_interval = time_diff / (profile.total_attempts - 1)
        
        logger.debug(f"📊 Perfil actualizado para {ip}: {profile.total_attempts} intentos")
        
        return profile
    
    def _identify_attack_pattern(self, profile: AttackerProfile) -> str:
        """Identifica el patrón de ataque"""
        
        unique_users = len(set(profile.usernames_tried))
        unique_passwords = len(set(profile.passwords_tried))
        total = profile.total_attempts
        
        # Brute force: Mismo usuario, muchos passwords
        if unique_users <= 2 and unique_passwords > 10:
            return "BRUTE_FORCE"
        
        # Credential stuffing: Muchos usuarios, pocos passwords comunes
        if unique_users > 10 and unique_passwords < unique_users * 0.5:
            return "CREDENTIAL_STUFFING"
        
        # Dictionary attack: Usuarios y passwords comunes
        if unique_users > 5 and unique_passwords > 5:
            common_users = ['root', 'admin', 'user', 'test', 'guest']
            if any(u in common_users for u in profile.usernames_tried[:5]):
                return "DICTIONARY_ATTACK"
        
        # Single attempt: Solo 1-2 intentos
        if total <= 2:
            return "SINGLE_ATTEMPT"
        
        # Slow brute force: Muchos intentos con intervalos largos
        if total > 5 and profile.average_attempt_interval > 30:
            return "SLOW_BRUTE_FORCE"
        
        return "UNKNOWN"
    
    def _calculate_sophistication(self, profile: AttackerProfile) -> str:
        """Calcula el nivel de sofisticación del atacante"""
        
        score = 0
        
        # Patrones avanzados
        if profile.attack_pattern in ["CREDENTIAL_STUFFING", "SLOW_BRUTE_FORCE"]:
            score += 2
        
        # Variedad de credenciales
        unique_users = len(set(profile.usernames_tried))
        unique_passwords = len(set(profile.passwords_tried))
        
        if unique_users > 20 or unique_passwords > 50:
            score += 2
        elif unique_users > 10 or unique_passwords > 20:
            score += 1
        
        # Timing (ataques lentos son más sofisticados)
        if profile.average_attempt_interval > 30:
            score += 2
        elif profile.average_attempt_interval > 10:
            score += 1
        
        # Evita credenciales obvias
        obvious = ['admin', 'root', '123456', 'password']
        non_obvious = sum(1 for p in profile.passwords_tried[:10] if p not in obvious)
        if non_obvious > 5:
            score += 1
        
        # Clasificar
        if score >= 5:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_threat_score(self, profile: AttackerProfile) -> float:
        """Calcula un threat score de 0-100"""
        
        score = 0.0
        
        # Volumen de intentos (max 40 puntos)
        score += min(profile.total_attempts * 2, 40)
        
        # Sofisticación (max 30 puntos)
        if profile.sophistication_level == "HIGH":
            score += 30
        elif profile.sophistication_level == "MEDIUM":
            score += 20
        else:
            score += 10
        
        # Persistencia (max 20 puntos)
        if profile.total_attempts > 50:
            score += 20
        elif profile.total_attempts > 20:
            score += 15
        elif profile.total_attempts > 10:
            score += 10
        else:
            score += 5
        
        # Patrón de ataque (max 10 puntos)
        if profile.attack_pattern in ["BRUTE_FORCE", "CREDENTIAL_STUFFING"]:
            score += 10
        elif profile.attack_pattern == "DICTIONARY_ATTACK":
            score += 7
        else:
            score += 3
        
        return min(score, 100.0)
    
    def get_profile(self, ip: str) -> AttackerProfile:
        """Obtiene el perfil de un atacante"""
        return self.profiles.get(ip)
    
    def get_top_attackers(self, limit: int = 10) -> List[AttackerProfile]:
        """Obtiene los atacantes más peligrosos"""
        sorted_profiles = sorted(
            self.profiles.values(),
            key=lambda p: p.threat_score,
            reverse=True
        )
        return sorted_profiles[:limit]
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas globales"""
        total_ips = len(self.profiles)
        total_attempts = sum(p.total_attempts for p in self.profiles.values())
        
        if not self.profiles:
            return {
                "total_attackers": 0,
                "total_attempts": 0,
                "avg_attempts_per_ip": 0,
                "patterns": {},
                "sophistication": {}
            }
        
        # Contar patrones
        patterns = Counter(p.attack_pattern for p in self.profiles.values())
        sophistication = Counter(p.sophistication_level for p in self.profiles.values())
        
        return {
            "total_attackers": total_ips,
            "total_attempts": total_attempts,
            "avg_attempts_per_ip": round(total_attempts / total_ips, 2),
            "patterns": dict(patterns),
            "sophistication": dict(sophistication),
            "avg_threat_score": round(
                sum(p.threat_score for p in self.profiles.values()) / total_ips,
                2
            )
        }