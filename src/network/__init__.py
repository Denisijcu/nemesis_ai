"""
Némesis IA - Network Module
Análisis de protocolos de red
"""

from .packet_capture import PacketCapture, PacketInfo
from .protocol_analyzer import (
    ProtocolAnalyzer, 
    HTTPRequest, 
    DNSQuery, 
    PortScanEvent
)
from .network_sentinel import NetworkSentinel

__all__ = [
    'PacketCapture', 
    'PacketInfo',
    'ProtocolAnalyzer',
    'HTTPRequest',
    'DNSQuery',
    'PortScanEvent',
    'NetworkSentinel'
]