#!/usr/bin/env python3
"""
Némesis IA - Quantum Education
Capítulo 7: El Colapso del RSA

Sistema educativo sobre la amenaza cuántica con visualizaciones
"""

import logging
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QuantumMilestone:
    """Representa un hito en computación cuántica"""
    year: int
    event: str
    qubits: int
    organization: str
    impact: str
    cryptographic_threat_level: str


class QuantumEducation:
    """Sistema educativo sobre amenazas cuánticas"""
    
    def __init__(self):
        """Inicializa el sistema educativo"""
        
        # Timeline histórico y proyectado
        self.timeline = self._build_timeline()
        
        # Conceptos clave
        self.key_concepts = self._build_key_concepts()
        
        logger.info("📚 QuantumEducation inicializado")
    
    def _build_timeline(self) -> List[QuantumMilestone]:
        """Construye timeline de computación cuántica"""
        
        return [
            # Historia
            QuantumMilestone(
                year=1994,
                event="Peter Shor descubre algoritmo de Shor",
                qubits=0,
                organization="MIT",
                impact="Demostró que RSA es vulnerable a computadoras cuánticas",
                cryptographic_threat_level="THEORETICAL"
            ),
            QuantumMilestone(
                year=1996,
                event="Lov Grover descubre algoritmo de Grover",
                qubits=0,
                organization="Bell Labs",
                impact="Demostró vulnerabilidad de cifrado simétrico",
                cryptographic_threat_level="THEORETICAL"
            ),
            QuantumMilestone(
                year=2001,
                event="Primera factorización cuántica (15 = 3 × 5)",
                qubits=7,
                organization="IBM",
                impact="Prueba de concepto de Shor",
                cryptographic_threat_level="PROOF_OF_CONCEPT"
            ),
            QuantumMilestone(
                year=2016,
                event="IBM lanza computadora cuántica en la nube",
                qubits=5,
                organization="IBM",
                impact="Acceso público a computación cuántica",
                cryptographic_threat_level="LOW"
            ),
            QuantumMilestone(
                year=2019,
                event="Google alcanza 'Quantum Supremacy'",
                qubits=53,
                organization="Google",
                impact="Cálculo imposible para computadoras clásicas",
                cryptographic_threat_level="LOW"
            ),
            QuantumMilestone(
                year=2021,
                event="IBM Quantum Eagle",
                qubits=127,
                organization="IBM",
                impact="Primera computadora >100 qubits",
                cryptographic_threat_level="MEDIUM"
            ),
            QuantumMilestone(
                year=2023,
                event="IBM Quantum Condor",
                qubits=1121,
                organization="IBM",
                impact="Primera computadora >1000 qubits",
                cryptographic_threat_level="MEDIUM"
            ),
            QuantumMilestone(
                year=2024,
                event="Atom Computing - 1000+ qubits",
                qubits=1180,
                organization="Atom Computing",
                impact="Átomos neutros como qubits",
                cryptographic_threat_level="MEDIUM"
            ),
            
            # Proyecciones futuras
            QuantumMilestone(
                year=2025,
                event="[PROYECCIÓN] ~2000 qubits lógicos",
                qubits=2000,
                organization="Multiple",
                impact="Puede romper RSA-1024",
                cryptographic_threat_level="HIGH"
            ),
            QuantumMilestone(
                year=2030,
                event="[PROYECCIÓN] ~10,000 qubits lógicos",
                qubits=10000,
                organization="Multiple",
                impact="Puede romper RSA-2048 en días",
                cryptographic_threat_level="CRITICAL"
            ),
            QuantumMilestone(
                year=2033,
                event="[PROYECCIÓN] Computadoras cuánticas tolerantes a fallos",
                qubits=20000,
                organization="Multiple",
                impact="RSA-4096 vulnerable en horas",
                cryptographic_threat_level="CRITICAL"
            ),
            QuantumMilestone(
                year=2035,
                event="[PROYECCIÓN] Criptografía clásica obsoleta",
                qubits=50000,
                organization="Multiple",
                impact="Toda criptografía pre-cuántica vulnerable",
                cryptographic_threat_level="CRITICAL"
            ),
        ]
    
    def _build_key_concepts(self) -> Dict[str, Dict]:
        """Construye diccionario de conceptos clave"""
        
        return {
            "superposition": {
                "name": "Superposición Cuántica",
                "simple_explanation": "Un qubit puede estar en 0 Y 1 al mismo tiempo",
                "detailed_explanation": (
                    "A diferencia de los bits clásicos que son 0 o 1, "
                    "los qubits existen en una superposición de ambos estados "
                    "hasta que se miden. Esto permite probar múltiples soluciones "
                    "simultáneamente."
                ),
                "cryptographic_impact": (
                    "Permite buscar factores de números grandes en paralelo, "
                    "rompiendo la base de seguridad de RSA."
                )
            },
            
            "entanglement": {
                "name": "Entrelazamiento Cuántico",
                "simple_explanation": "Qubits conectados que afectan instantáneamente entre sí",
                "detailed_explanation": (
                    "Cuando dos qubits están entrelazados, el estado de uno "
                    "afecta instantáneamente al otro, sin importar la distancia. "
                    "Einstein lo llamó 'acción fantasmagórica a distancia'."
                ),
                "cryptographic_impact": (
                    "Permite crear estados correlacionados que aceleran "
                    "algoritmos como Shor."
                )
            },
            
            "shor_algorithm": {
                "name": "Algoritmo de Shor",
                "simple_explanation": "Método cuántico para factorizar números grandes rápidamente",
                "detailed_explanation": (
                    "Desarrollado por Peter Shor en 1994, encuentra los factores "
                    "primos de un número en tiempo polinomial O(n³). Un problema "
                    "que tomaría millones de años clásicamente se resuelve en horas."
                ),
                "cryptographic_impact": (
                    "ROMPE completamente RSA, ECC, DSA, y todos los sistemas "
                    "basados en factorización o logaritmo discreto."
                )
            },
            
            "grover_algorithm": {
                "name": "Algoritmo de Grover",
                "simple_explanation": "Búsqueda cuántica que reduce la fuerza de cifrado simétrico",
                "detailed_explanation": (
                    "Desarrollado por Lov Grover en 1996, acelera la búsqueda "
                    "en bases de datos no ordenadas. Reduce la complejidad de "
                    "O(N) a O(√N)."
                ),
                "cryptographic_impact": (
                    "Reduce efectivamente la seguridad de AES-128 a AES-64. "
                    "Solución: doblar el tamaño de claves (AES-256 → 128 bits efectivos)."
                )
            },
            
            "quantum_error_correction": {
                "name": "Corrección de Errores Cuánticos",
                "simple_explanation": "Técnicas para hacer qubits más estables y confiables",
                "detailed_explanation": (
                    "Los qubits son extremadamente frágiles y pierden coherencia "
                    "rápidamente. La corrección de errores usa múltiples qubits "
                    "físicos para crear un qubit lógico confiable."
                ),
                "cryptographic_impact": (
                    "El factor limitante actual. Cuando se logre corrección "
                    "de errores efectiva (~2030), RSA será vulnerable."
                )
            },
            
            "harvest_now_decrypt_later": {
                "name": "Cosechar Ahora, Descifrar Después",
                "simple_explanation": "Atacantes guardan datos cifrados para descifrarlos en el futuro",
                "detailed_explanation": (
                    "Adversarios capturan datos cifrados HOY y los almacenan. "
                    "Cuando tengan computadoras cuánticas (2030-2035), descifran "
                    "todo retroactivamente."
                ),
                "cryptographic_impact": (
                    "Datos sensibles a largo plazo (médicos, gubernamentales) "
                    "deben usar PQC AHORA, aunque las QC no existan todavía."
                )
            },
            
            "post_quantum_cryptography": {
                "name": "Criptografía Post-Cuántica (PQC)",
                "simple_explanation": "Algoritmos resistentes a computadoras cuánticas",
                "detailed_explanation": (
                    "Algoritmos matemáticos que NO se pueden romper eficientemente "
                    "con computadoras cuánticas. NIST seleccionó Kyber (KEM) y "
                    "Dilithium (firmas) como estándares en 2022."
                ),
                "cryptographic_impact": (
                    "La SOLUCIÓN. Sistemas deben migrar a PQC antes de 2030 "
                    "para protegerse."
                )
            },
        }
    
    def explain_concept(self, concept_key: str) -> str:
        """
        Explica un concepto clave de forma educativa
        
        Args:
            concept_key: Clave del concepto
            
        Returns:
            Explicación formateada
        """
        
        if concept_key not in self.key_concepts:
            return f"Concepto '{concept_key}' no encontrado"
        
        concept = self.key_concepts[concept_key]
        
        explanation = f"""
╔══════════════════════════════════════════════════════════════════╗
║ {concept['name'].center(64)} ║
╚══════════════════════════════════════════════════════════════════╝

📘 EXPLICACIÓN SIMPLE:
   {concept['simple_explanation']}

📚 EXPLICACIÓN DETALLADA:
   {concept['detailed_explanation']}

🔐 IMPACTO CRIPTOGRÁFICO:
   {concept['cryptographic_impact']}

"""
        return explanation
    
    def show_timeline(self, start_year: int = 1994, end_year: int = 2035) -> str:
        """
        Muestra timeline de computación cuántica
        
        Args:
            start_year: Año inicial
            end_year: Año final
            
        Returns:
            Timeline formateado
        """
        
        output = "\n" + "="*70 + "\n"
        output += "TIMELINE DE COMPUTACIÓN CUÁNTICA Y AMENAZA CRIPTOGRÁFICA\n"
        output += "="*70 + "\n\n"
        
        filtered_timeline = [
            m for m in self.timeline 
            if start_year <= m.year <= end_year
        ]
        
        for milestone in filtered_timeline:
            threat_emoji = {
                "THEORETICAL": "📖",
                "PROOF_OF_CONCEPT": "🧪",
                "LOW": "🟢",
                "MEDIUM": "🟡",
                "HIGH": "🟠",
                "CRITICAL": "🔴"
            }.get(milestone.cryptographic_threat_level, "⚪")
            
            output += f"{threat_emoji} {milestone.year} - {milestone.event}\n"
            output += f"   Qubits: {milestone.qubits:,}\n"
            output += f"   Org:    {milestone.organization}\n"
            output += f"   Impact: {milestone.impact}\n"
            output += f"   Threat: {milestone.cryptographic_threat_level}\n"
            output += "\n"
        
        return output
    
    def get_current_status(self) -> Dict:
        """Obtiene estado actual de la amenaza cuántica"""
        
        current_year = datetime.now().year
        
        # Encontrar milestone más reciente
        past_milestones = [m for m in self.timeline if m.year <= current_year]
        latest = max(past_milestones, key=lambda m: m.year) if past_milestones else None
        
        # Encontrar próximo milestone crítico
        future_critical = [
            m for m in self.timeline 
            if m.year > current_year and m.cryptographic_threat_level == "CRITICAL"
        ]
        next_critical = min(future_critical, key=lambda m: m.year) if future_critical else None
        
        return {
            "current_year": current_year,
            "latest_milestone": {
                "year": latest.year,
                "event": latest.event,
                "qubits": latest.qubits,
                "threat_level": latest.cryptographic_threat_level
            } if latest else None,
            "years_until_critical": next_critical.year - current_year if next_critical else None,
            "next_critical_event": next_critical.event if next_critical else None,
            "recommendation": self._get_current_recommendation(current_year, next_critical)
        }
    
    def _get_current_recommendation(self, current_year: int, next_critical) -> str:
        """Genera recomendación basada en estado actual"""
        
        if not next_critical:
            return "Monitorear desarrollos en computación cuántica"
        
        years_until = next_critical.year - current_year
        
        if years_until <= 3:
            return "🚨 CRÍTICO: Migración a PQC debe ser INMEDIATA"
        elif years_until <= 5:
            return "⚠️ URGENTE: Iniciar migración a PQC en los próximos 6-12 meses"
        elif years_until <= 10:
            return "📋 PLANEAR: Desarrollar roadmap de migración a PQC ahora"
        else:
            return "📊 MONITOREAR: Preparar estrategia de migración a largo plazo"
    
    def generate_executive_summary(self) -> str:
        """Genera resumen ejecutivo sobre la amenaza cuántica"""
        
        status = self.get_current_status()
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════╗
║          RESUMEN EJECUTIVO: AMENAZA CUÁNTICA A RSA               ║
╚══════════════════════════════════════════════════════════════════╝

📅 ESTADO ACTUAL ({status['current_year']}):

   Último Hito:
   • {status['latest_milestone']['event']}
   • Qubits disponibles: {status['latest_milestone']['qubits']:,}
   • Nivel de amenaza: {status['latest_milestone']['threat_level']}

⚠️ PRÓXIMO HITO CRÍTICO:

   • Evento: {status['next_critical_event']}
   • Tiempo restante: ~{status['years_until_critical']} años
   
🎯 RECOMENDACIÓN:

   {status['recommendation']}

📊 DATOS CLAVE:

   • RSA-2048 (estándar actual): Vulnerable en ~{status['years_until_critical']} años
   • Datos con vida útil >10 años: USAR PQC AHORA
   • Ataque "Harvest Now, Decrypt Later": EN CURSO
   
🛡️ SOLUCIÓN:

   Migrar a Post-Quantum Cryptography:
   • Kyber (Key Encapsulation) - Estándar NIST 2022
   • Dilithium (Digital Signatures) - Estándar NIST 2022
   
   Timeline de migración sugerido:
   • 2024-2025: Evaluación y pruebas piloto
   • 2025-2027: Implementación gradual
   • 2027-2030: Migración completa
   
═══════════════════════════════════════════════════════════════════

⚠️ LA AMENAZA ES REAL. LA ACCIÓN ES NECESARIA.

═══════════════════════════════════════════════════════════════════
"""
        return summary
    
    def quiz_user(self) -> List[Dict]:
        """Genera preguntas de quiz educativo"""
        
        return [
            {
                "question": "¿Qué algoritmo cuántico rompe RSA?",
                "options": ["Grover", "Shor", "Deutsch", "Simon"],
                "correct": "Shor",
                "explanation": "El algoritmo de Shor factoriza números en tiempo polinomial, rompiendo RSA."
            },
            {
                "question": "¿Cuántos qubits aproximadamente se necesitan para romper RSA-2048?",
                "options": ["100", "500", "4000", "100000"],
                "correct": "4000",
                "explanation": "Se estiman ~4000 qubits lógicos estables para factorizar RSA-2048 en tiempo razonable."
            },
            {
                "question": "¿Qué es 'Harvest Now, Decrypt Later'?",
                "options": [
                    "Técnica de optimización",
                    "Guardar datos cifrados para descifrarlos cuando existan QC",
                    "Método de backup",
                    "Algoritmo de compresión"
                ],
                "correct": "Guardar datos cifrados para descifrarlos cuando existan QC",
                "explanation": "Adversarios capturan datos HOY para descifrarlos cuando tengan computadoras cuánticas."
            },
            {
                "question": "¿Cuál es el estándar NIST para Key Encapsulation post-cuántico?",
                "options": ["RSA", "Kyber", "Dilithium", "AES"],
                "correct": "Kyber",
                "explanation": "Kyber fue seleccionado por NIST en 2022 como estándar para KEM post-cuántico."
            },
            {
                "question": "¿Para cuándo se estima que RSA-2048 será vulnerable?",
                "options": ["2025", "2030", "2050", "2100"],
                "correct": "2030",
                "explanation": "Se estima que computadoras cuánticas suficientemente poderosas existirán alrededor de 2030-2035."
            }
        ]