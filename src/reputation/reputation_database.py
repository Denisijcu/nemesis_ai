#!/usr/bin/env python3
"""
Némesis IA - Reputation Database
Capítulo 7: Sistema de Reputación de IPs

Base de datos para persistir reputaciones, whitelist, blacklist
"""

import logging
import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from pathlib import Path

from .ip_checker import IPReputation

logger = logging.getLogger(__name__)


class ReputationDatabase:
    """Base de datos de reputación de IPs"""
    
    def __init__(self, db_path: str = "data/reputation.db"):
        """
        Inicializa la base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = db_path
        
        # Crear directorio si no existe
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Inicializar BD
        self._init_database()
        
        logger.info(f"💾 ReputationDatabase inicializada: {db_path}")
    
    def _init_database(self):
        """Inicializa las tablas de la base de datos"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabla de reputaciones
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ip_reputations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    reputation_score INTEGER NOT NULL,
                    threat_level TEXT NOT NULL,
                    country TEXT,
                    city TEXT,
                    isp TEXT,
                    asn TEXT,
                    abuse_reports INTEGER DEFAULT 0,
                    categories TEXT,
                    data_source TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    check_count INTEGER DEFAULT 1
                )
            """)
            
            # Índice en IP
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_ip 
                ON ip_reputations(ip)
            """)
            
            # Tabla de whitelist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS whitelist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT UNIQUE NOT NULL,
                    reason TEXT,
                    added_by TEXT DEFAULT 'SYSTEM',
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabla de blacklist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS blacklist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT UNIQUE NOT NULL,
                    reason TEXT,
                    severity TEXT DEFAULT 'HIGH',
                    added_by TEXT DEFAULT 'SYSTEM',
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            """)
            
            # Tabla de historial de reputación
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reputation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    reputation_score INTEGER NOT NULL,
                    threat_level TEXT NOT NULL,
                    event_type TEXT,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Índice en historial
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_ip 
                ON reputation_history(ip)
            """)
            
            conn.commit()
    
    def save_reputation(self, reputation: IPReputation):
        """
        Guarda o actualiza reputación de una IP
        
        Args:
            reputation: IPReputation a guardar
        """
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Verificar si ya existe
            cursor.execute("SELECT id, check_count FROM ip_reputations WHERE ip = ?", 
                          (reputation.ip,))
            existing = cursor.fetchone()
            
            categories_str = ','.join(reputation.categories) if reputation.categories else ''
            
            if existing:
                # Actualizar
                cursor.execute("""
                    UPDATE ip_reputations 
                    SET reputation_score = ?,
                        threat_level = ?,
                        country = ?,
                        city = ?,
                        isp = ?,
                        asn = ?,
                        abuse_reports = ?,
                        categories = ?,
                        data_source = ?,
                        last_checked = ?,
                        check_count = check_count + 1
                    WHERE ip = ?
                """, (
                    reputation.reputation_score,
                    reputation.threat_level,
                    reputation.country,
                    reputation.city,
                    reputation.isp,
                    reputation.asn,
                    reputation.abuse_reports,
                    categories_str,
                    reputation.data_source,
                    reputation.checked_at,
                    reputation.ip
                ))
                
                logger.debug(f"Reputación actualizada: {reputation.ip}")
            else:
                # Insertar nueva
                cursor.execute("""
                    INSERT INTO ip_reputations 
                    (ip, reputation_score, threat_level, country, city, isp, asn, 
                     abuse_reports, categories, data_source, last_checked)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    reputation.ip,
                    reputation.reputation_score,
                    reputation.threat_level,
                    reputation.country,
                    reputation.city,
                    reputation.isp,
                    reputation.asn,
                    reputation.abuse_reports,
                    categories_str,
                    reputation.data_source,
                    reputation.checked_at
                ))
                
                logger.debug(f"Nueva reputación guardada: {reputation.ip}")
            
            # Guardar en historial
            cursor.execute("""
                INSERT INTO reputation_history (ip, reputation_score, threat_level, event_type)
                VALUES (?, ?, ?, ?)
            """, (
                reputation.ip,
                reputation.reputation_score,
                reputation.threat_level,
                'CHECK'
            ))
            
            conn.commit()
    
    def get_reputation(self, ip: str) -> Optional[IPReputation]:
        """
        Obtiene reputación guardada de una IP
        
        Args:
            ip: Dirección IP
            
        Returns:
            IPReputation si existe, None si no
        """
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ip, reputation_score, threat_level, country, city, isp, asn,
                       abuse_reports, categories, data_source, last_checked
                FROM ip_reputations
                WHERE ip = ?
            """, (ip,))
            
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Verificar si está en whitelist/blacklist
            is_whitelisted = self.is_whitelisted(ip)
            is_blacklisted = self.is_blacklisted(ip)
            
            categories = row[8].split(',') if row[8] else []
            
            return IPReputation(
                ip=row[0],
                reputation_score=row[1],
                is_blacklisted=is_blacklisted,
                is_whitelisted=is_whitelisted,
                threat_level=row[2],
                country=row[3],
                city=row[4],
                isp=row[5],
                asn=row[6],
                abuse_reports=row[7],
                categories=categories,
                data_source=row[9],
                checked_at=datetime.fromisoformat(row[10]) if row[10] else None
            )
    
    def add_to_whitelist(self, ip: str, reason: str = None, added_by: str = "SYSTEM"):
        """Añade IP a whitelist"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO whitelist (ip, reason, added_by)
                    VALUES (?, ?, ?)
                """, (ip, reason, added_by))
                
                conn.commit()
                logger.info(f"✅ {ip} añadida a whitelist: {reason}")
                
                # Registrar en historial
                cursor.execute("""
                    INSERT INTO reputation_history (ip, reputation_score, threat_level, event_type)
                    VALUES (?, 100, 'LOW', 'WHITELISTED')
                """, (ip,))
                conn.commit()
                
            except sqlite3.IntegrityError:
                logger.warning(f"IP ya está en whitelist: {ip}")
    
    def add_to_blacklist(self, ip: str, reason: str = None, severity: str = "HIGH", 
                        expires_in_days: int = None, added_by: str = "SYSTEM"):
        """Añade IP a blacklist"""
        
        expires_at = None
        if expires_in_days:
            expires_at = datetime.now() + timedelta(days=expires_in_days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO blacklist (ip, reason, severity, added_by, expires_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (ip, reason, severity, added_by, expires_at))
                
                conn.commit()
                logger.info(f"🚫 {ip} añadida a blacklist: {reason} (severity: {severity})")
                
                # Registrar en historial
                cursor.execute("""
                    INSERT INTO reputation_history (ip, reputation_score, threat_level, event_type)
                    VALUES (?, 0, 'CRITICAL', 'BLACKLISTED')
                """, (ip,))
                conn.commit()
                
            except sqlite3.IntegrityError:
                logger.warning(f"IP ya está en blacklist: {ip}")
    
    def is_whitelisted(self, ip: str) -> bool:
        """Verifica si IP está en whitelist"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM whitelist WHERE ip = ?", (ip,))
            return cursor.fetchone() is not None
    
    def is_blacklisted(self, ip: str) -> bool:
        """Verifica si IP está en blacklist (y no expirada)"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1 FROM blacklist 
                WHERE ip = ? 
                AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            """, (ip,))
            return cursor.fetchone() is not None
    
    def remove_from_whitelist(self, ip: str):
        """Remueve IP de whitelist"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM whitelist WHERE ip = ?", (ip,))
            conn.commit()
            logger.info(f"Removida de whitelist: {ip}")
    
    def remove_from_blacklist(self, ip: str):
        """Remueve IP de blacklist"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blacklist WHERE ip = ?", (ip,))
            conn.commit()
            logger.info(f"Removida de blacklist: {ip}")
    
    def get_top_malicious_ips(self, limit: int = 10) -> List[tuple]:
        """Obtiene las IPs más maliciosas"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT ip, reputation_score, threat_level, country, isp, check_count
                FROM ip_reputations
                WHERE reputation_score < 50
                ORDER BY reputation_score ASC, check_count DESC
                LIMIT ?
            """, (limit,))
            
            return cursor.fetchall()
    
    def get_reputation_history(self, ip: str, limit: int = 50) -> List[Dict]:
        """Obtiene historial de reputación de una IP"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT reputation_score, threat_level, event_type, recorded_at
                FROM reputation_history
                WHERE ip = ?
                ORDER BY recorded_at DESC
                LIMIT ?
            """, (ip, limit))
            
            return [
                {
                    "score": row[0],
                    "threat_level": row[1],
                    "event": row[2],
                    "timestamp": row[3]
                }
                for row in cursor.fetchall()
            ]
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de la base de datos"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total IPs tracked
            cursor.execute("SELECT COUNT(*) FROM ip_reputations")
            total_ips = cursor.fetchone()[0]
            
            # Whitelisted
            cursor.execute("SELECT COUNT(*) FROM whitelist")
            whitelisted = cursor.fetchone()[0]
            
            # Blacklisted (no expiradas)
            cursor.execute("""
                SELECT COUNT(*) FROM blacklist 
                WHERE expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP
            """)
            blacklisted = cursor.fetchone()[0]
            
            # Por threat level
            cursor.execute("""
                SELECT threat_level, COUNT(*) 
                FROM ip_reputations 
                GROUP BY threat_level
            """)
            by_threat = dict(cursor.fetchall())
            
            # Por país
            cursor.execute("""
                SELECT country, COUNT(*) 
                FROM ip_reputations 
                WHERE country IS NOT NULL
                GROUP BY country
                ORDER BY COUNT(*) DESC
                LIMIT 10
            """)
            by_country = dict(cursor.fetchall())
            
            # Score promedio
            cursor.execute("SELECT AVG(reputation_score) FROM ip_reputations")
            avg_score = cursor.fetchone()[0] or 0
            
            return {
                "total_ips_tracked": total_ips,
                "whitelisted": whitelisted,
                "blacklisted": blacklisted,
                "by_threat_level": by_threat,
                "top_countries": by_country,
                "average_score": round(avg_score, 2)
            }
    
    def cleanup_expired(self):
        """Limpia entradas expiradas de la blacklist"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM blacklist 
                WHERE expires_at IS NOT NULL 
                AND expires_at <= CURRENT_TIMESTAMP
            """)
            
            removed = cursor.rowcount
            conn.commit()
            
            if removed > 0:
                logger.info(f"Limpiadas {removed} entradas expiradas de blacklist")
            
            return removed
    
    def decay_reputations(self, days_old: int = 30, decay_amount: int = 10):
        """
        Aplica decay a reputaciones viejas
        IPs no vistas recientemente mejoran su score gradualmente
        """
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Mejorar scores de IPs no vistas recientemente
            cursor.execute("""
                UPDATE ip_reputations
                SET reputation_score = MIN(100, reputation_score + ?)
                WHERE last_checked < ?
                AND reputation_score < 100
                AND ip NOT IN (SELECT ip FROM blacklist)
            """, (decay_amount, cutoff_date))
            
            updated = cursor.rowcount
            conn.commit()
            
            if updated > 0:
                logger.info(f"Decay aplicado a {updated} reputaciones")
            
            return updated