#!/usr/bin/env python3
"""
Demo Kyber-768 - Criptografía Post-Cuántica
"""
import sys
sys.path.insert(0, 'src')
from quantum.quantum_sentinel import QuantumSentinel
import time

# Inicializar
qs = QuantumSentinel()

print('⚛️  DEMOSTRACIÓN DE KYBER-768')
print('='*50)
print()

# Generar claves
print('1. Generando par de claves...')
start = time.time()
keypair = qs.kyber.generate_keypair()
elapsed = (time.time() - start) * 1000
print(f'   ✅ Claves generadas en {elapsed:.2f}ms')
print(f'   📊 Public key: {len(keypair.pk)} bytes')
print(f'   🔐 Secret key: {len(keypair.sk)} bytes')
print()

# Encapsular
print('2. Encapsulando secreto compartido...')
start = time.time()
ciphertext, shared_secret = qs.kyber.encapsulate(keypair.pk)
elapsed = (time.time() - start) * 1000
print(f'   ✅ Encapsulado en {elapsed:.2f}ms')
print(f'   📦 Ciphertext: {len(ciphertext)} bytes')
print(f'   🔑 Shared secret: {shared_secret.hex()[:32]}...')
print()

# Desencapsular
print('3. Desencapsulando...')
start = time.time()
recovered = qs.kyber.decapsulate(keypair.sk, ciphertext)
elapsed = (time.time() - start) * 1000
print(f'   ✅ Desencapsulado en {elapsed:.2f}ms')
print(f'   ✅ Secretos coinciden: {shared_secret == recovered}')
print()

print('='*50)
print('💡 Esto es RESISTENTE a computadoras cuánticas')
print('   Un quantum computer NO puede romper esto')
print('   Algoritmo: Kyber-768 (NIST 2022)')
print('   Security Level: 3 (≈ AES-192)')
print('='*50)