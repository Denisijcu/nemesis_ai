#!/usr/bin/env python3
"""
Némesis IA - Autonomous Cyber Defense Agent
Capítulo 1: El Agente Némesis

Sistema autónomo de detección y respuesta a amenazas cibernéticas
usando Machine Learning y el ciclo O.A.S. (Observe, Analyze, Sentence).

Original work Copyright (C) 2025 Némesis AI Project Contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import asyncio
import logging
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import joblib

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ThreatEvent:
    """Representa un evento de amenaza detectado"""
    timestamp: datetime
    source_ip: str
    payload: str
    log_line: str
    severity: str = "UNKNOWN"


@dataclass
class ThreatVerdict:
    """Veredicto sobre una amenaza"""
    is_malicious: bool
    confidence: float
    attack_type: str
    timestamp: datetime
    recommended_action: str


class NemesisAgent:
    """
    Agente autónomo de defensa cibernética
    
    Implementa el ciclo O.A.S.:
    - Observe: Monitorea logs en tiempo real
    - Analyze: Analiza amenazas con ML
    - Sentence: Ejecuta acciones defensivas
    """
    
    def __init__(
        self,
        model_path: str = "models/nemesis_brain.joblib",
        threshold: float = 0.9,
        network_interface: str = "eth0"
    ) -> None:
        """
        Inicializa el Agente Némesis
        
        Args:
            model_path: Ruta al modelo ML entrenado
            threshold: Umbral de confianza para detección
            network_interface: Interface de red a monitorear
        """
        self.model_path = model_path
        self.threshold = threshold
        self._network_interface = network_interface
        
        # Estado interno
        self._ai_brain: Optional[object] = None
        self._is_running: bool = False
        self._threats_detected: int = 0
        self._whitelist_ips: set = {"127.0.0.1", "::1"}
        
        logger.info(
            f"Némesis Agent initialized on interface {network_interface} "
            f"with threshold {threshold}"
        )
    
    async def start(self) -> None:
        """Inicia el agente autónomo"""
        logger.info("🚀 Iniciando Agente Némesis...")
        
        # Cargar modelo ML
        self._load_ai_brain()
        
        self._is_running = True
        
        logger.info("✅ Agente Némesis activo y vigilante")
        
        # Iniciar loops asíncronos
        await asyncio.gather(
            self._observe_loop(),
            self._health_check_loop()
        )
    
    async def stop(self) -> None:
        """Detiene el agente"""
        logger.info("⏸️  Deteniendo Agente Némesis...")
        self._is_running = False
        await asyncio.sleep(1)
        logger.info("✅ Agente detenido")
    
    def _load_ai_brain(self) -> None:
        """Carga el modelo de Machine Learning"""
        logger.info(f"🧠 Cargando cerebro AI desde {self.model_path}...")
        
        model_file = Path(self.model_path)
        
        if model_file.exists():
            try:
                self._ai_brain = joblib.load(self.model_path)
                logger.info("✅ Cerebro AI cargado")
            except Exception as e:
                logger.warning(f"⚠️  Error cargando modelo: {e}")
                logger.info("📋 Usando detección basada en reglas")
                self._ai_brain = None
        else:
            logger.warning(f"⚠️  Modelo no encontrado en {self.model_path}")
            logger.info("📋 Usando detección basada en reglas")
            self._ai_brain = None
    
    async def _observe_loop(self) -> None:
        """Loop principal de observación de logs"""
        logger.info("👁️  Iniciando observación de logs...")
        
        while self._is_running:
            # En producción, aquí se leería de archivos de log o syslog
            # Por ahora, solo mantiene el loop activo
            await asyncio.sleep(1)
    
    async def _health_check_loop(self) -> None:
        """Loop de health check cada 5 minutos"""
        while self._is_running:
            await asyncio.sleep(300)  # 5 minutos
            logger.info(
                f"💚 Health check - Amenazas detectadas: {self._threats_detected}"
            )
    
    async def process_log_line(self, log_line: str) -> Optional[ThreatVerdict]:
        """
        Procesa una línea de log y ejecuta el ciclo O.A.S.
        
        Args:
            log_line: Línea de log a analizar
            
        Returns:
            ThreatVerdict si se detecta amenaza, None si es legítimo
        """
        # OBSERVE: Parsear log
        event = self._parse_log(log_line)
        
        if not event:
            return None
        
        # Verificar whitelist
        if event.source_ip in self._whitelist_ips:
            return None
        
        # ANALYZE: Analizar amenaza
        verdict = await self._analyze_threat(event)
        
        if verdict and verdict.is_malicious:
            self._threats_detected += 1
            
            # Log de amenaza detectada
            logger.warning(
                f"🚨 AMENAZA DETECTADA: {verdict.attack_type} "
                f"desde {event.source_ip} (confianza: {verdict.confidence:.2%})"
            )
            
            # SENTENCE: Ejecutar acción defensiva
            await self._execute_sentence(verdict, event)
        
        return verdict
    
    def _parse_log(self, log_line: str) -> Optional[ThreatEvent]:
        """
        Parsea una línea de log tipo Apache/Nginx
        
        Formato esperado:
        IP - - [timestamp] "METHOD /path?query HTTP/1.1" status
        
        Args:
            log_line: Línea de log
            
        Returns:
            ThreatEvent o None si no se puede parsear
        """
        try:
            # Extraer IP (primer campo)
            parts = log_line.split()
            if len(parts) < 2:
                return None
            
            source_ip = parts[0]
            
            # Extraer request (entre comillas)
            if '"' not in log_line:
                return None
            
            request_start = log_line.index('"') + 1
            request_end = log_line.index('"', request_start)
            request = log_line[request_start:request_end]
            
            # Crear evento
            event = ThreatEvent(
                timestamp=datetime.now(),
                source_ip=source_ip,
                payload=request,
                log_line=log_line
            )
            
            return event
            
        except Exception as e:
            logger.debug(f"Error parseando log: {e}")
            return None
    
    async def _analyze_threat(self, event: ThreatEvent) -> ThreatVerdict:
        """
        Analiza un evento usando ML o reglas
        
        Args:
            event: Evento a analizar
            
        Returns:
            ThreatVerdict con el resultado del análisis
        """
        # Si hay modelo ML, usarlo
        if self._ai_brain is not None:
            return await self._ml_detection(event)
        
        # Fallback a detección basada en reglas
        return self._rule_based_detection(event)
    
    async def _ml_detection(self, event: ThreatEvent) -> ThreatVerdict:
        """
        Detección usando Machine Learning
        
        Args:
            event: Evento a analizar
            
        Returns:
            ThreatVerdict basado en predicción ML
        """
        try:
            # Extraer features
            features = self._extract_features(event)
            
            # Predicción
            prediction = self._ai_brain.predict([features])[0]
            probability = self._ai_brain.predict_proba([features])[0]
            
            # Interpretar resultado
            is_malicious = (prediction == 1)
            confidence = probability[1] if is_malicious else probability[0]
            
            # Identificar tipo de ataque si es malicioso
            if is_malicious:
                attack_type = self._identify_attack_type(event)
                action = "BLOCK" if confidence >= self.threshold else "MONITOR"
            else:
                attack_type = "BENIGN"
                action = "ALLOW"
            
            return ThreatVerdict(
                is_malicious=is_malicious,
                confidence=confidence,
                attack_type=attack_type,
                timestamp=datetime.now(),
                recommended_action=action
            )
            
        except Exception as e:
            logger.error(f"Error en ML detection: {e}")
            return self._rule_based_detection(event)
    
    def _extract_features(self, event: ThreatEvent) -> List[float]:
        """
        Extrae features del evento para ML
        
        Args:
            event: Evento a analizar
            
        Returns:
            Lista de features numéricas
        """
        payload = event.payload
        
        # Feature 1: Longitud
        length = len(payload)
        
        # Feature 2: Ratio de caracteres especiales
        special_chars = "'\"<>;()[]{}|&$`\\"
        special_count = sum(c in special_chars for c in payload)
        special_ratio = special_count / max(length, 1)
        
        # Feature 3: Entropía de Shannon
        entropy = self._calculate_entropy(payload)
        
        return [length, special_ratio, entropy]
    
    def _calculate_entropy(self, text: str) -> float:
        """Calcula entropía de Shannon"""
        if not text:
            return 0.0
        
        counts = Counter(text)
        length = len(text)
        
        entropy = -sum(
            (count / length) * math.log2(count / length)
            for count in counts.values()
        )
        
        return entropy
    
    def _identify_attack_type(self, event: ThreatEvent) -> str:
        """
        Identifica el tipo de ataque basado en el payload
        
        Args:
            event: Evento de amenaza
            
        Returns:
            Tipo de ataque identificado
        """
        payload = event.payload.lower()
        
        # SQL Injection patterns
        sql_patterns = ["'", "or", "union", "select", "insert", "drop", "--", ";--"]
        if any(pattern in payload for pattern in sql_patterns):
            return "SQL_INJECTION"
        
        # XSS patterns
        xss_patterns = ["<script", "javascript:", "onerror", "onload"]
        if any(pattern in payload for pattern in xss_patterns):
            return "XSS"
        
        # Path traversal
        if "../" in event.payload or "..\\" in event.payload:
            return "PATH_TRAVERSAL"
        
        # Command injection
        cmd_chars = ["|", "&", ";", "`", "$"]
        if any(c in event.payload for c in cmd_chars):
            return "COMMAND_INJECTION"
        
        return "UNKNOWN"
    
    def _rule_based_detection(self, event: ThreatEvent) -> ThreatVerdict:
        """
        Detección basada en reglas (fallback sin ML)
        
        Args:
            event: Evento a analizar
            
        Returns:
            ThreatVerdict basado en reglas
        """
        payload = event.payload.lower()
        
        # Detectar patrones de ataque
        attack_type = self._identify_attack_type(event)
        
        is_malicious = (attack_type != "UNKNOWN")
        confidence = 0.8 if is_malicious else 1.0
        action = "BLOCK" if is_malicious else "ALLOW"
        
        return ThreatVerdict(
            is_malicious=is_malicious,
            confidence=confidence,
            attack_type=attack_type if is_malicious else "BENIGN",
            timestamp=datetime.now(),
            recommended_action=action
        )
    
    async def _execute_sentence(
        self, 
        verdict: ThreatVerdict, 
        event: ThreatEvent
    ) -> None:
        """
        Ejecuta la acción defensiva (SENTENCE)
        
        Args:
            verdict: Veredicto de la amenaza
            event: Evento que causó la amenaza
        """
        if verdict.recommended_action == "BLOCK":
            await self._block_ip(event.source_ip)
        elif verdict.recommended_action == "MONITOR":
            logger.warning(
                f"⚠️  Monitoreando IP sospechosa: {event.source_ip}"
            )
        
        # Notificar a otros módulos
        await self._notify_modules(verdict, event)
    
    async def _block_ip(self, ip: str) -> None:
        """
        Bloquea una IP maliciosa
        
        Args:
            ip: Dirección IP a bloquear
        """
        logger.warning(f"🚫 Bloqueando IP: {ip}")
        
        # En producción, aquí se ejecutaría:
        # subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        
        # Por ahora, solo logging
        logger.info(f"✅ IP {ip} añadida a lista negra")
    
    async def _notify_modules(
        self, 
        verdict: ThreatVerdict, 
        event: ThreatEvent
    ) -> None:
        """
        Notifica a módulos externos (reporting, P2P, blockchain)
        
        Args:
            verdict: Veredicto de la amenaza
            event: Evento que causó la amenaza
        """
        # Placeholder para integración futura con:
        # - Módulo de reporting (Capítulos 10-12)
        # - Red P2P (Capítulo 13)
        # - Blockchain (Capítulo 9)
        pass
    
    def add_to_whitelist(self, ip: str) -> None:
        """
        Añade una IP a la whitelist
        
        Args:
            ip: IP a añadir
        """
        self._whitelist_ips.add(ip)
        logger.info(f"✅ IP {ip} añadida a whitelist")


async def main():
    """Función principal para ejecutar el agente"""
    agent = NemesisAgent()
    
    try:
        await agent.start()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Interrupción detectada")
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())