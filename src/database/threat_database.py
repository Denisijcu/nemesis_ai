#!/usr/bin/env python3
"""
Némesis IA - Threat Database
Sistema de persistencia con SQLite

Almacena amenazas, IPs bloqueadas y estadísticas
"""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ThreatRecord:
    """Registro de amenaza en la BD"""
    id: Optional[int]
    timestamp: datetime
    source_ip: str
    attack_type: str
    payload: str
    confidence: float
    action_taken: str
    blocked: bool


class ThreatDatabase:
    """Base de datos de amenazas con SQLite"""
    
    def __init__(self, db_path: str = "data/nemesis.db"):
        """
        Inicializa la base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.conn: Optional[sqlite3.Connection] = None
        self._init_database()
        
        logger.info(f"💾 ThreatDatabase inicializada: {self.db_path}")
    
    def _init_database(self):
        """Inicializa las tablas de la base de datos"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Tabla de amenazas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                attack_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                confidence REAL NOT NULL,
                action_taken TEXT NOT NULL,
                blocked BOOLEAN NOT NULL
            )
        """)
        
        # Tabla de IPs bloqueadas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocked_ips (
                ip TEXT PRIMARY KEY,
                blocked_at TEXT NOT NULL,
                reason TEXT NOT NULL,
                threat_count INTEGER DEFAULT 1
            )
        """)
        
        # Tabla de estadísticas diarias
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                total_logs INTEGER DEFAULT 0,
                threats_detected INTEGER DEFAULT 0,
                ips_blocked INTEGER DEFAULT 0,
                sql_injection INTEGER DEFAULT 0,
                xss INTEGER DEFAULT 0,
                path_traversal INTEGER DEFAULT 0,
                command_injection INTEGER DEFAULT 0,
                other INTEGER DEFAULT 0
            )
        """)
        
        # Índices para búsquedas rápidas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_threats_timestamp 
            ON threats(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_threats_source_ip 
            ON threats(source_ip)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_threats_attack_type 
            ON threats(attack_type)
        """)
        
        self.conn.commit()
        logger.info("✅ Tablas de BD inicializadas")
    
    def save_threat(self, threat: ThreatRecord) -> int:
        """
        Guarda una amenaza en la BD
        
        Args:
            threat: Registro de amenaza
            
        Returns:
            ID del registro insertado
        """
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO threats 
            (timestamp, source_ip, attack_type, payload, confidence, action_taken, blocked)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            threat.timestamp.isoformat(),
            threat.source_ip,
            threat.attack_type,
            threat.payload,
            threat.confidence,
            threat.action_taken,
            threat.blocked
        ))
        
        self.conn.commit()
        threat_id = cursor.lastrowid
        
        # Actualizar estadísticas
        self._update_daily_stats(threat)
        
        logger.debug(f"💾 Amenaza guardada: ID={threat_id}")
        return threat_id
    
    def block_ip(self, ip: str, reason: str):
        """
        Registra una IP bloqueada
        
        Args:
            ip: Dirección IP
            reason: Razón del bloqueo
        """
        cursor = self.conn.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT threat_count FROM blocked_ips WHERE ip = ?", (ip,))
        row = cursor.fetchone()
        
        if row:
            # Incrementar contador
            cursor.execute("""
                UPDATE blocked_ips 
                SET threat_count = threat_count + 1
                WHERE ip = ?
            """, (ip,))
        else:
            # Insertar nueva IP
            cursor.execute("""
                INSERT INTO blocked_ips (ip, blocked_at, reason, threat_count)
                VALUES (?, ?, ?, 1)
            """, (ip, datetime.now().isoformat(), reason))
        
        self.conn.commit()
        logger.debug(f"🚫 IP bloqueada registrada: {ip}")
    
    def get_threats(
        self, 
        limit: int = 100, 
        attack_type: Optional[str] = None,
        source_ip: Optional[str] = None
    ) -> List[ThreatRecord]:
        """
        Obtiene amenazas de la BD
        
        Args:
            limit: Número máximo de registros
            attack_type: Filtrar por tipo de ataque
            source_ip: Filtrar por IP
            
        Returns:
            Lista de amenazas
        """
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM threats WHERE 1=1"
        params = []
        
        if attack_type:
            query += " AND attack_type = ?"
            params.append(attack_type)
        
        if source_ip:
            query += " AND source_ip = ?"
            params.append(source_ip)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        threats = []
        for row in rows:
            threat = ThreatRecord(
                id=row['id'],
                timestamp=datetime.fromisoformat(row['timestamp']),
                source_ip=row['source_ip'],
                attack_type=row['attack_type'],
                payload=row['payload'],
                confidence=row['confidence'],
                action_taken=row['action_taken'],
                blocked=bool(row['blocked'])
            )
            threats.append(threat)
        
        return threats
    
    def get_blocked_ips(self) -> List[Dict]:
        """Obtiene lista de IPs bloqueadas"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT ip, blocked_at, reason, threat_count 
            FROM blocked_ips 
            ORDER BY blocked_at DESC
        """)
        
        rows = cursor.fetchall()
        
        blocked_ips = []
        for row in rows:
            blocked_ips.append({
                'ip': row['ip'],
                'blocked_at': row['blocked_at'],
                'reason': row['reason'],
                'threat_count': row['threat_count']
            })
        
        return blocked_ips
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas globales"""
        cursor = self.conn.cursor()
        
        # Total de amenazas
        cursor.execute("SELECT COUNT(*) as total FROM threats")
        total_threats = cursor.fetchone()['total']
        
        # Amenazas por tipo
        cursor.execute("""
            SELECT attack_type, COUNT(*) as count 
            FROM threats 
            GROUP BY attack_type
        """)
        threats_by_type = {row['attack_type']: row['count'] for row in cursor.fetchall()}
        
        # Total de IPs bloqueadas
        cursor.execute("SELECT COUNT(*) as total FROM blocked_ips")
        total_blocked_ips = cursor.fetchone()['total']
        
        # Top 10 IPs más maliciosas
        cursor.execute("""
            SELECT source_ip, COUNT(*) as count 
            FROM threats 
            GROUP BY source_ip 
            ORDER BY count DESC 
            LIMIT 10
        """)
        top_ips = [(row['source_ip'], row['count']) for row in cursor.fetchall()]
        
        # Amenazas últimas 24h
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM threats 
            WHERE timestamp > datetime('now', '-1 day')
        """)
        last_24h = cursor.fetchone()['count']
        
        return {
            'total_threats': total_threats,
            'threats_by_type': threats_by_type,
            'total_blocked_ips': total_blocked_ips,
            'top_malicious_ips': top_ips,
            'threats_last_24h': last_24h
        }
    
    def _update_daily_stats(self, threat: ThreatRecord):
        """Actualiza estadísticas diarias"""
        cursor = self.conn.cursor()
        
        date = threat.timestamp.date().isoformat()
        
        # Obtener o crear registro del día
        cursor.execute("SELECT * FROM daily_stats WHERE date = ?", (date,))
        row = cursor.fetchone()
        
        if row:
            # Actualizar existente
            attack_col = threat.attack_type.lower()
            if attack_col not in ['sql_injection', 'xss', 'path_traversal', 'command_injection']:
                attack_col = 'other'
            
            cursor.execute(f"""
                UPDATE daily_stats 
                SET total_logs = total_logs + 1,
                    threats_detected = threats_detected + 1,
                    {attack_col} = {attack_col} + 1
                WHERE date = ?
            """, (date,))
        else:
            # Crear nuevo
            cursor.execute("""
                INSERT INTO daily_stats (date, total_logs, threats_detected)
                VALUES (?, 1, 1)
            """, (date,))
        
        self.conn.commit()
    
    def close(self):
        """Cierra la conexión a la BD"""
        if self.conn:
            self.conn.close()
            logger.info("💾 Conexión a BD cerrada")