#!/usr/bin/env python3
"""
Némesis IA - Log Reader
Capítulo 3: El Centinela de Logs

Lee logs en tiempo real usando tail -f
"""

import asyncio
import logging
from pathlib import Path
from typing import AsyncGenerator, Optional

logger = logging.getLogger(__name__)


class LogReader:
    """Lee logs en tiempo real"""
    
    def __init__(self, log_file: str, follow: bool = True):
        """
        Inicializa el lector de logs
        
        Args:
            log_file: Ruta al archivo de log
            follow: Si True, hace tail -f (sigue el archivo)
        """
        self.log_file = Path(log_file)
        self.follow = follow
        self._process: Optional[asyncio.subprocess.Process] = None
        self._is_running = False
        
        logger.info(f"📖 LogReader inicializado: {self.log_file}")
    
    async def start(self) -> AsyncGenerator[str, None]:
        """
        Inicia la lectura de logs
        
        Yields:
            Líneas de log
        """
        if not self.log_file.exists():
            logger.error(f"❌ Archivo no existe: {self.log_file}")
            return
        
        self._is_running = True
        
        if self.follow:
            # Usar tail -f para seguir el archivo
            cmd = ["tail", "-f", str(self.log_file)]
            logger.info(f"🚀 Iniciando tail -f en {self.log_file}")
        else:
            # Leer archivo completo
            cmd = ["cat", str(self.log_file)]
            logger.info(f"📄 Leyendo archivo completo: {self.log_file}")
        
        try:
            self._process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            while self._is_running:
                line = await self._process.stdout.readline()
                
                if not line:
                    break
                
                decoded_line = line.decode('utf-8').strip()
                
                if decoded_line:
                    yield decoded_line
        
        except Exception as e:
            logger.error(f"❌ Error leyendo logs: {e}")
        
        finally:
            await self.stop()
    
    async def stop(self):
        """Detiene la lectura de logs"""
        self._is_running = False
        
        if self._process and self._process.returncode is None:
            try:
                self._process.terminate()
                await asyncio.wait_for(self._process.wait(), timeout=2.0)
                logger.info("✅ LogReader detenido")
            except asyncio.TimeoutError:
                self._process.kill()
                await self._process.wait()
                logger.warning("⚠️  LogReader forzado a terminar")
            except ProcessLookupError:
                logger.info("✅ LogReader ya estaba detenido")
        else:
            logger.info("✅ LogReader detenido")