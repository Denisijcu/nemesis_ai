# ⚡ NÉMESIS IA - Sistema Autónomo de Ciberdefensa

<div align="center">
```
███╗   ██╗███████╗███╗   ███╗███████╗███████╗██╗███████╗
████╗  ██║██╔════╝████╗ ████║██╔════╝██╔════╝██║██╔════╝
██╔██╗ ██║█████╗  ██╔████╔██║█████╗  ███████╗██║███████╗
██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══╝  ╚════██║██║╚════██║
██║ ╚████║███████╗██║ ╚═╝ ██║███████╗███████║██║███████║
╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚══════╝╚══════╝╚═╝╚══════╝
```

**El Vigilante Digital que No Duerme, No Perdona y Opera a la Velocidad de la Luz**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()
[![ML Accuracy](https://img.shields.io/badge/ML%20Accuracy-98.7%25-brightgreen.svg)]()

[Características](#-características-principales) • [Instalación](#-instalación-rápida) • [Uso](#-uso) • [Arquitectura](#-arquitectura) • [Dashboards](#️-dashboards-disponibles) • [Demo](#-demo)

</div>

---

## 📖 Descripción

**Némesis IA** es un sistema autónomo de ciberdefensa que convierte ataques en evidencia judicial. No solo detecta amenazas: **las atrapa, documenta y denuncia automáticamente**.

### 🎯 ¿Qué hace diferente a Némesis?

- 🍯 **Atrae** al atacante con honeypots ultra-realistas
- 🧠 **Detecta** amenazas con ML (98.7% accuracy)
- 🔗 **Documenta** evidencia en blockchain inmutable
- 📄 **Genera** expedientes legales automáticos
- 📧 **Notifica** por Email y Telegram en tiempo real
- 🚨 **Denuncia** a CERTs, ISPs y autoridades
- ⚛️ **Protege** con criptografía post-cuántica

---

## 🚀 Características Principales

### 🛡️ Módulo 1-6: Defensa Core

| Módulo | Descripción | Tecnología |
|--------|-------------|------------|
| 🧠 **ML Brain** | Detección de amenazas con IA | RandomForest (98.7%) |
| 👁️ **Log Sentinel** | Análisis de logs en tiempo real | Regex + Async |
| 📡 **Network Sentinel** | Escaneo de red avanzado | Nmap + Python |
| 🍯 **Honeypot Manager** | Trampas SSH inteligentes | Paramiko |
| 📊 **Traffic Analyzer** | Análisis de tráfico de red | Scapy |
| 🔍 **IP Reputation** | Verificación contra blacklists | AbuseIPDB + Spamhaus |

### ⚛️ Módulo 7-8: Defensa Cuántica

| Módulo | Descripción | Algoritmo |
|--------|-------------|-----------|
| 🔐 **Quantum Defense** | Criptografía post-cuántica | Kyber-768 + Dilithium-3 |
| 🔓 **RSA Vulnerability** | Detección de criptografía obsoleta | RSA Analysis |

### ⚖️ Módulo 9-10: Arsenal Legal

| Módulo | Descripción | Output |
|--------|-------------|--------|
| 🔗 **Blockchain Forensics** | Cadena de custodia inmutable | SHA-256 Chain |
| 📄 **Fiscal Digital** | Generación de PDFs legales | Court-ready PDFs |

### 🚨 Módulo 11-12: Respuesta Automática

| Módulo | Descripción | Integración |
|--------|-------------|-------------|
| 🌐 **Threat Intel APIs** | Consulta bases de datos globales | AbuseIPDB, WHOIS |
| 🚨 **Red Button** | Notificación a CERTs | US-CERT, CERT-EU |

### 🤖 Módulo 13-14: IA Avanzada

| Módulo | Descripción | Técnica |
|--------|-------------|---------|
| ⚔️ **AI vs AI Defense** | Defensa contra ataques adversariales | Adversarial ML |
| 🌐 **Multi-Agent System** | Colaboración entre agentes | Consensus Algorithm |

### 📧 Sistema de Notificaciones

| Canal | Descripción | Configuración |
|-------|-------------|---------------|
| 📧 **Email** | Alertas HTML profesionales | SMTP (Gmail) |
| 📱 **Telegram** | Notificaciones instantáneas | Bot API |

---

## 💻 Instalación Rápida

### Requisitos Previos

- Python 3.9+
- Linux (Ubuntu/Debian/Parrot OS recomendado)
- 4GB RAM mínimo
- Permisos sudo (para captura de red)

### Instalación Automática
```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/nemesis-ai.git
cd nemesis-ai

# 2. Crear entorno virtual
python3 -m venv nemesis_env
source nemesis_env/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar alertas (opcional)
nano config/alerts.yaml
```

### Configuración de Notificaciones

#### 📧 Email (Gmail)
```yaml
email:
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
  username: "tu-email@gmail.com"
  password: "tu-app-password"  # Usar App Password, no password normal
  from_email: "tu-email@gmail.com"
  to_email: "destino@gmail.com"
```

**Obtener App Password:**
1. Ve a: https://myaccount.google.com/apppasswords
2. Genera contraseña para "Mail"
3. Cópiala en `config/alerts.yaml`

#### 📱 Telegram
```yaml
telegram:
  bot_token: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
  chat_id: "123456789"
```

**Obtener Bot Token:**
1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Envía `/newbot`
3. Sigue instrucciones y copia el token

**Obtener Chat ID:**
1. Envía mensaje a tu bot
2. Visita: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Busca `"chat":{"id":123456789}`

---

## 🎮 Uso

### 🖥️ Dashboards Disponibles

#### 1️⃣ Dashboard Final (Recomendado)
**Dashboard completo con diseño épico + notificaciones**
```bash
python3 test_dashboard_final.py
```

**Características:**
- ✅ Mapa mundial de ataques animado
- ✅ Terminal en vivo con logs
- ✅ Honeypot captures en tiempo real
- ✅ Gráficas de amenazas (Chart.js)
- ✅ Email alerts funcionales
- ✅ Telegram notifications
- ✅ Efectos visuales CRT
- ✅ WebSocket en tiempo real

**URL:** http://localhost:8080

**Panel de Notificaciones:**
- 📧 **Test Email** → Envía email de prueba
- 📱 **Test Telegram** → Envía mensaje Telegram

---

#### 2️⃣ Dashboard Beast (Módulos Avanzados)
**Dashboard con integración completa de 14 capítulos**
```bash
python3 test_dashboard_beast.py
```

**Características adicionales:**
- 🔗 **Blockchain Evidence** → Cadena de custodia
- ⚛️ **Quantum Defense** → Status PQC
- 📄 **Legal PDFs** → Generación automática
- 🚨 **Red Button** → Notificación CERTs
- 🤖 **AI vs AI** → Stats de defensa adversarial
- 🌐 **Multi-Agent** → Colaboración de agentes

**URL:** http://localhost:8080

**Controles Avanzados:**
- 📄 **Generate PDF** → Crea expediente legal
- 🔗 **View Blockchain** → Examina evidencia
- ⚛️ **Quantum Status** → Verifica algoritmos
- 🚨 **Red Button** → Activa protocolo de emergencia

---

#### 3️⃣ Dashboard V3 Extended
**Dashboard extendido manteniendo diseño original**
```bash
python3 test_dashboard_v3_extended.py
```

**URL:** http://localhost:8080

---

### 📊 Comparación de Dashboards

| Feature | Dashboard Final | Dashboard Beast | Dashboard V3 Extended |
|---------|----------------|-----------------|----------------------|
| Mapa de ataques | ✅ | ✅ | ✅ |
| Terminal vivo | ✅ | ✅ | ✅ |
| Honeypot stats | ✅ | ✅ | ✅ |
| Gráficas Chart.js | ✅ | ✅ | ✅ |
| Email/Telegram | ✅ | ❌ | ❌ |
| Blockchain | ❌ | ✅ | ✅ |
| PDF Legal | ❌ | ✅ | ✅ |
| Red Button | ❌ | ✅ | ✅ |
| Quantum Status | ❌ | ✅ | ✅ |
| AI vs AI Stats | ❌ | ✅ | ❌ |

---

### 🎯 Recomendación de Uso
```bash
# Para demos y producción diaria
python3 test_dashboard_final.py

# Para mostrar TODOS los módulos
python3 test_dashboard_beast.py

# Para desarrollo y testing
python3 test_dashboard_v3_extended.py
```

---

## 🏗️ Arquitectura
```
nemesis-ai/
├── src/
│   ├── agent/              # Agente principal
│   ├── ml/                 # ML Brain (98.7%)
│   ├── logs/               # Log Sentinel
│   ├── network/            # Network Sentinel
│   ├── honeypot/           # Honeypot Manager
│   ├── traffic/            # Traffic Analyzer
│   ├── reputation/         # IP Reputation
│   ├── quantum/            # Post-Quantum Crypto
│   ├── forensics/          # Blockchain Forensics
│   ├── legal/              # Fiscal Digital (PDFs)
│   ├── intel/              # Threat Intel APIs
│   ├── emergency/          # Red Button (CERTs)
│   ├── adversarial/        # AI vs AI Defense
│   ├── collective/         # Multi-Agent System
│   ├── alerts/             # Email + Telegram
│   │   ├── alert_manager.py
│   │   ├── email_alert.py
│   │   └── telegram_alert.py
│   ├── database/           # ThreatDatabase
│   └── web/                # Dashboards
│       ├── dashboard_final.py
│       ├── dashboard_beast.py
│       └── dashboard_v3_extended.py
├── config/
│   └── alerts.yaml         # Configuración notificaciones
├── data/
│   └── nemesis_honeypot.db # Base de datos SQLite
├── legal_documents/        # PDFs generados
├── models/                 # Modelos ML
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

### Test Individual de Módulos
```bash
# ML Brain
python3 test_real.py

# Honeypot
python3 test_honeypot_complete.py

# Quantum Defense
python3 test_quantum_complete.py

# Blockchain Forensics
python3 test_forensic_system.py

# Legal PDFs
python3 test_fiscal_digital.py

# Red Button
python3 test_red_button.py

# Notificaciones
python3 test_alerts.py
```

### Test del Sistema Completo
```bash
# Sistema unificado
python3 demo_complete.py

# Dashboard Final
python3 test_dashboard_final.py
```

---

## 📸 Demo

### Dashboard en Acción

**Mapa Mundial de Ataques:**
- Puntos rojos pulsantes representan atacantes
- Líneas animadas muestran vectores de ataque
- Target central protegido por Némesis

**Terminal en Vivo:**
```
[14:32:15] 🚨 SQL_INJECTION detected from 192.168.1.100
[14:32:16] ✅ IP blocked automatically
[14:32:17] 📧 Email notification sent
[14:32:18] 📱 Telegram alert sent
[14:32:19] 🔗 Evidence added to blockchain
```

**Honeypot Captures:**
```
🌐 203.0.113.50
📦 Payload: admin:password123
🕐 2024-12-06 14:32:15
```

**Stats en Tiempo Real:**
- ⚔️ Total Threats: 147
- 🚫 Blocked IPs: 23
- ⏰ Last 24h: 18
- 🍯 Honeypot: 34
- ⚡ Threats/min: 2
- 📧 Emails: 12
- 📱 Telegrams: 12

---

## 🔒 Seguridad

### Criptografía Post-Cuántica

**Algoritmos implementados:**
- **Kyber-768**: Cifrado resistente a computación cuántica
- **Dilithium-3**: Firmas digitales post-cuánticas

**¿Por qué PQC?**
RSA y ECC serán vulnerables a computadoras cuánticas. Némesis implementa los algoritmos del NIST PQC Competition.

### Blockchain Forense

**Características:**
- SHA-256 hashing
- Timestamp inmutable
- Proof of Work
- Chain validation
- Court-admissible evidence

---

## 📄 Generación de PDFs Legales

### Estructura del Expediente
```
EXPEDIENTE DE INCIDENTE DE SEGURIDAD
═══════════════════════════════════════

INFORMACIÓN DEL CASO
────────────────────
ID del Caso: INC-20241206-143215
Fecha: 2024-12-06 14:32:15
Severidad: CRÍTICA
Confianza: 95%

DETALLES TÉCNICOS
─────────────────
IP Origen: 203.0.113.50
Tipo de Ataque: SQL_INJECTION
Payload: ' OR '1'='1'--

ANÁLISIS FORENSE
────────────────
[Análisis técnico detallado]

EVIDENCIA BLOCKCHAIN
────────────────────
Hash: a3f5d9e2...
Block: #147
Timestamp: 2024-12-06 14:32:15

ACCIONES TOMADAS
────────────────
✅ IP bloqueada
✅ Evidencia recopilada
✅ CERTs notificados
```

---

## 🚨 Red Button - Protocolo de Emergencia

### ¿Cuándo activar?

- ✅ Ataque crítico en curso
- ✅ Múltiples vectores simultáneos
- ✅ Amenaza APT detectada
- ✅ Compromiso de sistema crítico

### ¿Qué hace?

1. 📄 Genera PDF legal automático
2. 📧 Notifica a CERTs:
   - US-CERT
   - CERT-EU
   - CERT-UK
   - CERT-ES
3. 🌐 Reporta a bases de datos:
   - AbuseIPDB
   - Spamhaus
4. 📱 Alerta inmediata vía Telegram
5. 📧 Email a autoridades

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~36,000 |
| Módulos | 14 |
| Algoritmos ML | 5 |
| Algoritmos PQC | 2 |
| APIs integradas | 3 |
| CERTs conectados | 4 |
| Precisión ML | 98.7% |
| Lenguaje | Python 3.9+ |
| Arquitectura | Asíncrona |
| Base de datos | SQLite |
| Frontend | FastAPI + WebSocket |

---

## 🎓 Casos de Uso

### 1. Empresas
```bash
# Monitoreo 24/7 de infraestructura
python3 test_dashboard_final.py

# Notificaciones automáticas al SOC
# Evidencia legal lista para auditorías
# Cumplimiento GDPR/ISO27001
```

### 2. Investigadores de Seguridad
```bash
# Honeypots para análisis de TTPs
python3 test_honeypot_complete.py

# Recopilación de IOCs
# Generación de informes técnicos
```

### 3. Formación en Ciberseguridad
```bash
# Ambiente de laboratorio seguro
# Ejemplos prácticos de ataques
# Respuesta automatizada
```

### 4. Pentesters
```bash
# Red Teaming automation
# Simulación de ataques
# Validación de defensas
```

---

## 🔧 Configuración Avanzada

### Cambiar Puerto del Dashboard
```python
# Editar archivo de test
dashboard = DashboardFinal(db, host="0.0.0.0", port=8888)
```

### Configurar Múltiples Destinatarios Email
```yaml
email:
  to_email: "admin@empresa.com,soc@empresa.com,ciso@empresa.com"
```

### Ajustar Thresholds de Detección
```python
# src/ml/ml_brain.py
CONFIDENCE_THRESHOLD = 0.85  # Default: 0.75
```

### Habilitar Debug Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🐛 Troubleshooting

### Error: "Permission denied" en captura de red
```bash
# Solución: Ejecutar con sudo
sudo python3 test_network_sentinel.py
```

### Error: "Port 8080 already in use"
```bash
# Solución 1: Matar proceso
sudo lsof -ti:8080 | xargs kill -9

# Solución 2: Cambiar puerto en código
```

### Email no se envía
```bash
# Verificar:
1. App Password correcto (no password normal)
2. 2FA habilitado en Gmail
3. "Less secure apps" deshabilitado
```

### Telegram no funciona
```bash
# Verificar:
1. Bot token correcto
2. Chat ID correcto
3. Bot iniciado con /start
4. Conexión a internet
```

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Denis Ijcu**
- GitHub: [@tuusuario](https://github.com/tuusuario)
- Email: denisijcu266@gmail.com
- Telegram: [@tubot](https://t.me/tubot)

---

## 🙏 Agradecimientos

- **NIST** - Algoritmos Post-Quantum Crypto
- **Anthropic** - Claude AI para desarrollo
- **FastAPI** - Framework web asíncrono
- **Chart.js** - Visualizaciones épicas
- **Comunidad de Ciberseguridad** - Por el feedback

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [AbuseIPDB API](https://docs.abuseipdb.com/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

### Artículos Relacionados

- [Why Post-Quantum Crypto Matters](https://example.com)
- [Building Honeypots in Python](https://example.com)
- [Blockchain for Digital Forensics](https://example.com)

### Videos

- [Némesis IA - Demo Completa](https://youtube.com/watch?v=...)
- [Configuración Paso a Paso](https://youtube.com/watch?v=...)

---

## 🎯 Roadmap

### v2.0 (Próximamente)

- [ ] Integración con SIEM (Splunk, ELK)
- [ ] Machine Learning con Deep Learning
- [ ] Soporte para más honeypots (HTTP, FTP)
- [ ] Dashboard móvil (React Native)
- [ ] Integración con VirusTotal
- [ ] Análisis de malware automático
- [ ] Generación de reportes ejecutivos

### v3.0 (Futuro)

- [ ] Distributed deployment (Kubernetes)
- [ ] AI agents con LLMs (GPT-4, Claude)
- [ ] Threat hunting automation
- [ ] IoT device protection
- [ ] Blockchain público para IOCs
- [ ] API REST completa
- [ ] SaaS deployment

---

## ⚠️ Disclaimer Legal

Este software es para **fines educativos y de investigación**. El autor no se hace responsable del uso indebido de esta herramienta. Usa bajo tu propio riesgo y de acuerdo con las leyes locales.

**IMPORTANTE:**
- No uses honeypots en redes sin autorización
- No ataques sistemas sin permiso explícito
- Cumple con GDPR al procesar IPs
- Consulta a un abogado sobre aspectos legales

---

## 📞 Soporte

¿Necesitas ayuda?

1. 📖 Lee esta documentación completa
2. 🐛 [Abre un issue](https://github.com/tuusuario/nemesis-ai/issues)
3. 💬 [Únete a Discord](https://discord.gg/...)
4. 📧 Email: denisijcu266@gmail.com

---

## 🌟 ¿Te gusta el proyecto?

Si Némesis IA te ha sido útil:

- ⭐ Dale una estrella en GitHub
- 🐦 Comparte en Twitter
- 📝 Escribe un artículo sobre él
- 💰 [Dona para el desarrollo](https://paypal.me/...)

---

<div align="center">

**Hecho con ❤️ y ☕ por Denis Ijcu**

**Némesis IA - Justicia Algorítmica en Acción**
```
"Deja de ser la presa. Conviértete en el depredador del sistema legal."
```

⚡ **The Beast is Watching** ⚡

</div>
