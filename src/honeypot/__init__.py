"""
Némesis IA - Honeypot Module
Sistema de trampa para atacantes
"""

from .fake_ssh import FakeSSH, SSHAttempt
from .attacker_profiler import AttackerProfiler, AttackerProfile
from .honeypot_logger import HoneypotLogger

__all__ = [
    'FakeSSH', 
    'SSHAttempt', 
    'AttackerProfiler', 
    'AttackerProfile',
    'HoneypotLogger'
]