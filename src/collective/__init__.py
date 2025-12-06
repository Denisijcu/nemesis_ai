"""
Némesis IA - Collective Module
Sistema de defensa colectiva y multi-agente
"""

from .agent_network import AgentNetwork, AgentNode, AgentRole, ThreatIntelligence
from .collective_intelligence import CollectiveIntelligence

__all__ = [
    'AgentNetwork',
    'AgentNode',
    'AgentRole',
    'ThreatIntelligence',
    'CollectiveIntelligence'
]