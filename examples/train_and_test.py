#!/usr/bin/env python3
"""
Némesis IA - Script de Ejemplo: Entrenar y Probar el Modelo V2

Este script demuestra cómo:
1. Entrenar el modelo V2 (con features mejoradas)
2. Evaluar su performance
3. Probar con 9 ejemplos reales

Copyright (C) 2025 Némesis AI Project Contributors
Licensed under GPL-3.0
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ml.train_brain import train_model_v2, FeatureExtractorV2
import joblib


def train_model():
    """Entrenar modelo V2 con features mejoradas"""
    print("🚀 Entrenando modelo Némesis V2 (con features mejoradas)...")
    print()
    
    metrics = train_model_v2(
        output_path="models/nemesis_brain_v2.joblib",
        n_samples=10000,
        test_size=0.2
    )
    
    return metrics


def test_model_with_examples():
    """Probar modelo V2 con ejemplos reales"""
    print("\n" + "=" * 60)
    print("🧪 PROBANDO MODELO V2 CON EJEMPLOS REALES")
    print("=" * 60 + "\n")
    
    # Cargar modelo V2
    model_path = "models/nemesis_brain_v2.joblib"
    if not Path(model_path).exists():
        print(f"⚠️  Modelo V2 no encontrado en {model_path}")
        print("Entrenando primero...")
        train_model()
    
    model = joblib.load(model_path)
    extractor = FeatureExtractorV2()
    
    # Ejemplos de prueba
    test_cases = [
        # Legítimos
        {
            "payload": "GET /index.html HTTP/1.1",
            "expected": "LEGÍTIMO",
            "description": "Request simple a página principal"
        },
        {
            "payload": "GET /api/users?page=1&limit=10 HTTP/1.1",
            "expected": "LEGÍTIMO",
            "description": "API request con paginación"
        },
        {
            "payload": "GET /search?q=python+tutorial HTTP/1.1",
            "expected": "LEGÍTIMO",
            "description": "Búsqueda legítima"
        },
        
        # SQL Injection
        {
            "payload": "GET /login?user=admin' OR '1'='1'-- HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "SQL Injection clásico"
        },
        {
            "payload": "GET /products?id=1' UNION SELECT * FROM users-- HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "SQL Injection con UNION"
        },
        
        # XSS
        {
            "payload": "GET /search?q=<script>alert('XSS')</script> HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "XSS con script tag"
        },
        {
            "payload": "GET /comment?text=<img src=x onerror=alert(1)> HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "XSS con img onerror"
        },
        
        # Path Traversal
        {
            "payload": "GET /download?file=../../../etc/passwd HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "Path Traversal"
        },
        
        # Command Injection
        {
            "payload": "GET /ping?host=127.0.0.1; cat /etc/passwd HTTP/1.1",
            "expected": "MALICIOSO",
            "description": "Command Injection"
        },
    ]
    
    # Evaluar cada caso
    correct = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        payload = test_case["payload"]
        expected = test_case["expected"]
        description = test_case["description"]
        
        # Extraer features y predecir
        features = extractor.extract_features(payload)
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]
        
        # Interpretar predicción
        predicted = "MALICIOSO" if prediction == 1 else "LEGÍTIMO"
        confidence = probability[1] if prediction == 1 else probability[0]
        
        # Verificar si es correcto
        is_correct = (predicted == expected)
        if is_correct:
            correct += 1
        
        # Mostrar resultado
        status = "✅" if is_correct else "❌"
        print(f"{status} Test {i}/{total}")
        print(f"   Descripción:  {description}")
        print(f"   Payload:      {payload[:60]}...")
        print(f"   Esperado:     {expected}")
        print(f"   Predicción:   {predicted}")
        print(f"   Confianza:    {confidence:.2%}")
        
        # Mostrar detalles si falla
        if not is_correct:
            print(f"   📊 Features:  {features}")
        
        print()
    
    # Resumen
    accuracy = (correct / total) * 100
    print("=" * 60)
    print(f"📊 RESUMEN: {correct}/{total} correctos ({accuracy:.1f}% accuracy)")
    print("=" * 60)
    
    return accuracy


def main():
    """Función principal"""
    print("=" * 60)
    print("   NÉMESIS IA - ENTRENAMIENTO Y PRUEBA DEL MODELO V2")
    print("=" * 60)
    print()
    
    # Verificar si modelo ya existe
    model_path = Path("models/nemesis_brain_v2.joblib")
    
    if model_path.exists():
        print(f"ℹ️  Modelo V2 encontrado: {model_path}")
        response = input("¿Quieres re-entrenar? (s/n): ").lower()
        if response == 's':
            metrics = train_model()
        else:
            print("✅ Usando modelo V2 existente")
    else:
        print("ℹ️  No se encontró modelo V2. Entrenando nuevo modelo...")
        metrics = train_model()
    
    # Probar modelo
    print("\nPresiona Enter para probar el modelo con ejemplos reales...")
    input()
    
    accuracy = test_model_with_examples()
    
    # Conclusión
    print("\n" + "=" * 60)
    print("🎉 ¡Prueba completada!")
    print()
    if accuracy == 100:
        print("🌟 ¡PERFECTO! Modelo V2 alcanzó 100% accuracy")
    elif accuracy >= 90:
        print("✅ Excelente performance del modelo V2")
    else:
        print("⚠️  Considera re-entrenar con más samples")
    print()
    print("El modelo está listo para usar en el Agente Némesis.")
    print()
    print("Para usar el modelo:")
    print("  python3 src/core/nemesis_agent.py")
    print()
    print("Para entrenar con más samples:")
    print("  python3 src/ml/train_brain_v2.py")
    print("=" * 60)


if __name__ == "__main__":
    main()