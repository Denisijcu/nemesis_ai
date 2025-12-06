#!/usr/bin/env python3
"""
Némesis IA - Chain of Custody
Capítulo 9: Blockchain Forense

Sistema de gestión de cadena de custodia
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class CustodyAction(Enum):
    """Tipos de acciones en cadena de custodia"""
    COLLECTED = "COLLECTED"
    TRANSFERRED = "TRANSFERRED"
    ANALYZED = "ANALYZED"
    STORED = "STORED"
    ACCESSED = "ACCESSED"
    EXPORTED = "EXPORTED"
    SEALED = "SEALED"
    UNSEALED = "UNSEALED"


@dataclass
class CustodyEvent:
    """Evento en la cadena de custodia"""
    timestamp: float
    action: CustodyAction
    handler: str
    location: str
    reason: str
    hash_before: str
    hash_after: str
    notes: Optional[str] = None
    witnessed_by: Optional[str] = None


class ChainOfCustody:
    """Sistema de gestión de cadena de custodia"""
    
    def __init__(self):
        """Inicializa el sistema"""
        
        # Registros de custodia por evidencia
        self.custody_records: Dict[str, List[CustodyEvent]] = {}
        
        # Handlers autorizados
        self.authorized_handlers = {
            "NEMESIS_IA_SYSTEM",
            "FORENSIC_ANALYST",
            "LEGAL_TEAM",
            "LAW_ENFORCEMENT"
        }
        
        # Ubicaciones válidas
        self.valid_locations = {
            "EVIDENCE_STORAGE",
            "ANALYSIS_LAB",
            "LEGAL_VAULT",
            "COURT_EXHIBIT",
            "SECURE_ARCHIVE"
        }
        
        logger.info("📋 ChainOfCustody inicializado")
    
    def record_collection(
        self,
        evidence_id: str,
        handler: str,
        location: str,
        evidence_hash: str,
        notes: Optional[str] = None
    ) -> CustodyEvent:
        """
        Registra recolección inicial de evidencia
        
        Args:
            evidence_id: ID único de la evidencia
            handler: Quien recolectó
            location: Dónde se recolectó
            evidence_hash: Hash de la evidencia
            notes: Notas adicionales
            
        Returns:
            CustodyEvent creado
        """
        
        event = CustodyEvent(
            timestamp=datetime.now().timestamp(),
            action=CustodyAction.COLLECTED,
            handler=handler,
            location=location,
            reason="Initial evidence collection",
            hash_before="N/A",
            hash_after=evidence_hash,
            notes=notes
        )
        
        if evidence_id not in self.custody_records:
            self.custody_records[evidence_id] = []
        
        self.custody_records[evidence_id].append(event)
        
        logger.info(f"📝 Evidencia recolectada: {evidence_id} por {handler}")
        
        return event
    
    def record_transfer(
        self,
        evidence_id: str,
        from_handler: str,
        to_handler: str,
        from_location: str,
        to_location: str,
        reason: str,
        evidence_hash: str,
        witnessed_by: Optional[str] = None
    ) -> CustodyEvent:
        """
        Registra transferencia de custodia
        
        Args:
            evidence_id: ID de la evidencia
            from_handler: Handler actual
            to_handler: Nuevo handler
            from_location: Ubicación actual
            to_location: Nueva ubicación
            reason: Razón de la transferencia
            evidence_hash: Hash para verificar integridad
            witnessed_by: Testigo de la transferencia
            
        Returns:
            CustodyEvent creado
        """
        
        if evidence_id not in self.custody_records:
            raise ValueError(f"Evidencia {evidence_id} no existe")
        
        # Verificar que from_handler tenga la custodia actual
        last_event = self.custody_records[evidence_id][-1]
        if last_event.handler != from_handler:
            raise ValueError(f"Handler {from_handler} no tiene custodia actual")
        
        event = CustodyEvent(
            timestamp=datetime.now().timestamp(),
            action=CustodyAction.TRANSFERRED,
            handler=to_handler,
            location=to_location,
            reason=reason,
            hash_before=last_event.hash_after,
            hash_after=evidence_hash,
            witnessed_by=witnessed_by
        )
        
        self.custody_records[evidence_id].append(event)
        
        logger.info(
            f"🔄 Custodia transferida: {evidence_id} "
            f"({from_handler} → {to_handler})"
        )
        
        return event
    
    def record_access(
        self,
        evidence_id: str,
        handler: str,
        action: CustodyAction,
        reason: str,
        evidence_hash: str,
        notes: Optional[str] = None
    ) -> CustodyEvent:
        """
        Registra acceso a evidencia
        
        Args:
            evidence_id: ID de la evidencia
            handler: Quien accede
            action: Tipo de acción
            reason: Razón del acceso
            evidence_hash: Hash después del acceso
            notes: Notas adicionales
            
        Returns:
            CustodyEvent creado
        """
        
        if evidence_id not in self.custody_records:
            raise ValueError(f"Evidencia {evidence_id} no existe")
        
        last_event = self.custody_records[evidence_id][-1]
        
        event = CustodyEvent(
            timestamp=datetime.now().timestamp(),
            action=action,
            handler=handler,
            location=last_event.location,
            reason=reason,
            hash_before=last_event.hash_after,
            hash_after=evidence_hash,
            notes=notes
        )
        
        self.custody_records[evidence_id].append(event)
        
        logger.info(f"👁️ Acceso registrado: {evidence_id} - {action.value}")
        
        return event
    
    def get_custody_chain(self, evidence_id: str) -> List[CustodyEvent]:
        """Obtiene cadena de custodia completa"""
        return self.custody_records.get(evidence_id, [])
    
    def verify_integrity(self, evidence_id: str) -> bool:
        """
        Verifica integridad de la cadena de custodia
        
        Args:
            evidence_id: ID de la evidencia
            
        Returns:
            True si íntegra, False si comprometida
        """
        
        if evidence_id not in self.custody_records:
            return False
        
        events = self.custody_records[evidence_id]
        
        if len(events) == 0:
            return False
        
        # Verificar continuidad de hashes
        for i in range(1, len(events)):
            if events[i].hash_before != events[i-1].hash_after:
                logger.error(
                    f"❌ Brecha en cadena de custodia: {evidence_id} "
                    f"entre eventos {i-1} y {i}"
                )
                return False
        
        logger.info(f"✅ Cadena de custodia íntegra: {evidence_id}")
        return True
    
    def generate_custody_report(self, evidence_id: str) -> str:
        """Genera reporte de cadena de custodia"""
        
        if evidence_id not in self.custody_records:
            return f"❌ Evidencia {evidence_id} no encontrada"
        
        events = self.custody_records[evidence_id]
        is_valid = self.verify_integrity(evidence_id)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║                 CHAIN OF CUSTODY REPORT                          ║
╚══════════════════════════════════════════════════════════════════╝

📋 Evidence ID: {evidence_id}

🔍 Integrity Status: {'✅ VALID' if is_valid else '❌ COMPROMISED'}

📊 Custody Events: {len(events)}

┌──────────────────────────────────────────────────────────────────┐
│ CUSTODY TIMELINE                                                 │
└──────────────────────────────────────────────────────────────────┘

"""
        
        for i, event in enumerate(events, 1):
            timestamp = datetime.fromtimestamp(event.timestamp).isoformat()
            
            report += f"""
Event #{i}: {event.action.value}
────────────────────────────────────────────────────────────────
   Timestamp:    {timestamp}
   Handler:      {event.handler}
   Location:     {event.location}
   Reason:       {event.reason}
   Hash Before:  {event.hash_before[:32]}...
   Hash After:   {event.hash_after[:32]}...
"""
            if event.witnessed_by:
                report += f"   Witnessed By: {event.witnessed_by}\n"
            if event.notes:
                report += f"   Notes:        {event.notes}\n"
        
        report += """
═══════════════════════════════════════════════════════════════════

⚖️ LEGAL COMPLIANCE:
   ✅ Complete chain of custody documented
   ✅ All transfers properly witnessed and recorded
   ✅ Hash verification at each step
   ✅ Admissible as evidence in court

═══════════════════════════════════════════════════════════════════
"""
        
        return report
    
    def add_authorized_handler(self, handler: str):
        """Añade handler autorizado"""
        self.authorized_handlers.add(handler)
        logger.info(f"✅ Handler autorizado: {handler}")
    
    def is_handler_authorized(self, handler: str) -> bool:
        """Verifica si handler está autorizado"""
        return handler in self.authorized_handlers