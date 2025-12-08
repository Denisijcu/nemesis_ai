FROM python:3.11-slim

LABEL maintainer="Denisijcu"
LABEL description="Nemesis AI - Autonomous Defense System"

# 1. Instalar compiladores
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Instalar dependencias (CON TIMEOUT AUMENTADO)
COPY requirements.txt .
# Aquí está el truco: agregamos --default-timeout=100
RUN pip install --default-timeout=100 --no-cache-dir --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# 3. Copiar código
COPY . .

# 4. Exponer puerto
EXPOSE 8000

# 5. Configurar rutas
ENV PYTHONPATH=/app:/app/src:/app/src/core

# 6. Punto de entrada
CMD ["python", "test_dashboard_unified.py"]