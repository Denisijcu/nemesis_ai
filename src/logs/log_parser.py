#!/usr/bin/env python3
"""
Némesis IA - Log Parser
Capítulo 3: El Centinela de Logs

Parsea diferentes formatos de logs
"""

import re
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ParsedLog:
    """Log parseado"""
    timestamp: datetime
    source_ip: str
    method: str
    path: str
    status_code: int
    raw_line: str
    format_type: str


class LogParser:
    """Parsea logs de diferentes formatos"""
    
    # Regex para Apache/Nginx Common Log Format
    APACHE_PATTERN = re.compile(
        r'^(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<path>[^\s]+) HTTP/[\d\.]+" '
        r'(?P<status>\d+)'
    )
    
    # Regex para formato alternativo
    NGINX_PATTERN = re.compile(
        r'^(?P<ip>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] '
        r'"(?P<method>\w+) (?P<path>[^\s"]+)'
    )
    
    def parse(self, log_line: str) -> Optional[ParsedLog]:
        """
        Parsea una línea de log
        
        Args:
            log_line: Línea de log a parsear
            
        Returns:
            ParsedLog o None si no se puede parsear
        """
        # Intentar Apache/Nginx format
        parsed = self._parse_apache(log_line)
        if parsed:
            return parsed
        
        # Intentar formato alternativo
        parsed = self._parse_nginx(log_line)
        if parsed:
            return parsed
        
        logger.debug(f"⚠️  No se pudo parsear: {log_line[:50]}...")
        return None
    
    def _parse_apache(self, log_line: str) -> Optional[ParsedLog]:
        """Parsea formato Apache/Nginx"""
        match = self.APACHE_PATTERN.match(log_line)
        
        if not match:
            return None
        
        try:
            groups = match.groupdict()
            
            # Parsear timestamp
            timestamp_str = groups['timestamp']
            timestamp = self._parse_timestamp(timestamp_str)
            
            return ParsedLog(
                timestamp=timestamp,
                source_ip=groups['ip'],
                method=groups['method'],
                path=groups['path'],
                status_code=int(groups['status']),
                raw_line=log_line,
                format_type="apache"
            )
        
        except Exception as e:
            logger.debug(f"Error parseando Apache log: {e}")
            return None
    
    def _parse_nginx(self, log_line: str) -> Optional[ParsedLog]:
        """Parsea formato Nginx alternativo"""
        match = self.NGINX_PATTERN.match(log_line)
        
        if not match:
            return None
        
        try:
            groups = match.groupdict()
            
            timestamp_str = groups['timestamp']
            timestamp = self._parse_timestamp(timestamp_str)
            
            return ParsedLog(
                timestamp=timestamp,
                source_ip=groups['ip'],
                method=groups['method'],
                path=groups['path'],
                status_code=200,  # Default
                raw_line=log_line,
                format_type="nginx"
            )
        
        except Exception as e:
            logger.debug(f"Error parseando Nginx log: {e}")
            return None
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parsea timestamp de log"""
        # Formato: 04/Dec/2025:10:00:00 +0000
        try:
            # Remover timezone si existe
            if '+' in timestamp_str or '-' in timestamp_str:
                timestamp_str = timestamp_str.split()[0]
            
            return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
        except:
            return datetime.now()