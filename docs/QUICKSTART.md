# 🚀 Guía de Inicio Rápido - Némesis IA

Esta guía te llevará de 0 a tener Némesis funcionando en **10 minutos**.

## ⚡ Instalación Express (Ubuntu/Debian)

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/nemesis-ai.git
cd nemesis-ai

# 2. Ejecutar instalador automático
./scripts/install.sh

# 3. Activar entorno virtual
source venv/bin/activate

# 4. Listo! ✅
```

## 🔧 Configuración Mínima

```bash
# Copiar configuración de ejemplo
cp config/nemesis.conf.example config/nemesis.conf

# Editar (opcional para demo)
nano config/nemesis.conf
```

**Configuración mínima para demo:**
```ini
[general]
node_name = my-nemesis-node
network_interface = eth0
log_level = INFO

[ml]
model_path = models/nemesis_brain.joblib
detection_threshold = 0.90
```

## 🎓 Primera Ejecución

### Paso 1: Entrenar Modelo ML (Capítulo 2) ⭐

```bash
# Entrenar el cerebro de IA
python3 src/ml/train_brain.py

# Output esperado:
# 🧪 Generando dataset sintético...
# ✅ Dataset generado: 10000 muestras
# 🧠 Iniciando entrenamiento del cerebro...
# ✅ Entrenamiento completado en 3.45s
# 📊 Test Accuracy: 98.7%
# 💾 Modelo guardado en models/nemesis_brain.joblib
```

**O usar script interactivo:**
```bash
python3 examples/train_and_test.py
```

Este script:
- Genera 10,000 muestras de tráfico (legítimo + ataques)
- Entrena Random Forest con 100 árboles
- Evalúa con múltiples métricas
- Guarda modelo entrenado
- Prueba con ejemplos reales

### Paso 2: Iniciar Agente

```bash
python3 src/core/nemesis_agent.py
```

**Output esperado:**
```
2025-01-01 10:00:00 - nemesis.core - INFO - Némesis Agent initialized on interface eth0 with threshold 0.9
2025-01-01 10:00:00 - nemesis.core - INFO - 🚀 Iniciando Agente Némesis...
2025-01-01 10:00:00 - nemesis.core - WARNING - ⚠️  Modelo no encontrado. Entrenar primero con train_brain.py
2025-01-01 10:00:00 - nemesis.core - INFO - ✅ Agente Némesis activo y vigilante
2025-01-01 10:00:00 - nemesis.core - INFO - 👁️  Iniciando observación de logs...
```

### Paso 3: Probar Detección (Modo Interactivo)

```python
# En Python shell
from src.core import NemesisAgent
import asyncio

agent = NemesisAgent()

# Simular log con SQL Injection
log = "192.168.1.100 - - [01/Jan/2025:10:00:00] \"GET /login.php?user=' OR '1'='1' HTTP/1.1\""

verdict = asyncio.run(agent.process_log_line(log))
print(verdict)
# ThreatVerdict(is_malicious=True, confidence=0.8, attack_type='SQL_INJECTION', ...)
```

## 📊 Ver Estadísticas

```python
from src.core import NemesisAgent

agent = NemesisAgent()
stats = agent.get_stats()
print(stats)
# {'is_active': False, 'threats_detected': 0, 'whitelist_size': 2, 'model_loaded': False}
```

## 🧪 Ejecutar Tests (Cuando estén implementados)

```bash
# Activar entorno
source venv/bin/activate

# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=src --cov-report=html

# Ver reporte
open htmlcov/index.html
```

## 🐛 Troubleshooting Rápido

### Error: "Modelo no encontrado"
**Solución:** Normal en primera ejecución. El agente funcionará en modo rule-based. Implementa Capítulo 2 para ML.

### Error: "Permission denied" al ejecutar install.sh
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Error: "No module named 'nemesis'"
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements/base.txt
```

### Error: "Port already in use"
```bash
# Ver qué está usando el puerto
lsof -i :8000

# Cambiar puerto en config/nemesis.conf
[api]
api_port = 8001
```

## 📚 Siguiente Lectura

1. **[README.md](README.md)** - Overview completo del proyecto
2. **[CONTRIBUTING.md](CONTRIBUTING.md)** - Cómo contribuir
3. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Estructura del código
4. **[docs/](docs/)** - Documentación técnica completa

## 🎯 Próximos Capítulos a Implementar

- [ ] **Capítulo 2:** Entrenamiento del modelo ML
- [ ] **Capítulo 3:** Sentinel de logs en tiempo real
- [ ] **Capítulo 4-6:** Honeypots y deception tech
- [ ] **Capítulo 7-9:** Criptografía post-cuántica
- [ ] **Capítulo 10-12:** Reportes automáticos
- [ ] **Capítulo 13-14:** IA adversarial y red P2P

## 🤝 ¿Quieres Ayudar?

¡Genial! Busca issues con label `good first issue`:

```bash
# Ejemplos de tareas para comenzar:
- Implementar parsers de logs adicionales
- Añadir tests para nemesis_agent.py
- Mejorar mensajes de error
- Traducir documentación
```

---

**🎉 ¡Felicidades! Ya tienes Némesis ejecutándose.**

**¿Preguntas?** Abre un [issue](https://github.com/nemesis-ai/nemesis/issues) o busca ayuda en [Discussions](https://github.com/nemesis-ai/nemesis/discussions).