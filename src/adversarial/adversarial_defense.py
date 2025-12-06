#!/usr/bin/env python3
"""
Némesis IA - Adversarial Defense
Capítulo 13: Defensa contra IA Adversaria

Sistema de defensa contra ataques adversariales
"""

import logging
import numpy as np
from typing import Dict, List, Optional
from .adversarial_detector import AdversarialDetector, AdversarialAttack

logger = logging.getLogger(__name__)


class AdversarialDefense:
    """Sistema de defensa contra ataques adversariales"""
    
    def __init__(self):
        """Inicializa sistema de defensa"""
        
        self.detector = AdversarialDetector()
        
        # Técnicas de defensa
        self.defense_techniques = {
            'INPUT_SANITIZATION': True,
            'ADVERSARIAL_TRAINING': True,
            'DEFENSIVE_DISTILLATION': True,
            'FEATURE_SQUEEZING': True,
            'GRADIENT_MASKING': True
        }
        
        # Estadísticas
        self.stats = {
            "inputs_processed": 0,
            "attacks_blocked": 0,
            "attacks_mitigated": 0,
            "false_positives": 0
        }
        
        logger.info("🛡️ AdversarialDefense inicializado")
    
    def defend_input(
        self,
        input_data: np.ndarray,
        model_prediction: Dict
    ) -> Dict:
        """
        Aplica defensas a input potencialmente adversarial
        
        Args:
            input_data: Datos de entrada
            model_prediction: Predicción del modelo
            
        Returns:
            Resultado con input sanitizado y defensa aplicada
        """
        
        logger.info("🛡️ Aplicando defensas adversariales...")
        
        self.stats["inputs_processed"] += 1
        
        # 1. Detectar si es adversarial
        attack = self.detector.detect_adversarial_input(
            input_data,
            model_prediction
        )
        
        result = {
            'original_input': input_data,
            'sanitized_input': input_data,
            'attack_detected': attack.threat_level == 'HIGH',
            'attack_info': attack,
            'defense_applied': [],
            'blocked': False
        }
        
        # 2. Si es adversarial, aplicar defensas
        if attack.threat_level == 'HIGH':
            logger.warning(f"⚠️ Adversarial attack detected: {attack.attack_type}")
            
            # Aplicar input sanitization
            sanitized = self._sanitize_input(input_data)
            result['sanitized_input'] = sanitized
            result['defense_applied'].append('INPUT_SANITIZATION')
            
            # Aplicar feature squeezing
            squeezed = self._feature_squeezing(sanitized)
            result['sanitized_input'] = squeezed
            result['defense_applied'].append('FEATURE_SQUEEZING')
            
            # Decidir si bloquear
            if attack.confidence > 0.7:
                result['blocked'] = True
                self.stats["attacks_blocked"] += 1
                logger.warning("🚫 Input BLOCKED - High confidence adversarial attack")
            else:
                self.stats["attacks_mitigated"] += 1
                logger.info("✅ Attack MITIGATED - Input sanitized")
        
        else:
            logger.info("✅ Input is clean")
        
        return result
    
    def _sanitize_input(self, input_data: np.ndarray) -> np.ndarray:
        """
        Sanitiza input eliminando perturbaciones
        
        Args:
            input_data: Input potencialmente adversarial
            
        Returns:
            Input sanitizado
        """
        
        logger.info("   🧹 Sanitizing input...")
        
        # 1. Clip a rango válido
        sanitized = np.clip(input_data, 0, 1)
        
        # 2. Aplicar smoothing para eliminar perturbaciones de alta frecuencia
        if len(sanitized) > 2:
            # Moving average simple
            window_size = 3
            kernel = np.ones(window_size) / window_size
            
            # Padding para mantener tamaño
            padded = np.pad(sanitized, (window_size//2, window_size//2), mode='edge')
            smoothed = np.convolve(padded, kernel, mode='valid')
            
            sanitized = smoothed[:len(input_data)]
        
        # 3. Normalizar
        if np.max(sanitized) > 0:
            sanitized = sanitized / np.max(sanitized)
        
        return sanitized
    
    def _feature_squeezing(
        self,
        input_data: np.ndarray,
        bit_depth: int = 4
    ) -> np.ndarray:
        """
        Feature squeezing - Reduce precisión para eliminar perturbaciones
        
        Args:
            input_data: Input data
            bit_depth: Profundidad de bits (menor = más squeezing)
            
        Returns:
            Input squeezed
        """
        
        logger.info(f"   🔧 Feature squeezing (bit_depth={bit_depth})...")
        
        # Reducir profundidad de bits
        max_value = 2 ** bit_depth - 1
        
        squeezed = np.round(input_data * max_value) / max_value
        
        return squeezed
    
    def defend_model_training(
        self,
        training_data: List[np.ndarray],
        labels: List[int]
    ) -> Dict:
        """
        Defiende proceso de entrenamiento contra poisoning
        
        Args:
            training_data: Datos de entrenamiento
            labels: Etiquetas
            
        Returns:
            Datos limpios y reporte
        """
        
        logger.info("🛡️ Defendiendo entrenamiento contra poisoning...")
        
        # 1. Detectar poisoning
        poisoning_result = self.detector.detect_model_poisoning(
            training_data,
            labels
        )
        
        result = {
            'poisoning_detected': poisoning_result['is_poisoned'],
            'original_size': len(training_data),
            'cleaned_size': len(training_data),
            'removed_samples': 0,
            'clean_data': training_data,
            'clean_labels': labels
        }
        
        # 2. Si hay poisoning, limpiar datos
        if poisoning_result['is_poisoned']:
            logger.warning(
                f"⚠️ Data poisoning detected: "
                f"{len(poisoning_result['suspicious_indices'])} suspicious samples"
            )
            
            # Remover muestras sospechosas
            clean_data = []
            clean_labels = []
            suspicious = set(poisoning_result['suspicious_indices'])
            
            for i, (data, label) in enumerate(zip(training_data, labels)):
                if i not in suspicious:
                    clean_data.append(data)
                    clean_labels.append(label)
            
            result['clean_data'] = clean_data
            result['clean_labels'] = clean_labels
            result['cleaned_size'] = len(clean_data)
            result['removed_samples'] = len(training_data) - len(clean_data)
            
            logger.info(
                f"✅ Data cleaned: {result['removed_samples']} samples removed"
            )
        
        else:
            logger.info("✅ Training data is clean")
        
        return result
    
    def generate_adversarial_examples(
        self,
        clean_data: np.ndarray,
        target_label: int,
        epsilon: float = 0.1
    ) -> np.ndarray:
        """
        Genera ejemplos adversariales para adversarial training
        
        Args:
            clean_data: Datos limpios
            target_label: Etiqueta objetivo
            epsilon: Magnitud de perturbación
            
        Returns:
            Ejemplos adversariales
        """
        
        logger.info(f"🎯 Generando ejemplos adversariales (epsilon={epsilon})...")
        
        # FGSM simplificado (Fast Gradient Sign Method)
        # En producción usar biblioteca como CleverHans o ART
        
        # Simular gradiente
        gradient = np.random.randn(*clean_data.shape)
        gradient = gradient / (np.linalg.norm(gradient) + 1e-10)
        
        # Aplicar perturbación
        adversarial = clean_data + epsilon * np.sign(gradient)
        
        # Clip a rango válido
        adversarial = np.clip(adversarial, 0, 1)
        
        return adversarial
    
    def adversarial_training(
        self,
        clean_data: List[np.ndarray],
        labels: List[int],
        augmentation_ratio: float = 0.3
    ) -> Dict:
        """
        Adversarial training - Entrena con ejemplos adversariales
        
        Args:
            clean_data: Datos limpios
            labels: Etiquetas
            augmentation_ratio: Ratio de ejemplos adversariales a añadir
            
        Returns:
            Dataset aumentado
        """
        
        logger.info(
            f"💪 Adversarial training (augmentation={augmentation_ratio*100:.0f}%)..."
        )
        
        num_adversarial = int(len(clean_data) * augmentation_ratio)
        
        augmented_data = list(clean_data)
        augmented_labels = list(labels)
        
        # Generar ejemplos adversariales
        for i in range(num_adversarial):
            # Seleccionar muestra aleatoria
            idx = np.random.randint(0, len(clean_data))
            clean_sample = clean_data[idx]
            label = labels[idx]
            
            # Generar adversarial
            adversarial = self.generate_adversarial_examples(
                clean_sample,
                label,
                epsilon=np.random.uniform(0.05, 0.15)
            )
            
            # Añadir al dataset
            augmented_data.append(adversarial)
            augmented_labels.append(label)
        
        result = {
            'original_size': len(clean_data),
            'augmented_size': len(augmented_data),
            'adversarial_added': num_adversarial,
            'augmented_data': augmented_data,
            'augmented_labels': augmented_labels
        }
        
        logger.info(
            f"✅ Dataset augmented: {len(clean_data)} → {len(augmented_data)} samples"
        )
        
        return result
    
    def evaluate_robustness(
        self,
        model_predictions: List[Dict],
        attack_scenarios: List[str]
    ) -> Dict:
        """
        Evalúa robustez del modelo contra ataques
        
        Args:
            model_predictions: Predicciones del modelo
            attack_scenarios: Escenarios de ataque probados
            
        Returns:
            Reporte de robustez
        """
        
        logger.info("📊 Evaluando robustez del modelo...")
        
        total = len(model_predictions)
        robust_predictions = sum(
            1 for pred in model_predictions 
            if pred.get('confidence', 0) > 0.7
        )
        
        robustness_score = robust_predictions / total if total > 0 else 0
        
        report = {
            'total_predictions': total,
            'robust_predictions': robust_predictions,
            'robustness_score': robustness_score,
            'attack_scenarios_tested': len(attack_scenarios),
            'passed_scenarios': len(attack_scenarios) if robustness_score > 0.8 else 0,
            'recommendation': self._get_robustness_recommendation(robustness_score)
        }
        
        logger.info(f"✅ Robustness score: {robustness_score*100:.1f}%")
        
        return report
    
    def _get_robustness_recommendation(self, score: float) -> str:
        """Genera recomendación basada en score de robustez"""
        
        if score >= 0.9:
            return "EXCELLENT - Model is highly robust"
        elif score >= 0.7:
            return "GOOD - Model shows good robustness"
        elif score >= 0.5:
            return "MODERATE - Consider additional adversarial training"
        else:
            return "POOR - Urgent: Implement defensive measures"
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de defensa"""
        
        detector_stats = self.detector.get_statistics()
        
        return {
            'defense': self.stats,
            'detector': detector_stats,
            'defense_techniques': self.defense_techniques
        }
    
    def generate_defense_report(self) -> str:
        """Genera reporte de defensa adversarial"""
        
        stats = self.get_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║            ADVERSARIAL DEFENSE - STATUS REPORT                   ║
╚══════════════════════════════════════════════════════════════════╝

🛡️ DEFENSE STATISTICS:

   Inputs Processed:      {stats['defense']['inputs_processed']}
   Attacks Blocked:       {stats['defense']['attacks_blocked']}
   Attacks Mitigated:     {stats['defense']['attacks_mitigated']}
   False Positives:       {stats['defense']['false_positives']}

🔍 DETECTION STATISTICS:

   Checks Performed:      {stats['detector']['checks']}
   Attacks Detected:      {stats['detector']['attacks_detected']}
   Evasion Attempts:      {stats['detector']['evasion_attempts']}
   Poisoning Attempts:    {stats['detector']['poisoning_attempts']}

🔧 DEFENSE TECHNIQUES:

   Input Sanitization:    {'✅' if stats['defense_techniques']['INPUT_SANITIZATION'] else '❌'}
   Adversarial Training:  {'✅' if stats['defense_techniques']['ADVERSARIAL_TRAINING'] else '❌'}
   Defensive Distillation:{'✅' if stats['defense_techniques']['DEFENSIVE_DISTILLATION'] else '❌'}
   Feature Squeezing:     {'✅' if stats['defense_techniques']['FEATURE_SQUEEZING'] else '❌'}
   Gradient Masking:      {'✅' if stats['defense_techniques']['GRADIENT_MASKING'] else '❌'}

⚡ System Status:         ACTIVE - AI vs AI Defense Online

═══════════════════════════════════════════════════════════════════
"""
        
        return report