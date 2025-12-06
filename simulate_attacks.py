#!/usr/bin/env python3
"""
Simula diferentes tipos de ataques al honeypot
"""

import socket
import time
import sys


def send_ssh_attempt(username: str, password: str, port: int = 2222):
    """Envía un intento de login SSH"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', port))
        
        # Recibir banner
        banner = sock.recv(1024)
        
        # Recibir prompt "login:"
        prompt = sock.recv(1024)
        
        # Enviar username
        sock.send(f"{username}\n".encode())
        time.sleep(0.1)
        
        # Recibir "Password:"
        sock.recv(1024)
        
        # Enviar password
        sock.send(f"{password}\n".encode())
        time.sleep(0.1)
        
        # Recibir respuesta
        response = sock.recv(1024)
        
        sock.close()
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def brute_force_attack():
    """Simula ataque de fuerza bruta"""
    print("=" * 70)
    print("🔴 SIMULANDO BRUTE FORCE ATTACK")
    print("=" * 70)
    print("   (Mismo usuario, muchos passwords)")
    print()
    
    username = "admin"
    
    for i in range(1, 11):
        password = f"password{i}"
        print(f"Intento {i}/10: {username} / {password}")
        
        if send_ssh_attempt(username, password):
            print(f"  ✅ Enviado")
        
        time.sleep(0.5)
    
    print()


def dictionary_attack():
    """Simula ataque de diccionario"""
    print("=" * 70)
    print("🟡 SIMULANDO DICTIONARY ATTACK")
    print("=" * 70)
    print("   (Usuarios comunes con passwords comunes)")
    print()
    
    credentials = [
        ("root", "root"),
        ("admin", "admin"),
        ("admin", "password"),
        ("test", "test"),
        ("guest", "guest"),
        ("user", "user123"),
        ("administrator", "admin123"),
        ("root", "toor"),
    ]
    
    for i, (username, password) in enumerate(credentials, 1):
        print(f"Intento {i}/{len(credentials)}: {username} / {password}")
        
        if send_ssh_attempt(username, password):
            print(f"  ✅ Enviado")
        
        time.sleep(0.5)
    
    print()


def credential_stuffing():
    """Simula credential stuffing"""
    print("=" * 70)
    print("🟠 SIMULANDO CREDENTIAL STUFFING")
    print("=" * 70)
    print("   (Muchos usuarios diferentes, mismo password)")
    print()
    
    password = "123456"
    usernames = [
        "john", "alice", "bob", "charlie", "david",
        "emily", "frank", "grace", "henry", "isabel"
    ]
    
    for i, username in enumerate(usernames, 1):
        print(f"Intento {i}/{len(usernames)}: {username} / {password}")
        
        if send_ssh_attempt(username, password):
            print(f"  ✅ Enviado")
        
        time.sleep(0.5)
    
    print()


def slow_brute_force():
    """Simula slow brute force (más sigiloso)"""
    print("=" * 70)
    print("🟣 SIMULANDO SLOW BRUTE FORCE")
    print("=" * 70)
    print("   (Intentos lentos para evitar detección)")
    print()
    
    username = "root"
    
    for i in range(1, 6):
        password = f"pass{i:03d}"
        print(f"Intento {i}/5: {username} / {password}")
        
        if send_ssh_attempt(username, password):
            print(f"  ✅ Enviado")
        
        print(f"  ⏰ Esperando 3 segundos...")
        time.sleep(3)
    
    print()


def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "SIMULADOR DE ATAQUES" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("⚠️  IMPORTANTE: Asegúrate que el honeypot esté corriendo")
    print("   En otra terminal ejecuta: python3 test_profiler.py")
    print()
    
    # Verificar que el honeypot esté activo
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 2222))
        sock.close()
        
        if result != 0:
            print("❌ ERROR: El honeypot no está corriendo en puerto 2222")
            print("   Ejecuta primero: python3 test_profiler.py")
            return
    except:
        print("❌ ERROR: No se puede conectar al honeypot")
        return
    
    print("✅ Honeypot detectado en puerto 2222")
    print()
    print("Selecciona tipo de ataque:")
    print("  1. Brute Force (10 intentos)")
    print("  2. Dictionary Attack (8 intentos)")
    print("  3. Credential Stuffing (10 intentos)")
    print("  4. Slow Brute Force (5 intentos lentos)")
    print("  5. TODOS (ejecutar todos los ataques)")
    print("  0. Salir")
    print()
    
    try:
        choice = input("Opción: ").strip()
        print()
        
        if choice == "1":
            brute_force_attack()
        elif choice == "2":
            dictionary_attack()
        elif choice == "3":
            credential_stuffing()
        elif choice == "4":
            slow_brute_force()
        elif choice == "5":
            print("🔥 EJECUTANDO TODOS LOS ATAQUES")
            print()
            brute_force_attack()
            time.sleep(2)
            dictionary_attack()
            time.sleep(2)
            credential_stuffing()
            time.sleep(2)
            slow_brute_force()
        elif choice == "0":
            print("👋 Saliendo...")
            return
        else:
            print("❌ Opción inválida")
            return
        
        print("=" * 70)
        print("✅ SIMULACIÓN COMPLETADA")
        print("=" * 70)
        print()
        print("💡 Revisa la terminal del honeypot para ver:")
        print("   • Intentos detectados")
        print("   • Perfiles de atacantes")
        print("   • Patrones identificados")
        print("   • Threat scores")
        print()
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulación detenida")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()