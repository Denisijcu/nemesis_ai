#!/usr/bin/env python3
"""
Némesis IA - Agent Network
Capítulo 14: Inmunidad de Rebaño

Red de agentes colaborativos para defensa distribuida
"""

import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Roles de agentes en la red"""
    DETECTOR = "DETECTOR"           # Detecta amenazas
    ANALYZER = "ANALYZER"           # Analiza amenazas
    RESPONDER = "RESPONDER"         # Responde a amenazas
    COORDINATOR = "COORDINATOR"     # Coordina respuestas
    INTELLIGENCE = "INTELLIGENCE"   # Recopila intel


@dataclass
class AgentNode:
    """Nodo de agente en la red"""
    agent_id: str
    role: AgentRole
    location: str
    status: str
    threats_detected: int = 0
    threats_shared: int = 0
    consensus_votes: int = 0
    reputation_score: float = 1.0
    last_active: str = None
    
    def __post_init__(self):
        if self.last_active is None:
            self.last_active = datetime.now().isoformat()


@dataclass
class ThreatIntelligence:
    """Inteligencia de amenazas compartida"""
    threat_id: str
    source_agent: str
    threat_type: str
    threat_data: Dict
    confidence: float
    timestamp: str
    verified_by: Set[str]
    votes: int = 0


class AgentNetwork:
    """Red de agentes colaborativos"""
    
    def __init__(self, network_name: str = "NEMESIS_NETWORK"):
        """
        Inicializa red de agentes
        
        Args:
            network_name: Nombre de la red
        """
        
        self.network_name = network_name
        self.network_id = str(uuid.uuid4())[:8]
        
        # Agentes en la red
        self.agents: Dict[str, AgentNode] = {}
        
        # Inteligencia compartida
        self.shared_intelligence: Dict[str, ThreatIntelligence] = {}
        
        # Configuración
        self.consensus_threshold = 0.6  # 60% consenso requerido
        self.reputation_threshold = 0.7  # Reputación mínima
        
        # Estadísticas
        self.stats = {
            "agents_joined": 0,
            "agents_active": 0,
            "threats_shared": 0,
            "consensus_reached": 0,
            "coordinated_responses": 0
        }
        
        logger.info(f"🌐 AgentNetwork '{network_name}' inicializada")
    
    def join_network(
        self,
        agent_id: Optional[str] = None,
        role: AgentRole = AgentRole.DETECTOR,
        location: str = "UNKNOWN"
    ) -> AgentNode:
        """
        Agente se une a la red
        
        Args:
            agent_id: ID del agente (generado si None)
            role: Rol del agente
            location: Ubicación del agente
            
        Returns:
            AgentNode creado
        """
        
        if agent_id is None:
            agent_id = f"AGENT-{str(uuid.uuid4())[:8]}"
        
        node = AgentNode(
            agent_id=agent_id,
            role=role,
            location=location,
            status="ACTIVE"
        )
        
        self.agents[agent_id] = node
        self.stats["agents_joined"] += 1
        self.stats["agents_active"] += 1
        
        logger.info(
            f"✅ Agent {agent_id} joined network "
            f"(role: {role.value}, location: {location})"
        )
        
        return node
    
    def share_threat_intelligence(
        self,
        agent_id: str,
        threat_type: str,
        threat_data: Dict,
        confidence: float
    ) -> ThreatIntelligence:
        """
        Agente comparte inteligencia de amenaza
        
        Args:
            agent_id: ID del agente que comparte
            threat_type: Tipo de amenaza
            threat_data: Datos de la amenaza
            confidence: Confianza del agente
            
        Returns:
            ThreatIntelligence creado
        """
        
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not in network")
        
        threat_id = f"THREAT-{str(uuid.uuid4())[:8]}"
        
        intel = ThreatIntelligence(
            threat_id=threat_id,
            source_agent=agent_id,
            threat_type=threat_type,
            threat_data=threat_data,
            confidence=confidence,
            timestamp=datetime.now().isoformat(),
            verified_by=set([agent_id])
        )
        
        self.shared_intelligence[threat_id] = intel
        
        # Actualizar stats del agente
        self.agents[agent_id].threats_shared += 1
        self.stats["threats_shared"] += 1
        
        logger.info(
            f"📡 Agent {agent_id} shared threat: {threat_type} "
            f"(confidence: {confidence:.2f})"
        )
        
        return intel
    
    def vote_on_threat(
        self,
        agent_id: str,
        threat_id: str,
        vote: bool
    ) -> Dict:
        """
        Agente vota sobre una amenaza compartida
        
        Args:
            agent_id: ID del agente que vota
            threat_id: ID de la amenaza
            vote: True si confirma, False si rechaza
            
        Returns:
            Resultado del voto y estado de consenso
        """
        
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not in network")
        
        if threat_id not in self.shared_intelligence:
            raise ValueError(f"Threat {threat_id} not found")
        
        intel = self.shared_intelligence[threat_id]
        
        # Registrar voto
        if vote:
            intel.verified_by.add(agent_id)
            intel.votes += 1
        
        # Actualizar stats del agente
        self.agents[agent_id].consensus_votes += 1
        
        # Verificar consenso
        total_agents = len([a for a in self.agents.values() if a.status == "ACTIVE"])
        consensus_ratio = len(intel.verified_by) / total_agents if total_agents > 0 else 0
        
        consensus_reached = consensus_ratio >= self.consensus_threshold
        
        if consensus_reached and intel.votes == len(intel.verified_by):
            # Primera vez alcanzando consenso
            self.stats["consensus_reached"] += 1
            logger.info(
                f"🎯 CONSENSUS REACHED on {threat_id} "
                f"({len(intel.verified_by)}/{total_agents} agents)"
            )
        
        result = {
            'threat_id': threat_id,
            'votes': intel.votes,
            'verified_by': len(intel.verified_by),
            'total_agents': total_agents,
            'consensus_ratio': consensus_ratio,
            'consensus_reached': consensus_reached
        }
        
        return result
    
    def coordinate_response(
        self,
        threat_id: str,
        coordinator_id: str
    ) -> Dict:
        """
        Coordina respuesta distribuida a amenaza
        
        Args:
            threat_id: ID de la amenaza
            coordinator_id: ID del agente coordinador
            
        Returns:
            Plan de respuesta coordinada
        """
        
        if threat_id not in self.shared_intelligence:
            raise ValueError(f"Threat {threat_id} not found")
        
        intel = self.shared_intelligence[threat_id]
        
        # Verificar consenso
        total_agents = len([a for a in self.agents.values() if a.status == "ACTIVE"])
        consensus_ratio = len(intel.verified_by) / total_agents if total_agents > 0 else 0
        
        if consensus_ratio < self.consensus_threshold:
            logger.warning(
                f"⚠️ Cannot coordinate - consensus not reached "
                f"({consensus_ratio*100:.1f}% < {self.consensus_threshold*100:.1f}%)"
            )
            return {
                'coordinated': False,
                'reason': 'Consensus not reached'
            }
        
        # Seleccionar agentes para respuesta
        responders = [
            agent_id for agent_id, agent in self.agents.items()
            if agent.role in [AgentRole.RESPONDER, AgentRole.COORDINATOR]
            and agent.status == "ACTIVE"
            and agent.reputation_score >= self.reputation_threshold
        ]
        
        # Crear plan de respuesta
        response_plan = {
            'coordinated': True,
            'threat_id': threat_id,
            'threat_type': intel.threat_type,
            'coordinator': coordinator_id,
            'responders': responders,
            'actions': self._generate_response_actions(intel),
            'timestamp': datetime.now().isoformat()
        }
        
        self.stats["coordinated_responses"] += 1
        
        logger.info(
            f"🎯 Coordinated response initiated: {threat_id} "
            f"({len(responders)} responders)"
        )
        
        return response_plan
    
    def _generate_response_actions(
        self,
        intel: ThreatIntelligence
    ) -> List[Dict]:
        """Genera acciones de respuesta basadas en amenaza"""
        
        actions = []
        
        # Acción 1: Bloqueo
        if intel.threat_data.get('source_ip'):
            actions.append({
                'action': 'BLOCK_IP',
                'target': intel.threat_data['source_ip'],
                'priority': 'HIGH'
            })
        
        # Acción 2: Alertas
        actions.append({
            'action': 'ALERT_ALL_AGENTS',
            'message': f"Threat {intel.threat_type} confirmed by consensus",
            'priority': 'HIGH'
        })
        
        # Acción 3: Evidencia
        actions.append({
            'action': 'COLLECT_EVIDENCE',
            'threat_id': intel.threat_id,
            'priority': 'MEDIUM'
        })
        
        # Acción 4: Reporte
        if intel.confidence > 0.9:
            actions.append({
                'action': 'REPORT_TO_CERT',
                'threat_data': intel.threat_data,
                'priority': 'CRITICAL'
            })
        
        return actions
    
    def update_agent_reputation(
        self,
        agent_id: str,
        performance_score: float
    ):
        """
        Actualiza reputación de agente
        
        Args:
            agent_id: ID del agente
            performance_score: Score de rendimiento (0-1)
        """
        
        if agent_id not in self.agents:
            return
        
        agent = self.agents[agent_id]
        
        # Promedio ponderado
        alpha = 0.3  # Factor de aprendizaje
        agent.reputation_score = (
            alpha * performance_score +
            (1 - alpha) * agent.reputation_score
        )
        
        logger.info(
            f"📊 Agent {agent_id} reputation: {agent.reputation_score:.2f}"
        )
    
    def get_network_status(self) -> Dict:
        """Obtiene estado de la red"""
        
        active_agents = [a for a in self.agents.values() if a.status == "ACTIVE"]
        
        # Contar por rol
        role_distribution = {}
        for agent in active_agents:
            role = agent.role.value
            role_distribution[role] = role_distribution.get(role, 0) + 1
        
        # Calcular reputación promedio
        avg_reputation = (
            sum(a.reputation_score for a in active_agents) / len(active_agents)
            if active_agents else 0
        )
        
        return {
            'network_name': self.network_name,
            'network_id': self.network_id,
            'total_agents': len(self.agents),
            'active_agents': len(active_agents),
            'role_distribution': role_distribution,
            'average_reputation': avg_reputation,
            'shared_threats': len(self.shared_intelligence),
            'consensus_threshold': self.consensus_threshold,
            'statistics': self.stats
        }
    
    def generate_network_report(self) -> str:
        """Genera reporte de la red"""
        
        status = self.get_network_status()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              AGENT NETWORK - STATUS REPORT                       ║
╚══════════════════════════════════════════════════════════════════╝

🌐 NETWORK: {status['network_name']} (ID: {status['network_id']})

📊 AGENTS:

   Total Agents:          {status['total_agents']}
   Active Agents:         {status['active_agents']}
   Average Reputation:    {status['average_reputation']:.2f}

📋 ROLE DISTRIBUTION:

"""
        
        for role, count in status['role_distribution'].items():
            report += f"   {role:15} {count}\n"
        
        report += f"""
🎯 COLLABORATION:

   Threats Shared:        {status['shared_threats']}
   Consensus Reached:     {status['statistics']['consensus_reached']}
   Coordinated Responses: {status['statistics']['coordinated_responses']}
   Consensus Threshold:   {status['consensus_threshold']*100:.0f}%

⚡ Status:                COLLECTIVE DEFENSE ACTIVE

═══════════════════════════════════════════════════════════════════
"""
        
        return report