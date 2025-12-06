#!/usr/bin/env python3
"""
Némesis IA - Fake SSH Honeypot
Capítulo 5: Honeypots Inteligentes

Servidor SSH falso que registra intentos de login
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SSHAttempt:
    """Registro de un intento de login SSH"""
    timestamp: datetime
    attacker_ip: str
    attacker_port: int
    username: str
    password: str
    success: bool = False


class FakeSSH:
    """Servidor SSH falso - La Trampa"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 2222, callback: Optional[Callable] = None):
        """
        Inicializa el FakeSSH
        
        Args:
            host: Host del servidor (0.0.0.0 = todas las interfaces)
            port: Puerto (2222 por defecto, no 22 para evitar conflicto)
            callback: Función a llamar cuando hay un intento
        """
        self.host = host
        self.port = port
        self.callback = callback
        
        self.attempts = []
        self.server = None
        self._is_running = False
        
        logger.info(f"🍯 FakeSSH inicializado en {host}:{port}")
    
    async def start(self):
        """Inicia el servidor SSH falso"""
        logger.info(f"🚀 Iniciando FakeSSH en {self.host}:{self.port}...")
        
        self.server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port
        )
        
        self._is_running = True
        
        logger.info(f"✅ FakeSSH escuchando en puerto {self.port}")
        logger.info("🎣 Esperando conexiones maliciosas...")
        
        async with self.server:
            await self.server.serve_forever()
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Maneja una conexión de cliente"""
        
        # Obtener IP del atacante
        addr = writer.get_extra_info('peername')
        attacker_ip = addr[0]
        attacker_port = addr[1]
        
        logger.warning(f"🚨 Nueva conexión desde {attacker_ip}:{attacker_port}")
        
        try:
            # Enviar banner SSH falso
            banner = b"SSH-2.0-OpenSSH_7.4\r\n"
            writer.write(banner)
            await writer.drain()
            
            # Simular prompt de login
            writer.write(b"\r\nUbuntu 20.04.3 LTS\r\n")
            writer.write(f"{attacker_ip} login: ".encode())
            await writer.drain()
            
            # Leer username
            username_data = await asyncio.wait_for(reader.readline(), timeout=30.0)
            username = username_data.decode('utf-8', errors='ignore').strip()
            
            if not username:
                writer.close()
                await writer.wait_closed()
                return
            
            logger.info(f"👤 Username intentado: {username}")
            
            # Pedir password
            writer.write(b"Password: ")
            await writer.drain()
            
            # Leer password
            password_data = await asyncio.wait_for(reader.readline(), timeout=30.0)
            password = password_data.decode('utf-8', errors='ignore').strip()
            
            logger.warning(f"🔑 Password intentado: {password}")
            
            # Registrar intento
            attempt = SSHAttempt(
                timestamp=datetime.now(),
                attacker_ip=attacker_ip,
                attacker_port=attacker_port,
                username=username,
                password=password,
                success=False
            )
            
            self.attempts.append(attempt)
            
            # Callback
            if self.callback:
                await self.callback(attempt)
            
            # Simular delay de auth
            await asyncio.sleep(1)
            
            # Siempre rechazar
            writer.write(b"\r\nPermission denied, please try again.\r\n")
            await writer.drain()
            
            # Cerrar conexión
            writer.close()
            await writer.wait_closed()
            
            logger.info(f"🔒 Conexión cerrada de {attacker_ip}")
        
        except asyncio.TimeoutError:
            logger.warning(f"⏰ Timeout esperando datos de {attacker_ip}")
        except Exception as e:
            logger.error(f"❌ Error manejando cliente {attacker_ip}: {e}")
        finally:
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
    
    async def stop(self):
        """Detiene el servidor"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self._is_running = False
            logger.info("⏹️  FakeSSH detenido")
    
    @property
    def stats(self):
        """Retorna estadísticas"""
        unique_ips = len(set(a.attacker_ip for a in self.attempts))
        unique_users = len(set(a.username for a in self.attempts))
        unique_passwords = len(set(a.password for a in self.attempts))
        
        return {
            "total_attempts": len(self.attempts),
            "unique_ips": unique_ips,
            "unique_usernames": unique_users,
            "unique_passwords": unique_passwords,
            "is_running": self._is_running
        }