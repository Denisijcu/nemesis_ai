#!/usr/bin/env python3
"""
Némesis IA - Forensic Sentinel
Capítulo 9: Blockchain Forense

Sistema integrador de evidencia forense con blockchain
"""

import logging
import hashlib
from datetime import datetime
from typing import Dict, Optional, List

from .blockchain_evidence import BlockchainEvidence, EvidenceBlock
from .chain_of_custody import ChainOfCustody, CustodyAction

logger = logging.getLogger(__name__)


class ForensicSentinel:
    """Sistema completo de evidencia forense con blockchain"""
    
    def __init__(self, threat_database=None):
        """
        Inicializa Forensic Sentinel
        
        Args:
            threat_database: ThreatDatabase para integración
        """
        
        # Componentes forenses
        self.blockchain = BlockchainEvidence()
        self.custody = ChainOfCustody()
        
        # Integración
        self.threat_database = threat_database
        
        # Estadísticas
        self.stats = {
            "threats_processed": 0,
            "evidence_collected": 0,
            "custody_transfers": 0,
            "integrity_checks": 0
        }
        
        logger.info("🔬 ForensicSentinel inicializado")
    
    def collect_threat_evidence(
        self,
        threat_data: Dict,
        collected_by: str = "NEMESIS_IA",
        classification: str = "CONFIDENTIAL"
    ) -> tuple[EvidenceBlock, str]:
        """
        Recolecta evidencia de una amenaza y la guarda en blockchain
        
        Args:
            threat_data: Datos de la amenaza
            collected_by: Quien recolecta
            classification: Nivel de clasificación
            
        Returns:
            Tuple (EvidenceBlock, evidence_id)
        """
        
        logger.info(f"🔬 Recolectando evidencia de amenaza...")
        
        # Generar ID de evidencia
        evidence_id = self._generate_evidence_id(threat_data)
        
        # Calcular hash de la evidencia
        evidence_hash = self._hash_evidence(threat_data)
        
        # Preparar datos para blockchain
        blockchain_data = {
            "type": "THREAT_EVIDENCE",
            "evidence_id": evidence_id,
            "threat_type": threat_data.get("attack_type", "UNKNOWN"),
            "source_ip": threat_data.get("source_ip", "UNKNOWN"),
            "timestamp": threat_data.get("timestamp", datetime.now().isoformat()),
            "confidence": threat_data.get("confidence", 0.0),
            "evidence_hash": evidence_hash,
            "collected_at": datetime.now().isoformat(),
            "data": threat_data
        }
        
        # Añadir a blockchain
        block = self.blockchain.add_evidence(
            evidence_data=blockchain_data,
            collected_by=collected_by,
            classification=classification
        )
        
        # Registrar en chain of custody
        self.custody.record_collection(
            evidence_id=evidence_id,
            handler=collected_by,
            location="EVIDENCE_STORAGE",
            evidence_hash=evidence_hash,
            notes=f"Threat type: {blockchain_data['threat_type']}"
        )
        
        self.stats["threats_processed"] += 1
        self.stats["evidence_collected"] += 1
        
        logger.info(f"✅ Evidencia recolectada: {evidence_id}")
        
        return block, evidence_id
    
    def transfer_evidence(
        self,
        evidence_id: str,
        from_handler: str,
        to_handler: str,
        reason: str,
        witnessed_by: Optional[str] = None
    ) -> bool:
        """
        Transfiere custodia de evidencia
        
        Args:
            evidence_id: ID de la evidencia
            from_handler: Handler actual
            to_handler: Nuevo handler
            reason: Razón de la transferencia
            witnessed_by: Testigo
            
        Returns:
            True si exitoso
        """
        
        logger.info(f"🔄 Transfiriendo evidencia {evidence_id}...")
        
        # Buscar bloque en blockchain
        blocks = self.blockchain.search_evidence({"evidence_id": evidence_id})
        
        if not blocks:
            logger.error(f"❌ Evidencia {evidence_id} no encontrada en blockchain")
            return False
        
        original_block = blocks[0]
        evidence_hash = original_block.evidence_data.get("evidence_hash")
        
        # Registrar transferencia en custody
        self.custody.record_transfer(
            evidence_id=evidence_id,
            from_handler=from_handler,
            to_handler=to_handler,
            from_location="EVIDENCE_STORAGE",
            to_location="ANALYSIS_LAB",
            reason=reason,
            evidence_hash=evidence_hash,
            witnessed_by=witnessed_by
        )
        
        # Añadir bloque de transferencia a blockchain
        self.blockchain.add_custody_handler(
            block_index=original_block.index,
            handler=to_handler
        )
        
        self.stats["custody_transfers"] += 1
        
        logger.info(f"✅ Evidencia transferida: {from_handler} → {to_handler}")
        
        return True
    
    def verify_evidence_integrity(self, evidence_id: str) -> Dict:
        """
        Verifica integridad completa de evidencia
        
        Args:
            evidence_id: ID de la evidencia
            
        Returns:
            Diccionario con resultados de verificación
        """
        
        logger.info(f"🔍 Verificando integridad: {evidence_id}")
        
        self.stats["integrity_checks"] += 1
        
        # Verificar blockchain
        blockchain_valid = self.blockchain.validate_chain()
        
        # Verificar custody chain
        custody_valid = self.custody.verify_integrity(evidence_id)
        
        # Buscar evidencia
        blocks = self.blockchain.search_evidence({"evidence_id": evidence_id})
        
        if not blocks:
            return {
                "valid": False,
                "reason": "Evidence not found in blockchain"
            }
        
        return {
            "valid": blockchain_valid and custody_valid,
            "blockchain_valid": blockchain_valid,
            "custody_chain_valid": custody_valid,
            "evidence_id": evidence_id,
            "block_index": blocks[0].index,
            "block_hash": blocks[0].hash,
            "checked_at": datetime.now().isoformat()
        }
    
    def _generate_evidence_id(self, threat_data: Dict) -> str:
        """Genera ID único para evidencia"""
        
        unique_string = (
            str(threat_data.get("source_ip", "")) +
            str(threat_data.get("timestamp", "")) +
            str(datetime.now().timestamp())
        )
        
        return "EVD-" + hashlib.md5(unique_string.encode()).hexdigest()[:16].upper()
    
    def _hash_evidence(self, evidence_data: Dict) -> str:
        """Calcula hash SHA-256 de evidencia"""
        
        import json
        evidence_str = json.dumps(evidence_data, sort_keys=True)
        return hashlib.sha256(evidence_str.encode()).hexdigest()
    
    def search_evidence(self, criteria: Dict) -> List[EvidenceBlock]:
        """Busca evidencia en blockchain"""
        return self.blockchain.search_evidence(criteria)
    
    def get_custody_report(self, evidence_id: str) -> str:
        """Genera reporte de custodia"""
        return self.custody.generate_custody_report(evidence_id)
    
    def get_integrity_report(self) -> str:
        """Genera reporte de integridad"""
        return self.blockchain.generate_integrity_report()
    
    def export_evidence(self, filepath: str):
        """Exporta toda la evidencia"""
        self.blockchain.export_chain(filepath)
        logger.info(f"💾 Evidencia exportada: {filepath}")
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas completas"""
        
        blockchain_stats = self.blockchain.get_statistics()
        
        return {
            "sentinel": self.stats,
            "blockchain": blockchain_stats,
            "total_evidence": len(self.custody.custody_records)
        }
    
    def generate_legal_package(self, evidence_id: str) -> Dict:
        """
        Genera paquete legal completo para una evidencia
        
        Args:
            evidence_id: ID de la evidencia
            
        Returns:
            Diccionario con todos los documentos legales
        """
        
        logger.info(f"⚖️ Generando paquete legal: {evidence_id}")
        
        # Verificar integridad
        integrity = self.verify_evidence_integrity(evidence_id)
        
        # Obtener reportes
        custody_report = self.get_custody_report(evidence_id)
        integrity_report = self.get_integrity_report()
        
        # Buscar evidencia
        blocks = self.blockchain.search_evidence({"evidence_id": evidence_id})
        
        if not blocks:
            return {"error": "Evidence not found"}
        
        evidence_block = blocks[0]
        
        return {
            "evidence_id": evidence_id,
            "generated_at": datetime.now().isoformat(),
            "integrity_verified": integrity["valid"],
            "evidence_block": evidence_block.to_dict(),
            "custody_report": custody_report,
            "blockchain_integrity_report": integrity_report,
            "admissible": integrity["valid"],
            "compliance": "ISO/IEC 27037:2012"
        }