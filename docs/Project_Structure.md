# Estructura del Proyecto Némesis IA

Este documento explica la organización del repositorio.

## 📁 Estructura de Directorios

```
nemesis-ai/
├── README.md                    # Descripción principal del proyecto
├── LICENSE                      # GPL-3.0 License
├── CONTRIBUTING.md              # Guía de contribución
├── setup.py                     # Setup para instalación con pip
├── .gitignore                   # Archivos ignorados por git
│
├── src/                         # Código fuente principal
│   ├── core/                    # Módulo principal
│   │   ├── __init__.py
│   │   └── nemesis_agent.py     # ⭐ Agente Némesis (Capítulo 1)
│   ├── ml/                      # Machine Learning
│   │   ├── __init__.py
│   │   └── train_brain.py       # Entrenamiento del modelo
│   ├── deception/               # Honeypots y deception tech
│   ├── crypto/                  # Criptografía post-cuántica
│   ├── reporting/               # Generación de reportes
│   ├── p2p/                     # Red peer-to-peer
│   └── utils/                   # Utilidades compartidas
│
├── tests/                       # Tests automatizados
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Datos de prueba
│
├── docs/                        # Documentación
│   ├── README.md                # Índice de documentación
│   ├── book/                    # 📖 Libro completo (manuscrito)
│   ├── api/                     # Documentación de API
│   ├── architecture/            # Diagramas de arquitectura
│   └── tutorials/               # Tutoriales paso a paso
│
├── config/                      # Archivos de configuración
│   └── nemesis.conf.example     # Template de configuración
│
├── requirements/                # Dependencias Python
│   ├── base.txt                 # Dependencias core
│   ├── dev.txt                  # Dependencias de desarrollo
│   └── test.txt                 # Dependencias de testing
│
├── scripts/                     # Scripts de utilidad
│   ├── install.sh               # ⭐ Instalador automatizado
│   └── setup_dev.sh             # Setup de entorno de desarrollo
│
├── docker/                      # Docker setup
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── examples/                    # Ejemplos de uso
│   ├── basic_deployment/
│   ├── multi_node_network/
│   └── integration_with_siem/
│
├── data/                        # Datos (gitignored)
├── models/                      # Modelos ML (gitignored)
├── blockchain/                  # Blockchain data (gitignored)
└── logs/                        # Logs (gitignored)
```

## 🚀 Estado Actual del Proyecto

### ✅ Implementado (v1.0 - Capítulo 1)

- **README.md** - Documentación principal completa
- **LICENSE** - GPL-3.0
- **CONTRIBUTING.md** - Guía de contribución completa
- **src/core/nemesis_agent.py** - Agente Némesis funcional
- **config/nemesis.conf.example** - Template de configuración
- **requirements/** - Dependencias definidas
- **scripts/install.sh** - Instalador automatizado
- **setup.py** - Instalación como paquete Python

### 🚧 Pendiente de Implementación

#### Capítulo 2-3 (Módulo 1)
- `src/ml/train_brain.py` - Entrenamiento del modelo
- `src/core/log_sentinel.py` - Sentinel de logs en tiempo real

#### Capítulo 4-6 (Módulo 2)
- `src/deception/honeypot_ssh.py` - Honeypot SSH
- `src/deception/honeypot_http.py` - Honeypot HTTP
- `src/deception/tarpit.py` - Tarpit implementation
- `src/deception/profiler.py` - Perfilado de atacantes

#### Capítulo 7-9 (Módulo 3)
- `src/crypto/quantum_shield.py` - Criptografía post-cuántica
- `src/crypto/blockchain.py` - Blockchain forense

#### Capítulo 10-12 (Módulo 4)
- `src/reporting/pdf_generator.py` - Generación de PDFs
- `src/reporting/abuse_reporter.py` - Integración AbuseIPDB
- `src/reporting/mailer.py` - Envío automático de emails

#### Capítulo 13-14 (Módulo 5)
- `src/ml/adversarial.py` - Defensa adversarial
- `src/p2p/hive_node.py` - Nodo P2P
- `src/p2p/blockchain.py` - Blockchain distribuida
- `src/p2p/api.py` - API REST

## 📝 Próximos Pasos

### Para Desarrolladores

1. **Implementar Capítulo 2:**
   ```bash
   # Crear src/ml/train_brain.py
   # Implementar entrenamiento de Random Forest
   # Generar dataset sintético
   ```

2. **Implementar Capítulo 3:**
   ```bash
   # Crear src/core/log_sentinel.py
   # Integrar con nemesis_agent.py
   # Implementar parsers de logs
   ```

3. **Tests:**
   ```bash
   # Crear tests para cada módulo
   # Configurar CI/CD con GitHub Actions
   ```

### Para Contribuyentes

1. **Mejorar Documentación:**
   - Añadir ejemplos de uso
   - Traducir a otros idiomas
   - Crear tutoriales en video

2. **Reportar Issues:**
   - Bugs encontrados
   - Mejoras sugeridas
   - Preguntas de clarificación

## 🎯 Roadmap

- [x] **Fase 1:** Estructura del repositorio y Capítulo 1
- [ ] **Fase 2:** Capítulos 2-3 (ML y Log Analysis)
- [ ] **Fase 3:** Capítulos 4-6 (Deception Tech)
- [ ] **Fase 4:** Capítulos 7-9 (Post-Quantum Crypto)
- [ ] **Fase 5:** Capítulos 10-12 (Automated Reporting)
- [ ] **Fase 6:** Capítulos 13-14 (Adversarial AI y P2P)
- [ ] **Fase 7:** Tests comprehensivos y CI/CD
- [ ] **Fase 8:** Docker y Kubernetes
- [ ] **Fase 9:** Documentación completa y sitio web
- [ ] **Fase 10:** Release v1.0 🚀

## 📖 Convenciones de Código

### Python Style

- **PEP 8** con `black` formatter
- **Type hints** en todas las funciones
- **Docstrings** formato Google
- **Async/await** para operaciones I/O

### Git Commits

```
<type>: <subject>

<body>

<footer>
```

**Types:** feat, fix, docs, style, refactor, test, chore

### Naming

- **Archivos:** `snake_case.py`
- **Clases:** `PascalCase`
- **Funciones:** `snake_case()`
- **Constantes:** `UPPER_SNAKE_CASE`

## 🤝 Cómo Contribuir

1. Fork del repositorio
2. Crear branch: `feature/mi-feature`
3. Implementar con tests
4. Commit siguiendo convenciones
5. Push y crear Pull Request

Ver [CONTRIBUTING.md](../CONTRIBUTING.md) para detalles completos.

---

**¿Preguntas?** Abre un [issue](https://github.com/nemesis-ai/nemesis/issues) o únete a nuestro [Discord](#).