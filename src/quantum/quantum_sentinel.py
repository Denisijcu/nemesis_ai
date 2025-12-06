#!/usr/bin/env python3
"""
Némesis IA - Quantum Sentinel
Capítulo 8: Kyber y Dilithium

Sistema integrador de Post-Quantum Cryptography
"""

import logging
import time
from typing import Dict, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass

from .kyber_implementation import KyberImplementation, KyberLevel, KyberKeyPair
from .dilithium_implementation import DilithiumImplementation, DilithiumLevel, DilithiumKeyPair
from .quantum_threat_analyzer import QuantumThreatAnalyzer

logger = logging.getLogger(__name__)


@dataclass
class QuantumProtectedData:
    """Datos protegidos con PQC"""
    encrypted_data: bytes
    signature: bytes
    kyber_ciphertext: bytes
    dilithium_public_key: bytes
    timestamp: float
    security_level: str


class QuantumSentinel:
    """Sistema completo de Post-Quantum Cryptography"""
    
    def __init__(
        self,
        kyber_level: KyberLevel = KyberLevel.KYBER_768,
        dilithium_level: DilithiumLevel = DilithiumLevel.DILITHIUM_3
    ):
        """
        Inicializa Quantum Sentinel
        
        Args:
            kyber_level: Nivel de seguridad para Kyber
            dilithium_level: Nivel de seguridad para Dilithium
        """
        
        # Componentes PQC
        self.kyber = KyberImplementation(kyber_level)
        self.dilithium = DilithiumImplementation(dilithium_level)
        
        # Analizador de amenazas
        self.threat_analyzer = QuantumThreatAnalyzer()
        
        # Claves del sistema
        self.kyber_keypair: Optional[KyberKeyPair] = None
        self.dilithium_keypair: Optional[DilithiumKeyPair] = None
        
        # Estadísticas
        self.stats = {
            "encryptions": 0,
            "decryptions": 0,
            "signatures": 0,
            "verifications": 0,
            "threats_analyzed": 0
        }
        
        logger.info(
            f"🛡️  QuantumSentinel inicializado "
            f"(Kyber-{kyber_level.value}, Dilithium-{dilithium_level.value})"
        )
    
    def initialize_system(self):
        """Inicializa el sistema generando claves maestras"""
        
        logger.info("🔐 Inicializando sistema Quantum Sentinel...")
        
        start = time.time()
        
        # Generar par de claves Kyber
        logger.info("Generando claves Kyber...")
        self.kyber_keypair = self.kyber.generate_keypair()
        
        # Generar par de claves Dilithium
        logger.info("Generando claves Dilithium...")
        self.dilithium_keypair = self.dilithium.generate_keypair()
        
        elapsed = time.time() - start
        
        logger.info(f"✅ Sistema inicializado en {elapsed*1000:.2f}ms")
        
        return {
            "kyber_public_key": self.kyber_keypair.public_key,
            "dilithium_public_key": self.dilithium_keypair.public_key,
            "initialization_time_ms": round(elapsed * 1000, 2)
        }
    
    def protect_data(self, data: bytes) -> QuantumProtectedData:
        """
        Protege datos con PQC completo (Kyber + Dilithium)
        
        Args:
            data: Datos a proteger
            
        Returns:
            QuantumProtectedData con cifrado y firma
        """
        
        if not self.kyber_keypair or not self.dilithium_keypair:
            raise RuntimeError("Sistema no inicializado. Llamar initialize_system() primero")
        
        logger.info(f"🔒 Protegiendo {len(data)} bytes con PQC...")
        
        start = time.time()
        
        # 1. Encapsular shared secret con Kyber
        kyber_result = self.kyber.encapsulate(self.kyber_keypair.public_key)
        shared_secret = kyber_result.shared_secret
        
        # 2. Cifrar datos con shared secret (AES-256-GCM en producción)
        # Simplificación: XOR con shared secret expandido
        encrypted_data = self._symmetric_encrypt(data, shared_secret)
        
        # 3. Firmar datos cifrados con Dilithium
        signature_obj = self.dilithium.sign(
            encrypted_data,
            self.dilithium_keypair.secret_key
        )
        
        elapsed = time.time() - start
        
        self.stats["encryptions"] += 1
        self.stats["signatures"] += 1
        
        logger.info(
            f"✅ Datos protegidos en {elapsed*1000:.2f}ms "
            f"(ct: {len(encrypted_data)} bytes, sig: {len(signature_obj.signature)} bytes)"
        )
        
        return QuantumProtectedData(
            encrypted_data=encrypted_data,
            signature=signature_obj.signature,
            kyber_ciphertext=kyber_result.ciphertext,
            dilithium_public_key=self.dilithium_keypair.public_key,
            timestamp=time.time(),
            security_level=f"{self.kyber.security_level.value}+{self.dilithium.security_level.value}"
        )
    
    def unprotect_data(self, protected: QuantumProtectedData) -> Optional[bytes]:
        """
        Desprotege datos verificando firma y descifrando
        
        Args:
            protected: Datos protegidos
            
        Returns:
            Datos originales si verificación exitosa, None si falla
        """
        
        if not self.kyber_keypair or not self.dilithium_keypair:
            raise RuntimeError("Sistema no inicializado")
        
        logger.info("🔓 Desprotegiendo datos...")
        
        start = time.time()
        
        # 1. Verificar firma
        valid = self.dilithium.verify(
            protected.encrypted_data,
            protected.signature,
            protected.dilithium_public_key
        )
        
        if not valid:
            logger.error("❌ Firma inválida, datos comprometidos")
            return None
        
        self.stats["verifications"] += 1
        
        # 2. Decapsular shared secret
        shared_secret = self.kyber.decapsulate(
            protected.kyber_ciphertext,
            self.kyber_keypair.secret_key
        )
        
        # 3. Descifrar datos
        decrypted_data = self._symmetric_decrypt(
            protected.encrypted_data,
            shared_secret
        )
        
        elapsed = time.time() - start
        
        self.stats["decryptions"] += 1
        
        logger.info(f"✅ Datos desprotegidos en {elapsed*1000:.2f}ms")
        
        return decrypted_data
    
    def _symmetric_encrypt(self, data: bytes, key: bytes) -> bytes:
        """
        Cifrado simétrico con clave compartida
        
        En producción: AES-256-GCM
        Aquí: XOR simple para educación
        """
        
        # Expandir clave al tamaño de los datos
        import hashlib
        expanded_key = hashlib.shake_256(key).digest(len(data))
        
        # XOR
        encrypted = bytes(a ^ b for a, b in zip(data, expanded_key))
        
        return encrypted
    
    def _symmetric_decrypt(self, encrypted: bytes, key: bytes) -> bytes:
        """Descifrado simétrico (XOR es su propio inverso)"""
        return self._symmetric_encrypt(encrypted, key)
    
    def analyze_migration_from_rsa(self, rsa_key_size: int = 2048) -> Dict:
        """
        Analiza migración desde RSA a PQC
        
        Args:
            rsa_key_size: Tamaño actual de claves RSA
            
        Returns:
            Análisis de migración
        """
        
        logger.info(f"📊 Analizando migración RSA-{rsa_key_size} → PQC...")
        
        # Analizar amenaza actual
        threat = self.threat_analyzer.analyze_algorithm("RSA", rsa_key_size)
        
        # Tamaños de clave
        kyber_sizes = self.kyber.get_key_sizes()
        dilithium_sizes = self.dilithium.get_key_sizes()
        
        # Estimación de tamaños RSA equivalentes
        rsa_pk_size = rsa_key_size // 8  # Aproximación
        rsa_sig_size = rsa_key_size // 8
        
        return {
            "current_threat": {
                "algorithm": f"RSA-{rsa_key_size}",
                "years_until_vulnerable": threat.years_until_vulnerable,
                "risk_level": threat.risk_level,  # ← CORREGIDO
                "recommendation": threat.recommendation
            },
            "size_comparison": {
                "rsa_public_key": rsa_pk_size,
                "kyber_public_key": kyber_sizes["public_key_bytes"],
                "increase_factor": round(kyber_sizes["public_key_bytes"] / rsa_pk_size, 2),
                
                "rsa_signature": rsa_sig_size,
                "dilithium_signature": dilithium_sizes["signature_bytes"],
                "sig_increase_factor": round(dilithium_sizes["signature_bytes"] / rsa_sig_size, 2)
            },
            "migration_urgency": self._calculate_urgency(threat.years_until_vulnerable),
            "recommended_levels": {
                "kyber": "KYBER_768" if rsa_key_size <= 2048 else "KYBER_1024",
                "dilithium": "DILITHIUM_3" if rsa_key_size <= 2048 else "DILITHIUM_5"
            }
        }
    
    def _calculate_urgency(self, years_until: int) -> str:
        """Calcula urgencia de migración"""
        
        if years_until <= 3:
            return "CRITICAL - Migrar INMEDIATAMENTE"
        elif years_until <= 5:
            return "HIGH - Migrar en los próximos 6-12 meses"
        elif years_until <= 10:
            return "MEDIUM - Planear migración en 1-2 años"
        else:
            return "LOW - Monitorear y preparar"
    
    def benchmark_vs_classical(self) -> Dict:
        """
        Compara rendimiento PQC vs criptografía clásica
        
        Returns:
            Comparación de rendimiento
        """
        
        logger.info("🔬 Benchmarking PQC vs Classical...")
        
        # Benchmark Kyber
        kyber_bench = self.kyber.benchmark(iterations=50)
        
        # Benchmark Dilithium
        dilithium_bench = self.dilithium.benchmark(iterations=50)
        
        # Estimaciones RSA (basadas en literatura)
        # RSA-2048: ~2ms keygen, ~0.5ms sign, ~0.1ms verify
        rsa_2048 = {
            "keygen_ms": 2.0,
            "sign_ms": 0.5,
            "verify_ms": 0.1
        }
        
        return {
            "kyber": kyber_bench,
            "dilithium": dilithium_bench,
            "rsa_2048_estimate": rsa_2048,
            "comparison": {
                "kyber_vs_rsa_keygen": round(kyber_bench["keygen_ms"] / rsa_2048["keygen_ms"], 2),
                "dilithium_vs_rsa_sign": round(dilithium_bench["sign_ms"] / rsa_2048["sign_ms"], 2),
                "dilithium_vs_rsa_verify": round(dilithium_bench["verify_ms"] / rsa_2048["verify_ms"], 2)
            },
            "note": "PQC es más lento que RSA, pero RESISTENTE a ataques cuánticos"
        }
    
    def get_system_status(self) -> Dict:
        """Obtiene estado del sistema"""
        
        return {
            "initialized": self.kyber_keypair is not None and self.dilithium_keypair is not None,
            "kyber_level": self.kyber.security_level.value,
            "dilithium_level": self.dilithium.security_level.value,
            "statistics": self.stats,
            "keys_generated_at": {
                "kyber": self.kyber_keypair.generated_at if self.kyber_keypair else None,
                "dilithium": self.dilithium_keypair.generated_at if self.dilithium_keypair else None
            }
        }
    
    def generate_security_report(self) -> str:
        """Genera reporte de seguridad del sistema"""
        
        status = self.get_system_status()
        migration = self.analyze_migration_from_rsa(2048)
        benchmark = self.benchmark_vs_classical()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║               QUANTUM SENTINEL - SECURITY REPORT                 ║
╚══════════════════════════════════════════════════════════════════╝

📅 Timestamp: {datetime.now().isoformat()}

🔐 CONFIGURACIÓN ACTUAL:

   Kyber Level:     {status['kyber_level']}
   Dilithium Level: {status['dilithium_level']}
   Sistema:         {'✅ Inicializado' if status['initialized'] else '❌ No inicializado'}

📊 ESTADÍSTICAS DE USO:

   Encriptaciones:  {status['statistics']['encryptions']}
   Desencriptaciones: {status['statistics']['decryptions']}
   Firmas:          {status['statistics']['signatures']}
   Verificaciones:  {status['statistics']['verifications']}

⚠️ ANÁLISIS DE AMENAZA (RSA-2048):

   Años hasta vulnerabilidad: {migration['current_threat']['years_until_vulnerable']}
   Nivel de amenaza:          {migration['current_threat']['risk_level']}
   Urgencia de migración:     {migration['migration_urgency']}

📏 COMPARACIÓN DE TAMAÑOS:

   RSA-2048 Public Key:    {migration['size_comparison']['rsa_public_key']} bytes
   Kyber Public Key:       {migration['size_comparison']['kyber_public_key']} bytes
   Incremento:             {migration['size_comparison']['increase_factor']}x

   RSA-2048 Signature:     {migration['size_comparison']['rsa_signature']} bytes
   Dilithium Signature:    {migration['size_comparison']['dilithium_signature']} bytes
   Incremento:             {migration['size_comparison']['sig_increase_factor']}x

⚡ RENDIMIENTO:

   Kyber KeyGen:    {benchmark['kyber']['keygen_ms']:.2f}ms
   Kyber Encaps:    {benchmark['kyber']['encaps_ms']:.2f}ms
   Kyber Decaps:    {benchmark['kyber']['decaps_ms']:.2f}ms

   Dilithium KeyGen: {benchmark['dilithium']['keygen_ms']:.2f}ms
   Dilithium Sign:   {benchmark['dilithium']['sign_ms']:.2f}ms
   Dilithium Verify: {benchmark['dilithium']['verify_ms']:.2f}ms

🎯 RECOMENDACIONES:

   {migration['current_threat']['recommendation']}

   Niveles sugeridos para migración:
   • Kyber:     {migration['recommended_levels']['kyber']}
   • Dilithium: {migration['recommended_levels']['dilithium']}

🛡️ PROTECCIÓN CUÁNTICA: ACTIVA
   ✅ Resistente a algoritmo de Shor
   ✅ Resistente a algoritmo de Grover
   ✅ Estándares NIST 2022

═══════════════════════════════════════════════════════════════════
"""
        
        return report


def demonstrate_hybrid_crypto():
    """Demuestra criptografía híbrida (Classical + PQC)"""
    
    print("\n" + "="*70)
    print("DEMOSTRACIÓN: CRIPTOGRAFÍA HÍBRIDA")
    print("="*70 + "\n")
    
    print("💡 Concepto: Usar RSA Y Kyber simultáneamente")
    print("   Ventaja: Protección si cualquiera de los dos es comprometido")
    print()
    
    # Simulación
    print("1️⃣  Cifrado híbrido:")
    print("   • Generar shared_secret_1 con RSA")
    print("   • Generar shared_secret_2 con Kyber")
    print("   • Combinar: final_key = KDF(shared_secret_1 || shared_secret_2)")
    print("   • Cifrar datos con final_key usando AES-256")
    print()
    
    print("2️⃣  Ventajas:")
    print("   ✅ Si computadora cuántica rompe RSA → Kyber protege")
    print("   ✅ Si fallo en Kyber → RSA protege (backup clásico)")
    print("   ✅ Transición gradual sin romper compatibilidad")
    print()
    
    print("3️⃣  Uso en producción:")
    print("   • TLS 1.3 con PQC híbrido")
    print("   • Signal protocol con Kyber")
    print("   • Google Chrome experimenta con híbrido")
    print()
    
    print("="*70 + "\n")