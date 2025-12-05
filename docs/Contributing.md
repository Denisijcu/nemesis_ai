# Contribuyendo a Némesis IA

¡Gracias por tu interés en contribuir a Némesis IA! 🎉

Este documento es tu guía completa para contribuir al proyecto.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Configurando Entorno de Desarrollo](#configurando-entorno-de-desarrollo)
- [Workflow de Contribución](#workflow-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Tests](#tests)
- [Documentación](#documentación)

---

## 🤝 Código de Conducta

Lee nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Al participar, aceptas seguir sus términos.

**TL;DR:** Sé respetuoso, inclusivo y profesional.

---

## 💡 ¿Cómo Puedo Contribuir?

### Reportar Bugs

- Usa el [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Incluye pasos para reproducir
- Añade logs relevantes
- Especifica tu entorno (OS, Python version, etc.)

### Sugerir Features

- Usa el [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explica el problema que resuelve
- Proporciona ejemplos de uso
- Discute alternativas consideradas

### Mejorar Documentación

- Corregir typos
- Clarificar instrucciones confusas
- Añadir ejemplos
- Traducir a otros idiomas

### Contribuir Código

- Arreglar bugs
- Implementar features
- Optimizar performance
- Añadir tests

---

## 🛠️ Configurando Entorno de Desarrollo

### 1. Fork y Clone

```bash
# Fork en GitHub, luego:
git clone https://github.com/TU_USUARIO/nemesis.git
cd nemesis
git remote add upstream https://github.com/nemesis-ai/nemesis.git
```

### 2. Instalar Dependencias

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
pip install -r requirements/dev.txt
```

### 3. Configurar Pre-commit Hooks

```bash
pre-commit install
```

Esto ejecutará automáticamente:
- black (formatting)
- flake8 (linting)
- mypy (type checking)

### 4. Verificar Instalación

```bash
pytest tests/
flake8 src/
mypy src/
```

---

## 🔄 Workflow de Contribución

### 1. Sincronizar con Upstream

```bash
git checkout main
git pull upstream main
```

### 2. Crear Branch

```bash
git checkout -b feature/nombre-descriptivo
# o
git checkout -b bugfix/descripcion-bug
```

**Convenciones de nombres:**
- `feature/` - Nuevos features
- `bugfix/` - Arreglos de bugs
- `docs/` - Cambios de documentación
- `refactor/` - Refactorización de código
- `test/` - Añadir/mejorar tests

### 3. Hacer Cambios

- Escribe código limpio siguiendo [Estándares](#estándares-de-código)
- Añade tests para nuevo código
- Actualiza documentación si es necesario

### 4. Commit

```bash
git add .
git commit -m "feat: Descripción concisa del cambio

- Detalle 1
- Detalle 2

Closes #123"
```

**Formato de mensajes:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat` - Nuevo feature
- `fix` - Bug fix
- `docs` - Cambios de documentación
- `style` - Formatting, sin cambios de código
- `refactor` - Refactorización
- `test` - Añadir tests
- `chore` - Mantenimiento

### 5. Push y Pull Request

```bash
git push origin feature/nombre-descriptivo
```

Luego en GitHub:
1. Ve a tu fork
2. Click "Pull Request"
3. Llena el template de PR
4. Espera code review

---

## 📝 Estándares de Código

### Python Style Guide

Seguimos **PEP 8** con black formatter.

#### Type Hints

```python
def analyze_threat(event: ThreatEvent) -> ThreatVerdict:
    """
    Analyze a potential threat event.
    
    Args:
        event: The suspicious event to analyze
        
    Returns:
        Verdict indicating whether event is malicious
        
    Raises:
        ModelNotLoadedError: If AI model hasn't been loaded
    """
    ...
```

#### Docstrings

Usa formato Google:

```python
def function(arg1: str, arg2: int) -> bool:
    """Summary line.

    Extended description of function.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: If arg2 is negative
    """
    ...
```

#### Imports

```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# 3. Local
from nemesis.core import NemesisAgent
from nemesis.utils import calculate_entropy
```

#### Error Handling

```python
# Usa excepciones específicas
try:
    model = load_model("model.joblib")
except FileNotFoundError as e:
    raise ModelNotLoadedError(f"Model file not found: {e}") from e
```

---

## 🧪 Tests

### Escribir Tests

```python
# tests/unit/test_agent.py
import pytest
from nemesis.core import NemesisAgent

class TestNemesisAgent:
    @pytest.fixture
    def agent(self):
        return NemesisAgent(interface="lo")
    
    def test_detection(self, agent):
        """Should detect SQL injection"""
        event = create_sql_injection_event()
        verdict = agent.analyze(event)
        assert verdict.is_malicious is True
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Tests específicos
pytest tests/unit/test_agent.py::TestNemesisAgent::test_detection
```

### Coverage

- Objetivo: **80% minimum** para nuevo código
- Módulos críticos: **95%+**

---

## 📖 Documentación

### Documentar Features

Cuando añades un feature:
1. Actualiza README.md si es relevante
2. Añade docstrings comprehensivos
3. Crea ejemplos de uso
4. Actualiza API docs si aplica

### Escribir Tutoriales

Los tutoriales van en `docs/tutorials/`:
- Paso a paso
- Con código funcional
- Screenshots si ayudan
- Links a conceptos relacionados

---

## 🎯 Good First Issues

¿Nuevo en el proyecto? Busca issues con label `good first issue`:

Ejemplos:
- Corregir typos
- Añadir tests
- Mejorar mensajes de error
- Traducir documentación

---

## 💬 ¿Preguntas?

- **GitHub Discussions:** Para preguntas generales
- **Discord:** Para chat en tiempo real (link en README)
- **Issues:** Para bugs y features

---

## 🏆 Reconocimiento

Todos los contributors son reconocidos en:
- README.md
- CONTRIBUTORS.md
- Release notes

---

**¡Gracias por hacer de Némesis IA un proyecto mejor!** 🚀