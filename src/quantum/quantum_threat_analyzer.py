#!/usr/bin/env python3
"""
Némesis IA - Quantum Threat Analyzer
Capítulo 7: El Colapso del RSA

Analiza y demuestra la amenaza cuántica a RSA/ECC
"""

import logging
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QuantumThreat:
    """Representa una amenaza cuántica"""
    algorithm: str  # RSA, ECC, AES, etc
    key_size: int
    currently_secure: bool
    years_until_vulnerable: int
    quantum_attack: str
    recommendation: str
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL


class QuantumThreatAnalyzer:
    """Analizador de amenazas cuánticas"""
    
    def __init__(self):
        """Inicializa el analizador"""
        
        # Timeline estimado de computadoras cuánticas
        self.quantum_timeline = {
            2024: {"qubits": 1000, "error_rate": 0.001},
            2025: {"qubits": 2000, "error_rate": 0.0005},
            2030: {"qubits": 10000, "error_rate": 0.0001},
            2035: {"qubits": 100000, "error_rate": 0.00001},
            2040: {"qubits": 1000000, "error_rate": 0.000001}
        }
        
        # Qubits necesarios para romper algoritmos
        self.breaking_requirements = {
            "RSA-1024": 2048,
            "RSA-2048": 4096,
            "RSA-4096": 8192,
            "ECC-256": 2330,
            "ECC-384": 3484,
            "AES-128": 2953,  # Grover's algorithm
            "AES-256": 6681
        }
        
        logger.info("⚛️  QuantumThreatAnalyzer inicializado")
    
    def analyze_algorithm(self, algorithm: str, key_size: int) -> QuantumThreat:
        """
        Analiza vulnerabilidad de un algoritmo a ataques cuánticos
        
        Args:
            algorithm: Nombre del algoritmo (RSA, ECC, AES)
            key_size: Tamaño de clave en bits
            
        Returns:
            QuantumThreat con análisis completo
        """
        
        algo_key = f"{algorithm.upper()}-{key_size}"
        
        # Determinar qubits necesarios
        qubits_needed = self._estimate_qubits_needed(algorithm, key_size)
        
        # Estimar años hasta vulnerabilidad
        years_until = self._estimate_years_until_broken(qubits_needed)
        
        # Determinar ataque cuántico aplicable
        quantum_attack = self._get_quantum_attack(algorithm)
        
        # Generar recomendación
        recommendation = self._get_recommendation(algorithm, key_size, years_until)
        
        # Calcular nivel de riesgo
        risk_level = self._calculate_risk_level(years_until)
        
        currently_secure = years_until > 5
        
        threat = QuantumThreat(
            algorithm=algo_key,
            key_size=key_size,
            currently_secure=currently_secure,
            years_until_vulnerable=years_until,
            quantum_attack=quantum_attack,
            recommendation=recommendation,
            risk_level=risk_level
        )
        
        logger.info(
            f"Análisis: {algo_key} - "
            f"Vulnerable en ~{years_until} años ({risk_level})"
        )
        
        return threat
    
    def _estimate_qubits_needed(self, algorithm: str, key_size: int) -> int:
        """Estima qubits necesarios para romper el algoritmo"""
        
        algo_upper = algorithm.upper()
        
        if algo_upper == "RSA":
            # Algoritmo de Shor para RSA
            # Aproximadamente 2n qubits para factorizar número de n bits
            return key_size * 2
        
        elif algo_upper == "ECC":
            # Algoritmo de Shor para ECC
            # Más eficiente que RSA
            return int(key_size * 9.1)  # Aproximación
        
        elif algo_upper == "AES":
            # Algoritmo de Grover para AES
            # Reduce efectivamente la fuerza a la mitad
            return int(key_size * 23.1)  # Aproximación para búsqueda
        
        else:
            # Estimación conservadora
            return key_size * 10
    
    def _estimate_years_until_broken(self, qubits_needed: int) -> int:
        """Estima años hasta que exista una computadora cuántica capaz"""
        
        current_year = datetime.now().year
        
        # Buscar en timeline
        for year, specs in sorted(self.quantum_timeline.items()):
            if specs["qubits"] >= qubits_needed:
                return year - current_year
        
        # Si no está en timeline, extrapolar
        # Ley de Rose: doblar qubits cada ~2 años
        last_year = max(self.quantum_timeline.keys())
        last_qubits = self.quantum_timeline[last_year]["qubits"]
        
        if qubits_needed <= last_qubits:
            return last_year - current_year
        
        # Calcular años adicionales necesarios
        years_needed = math.log2(qubits_needed / last_qubits) * 2
        total_years = (last_year - current_year) + int(years_needed)
        
        return max(0, total_years)
    
    def _get_quantum_attack(self, algorithm: str) -> str:
        """Retorna el ataque cuántico aplicable"""
        
        attacks = {
            "RSA": "Shor's Algorithm (Factorización)",
            "ECC": "Shor's Algorithm (Problema del Logaritmo Discreto)",
            "AES": "Grover's Algorithm (Búsqueda Exhaustiva Mejorada)",
            "SHA": "Grover's Algorithm (Colisiones)",
            "DSA": "Shor's Algorithm",
            "ECDSA": "Shor's Algorithm"
        }
        
        return attacks.get(algorithm.upper(), "Ataque Cuántico Genérico")
    
    def _get_recommendation(self, algorithm: str, key_size: int, years_until: int) -> str:
        """Genera recomendación de migración"""
        
        algo_upper = algorithm.upper()
        
        if years_until <= 5:
            # URGENTE
            if algo_upper in ["RSA", "ECC", "DSA", "ECDSA"]:
                return "URGENTE: Migrar a Post-Quantum Cryptography (Kyber, Dilithium)"
            else:
                return f"URGENTE: Duplicar tamaño de clave a {key_size * 2} bits"
        
        elif years_until <= 10:
            # PLANEAR MIGRACIÓN
            if algo_upper in ["RSA", "ECC"]:
                return "PLANEAR: Iniciar migración a algoritmos post-cuánticos en 2-3 años"
            else:
                return "MONITOREAR: Preparar plan de migración"
        
        else:
            # SEGURO POR AHORA
            if algo_upper in ["RSA", "ECC"]:
                return "SEGURO: Pero planear transición post-cuántica a largo plazo"
            else:
                return "SEGURO: Mantener y monitorear desarrollos cuánticos"
    
    def _calculate_risk_level(self, years_until: int) -> str:
        """Calcula nivel de riesgo"""
        
        if years_until <= 3:
            return "CRITICAL"
        elif years_until <= 7:
            return "HIGH"
        elif years_until <= 12:
            return "MEDIUM"
        else:
            return "LOW"
    
    def analyze_common_algorithms(self) -> List[QuantumThreat]:
        """Analiza algoritmos comunes en uso hoy"""
        
        common_algos = [
            ("RSA", 1024),
            ("RSA", 2048),
            ("RSA", 4096),
            ("ECC", 256),
            ("ECC", 384),
            ("AES", 128),
            ("AES", 256),
        ]
        
        threats = []
        for algo, key_size in common_algos:
            threat = self.analyze_algorithm(algo, key_size)
            threats.append(threat)
        
        return threats
    
    def generate_threat_report(self) -> Dict:
        """Genera reporte completo de amenazas cuánticas"""
        
        threats = self.analyze_common_algorithms()
        
        # Clasificar por riesgo
        by_risk = {
            "CRITICAL": [],
            "HIGH": [],
            "MEDIUM": [],
            "LOW": []
        }
        
        for threat in threats:
            by_risk[threat.risk_level].append(threat)
        
        # Calcular estadísticas
        vulnerable_soon = sum(1 for t in threats if t.years_until_vulnerable <= 10)
        currently_safe = sum(1 for t in threats if t.currently_secure)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_algorithms_analyzed": len(threats),
            "currently_safe": currently_safe,
            "vulnerable_within_10_years": vulnerable_soon,
            "threats_by_risk": {
                level: [
                    {
                        "algorithm": t.algorithm,
                        "years_until_vulnerable": t.years_until_vulnerable,
                        "quantum_attack": t.quantum_attack,
                        "recommendation": t.recommendation
                    }
                    for t in threats_list
                ]
                for level, threats_list in by_risk.items()
            },
            "quantum_timeline": self.quantum_timeline,
            "summary": self._generate_summary(threats)
        }
    
    def _generate_summary(self, threats: List[QuantumThreat]) -> str:
        """Genera resumen ejecutivo"""
        
        critical = sum(1 for t in threats if t.risk_level == "CRITICAL")
        high = sum(1 for t in threats if t.risk_level == "HIGH")
        
        if critical > 0:
            return (
                f"⚠️ ALERTA CRÍTICA: {critical} algoritmos en riesgo inmediato. "
                f"Migración a Post-Quantum Cryptography URGENTE."
            )
        elif high > 0:
            return (
                f"⚠️ ADVERTENCIA: {high} algoritmos vulnerables en <10 años. "
                f"Planear migración a PQC pronto."
            )
        else:
            return (
                "✅ Algoritmos actuales seguros por ahora, pero monitorear "
                "desarrollo de computación cuántica."
            )
    
    def calculate_data_lifetime_risk(self, data_sensitivity_years: int) -> Dict:
        """
        Calcula riesgo para datos que deben permanecer confidenciales
        
        Args:
            data_sensitivity_years: Años que los datos deben estar protegidos
            
        Returns:
            Análisis de riesgo
        """
        
        # "Harvest Now, Decrypt Later" attack
        # Atacantes pueden guardar datos cifrados ahora
        # y descifrarlos cuando tengan computadora cuántica
        
        threats = self.analyze_common_algorithms()
        
        at_risk_algorithms = []
        safe_algorithms = []
        
        for threat in threats:
            if threat.years_until_vulnerable < data_sensitivity_years:
                at_risk_algorithms.append({
                    "algorithm": threat.algorithm,
                    "years_until_vulnerable": threat.years_until_vulnerable,
                    "data_will_be_exposed_in": threat.years_until_vulnerable
                })
            else:
                safe_algorithms.append(threat.algorithm)
        
        risk_level = "CRITICAL" if at_risk_algorithms else "LOW"
        
        return {
            "data_sensitivity_years": data_sensitivity_years,
            "risk_level": risk_level,
            "at_risk_algorithms": at_risk_algorithms,
            "safe_algorithms": safe_algorithms,
            "recommendation": (
                "Usar Post-Quantum Cryptography AHORA para datos sensibles a largo plazo"
                if at_risk_algorithms else
                "Algoritmos actuales adecuados para esta sensibilidad"
            )
        }
    
    def get_migration_priority(self) -> List[Tuple[str, str]]:
        """Retorna lista priorizada de migraciones necesarias"""
        
        threats = self.analyze_common_algorithms()
        
        # Ordenar por años hasta vulnerabilidad
        sorted_threats = sorted(threats, key=lambda t: t.years_until_vulnerable)
        
        priority_list = []
        for threat in sorted_threats:
            if not threat.currently_secure or threat.years_until_vulnerable <= 10:
                priority = "URGENT" if threat.years_until_vulnerable <= 5 else "HIGH"
                priority_list.append((threat.algorithm, priority))
        
        return priority_list