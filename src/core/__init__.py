"""
Némesis IA - Core Module

Este módulo contiene los componentes principales del sistema:
- NemesisAgent: Agente autónomo de detección
- ThreatEvent: Clase de datos para eventos
- ThreatVerdict: Clase de datos para veredictos

Copyright (C) 2025 Némesis AI Project Contributors
Licensed under GPL-3.0
"""

from .nemesis_agent import NemesisAgent, ThreatEvent, ThreatVerdict

__all__ = ["NemesisAgent", "ThreatEvent", "ThreatVerdict"]
__version__ = "1.0.0"
