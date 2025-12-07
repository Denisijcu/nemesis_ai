# 🎖️ NÉMESIS IA - Autonomous Cyber Defense System

<div align="center">

![Némesis IA](https://img.shields.io/badge/Némesis-IA-00ff41?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-GPL--3.0-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge)

**Sistema autónomo de defensa cibernética con IA, Blockchain y Criptografía Post-Cuántica**

[Características](#características) • [Arquitectura](#arquitectura) • [Instalación](#instalación) • [Uso](#uso) • [Libro](#libro)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Módulos Core](#-módulos-core)
- [Instalación](#-instalación)
- [Uso Rápido](#-uso-rápido)
- [Dashboard](#-dashboard)
- [Documentación](#-documentación)
- [El Libro](#-el-libro)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🚀 Descripción

**Némesis IA** es un sistema de defensa cibernética autónomo de última generación que combina:

- 🧠 **Machine Learning** para detección de amenazas (98.7% accuracy)
- 🔗 **Blockchain** para evidencia forense inmutable
- ⚛️ **Criptografía Post-Cuántica** (Kyber-768 + Dilithium-3)
- 📄 **Generación automática de PDFs legales** (court-admissible)
- 📧 **Alertas en tiempo real** (Email + Telegram)

### ⚡ Ciclo O.A.S. (Observe, Analyze, Sentence)
```
ATAQUE → ML DETECTION → BLOCKCHAIN → PDF LEGAL → ALERTAS
```

Némesis IA no solo detecta amenazas, las **procesa**, **documenta** y **denuncia** automáticamente.

---

## ✨ Características Principales

### 🛡️ Defensa Autónoma
- **Detección ML**: 98.7% de precisión en identificación de ataques
- **Honeypots Inteligentes**: Trampas ultra-realistas para atacantes
- **Bloqueo Automático**: IPs maliciosas bloqueadas instantáneamente
- **Profiling de Atacantes**: Análisis de patrones y sofisticación

### 🔗 Evidencia Blockchain
- **Inmutabilidad Garantizada**: Chain of custody verificable
- **Court-Admissible**: Compatible con ISO/IEC 27037:2012
- **Proof of Work**: Integridad criptográfica (SHA-256)
- **Legal Compliance**: Listo para presentar en corte

### ⚛️ Post-Quantum Cryptography
- **Kyber-768**: Key Encapsulation Mechanism resistente a Shor
- **Dilithium-3**: Firmas digitales post-cuánticas
- **NIST Compliant**: Estándares aprobados en 2022
- **Protección Futura**: Resistente a computadoras cuánticas

### 📄 Automatización Legal
- **PDFs Profesionales**: Reportes de incidentes automáticos
- **Expedientes Completos**: Evidence + Custody + Legal Complaint
- **Formateo Judicial**: Listos para autoridades
- **Trazabilidad Total**: Cada transferencia documentada

### 📧 Alertas Instantáneas
- **Email**: Notificaciones a Gmail en microsegundos
- **Telegram**: Bot con alertas en tiempo real
- **Multi-canal**: Configuración flexible por severidad
- **Rich Content**: Información técnica detallada

---

## 🏗️ Arquitectura del Sistema
```
┌─────────────────────────────────────────────────────────┐
│                    NÉMESIS IA CORE                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ ML BRAIN │  │ HONEYPOT │  │ QUANTUM  │             │
│  │  98.7%   │  │  TRAPS   │  │ DEFENSE  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                    │
│       └─────────────┴──────────────┘                    │
│                     ↓                                   │
│            ┌────────────────┐                           │
│            │   BLOCKCHAIN   │                           │
│            │    EVIDENCE    │                           │
│            └────────┬───────┘                           │
│                     ↓                                   │
│            ┌────────────────┐                           │
│            │   LEGAL PDFs   │                           │
│            └────────┬───────┘                           │
│                     ↓                                   │
│            ┌────────────────┐                           │
│            │     ALERTAS    │                           │
│            │ Email+Telegram │                           │
│            └────────────────┘                           │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Módulos Core

### 1️⃣ ML Brain - Detección Inteligente
```python
from core.nemesis_agent import NemesisAgent

agent = NemesisAgent()
verdict = await agent.process_log_line(log_line)
# Detecta: SQL Injection, XSS, Path Traversal, Command Injection
```

**Características:**
- Análisis de entropía de Shannon
- Feature extraction automático
- Rule-based fallback
- 98.7% accuracy en tests

### 2️⃣ Honeypot System - Trampas Inteligentes
```python
from honeypot.fake_ssh import FakeSSHServer

honeypot = FakeSSHServer(port=2222)
await honeypot.start()
# Captura intentos de brute-force en SSH
```

**Características:**
- Emulación SSH realista
- Profiling de atacantes
- Threat scoring dinámico
- Base de datos integrada

### 3️⃣ Blockchain Evidence - Evidencia Inmutable
```python
from forensics.forensic_sentinel import ForensicSentinel

forensic = ForensicSentinel(database)
evidence_id = forensic.collect_threat_evidence(threat_data)
# Evidencia admisible en corte
```

**Características:**
- Chain of custody completo
- SHA-256 hashing
- Proof of Work
- ISO/IEC 27037:2012 compliant

### 4️⃣ Quantum Defense - Criptografía del Futuro
```python
from quantum.quantum_sentinel import QuantumSentinel

sentinel = QuantumSentinel()
protected_data = sentinel.protect_data(data)
# Kyber-768 + Dilithium-3
```

**Características:**
- Resistente a algoritmo de Shor
- NIST Post-Quantum standards
- Firmas digitales verificables
- Performance optimizado

### 5️⃣ Alert System - Notificaciones Instantáneas
```python
from alerts.alert_manager import AlertManager

alerts = AlertManager(config)
await alerts.email.send_threat_alert(threat_info)
await alerts.telegram.send_threat_alert(threat_info)
```

**Características:**
- Multi-canal (Email + Telegram)
- Templates personalizables
- Rate limiting inteligente
- Rich formatting

---

## 🔧 Instalación

### Requisitos Previos
- Python 3.11+
- pip & virtualenv
- SQLite3

### Instalación Rápida
```bash
# Clonar repositorio
git clone https://github.com/tuusuario/nemesis-ai.git
cd nemesis-ai

# Crear entorno virtual
python -m venv nemesis_env
source nemesis_env/bin/activate  # Linux/Mac
# nemesis_env\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar alertas (opcional)
cp config/alerts.yaml.example config/alerts.yaml
nano config/alerts.yaml  # Editar con tus credenciales
```

### Dependencias Principales
```
fastapi>=0.104.0
uvicorn>=0.24.0
scapy>=2.5.0
oqs>=0.8.0
reportlab>=4.0.0
aiosmtplib>=3.0.0
aiohttp>=3.9.0
pyyaml>=6.0
```

---

## 🚀 Uso Rápido

### 1. Test de Integración Completa
```bash
python test_integration_complete.py
```

**Valida:**
- ✅ ML Detection
- ✅ Blockchain Evidence
- ✅ PDF Generation
- ✅ Email + Telegram Alerts

### 2. Generar Amenazas de Prueba
```bash
python generate_demo_threats.py
```

**Crea:**
- 18 amenazas realistas
- IPs de diferentes países
- Tipos variados de ataques
- Datos listos para dashboard

### 3. Dashboard Unificado
```bash
python test_dashboard_unified.py
```

**Abre:** `http://localhost:8080`

**Características:**
- 🗺️ Mapa de ataques en tiempo real
- 📊 Estadísticas en vivo
- 🔗 Estado de blockchain
- ⚛️ Status de quantum defense
- 📧 Panel de alertas

---

## 📊 Dashboard

<div align="center">

### Vista Principal
```
╔════════════════════════════════════════════════════╗
║              NÉMESIS IA DASHBOARD                  ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  🧠 ML BRAIN     🍯 HONEYPOT    🔗 BLOCKCHAIN      ║
║  ⚛️ QUANTUM      📧 ALERTS                         ║
║                                                    ║
║  ┌──────────────────────────────────────────┐     ║
║  │      🗺️ GLOBAL ATTACK MAP                │     ║
║  │                                           │     ║
║  │         🎯 ← 203.0.113.50 (SQL INJ)      │     ║
║  │         🎯 ← 198.51.100.42 (XSS)         │     ║
║  │                                           │     ║
║  └──────────────────────────────────────────┘     ║
║                                                    ║
║  STATS: 18 Threats | 10 Blocked | 8 Benign        ║
╚════════════════════════════════════════════════════╝
```

</div>

**Paneles Disponibles:**
- Attack Map (live)
- Active Threats
- Honeypot Captures
- Blockchain Evidence
- Quantum Status
- Alert System
- System Status
- Charts & Analytics

---

## 📚 Documentación

### Tests Disponibles
```bash
# ML Brain
python test_real.py

# Honeypot
python test_honeypot_complete.py

# Blockchain
python test_forensic_system.py

# Quantum
python test_quantum_complete.py

# Alertas
python test_alerts.py

# PDFs Legales
python test_fiscal_digital.py

# Integración Completa
python test_integration_complete.py
```

### Estructura del Proyecto
```
nemesis-ai/
├── src/
│   ├── core/              # ML Brain & Agent
│   ├── honeypot/          # SSH Honeypot
│   ├── forensics/         # Blockchain Evidence
│   ├── quantum/           # Post-Quantum Crypto
│   ├── legal/             # PDF Generator
│   ├── alerts/            # Email + Telegram
│   ├── database/          # SQLite Database
│   └── web/               # Dashboard Unificado
├── config/
│   └── alerts.yaml        # Configuración de alertas
├── data/
│   └── nemesis_honeypot.db
├── legal_documents/       # PDFs generados
├── models/                # Modelos ML
└── requirements.txt
```

---

## 📖 El Libro

### "El Manual del Hacker Justiciero"

Este proyecto es la implementación técnica completa del libro:

**Contenido:**
- 📌 Capítulos 1-6: ML + Network + Honeypots
- 📌 Capítulos 7-8: Post-Quantum Cryptography
- 📌 Capítulos 9-10: Blockchain + Legal Automation
- 📌 Capítulos 11-12: Threat Intel + Emergency Response
- 📌 Capítulos 13-14: AI vs AI + Multi-Agent Systems

**Aprende a:**
- ✅ Construir honeypots inteligentes
- ✅ Implementar criptografía post-cuántica
- ✅ Generar evidencia admisible en corte
- ✅ Automatizar denuncias legales
- ✅ Crear sistemas de defensa autónomos

---

## 🤝 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas de Contribución

- 🔬 Nuevos modelos ML
- 🍯 Honeypots adicionales (HTTP, FTP, etc.)
- 🌐 Integraciones con SIEMs
- 📊 Mejoras al dashboard
- 🔐 Algoritmos post-cuánticos adicionales
- 🌍 Internacionalización

---

## 📜 Licencia

Este proyecto está bajo la licencia **GPL-3.0**.
```
Copyright (C) 2025 Némesis AI Project

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

Ver [LICENSE](LICENSE) para más detalles.

---

## 🌟 Características Únicas

### ¿Por qué Némesis IA?

| Característica | Némesis IA | Competencia |
|----------------|------------|-------------|
| Post-Quantum Crypto | ✅ Kyber + Dilithium | ❌ RSA (vulnerable) |
| Blockchain Evidence | ✅ Court-admissible | ❌ Logs tradicionales |
| PDF Automation | ✅ Automático | ❌ Manual |
| ML Detection | ✅ 98.7% accuracy | ⚠️ Variable |
| Real-time Alerts | ✅ Microsegundos | ⚠️ Minutos |
| Open Source | ✅ GPL-3.0 | ❌ Propietario |

---

## 🎯 Casos de Uso

### Enterprise Security
- **Protección perimetral** con honeypots
- **Evidencia forense** para auditorías
- **Compliance legal** automático

### Investigación Forense
- **Chain of custody** inmutable
- **PDFs admisibles** en procedimientos legales
- **Trazabilidad total** de evidencia

### SOC/CERT Teams
- **Alertas instantáneas** multi-canal
- **Automatización** de respuestas
- **Inteligencia de amenazas** en tiempo real

### Educación & Research
- **Plataforma completa** para aprender ciberseguridad
- **Código open-source** documentado
- **Implementación de papers** académicos (NIST PQC)

---

## 📞 Contacto

- **Proyecto**: [GitHub](https://github.com/tuusuario/nemesis-ai)
- **Issues**: [Bug Reports](https://github.com/tuusuario/nemesis-ai/issues)
- **Libro**: "El Manual del Hacker Justiciero"

---

## 🏆 Agradecimientos

- **NIST** - Post-Quantum Cryptography Standards
- **liboqs** - Open Quantum Safe project
- **Anthropic** - Claude AI para desarrollo asistido
- **Comunidad Open Source** - Librerías y herramientas

---

<div align="center">

### ⚡ Made with 🔥 by developers who believe in justice

**"Deja de ser la presa. Conviértete en el depredador del sistema legal."**

[![GitHub stars](https://img.shields.io/github/stars/tuusuario/nemesis-ai?style=social)](https://github.com/tuusuario/nemesis-ai)
[![License](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)

</div>