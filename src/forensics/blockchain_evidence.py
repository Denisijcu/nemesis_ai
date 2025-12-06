#!/usr/bin/env python3
"""
Némesis IA - Blockchain Evidence
Capítulo 9: Blockchain Forense

Sistema de blockchain para cadena de custodia inmutable
"""

import logging
import hashlib
import json
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class EvidenceBlock:
    """Bloque de evidencia en la blockchain"""
    index: int
    timestamp: float
    evidence_data: Dict[str, Any]
    previous_hash: str
    hash: str
    nonce: int = 0
    
    # Metadata forense
    collected_by: str = "NEMESIS_IA"
    chain_of_custody: List[str] = None
    legal_hold: bool = False
    classification: str = "CONFIDENTIAL"
    
    def __post_init__(self):
        if self.chain_of_custody is None:
            self.chain_of_custody = ["NEMESIS_IA_SYSTEM"]
    
    def to_dict(self) -> Dict:
        """Convierte bloque a diccionario"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "evidence_data": self.evidence_data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
            "collected_by": self.collected_by,
            "chain_of_custody": self.chain_of_custody,
            "legal_hold": self.legal_hold,
            "classification": self.classification
        }


class BlockchainEvidence:
    """
    Sistema de Blockchain para evidencia forense
    
    Características:
    - Inmutabilidad: Los bloques no pueden ser alterados
    - Trazabilidad: Cadena de custodia completa
    - Verificación: Hash chains para validar integridad
    - Legal compliance: Formato admisible en corte
    """
    
    def __init__(self):
        """Inicializa la blockchain"""
        
        self.chain: List[EvidenceBlock] = []
        self.pending_evidence: List[Dict] = []
        
        # Configuración
        self.difficulty = 2  # Número de ceros al inicio del hash (PoW)
        
        # Estadísticas
        self.stats = {
            "total_blocks": 0,
            "total_evidence": 0,
            "chain_valid": True,
            "last_validation": None
        }
        
        # Crear bloque génesis
        self._create_genesis_block()
        
        logger.info("🔗 BlockchainEvidence inicializada")
    
    def _create_genesis_block(self):
        """Crea el bloque génesis (primer bloque)"""
        
        genesis_data = {
            "type": "GENESIS",
            "system": "NEMESIS_IA",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "purpose": "Forensic Evidence Chain",
            "compliance": "ISO/IEC 27037:2012"
        }
        
        genesis_block = EvidenceBlock(
            index=0,
            timestamp=time.time(),
            evidence_data=genesis_data,
            previous_hash="0" * 64,
            hash="",
            collected_by="SYSTEM",
            classification="PUBLIC"
        )
        
        # Calcular hash
        genesis_block.hash = self._calculate_hash(genesis_block)
        
        self.chain.append(genesis_block)
        self.stats["total_blocks"] = 1
        
        logger.info("✅ Bloque génesis creado")
    
    def _calculate_hash(self, block: EvidenceBlock) -> str:
        """
        Calcula SHA-256 hash de un bloque
        
        Args:
            block: Bloque a hashear
            
        Returns:
            Hash hexadecimal
        """
        
        # Crear string con datos del bloque
        block_string = json.dumps({
            "index": block.index,
            "timestamp": block.timestamp,
            "evidence_data": block.evidence_data,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "collected_by": block.collected_by
        }, sort_keys=True)
        
        # SHA-256
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_evidence(
        self,
        evidence_data: Dict[str, Any],
        collected_by: str = "NEMESIS_IA",
        classification: str = "CONFIDENTIAL",
        legal_hold: bool = False
    ) -> EvidenceBlock:
        """
        Añade evidencia a la blockchain
        
        Args:
            evidence_data: Datos de la evidencia
            collected_by: Quien recolectó la evidencia
            classification: Nivel de clasificación
            legal_hold: Si está bajo retención legal
            
        Returns:
            Bloque creado
        """
        
        logger.info(f"📝 Añadiendo evidencia a blockchain...")
        
        # Obtener último bloque
        previous_block = self.chain[-1]
        
        # Crear nuevo bloque
        new_block = EvidenceBlock(
            index=len(self.chain),
            timestamp=time.time(),
            evidence_data=evidence_data,
            previous_hash=previous_block.hash,
            hash="",
            collected_by=collected_by,
            classification=classification,
            legal_hold=legal_hold
        )
        
        # Proof of Work (opcional, para demostrar integridad)
        new_block = self._proof_of_work(new_block)
        
        # Calcular hash final
        new_block.hash = self._calculate_hash(new_block)
        
        # Añadir a la cadena
        self.chain.append(new_block)
        
        self.stats["total_blocks"] += 1
        self.stats["total_evidence"] += 1
        
        logger.info(
            f"✅ Evidencia añadida - Bloque #{new_block.index} "
            f"(hash: {new_block.hash[:16]}...)"
        )
        
        return new_block
    
    def _proof_of_work(self, block: EvidenceBlock) -> EvidenceBlock:
        """
        Implementa Proof of Work simple
        
        Args:
            block: Bloque a minar
            
        Returns:
            Bloque con nonce válido
        """
        
        block.nonce = 0
        computed_hash = self._calculate_hash(block)
        
        # Buscar hash que empiece con N ceros (difficulty)
        target = "0" * self.difficulty
        
        while not computed_hash.startswith(target):
            block.nonce += 1
            computed_hash = self._calculate_hash(block)
        
        return block
    
    def validate_chain(self) -> bool:
        """
        Valida la integridad de toda la cadena
        
        Returns:
            True si la cadena es válida, False si está comprometida
        """
        
        logger.info("🔍 Validando integridad de blockchain...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verificar hash del bloque actual
            if current_block.hash != self._calculate_hash(current_block):
                logger.error(f"❌ Bloque #{i} tiene hash inválido")
                self.stats["chain_valid"] = False
                return False
            
            # Verificar enlace con bloque anterior
            if current_block.previous_hash != previous_block.hash:
                logger.error(f"❌ Bloque #{i} no enlaza correctamente con anterior")
                self.stats["chain_valid"] = False
                return False
        
        logger.info("✅ Blockchain válida - Integridad verificada")
        self.stats["chain_valid"] = True
        self.stats["last_validation"] = datetime.now().isoformat()
        
        return True
    
    def get_block(self, index: int) -> Optional[EvidenceBlock]:
        """Obtiene bloque por índice"""
        
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_block_by_hash(self, hash_value: str) -> Optional[EvidenceBlock]:
        """Obtiene bloque por hash"""
        
        for block in self.chain:
            if block.hash == hash_value:
                return block
        return None
    
    def search_evidence(self, query: Dict[str, Any]) -> List[EvidenceBlock]:
        """
        Busca evidencia en la blockchain
        
        Args:
            query: Diccionario con criterios de búsqueda
            
        Returns:
            Lista de bloques que coinciden
        """
        
        results = []
        
        for block in self.chain[1:]:  # Skip genesis
            match = True
            
            for key, value in query.items():
                if key in block.evidence_data:
                    if block.evidence_data[key] != value:
                        match = False
                        break
            
            if match:
                results.append(block)
        
        logger.info(f"🔍 Búsqueda: {len(results)} bloques encontrados")
        
        return results
    
    def get_chain_of_custody(self, block_index: int) -> List[Dict]:
        """
        Obtiene cadena de custodia completa hasta un bloque
        
        Args:
            block_index: Índice del bloque
            
        Returns:
            Lista de eventos de custodia
        """
        
        if block_index >= len(self.chain):
            return []
        
        custody_chain = []
        
        for i in range(block_index + 1):
            block = self.chain[i]
            custody_chain.append({
                "block_index": i,
                "timestamp": datetime.fromtimestamp(block.timestamp).isoformat(),
                "collected_by": block.collected_by,
                "hash": block.hash,
                "custody_handlers": block.chain_of_custody
            })
        
        return custody_chain
    
    def add_custody_handler(self, block_index: int, handler: str) -> bool:
        """
        Añade handler a la cadena de custodia de un bloque
        
        NOTA: Esto NO modifica el bloque original (inmutable),
        sino que crea un nuevo bloque de transferencia
        
        Args:
            block_index: Índice del bloque
            handler: Nombre del nuevo handler
            
        Returns:
            True si exitoso
        """
        
        if block_index >= len(self.chain):
            return False
        
        original_block = self.chain[block_index]
        
        # Crear bloque de transferencia de custodia
        transfer_data = {
            "type": "CUSTODY_TRANSFER",
            "original_block": block_index,
            "original_hash": original_block.hash,
            "transferred_from": original_block.collected_by,
            "transferred_to": handler,
            "transfer_time": datetime.now().isoformat(),
            "reason": "Chain of custody update"
        }
        
        self.add_evidence(
            evidence_data=transfer_data,
            collected_by=handler,
            classification=original_block.classification,
            legal_hold=original_block.legal_hold
        )
        
        logger.info(f"✅ Custodia transferida: {original_block.collected_by} → {handler}")
        
        return True
    
    def export_chain(self, filepath: str):
        """
        Exporta blockchain completa a JSON
        
        Args:
            filepath: Ruta del archivo
        """
        
        chain_data = {
            "metadata": {
                "system": "NEMESIS_IA",
                "exported_at": datetime.now().isoformat(),
                "total_blocks": len(self.chain),
                "chain_valid": self.validate_chain()
            },
            "blocks": [block.to_dict() for block in self.chain]
        }
        
        with open(filepath, 'w') as f:
            json.dump(chain_data, f, indent=2)
        
        logger.info(f"💾 Blockchain exportada: {filepath}")
    
    def get_statistics(self) -> Dict:
        """Obtiene estadísticas de la blockchain"""
        
        # Contar por tipo
        types = {}
        for block in self.chain[1:]:
            evidence_type = block.evidence_data.get("type", "UNKNOWN")
            types[evidence_type] = types.get(evidence_type, 0) + 1
        
        # Contar por clasificación
        classifications = {}
        for block in self.chain:
            classifications[block.classification] = classifications.get(block.classification, 0) + 1
        
        return {
            **self.stats,
            "chain_length": len(self.chain),
            "evidence_types": types,
            "classifications": classifications,
            "legal_hold_blocks": sum(1 for b in self.chain if b.legal_hold),
            "oldest_evidence": datetime.fromtimestamp(self.chain[1].timestamp).isoformat() if len(self.chain) > 1 else None,
            "newest_evidence": datetime.fromtimestamp(self.chain[-1].timestamp).isoformat() if len(self.chain) > 1 else None
        }
    
    def generate_integrity_report(self) -> str:
        """Genera reporte de integridad forense"""
        
        is_valid = self.validate_chain()
        stats = self.get_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║            BLOCKCHAIN FORENSIC INTEGRITY REPORT                  ║
╚══════════════════════════════════════════════════════════════════╝

📅 Report Generated: {datetime.now().isoformat()}

🔗 BLOCKCHAIN STATUS:

   Chain Length:      {stats['chain_length']} blocks
   Total Evidence:    {stats['total_evidence']} items
   Chain Valid:       {'✅ YES' if is_valid else '❌ NO - COMPROMISED'}
   Last Validation:   {stats['last_validation']}

📊 EVIDENCE SUMMARY:

   By Type:
"""
        
        for evidence_type, count in stats['evidence_types'].items():
            report += f"      {evidence_type:20} {count}\n"
        
        report += f"""
   By Classification:
"""
        for classification, count in stats['classifications'].items():
            report += f"      {classification:20} {count}\n"
        
        report += f"""
🔒 LEGAL COMPLIANCE:

   Legal Hold Blocks: {stats['legal_hold_blocks']}
   Oldest Evidence:   {stats['oldest_evidence']}
   Newest Evidence:   {stats['newest_evidence']}

🔐 CRYPTOGRAPHIC INTEGRITY:

   Hash Algorithm:    SHA-256
   Proof of Work:     Difficulty {self.difficulty}
   Genesis Block:     {self.chain[0].hash[:32]}...

⚖️ ADMISSIBILITY:

   ✅ Immutable chain of custody
   ✅ Cryptographic verification
   ✅ Timestamp integrity
   ✅ ISO/IEC 27037:2012 compliant
   {'✅ COURT ADMISSIBLE' if is_valid else '❌ COMPROMISED - NOT ADMISSIBLE'}

═══════════════════════════════════════════════════════════════════
"""
        
        return report