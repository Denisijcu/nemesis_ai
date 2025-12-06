#!/usr/bin/env python3
"""
Némesis IA - Adversarial Detector
Capítulo 13: Defensa contra IA Adversaria

Detección de ataques adversariales contra modelos ML
"""

import logging
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AdversarialAttack:
    """Información de ataque adversarial detectado"""
    attack_type: str
    confidence: float
    perturbation_detected: bool
    original_prediction: str
    adversarial_prediction: str
    threat_level: str


class AdversarialDetector:
    """Detector de ataques adversariales contra ML"""
    
    # Tipos de ataques adversariales
    ATTACK_TYPES = {
        'FGSM': 'Fast Gradient Sign Method',
        'PGD': 'Projected Gradient Descent',
        'DEEPFOOL': 'DeepFool Attack',
        'CARLINI_WAGNER': 'Carlini & Wagner',
        'POISON': 'Data Poisoning',
        'BACKDOOR': 'Backdoor Attack',
        'EVASION': 'Evasion Attack'
    }
    
    def __init__(self):
        """Inicializa detector adversarial"""
        
        # Umbrales de detección
        self.thresholds = {
            'perturbation': 0.1,      # Umbral de perturbación
            'confidence_drop': 0.3,    # Caída en confianza
            'prediction_flip': True    # Detección de flip
        }
        
        # Estadísticas
        self.stats = {
            "checks": 0,
            "attacks_detected": 0,
            "evasion_attempts": 0,
            "poisoning_attempts": 0
        }
        
        logger.info("🤖 AdversarialDetector inicializado")
    
    def detect_adversarial_input(
        self,
        input_data: np.ndarray,
        model_prediction: Dict,
        reference_baseline: Optional[np.ndarray] = None
    ) -> AdversarialAttack:
        """
        Detecta si input es adversarial
        
        Args:
            input_data: Datos de entrada
            model_prediction: Predicción del modelo
            reference_baseline: Baseline de referencia (opcional)
            
        Returns:
            AdversarialAttack con detección
        """
        
        logger.info("🔍 Analizando input para ataques adversariales...")
        
        self.stats["checks"] += 1
        
        # 1. Análisis de perturbación
        perturbation_score = self._detect_perturbation(
            input_data,
            reference_baseline
        )
        
        # 2. Análisis de confianza
        confidence = model_prediction.get('confidence', 1.0)
        confidence_anomaly = self._detect_confidence_anomaly(confidence)
        
        # 3. Análisis de gradiente
        gradient_anomaly = self._detect_gradient_anomaly(input_data)
        
        # 4. Determinar si es ataque
        is_adversarial = (
            perturbation_score > self.thresholds['perturbation'] or
            confidence_anomaly or
            gradient_anomaly
        )
        
        if is_adversarial:
            self.stats["attacks_detected"] += 1
            attack_type = self._classify_attack_type(
                perturbation_score,
                confidence_anomaly,
                gradient_anomaly
            )
        else:
            attack_type = 'NONE'
        
        # Crear resultado
        attack = AdversarialAttack(
            attack_type=attack_type,
            confidence=perturbation_score,
            perturbation_detected=perturbation_score > self.thresholds['perturbation'],
            original_prediction=model_prediction.get('attack_type', 'UNKNOWN'),
            adversarial_prediction=model_prediction.get('attack_type', 'UNKNOWN'),
            threat_level='HIGH' if is_adversarial else 'LOW'
        )
        
        if is_adversarial:
            logger.warning(
                f"⚠️ Adversarial attack detected: {attack_type} "
                f"(confidence: {perturbation_score:.2f})"
            )
        else:
            logger.info("✅ Input is clean (no adversarial attack)")
        
        return attack
    
    def _detect_perturbation(
        self,
        input_data: np.ndarray,
        baseline: Optional[np.ndarray]
    ) -> float:
        """
        Detecta perturbaciones adversariales
        
        Returns:
            Score de perturbación (0-1)
        """
        
        if baseline is None:
            # Sin baseline, usar análisis estadístico
            # Detectar outliers y anomalías
            mean = np.mean(input_data)
            std = np.std(input_data)
            
            # Z-score para anomalías
            z_scores = np.abs((input_data - mean) / (std + 1e-10))
            outlier_ratio = np.sum(z_scores > 3) / len(input_data)
            
            return float(outlier_ratio)
        
        else:
            # Con baseline, calcular diferencia L2
            diff = np.linalg.norm(input_data - baseline)
            normalized_diff = diff / (np.linalg.norm(baseline) + 1e-10)
            
            return float(np.clip(normalized_diff, 0, 1))
    
    def _detect_confidence_anomaly(self, confidence: float) -> bool:
        """
        Detecta anomalías en confianza del modelo
        
        Args:
            confidence: Confianza de la predicción
            
        Returns:
            True si hay anomalía
        """
        
        # Confianza sospechosamente baja o alta
        if confidence < 0.3 or confidence > 0.999:
            return True
        
        return False
    
    def _detect_gradient_anomaly(self, input_data: np.ndarray) -> bool:
        """
        Detecta anomalías en gradientes (simplificado)
        
        Returns:
            True si hay anomalía
        """
        
        # Análisis simplificado de gradientes locales
        if len(input_data) < 2:
            return False
        
        gradients = np.diff(input_data)
        gradient_variance = np.var(gradients)
        
        # Alta varianza puede indicar perturbaciones adversariales
        return float(gradient_variance) > 1.0
    
    def _classify_attack_type(
        self,
        perturbation: float,
        confidence_anomaly: bool,
        gradient_anomaly: bool
    ) -> str:
        """Clasifica tipo de ataque adversarial"""
        
        if perturbation > 0.5:
            return 'FGSM'  # Fast Gradient Sign Method
        elif gradient_anomaly:
            return 'PGD'   # Projected Gradient Descent
        elif confidence_anomaly:
            return 'EVASION'  # Evasion attack
        else:
            return 'UNKNOWN'
    
    def detect_model_poisoning(
        self,
        training_data: List[np.ndarray],
        labels: List[int]
    ) -> Dict:
        """
        Detecta envenenamiento del modelo (data poisoning)
        
        Args:
            training_data: Datos de entrenamiento
            labels: Etiquetas
            
        Returns:
            Resultado de detección
        """
        
        logger.info("🔍 Analizando datos de entrenamiento para poisoning...")
        
        self.stats["poisoning_attempts"] += 1
        
        # 1. Detectar outliers en datos
        outliers = self._detect_outliers(training_data)
        
        # 2. Detectar etiquetas inconsistentes
        label_anomalies = self._detect_label_anomalies(training_data, labels)
        
        # 3. Calcular score de poisoning
        poisoning_score = (len(outliers) + len(label_anomalies)) / len(training_data)
        
        is_poisoned = poisoning_score > 0.05  # 5% threshold
        
        result = {
            'is_poisoned': is_poisoned,
            'poisoning_score': poisoning_score,
            'outliers_detected': len(outliers),
            'label_anomalies': len(label_anomalies),
            'total_samples': len(training_data),
            'suspicious_indices': outliers + label_anomalies
        }
        
        if is_poisoned:
            logger.warning(
                f"⚠️ Model poisoning detected: {poisoning_score*100:.1f}% "
                f"suspicious samples"
            )
        else:
            logger.info("✅ Training data appears clean")
        
        return result
    
    def _detect_outliers(self, data: List[np.ndarray]) -> List[int]:
        """Detecta outliers en datos de entrenamiento"""
        
        outliers = []
        
        # Calcular centroide
        centroid = np.mean(data, axis=0)
        
        # Calcular distancias
        for i, sample in enumerate(data):
            distance = np.linalg.norm(sample - centroid)
            
            # Si distancia es muy grande, es outlier
            if distance > 3.0:  # Threshold simplificado
                outliers.append(i)
        
        return outliers
    
    def _detect_label_anomalies(
        self,
        data: List[np.ndarray],
        labels: List[int]
    ) -> List[int]:
        """Detecta anomalías en etiquetas"""
        
        anomalies = []
        
        # Agrupar por etiqueta
        label_groups = {}
        for i, label in enumerate(labels):
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(i)
        
        # Buscar samples que están muy lejos de su grupo
        for label, indices in label_groups.items():
            if len(indices) < 2:
                continue
            
            group_data = [data[i] for i in indices]
            group_centroid = np.mean(group_data, axis=0)
            
            for idx in indices:
                distance = np.linalg.norm(data[idx] - group_centroid)
                
                if distance > 2.0:  # Threshold
                    anomalies.append(idx)
        
        return anomalies
    
    def detect_backdoor(
        self,
        input_data: np.ndarray,
        trigger_patterns: Optional[List[np.ndarray]] = None
    ) -> Dict:
        """
        Detecta backdoor triggers en input
        
        Args:
            input_data: Datos de entrada
            trigger_patterns: Patrones de trigger conocidos
            
        Returns:
            Resultado de detección
        """
        
        logger.info("🔍 Analizando input para backdoor triggers...")
        
        result = {
            'backdoor_detected': False,
            'trigger_found': False,
            'similarity_score': 0.0
        }
        
        if trigger_patterns is None:
            # Sin patrones conocidos, usar heurísticas
            # Buscar patrones repetitivos sospechosos
            pattern_score = self._detect_suspicious_patterns(input_data)
            result['similarity_score'] = pattern_score
            result['backdoor_detected'] = pattern_score > 0.8
        else:
            # Comparar con triggers conocidos
            max_similarity = 0.0
            
            for trigger in trigger_patterns:
                similarity = self._calculate_similarity(input_data, trigger)
                max_similarity = max(max_similarity, similarity)
            
            result['similarity_score'] = max_similarity
            result['trigger_found'] = max_similarity > 0.9
            result['backdoor_detected'] = result['trigger_found']
        
        if result['backdoor_detected']:
            logger.warning("⚠️ Backdoor trigger detected!")
        
        return result
    
    def _detect_suspicious_patterns(self, data: np.ndarray) -> float:
        """Detecta patrones sospechosos en datos"""
        
        # Análisis de entropía
        unique_ratio = len(np.unique(data)) / len(data)
        
        # Baja entropía = patrón repetitivo = sospechoso
        if unique_ratio < 0.1:
            return 0.9
        elif unique_ratio < 0.3:
            return 0.6
        else:
            return 0.2
    
    def _calculate_similarity(
        self,
        data1: np.ndarray,
        data2: np.ndarray
    ) -> float:
        """Calcula similitud entre dos arrays"""
        
        if len(data1) != len(data2):
            return 0.0
        
        # Similitud coseno
        dot_product = np.dot(data1, data2)
        norm1 = np.linalg.norm(data1)
        norm2 = np.linalg.norm(data2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        
        return float(np.clip(similarity, 0, 1))
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas del detector"""
        return self.stats.copy()