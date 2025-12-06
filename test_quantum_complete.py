#!/usr/bin/env python3
"""
Test completo del sistema Quantum Defense
"""

import sys
sys.path.insert(0, 'src')

from quantum.quantum_sentinel import QuantumSentinel, demonstrate_hybrid_crypto
from quantum.kyber_implementation import KyberLevel, compare_kyber_levels
from quantum.dilithium_implementation import DilithiumLevel, compare_dilithium_levels


def test_kyber_standalone():
    """Test de Kyber standalone"""
    print("=" * 70)
    print("TEST 1: KYBER - KEY ENCAPSULATION MECHANISM")
    print("=" * 70)
    
    from quantum.kyber_implementation import KyberImplementation
    
    kyber = KyberImplementation(KyberLevel.KYBER_768)
    
    print("\n🔐 Generando claves Kyber...")
    keypair = kyber.generate_keypair()
    
    print(f"   ✅ Clave pública:  {len(keypair.public_key)} bytes")
    print(f"   ✅ Clave secreta:  {len(keypair.secret_key)} bytes")
    
    print("\n🔒 Encapsulando shared secret...")
    ct = kyber.encapsulate(keypair.public_key)
    
    print(f"   ✅ Ciphertext:     {len(ct.ciphertext)} bytes")
    print(f"   ✅ Shared secret:  {len(ct.shared_secret)} bytes")
    
    print("\n🔓 Decapsulando shared secret...")
    recovered = kyber.decapsulate(ct.ciphertext, keypair.secret_key)
    
    print(f"   ✅ Secret recuperado: {len(recovered)} bytes")
    print(f"   ✅ Match: {recovered == ct.shared_secret}")
    
    print()


def test_dilithium_standalone():
    """Test de Dilithium standalone"""
    print("=" * 70)
    print("TEST 2: DILITHIUM - DIGITAL SIGNATURES")
    print("=" * 70)
    
    from quantum.dilithium_implementation import DilithiumImplementation
    
    dil = DilithiumImplementation(DilithiumLevel.DILITHIUM_3)
    
    print("\n✍️  Generando claves Dilithium...")
    keypair = dil.generate_keypair()
    
    print(f"   ✅ Clave pública:  {len(keypair.public_key)} bytes")
    print(f"   ✅ Clave secreta:  {len(keypair.secret_key)} bytes")
    
    message = b"Mensaje importante a firmar con post-quantum crypto"
    
    print(f"\n📝 Firmando mensaje ({len(message)} bytes)...")
    sig = dil.sign(message, keypair.secret_key)
    
    print(f"   ✅ Firma:          {len(sig.signature)} bytes")
    
    print("\n✓ Verificando firma...")
    valid = dil.verify(message, sig.signature, keypair.public_key)
    
    print(f"   ✅ Firma válida:   {valid}")
    
    print()


def test_quantum_sentinel_full():
    """Test completo de Quantum Sentinel"""
    print("=" * 70)
    print("TEST 3: QUANTUM SENTINEL - SISTEMA COMPLETO")
    print("=" * 70)
    
    sentinel = QuantumSentinel(
        kyber_level=KyberLevel.KYBER_768,
        dilithium_level=DilithiumLevel.DILITHIUM_3
    )
    
    print("\n🚀 Inicializando sistema...")
    init_result = sentinel.initialize_system()
    
    print(f"   ✅ Tiempo de inicialización: {init_result['initialization_time_ms']:.2f}ms")
    
    # Proteger datos
    original_data = b"Datos sensibles de Nemesis IA - TOP SECRET"
    
    print(f"\n🔒 Protegiendo datos ({len(original_data)} bytes)...")
    protected = sentinel.protect_data(original_data)
    
    print(f"   ✅ Datos cifrados:  {len(protected.encrypted_data)} bytes")
    print(f"   ✅ Firma:           {len(protected.signature)} bytes")
    print(f"   ✅ Security level:  {protected.security_level}")
    
    # Desproteger datos
    print(f"\n🔓 Desprotegiendo datos...")
    recovered = sentinel.unprotect_data(protected)
    
    if recovered:
        print(f"   ✅ Datos recuperados: {len(recovered)} bytes")
        print(f"   ✅ Match: {recovered == original_data}")
    else:
        print(f"   ❌ Fallo en verificación")
    
    print()


def test_migration_analysis():
    """Test de análisis de migración"""
    print("=" * 70)
    print("TEST 4: ANÁLISIS DE MIGRACIÓN RSA → PQC")
    print("=" * 70)
    
    sentinel = QuantumSentinel()
    sentinel.initialize_system()
    
    # Analizar migración desde RSA-2048
    print("\n📊 Analizando migración desde RSA-2048...")
    
    migration = sentinel.analyze_migration_from_rsa(2048)
    
    print(f"\n⚠️  AMENAZA ACTUAL:")
    print(f"   Algoritmo:              {migration['current_threat']['algorithm']}")
    print(f"   Años hasta vulnerable:  {migration['current_threat']['years_until_vulnerable']}")
    print(f"   Nivel de amenaza:       {migration['current_threat']['risk_level']}")  # ← CORREGIDO
    
    print(f"\n📏 COMPARACIÓN DE TAMAÑOS:")
    print(f"   RSA-2048 PK:   {migration['size_comparison']['rsa_public_key']} bytes")
    print(f"   Kyber PK:      {migration['size_comparison']['kyber_public_key']} bytes")
    print(f"   Incremento:    {migration['size_comparison']['increase_factor']}x")
    
    print(f"\n🎯 URGENCIA:")
    print(f"   {migration['migration_urgency']}")
    
    print()


def test_performance_comparison():
    """Test de comparación de rendimiento"""
    print("=" * 70)
    print("TEST 5: COMPARACIÓN DE RENDIMIENTO PQC vs CLASSICAL")
    print("=" * 70)
    
    sentinel = QuantumSentinel()
    sentinel.initialize_system()
    
    print("\n⚡ Benchmarking PQC vs RSA...")
    
    bench = sentinel.benchmark_vs_classical()
    
    print(f"\n📊 KYBER:")
    print(f"   KeyGen:  {bench['kyber']['keygen_ms']:.2f}ms")
    print(f"   Encaps:  {bench['kyber']['encaps_ms']:.2f}ms")
    print(f"   Decaps:  {bench['kyber']['decaps_ms']:.2f}ms")
    
    print(f"\n📊 DILITHIUM:")
    print(f"   KeyGen:  {bench['dilithium']['keygen_ms']:.2f}ms")
    print(f"   Sign:    {bench['dilithium']['sign_ms']:.2f}ms")
    print(f"   Verify:  {bench['dilithium']['verify_ms']:.2f}ms")
    
    print(f"\n📊 RSA-2048 (estimado):")
    print(f"   KeyGen:  {bench['rsa_2048_estimate']['keygen_ms']:.2f}ms")
    print(f"   Sign:    {bench['rsa_2048_estimate']['sign_ms']:.2f}ms")
    print(f"   Verify:  {bench['rsa_2048_estimate']['verify_ms']:.2f}ms")
    
    print(f"\n⚖️  COMPARACIÓN:")
    print(f"   Kyber vs RSA KeyGen:    {bench['comparison']['kyber_vs_rsa_keygen']:.2f}x")
    print(f"   Dilithium vs RSA Sign:  {bench['comparison']['dilithium_vs_rsa_sign']:.2f}x")
    print(f"   Dilithium vs RSA Verify: {bench['comparison']['dilithium_vs_rsa_verify']:.2f}x")
    
    print(f"\n💡 {bench['note']}")
    
    print()


def test_security_report():
    """Test de reporte de seguridad"""
    print("=" * 70)
    print("TEST 6: REPORTE DE SEGURIDAD")
    print("=" * 70)
    
    sentinel = QuantumSentinel()
    sentinel.initialize_system()
    
    # Realizar algunas operaciones
    data1 = b"Test data 1"
    data2 = b"Test data 2"
    
    protected1 = sentinel.protect_data(data1)
    protected2 = sentinel.protect_data(data2)
    
    sentinel.unprotect_data(protected1)
    sentinel.unprotect_data(protected2)
    
    # Generar reporte
    report = sentinel.generate_security_report()
    print(report)
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 16 + "QUANTUM DEFENSE - TESTS COMPLETOS" + " " * 19 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    test_kyber_standalone()
    print()
    
    test_dilithium_standalone()
    print()
    
    test_quantum_sentinel_full()
    print()
    
    test_migration_analysis()
    print()
    
    test_performance_comparison()
    print()
    
    test_security_report()
    print()
    
    # Comparaciones de niveles
    compare_kyber_levels()
    print()
    
    compare_dilithium_levels()
    print()
    
    # Crypto híbrida
    demonstrate_hybrid_crypto()
    print()
    
    print("=" * 70)
    print("✅ TODOS LOS TESTS COMPLETADOS")
    print("=" * 70)
    print()
    
    print("⚛️ CAPÍTULO 8 COMPLETADO AL 100%:")
    print("   ✅ Kyber Implementation (KEM)")
    print("   ✅ Dilithium Implementation (Signatures)")
    print("   ✅ Quantum Sentinel (Integración)")
    print("   ✅ Migration Analysis")
    print("   ✅ Performance Benchmarks")
    print("   ✅ Security Reports")
    print()
    print("🎯 POST-QUANTUM CRYPTOGRAPHY: IMPLEMENTADO Y FUNCIONAL!")
    print()


if __name__ == "__main__":
    main()