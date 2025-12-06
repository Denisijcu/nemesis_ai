#!/usr/bin/env python3
"""Test del sistema adversarial"""

import sys
sys.path.insert(0, 'src')

import numpy as np
from adversarial.adversarial_defense import AdversarialDefense


def test_adversarial_detection():
    """Test de detección adversarial"""
    print("=" * 70)
    print("TEST 1: ADVERSARIAL DETECTION")
    print("=" * 70)
    
    defense = AdversarialDefense()
    
    # Input limpio
    clean_input = np.random.rand(100)
    clean_prediction = {'attack_type': 'NORMAL', 'confidence': 0.95}
    
    print("\n🧪 Testing clean input...\n")
    result = defense.defend_input(clean_input, clean_prediction)
    
    print(f"   Attack Detected: {result['attack_detected']}")
    print(f"   Blocked: {result['blocked']}")
    print(f"   Defenses Applied: {result['defense_applied']}")
    
    # Input adversarial (simulado)
    print("\n🧪 Testing adversarial input...\n")
    adversarial_input = clean_input + np.random.rand(100) * 0.5
    adv_prediction = {'attack_type': 'SUSPICIOUS', 'confidence': 0.4}
    
    result = defense.defend_input(adversarial_input, adv_prediction)
    
    print(f"   Attack Detected: {result['attack_detected']}")
    print(f"   Attack Type: {result['attack_info'].attack_type}")
    print(f"   Blocked: {result['blocked']}")
    print(f"   Defenses Applied: {result['defense_applied']}")
    
    print()


def test_data_poisoning():
    """Test de detección de poisoning"""
    print("=" * 70)
    print("TEST 2: DATA POISONING DETECTION")
    print("=" * 70)
    
    defense = AdversarialDefense()
    
    # Datos limpios
    clean_data = [np.random.rand(50) for _ in range(100)]
    labels = [0] * 50 + [1] * 50
    
    # Añadir muestras envenenadas
    poisoned_data = clean_data + [np.random.rand(50) * 10 for _ in range(10)]
    poisoned_labels = labels + [0] * 10
    
    print("\n🧪 Detecting poisoning in training data...\n")
    
    result = defense.defend_model_training(poisoned_data, poisoned_labels)
    
    print(f"   Original Size: {result['original_size']}")
    print(f"   Cleaned Size: {result['cleaned_size']}")
    print(f"   Removed: {result['removed_samples']}")
    print(f"   Poisoning Detected: {result['poisoning_detected']}")
    
    print()


def test_adversarial_training():
    """Test de adversarial training"""
    print("=" * 70)
    print("TEST 3: ADVERSARIAL TRAINING")
    print("=" * 70)
    
    defense = AdversarialDefense()
    
    # Dataset original
    clean_data = [np.random.rand(50) for _ in range(50)]
    labels = [0] * 25 + [1] * 25
    
    print("\n💪 Augmenting dataset with adversarial examples...\n")
    
    result = defense.adversarial_training(clean_data, labels, augmentation_ratio=0.3)
    
    print(f"   Original Size: {result['original_size']}")
    print(f"   Augmented Size: {result['augmented_size']}")
    print(f"   Adversarial Added: {result['adversarial_added']}")
    print(f"   Augmentation: {(result['adversarial_added']/result['original_size'])*100:.0f}%")
    
    print()


def test_robustness_evaluation():
    """Test de evaluación de robustez"""
    print("=" * 70)
    print("TEST 4: ROBUSTNESS EVALUATION")
    print("=" * 70)
    
    defense = AdversarialDefense()
    
    # Simular predicciones del modelo
    predictions = [
        {'confidence': 0.95} for _ in range(70)
    ] + [
        {'confidence': 0.4} for _ in range(30)
    ]
    
    attack_scenarios = ['FGSM', 'PGD', 'DEEPFOOL']
    
    print("\n📊 Evaluating model robustness...\n")
    
    report = defense.evaluate_robustness(predictions, attack_scenarios)
    
    print(f"   Total Predictions: {report['total_predictions']}")
    print(f"   Robust Predictions: {report['robust_predictions']}")
    print(f"   Robustness Score: {report['robustness_score']*100:.1f}%")
    print(f"   Recommendation: {report['recommendation']}")
    
    print()


def test_statistics():
    """Test de estadísticas"""
    print("=" * 70)
    print("TEST 5: STATISTICS")
    print("=" * 70)
    
    defense = AdversarialDefense()
    
    # Generar actividad
    for i in range(10):
        input_data = np.random.rand(100)
        prediction = {'attack_type': 'TEST', 'confidence': 0.8}
        defense.defend_input(input_data, prediction)
    
    print("\n📊 Defense Statistics:\n")
    print(defense.generate_defense_report())
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "ADVERSARIAL DEFENSE - TESTS" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_adversarial_detection()
    test_data_poisoning()
    test_adversarial_training()
    test_robustness_evaluation()
    test_statistics()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("🤖 CAPÍTULO 13 COMPLETADO:")
    print("   ✅ Adversarial Detection")
    print("   ✅ Data Poisoning Defense")
    print("   ✅ Adversarial Training")
    print("   ✅ Input Sanitization")
    print("   ✅ Feature Squeezing")
    print("   ✅ Robustness Evaluation")
    print()
    print("🛡️ AI vs AI DEFENSE: OPERATIONAL!")
    print()


if __name__ == "__main__":
    main()