#!/usr/bin/env python3
"""
Némesis IA - Collective Intelligence
Capítulo 14: Inmunidad de Rebaño

Sistema de inteligencia colectiva y consenso distribuido
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from .agent_network import AgentNetwork, AgentRole

logger = logging.getLogger(__name__)


class CollectiveIntelligence:
    """Sistema de inteligencia colectiva"""
    
    def __init__(self):
        """Inicializa sistema de inteligencia colectiva"""
        
        self.network = AgentNetwork("NEMESIS_COLLECTIVE")
        
        # Estadísticas
        self.stats = {
            "threats_analyzed": 0,
            "collective_decisions": 0,
            "false_positives_prevented": 0,
            "coordinated_blocks": 0
        }
        
        logger.info("🧠 CollectiveIntelligence inicializado")
    
    def analyze_threat_collectively(
        self,
        threat_data: Dict,
        reporting_agents: List[str]
    ) -> Dict:
        """
        Análisis colectivo de amenaza
        
        Args:
            threat_data: Datos de la amenaza
            reporting_agents: Agentes que reportan
            
        Returns:
            Decisión colectiva
        """
        
        logger.info(
            f"🧠 Analyzing threat collectively "
            f"({len(reporting_agents)} agents reporting)..."
        )
        
        self.stats["threats_analyzed"] += 1
        
        # Recopilar votos de todos los agentes
        votes = []
        for agent_id in reporting_agents:
            if agent_id in self.network.agents:
                agent = self.network.agents[agent_id]
                
                # Voto ponderado por reputación
                vote_weight = agent.reputation_score
                votes.append({
                    'agent_id': agent_id,
                    'vote': True,  # Simplificado
                    'weight': vote_weight,
                    'confidence': threat_data.get('confidence', 0.5)
                })
        
        # Calcular decisión colectiva
        total_weight = sum(v['weight'] for v in votes)
        weighted_confidence = sum(
            v['confidence'] * v['weight'] for v in votes
        ) / total_weight if total_weight > 0 else 0
        
        # Decisión por consenso
        consensus = len(votes) >= 3 and weighted_confidence > 0.6
        
        decision = {
            'threat_confirmed': consensus,
            'collective_confidence': weighted_confidence,
            'reporting_agents': len(reporting_agents),
            'total_votes': len(votes),
            'decision_timestamp': datetime.now().isoformat(),
            'action_recommended': 'BLOCK' if consensus else 'MONITOR'
        }
        
        if consensus:
            self.stats["collective_decisions"] += 1
            logger.info(
                f"✅ CONSENSUS: Threat confirmed "
                f"(confidence: {weighted_confidence:.2f})"
            )
        else:
            self.stats["false_positives_prevented"] += 1
            logger.info(
                f"⚠️ NO CONSENSUS: Possible false positive "
                f"(confidence: {weighted_confidence:.2f})"
            )
        
        return decision
    
    def coordinate_distributed_block(
        self,
        target_ip: str,
        threat_type: str,
        coordinator_id: str
    ) -> Dict:
        """
        Coordina bloqueo distribuido
        
        Args:
            target_ip: IP a bloquear
            threat_type: Tipo de amenaza
            coordinator_id: Agente coordinador
            
        Returns:
            Resultado de coordinación
        """
        
        logger.info(f"🎯 Coordinating distributed block: {target_ip}...")
        
        # Compartir amenaza en la red
        intel = self.network.share_threat_intelligence(
            agent_id=coordinator_id,
            threat_type=threat_type,
            threat_data={'source_ip': target_ip},
            confidence=0.9
        )
        
        # Simular votos de otros agentes
        active_agents = [
            a for a in self.network.agents.values()
            if a.status == "ACTIVE" and a.agent_id != coordinator_id
        ]
        
        for agent in active_agents[:3]:  # Top 3 agentes
            self.network.vote_on_threat(
                agent_id=agent.agent_id,
                threat_id=intel.threat_id,
                vote=True
            )
        
        # Coordinar respuesta
        response = self.network.coordinate_response(
            threat_id=intel.threat_id,
            coordinator_id=coordinator_id
        )
        
        if response['coordinated']:
            self.stats["coordinated_blocks"] += 1
            logger.info(f"✅ Distributed block coordinated: {target_ip}")
        
        return response
    
    def share_threat_patterns(
        self,
        agent_id: str,
        patterns: List[Dict]
    ) -> Dict:
        """
        Comparte patrones de amenazas con la red
        
        Args:
            agent_id: Agente que comparte
            patterns: Patrones detectados
            
        Returns:
            Resultado de compartición
        """
        
        logger.info(f"📡 Agent {agent_id} sharing {len(patterns)} patterns...")
        
        shared_patterns = []
        
        for pattern in patterns:
            intel = self.network.share_threat_intelligence(
                agent_id=agent_id,
                threat_type=pattern.get('type', 'UNKNOWN'),
                threat_data=pattern,
                confidence=pattern.get('confidence', 0.5)
            )
            shared_patterns.append(intel.threat_id)
        
        return {
            'agent_id': agent_id,
            'patterns_shared': len(patterns),
            'threat_ids': shared_patterns,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_collective_statistics(self) -> Dict:
        """Obtiene estadísticas colectivas"""
        
        network_status = self.network.get_network_status()
        
        return {
            'collective': self.stats,
            'network': network_status
        }
    
    def generate_collective_report(self) -> str:
        """Genera reporte de inteligencia colectiva"""
        
        stats = self.get_collective_statistics()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║           COLLECTIVE INTELLIGENCE - STATUS REPORT                ║
╚══════════════════════════════════════════════════════════════════╝

🧠 COLLECTIVE ANALYSIS:

   Threats Analyzed:         {stats['collective']['threats_analyzed']}
   Collective Decisions:     {stats['collective']['collective_decisions']}
   False Positives Prevented:{stats['collective']['false_positives_prevented']}
   Coordinated Blocks:       {stats['collective']['coordinated_blocks']}

🌐 NETWORK STATUS:

   Active Agents:            {stats['network']['active_agents']}
   Shared Intelligence:      {stats['network']['shared_threats']}
   Consensus Reached:        {stats['network']['statistics']['consensus_reached']}
   Average Reputation:       {stats['network']['average_reputation']:.2f}

⚡ Collective Defense:       ACTIVE - Herd Immunity Operational

═══════════════════════════════════════════════════════════════════
"""
        
        return report