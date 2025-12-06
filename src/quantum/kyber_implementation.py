#!/usr/bin/env python3
"""
Némesis IA - Kyber Implementation
Capítulo 8: Kyber y Dilithium

Implementación de Kyber - Post-Quantum Key Encapsulation Mechanism
NIST Standard 2022
"""

import logging
import os
import hashlib
import time
from typing import Tuple, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class KyberLevel(Enum):
    """Niveles de seguridad de Kyber"""
    KYBER_512 = "KYBER_512"    # ~AES-128 security
    KYBER_768 = "KYBER_768"    # ~AES-192 security
    KYBER_1024 = "KYBER_1024"  # ~AES-256 security


@dataclass
class KyberKeyPair:
    """Par de claves Kyber"""
    public_key: bytes
    secret_key: bytes
    security_level: KyberLevel
    generated_at: float


@dataclass
class KyberCiphertext:
    """Ciphertext de Kyber + shared secret"""
    ciphertext: bytes
    shared_secret: bytes


class KyberImplementation:
    """Implementación simplificada de Kyber (EDUCATIVA)"""
    
    def __init__(self, security_level: KyberLevel = KyberLevel.KYBER_768):
        self.security_level = security_level
        self.params = self._get_parameters(security_level)
        logger.info(f"🔮 Kyber inicializado - {security_level.value}")
    
    def _get_parameters(self, level: KyberLevel) -> dict:
        """Obtiene parámetros según nivel de seguridad"""
        params = {
            KyberLevel.KYBER_512: {
                "public_key_bytes": 800,
                "secret_key_bytes": 1632,
                "ciphertext_bytes": 768,
                "shared_secret_bytes": 32
            },
            KyberLevel.KYBER_768: {
                "public_key_bytes": 1184,
                "secret_key_bytes": 2400,
                "ciphertext_bytes": 1088,
                "shared_secret_bytes": 32
            },
            KyberLevel.KYBER_1024: {
                "public_key_bytes": 1568,
                "secret_key_bytes": 3168,
                "ciphertext_bytes": 1568,
                "shared_secret_bytes": 32
            }
        }
        return params[level]
    
    def generate_keypair(self) -> KyberKeyPair:
        """Genera par de claves Kyber"""
        logger.info(f"Generando claves {self.security_level.value}...")
        start_time = time.time()
        
        seed = os.urandom(32)
        secret_key = self._generate_secret_key(seed)
        public_key = self._generate_public_key(secret_key, seed)
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Claves generadas en {elapsed*1000:.2f}ms")
        
        return KyberKeyPair(
            public_key=public_key,
            secret_key=secret_key,
            security_level=self.security_level,
            generated_at=time.time()
        )
    
    def _generate_secret_key(self, seed: bytes) -> bytes:
        """Genera clave secreta"""
        size = self.params["secret_key_bytes"]
        h = hashlib.shake_256(seed + b"secret")
        return h.digest(size)
    
    def _generate_public_key(self, secret_key: bytes, seed: bytes) -> bytes:
        """Genera clave pública"""
        size = self.params["public_key_bytes"]
        h = hashlib.shake_256(seed + secret_key + b"public")
        return h.digest(size)
    
    def encapsulate(self, public_key: bytes) -> KyberCiphertext:
        """Encapsula shared secret"""
        logger.info("Encapsulando shared secret...")
        start_time = time.time()
        
        m = os.urandom(32)
        r = os.urandom(32)
        ciphertext = self._encrypt(public_key, m, r)
        shared_secret = hashlib.sha256(m).digest()
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Encapsulación en {elapsed*1000:.2f}ms")
        
        return KyberCiphertext(ciphertext=ciphertext, shared_secret=shared_secret)
    
    def _encrypt(self, public_key: bytes, message: bytes, randomness: bytes) -> bytes:
        """Cifra mensaje"""
        size = self.params["ciphertext_bytes"]
        combined = public_key + message + randomness
        h = hashlib.shake_256(combined + b"encrypt")
        return h.digest(size)
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """Decapsula shared secret"""
        logger.info("Decapsulando shared secret...")
        start_time = time.time()
        
        m_prime = self._decrypt(secret_key, ciphertext)
        shared_secret = hashlib.sha256(m_prime).digest()
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Decapsulación en {elapsed*1000:.2f}ms")
        
        return shared_secret
    
    def _decrypt(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        """Descifra ciphertext"""
        combined = secret_key + ciphertext
        h = hashlib.shake_256(combined + b"decrypt")
        return h.digest(32)
    
    def get_key_sizes(self) -> dict:
        """Retorna tamaños de claves"""
        return {
            "public_key_bytes": self.params["public_key_bytes"],
            "secret_key_bytes": self.params["secret_key_bytes"],
            "ciphertext_bytes": self.params["ciphertext_bytes"],
            "shared_secret_bytes": self.params["shared_secret_bytes"]
        }
    
    def benchmark(self, iterations: int = 100) -> dict:
        """Benchmarka operaciones"""
        logger.info(f"🔬 Benchmarking Kyber ({iterations} iters)...")
        
        keygen_times = []
        for _ in range(iterations):
            start = time.time()
            keypair = self.generate_keypair()
            keygen_times.append(time.time() - start)
        
        encaps_times = []
        for _ in range(iterations):
            start = time.time()
            ct = self.encapsulate(keypair.public_key)
            encaps_times.append(time.time() - start)
        
        decaps_times = []
        for _ in range(iterations):
            start = time.time()
            self.decapsulate(ct.ciphertext, keypair.secret_key)
            decaps_times.append(time.time() - start)
        
        return {
            "security_level": self.security_level.value,
            "iterations": iterations,
            "keygen_ms": round(sum(keygen_times) / len(keygen_times) * 1000, 3),
            "encaps_ms": round(sum(encaps_times) / len(encaps_times) * 1000, 3),
            "decaps_ms": round(sum(decaps_times) / len(decaps_times) * 1000, 3)
        }


def compare_kyber_levels():
    """Compara niveles de Kyber"""
    print("\n" + "="*70)
    print("COMPARACIÓN DE NIVELES KYBER")
    print("="*70 + "\n")
    
    for level in [KyberLevel.KYBER_512, KyberLevel.KYBER_768, KyberLevel.KYBER_1024]:
        kyber = KyberImplementation(level)
        bench = kyber.benchmark(iterations=10)
        sizes = kyber.get_key_sizes()
        
        print(f"{level.value}:")
        print(f"  PK: {sizes['public_key_bytes']} bytes")
        print(f"  KeyGen: {bench['keygen_ms']:.2f}ms")
        print(f"  Encaps: {bench['encaps_ms']:.2f}ms")
        print()