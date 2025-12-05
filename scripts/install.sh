#!/bin/bash
# Némesis IA - Installation Script
# Automatic installation for Ubuntu/Debian systems

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    NÉMESIS IA                            ║"
echo "║        Sistema de Defensa Cibernética con IA            ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar si es root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}Error: No ejecutar como root${NC}"
   echo "Ejecuta sin sudo. El script pedirá permisos cuando los necesite."
   exit 1
fi

echo -e "${GREEN}[1/8] Detectando sistema operativo...${NC}"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    echo "Detectado: $OS $VER"
else
    echo -e "${RED}No se pudo detectar el sistema operativo${NC}"
    exit 1
fi

echo -e "${GREEN}[2/8] Actualizando repositorios...${NC}"
sudo apt update

echo -e "${GREEN}[3/8] Instalando dependencias del sistema...${NC}"
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    cmake \
    ninja-build \
    libssl-dev \
    pkg-config \
    curl \
    wget

echo -e "${GREEN}[4/8] Creando entorno virtual de Python...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual ya existe"
fi

echo -e "${GREEN}[5/8] Activando entorno virtual...${NC}"
source venv/bin/activate

echo -e "${GREEN}[6/8] Actualizando pip...${NC}"
pip install --upgrade pip setuptools wheel

echo -e "${GREEN}[7/8] Instalando dependencias de Python...${NC}"
pip install -r requirements/base.txt

echo -e "${YELLOW}[7.5/8] Instalando liboqs (Post-Quantum Crypto)...${NC}"
echo "Esto puede tardar varios minutos..."

# Verificar si liboqs ya está instalado
if python3 -c "import oqs" 2>/dev/null; then
    echo "✓ liboqs ya instalado"
else
    echo "Instalando liboqs-python..."
    pip install liboqs-python --break-system-packages || {
        echo -e "${YELLOW}⚠️  Instalación de liboqs falló. Continuando sin criptografía post-cuántica.${NC}"
    }
fi

echo -e "${GREEN}[8/8] Configurando estructura de directorios...${NC}"
mkdir -p logs
mkdir -p data
mkdir -p models
mkdir -p blockchain

echo -e "${GREEN}[8.1/8] Copiando configuración de ejemplo...${NC}"
if [ ! -f "config/nemesis.conf" ]; then
    cp config/nemesis.conf.example config/nemesis.conf
    echo "✓ Configuración copiada a config/nemesis.conf"
    echo -e "${YELLOW}⚠️  Edita config/nemesis.conf antes de usar en producción${NC}"
else
    echo "✓ Configuración ya existe"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗"
echo "║           ✅ INSTALACIÓN COMPLETADA                      ║"
echo "╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Activar entorno virtual:"
echo "   source venv/bin/activate"
echo ""
echo "2. Editar configuración:"
echo "   nano config/nemesis.conf"
echo ""
echo "3. Entrenar modelo inicial:"
echo "   python3 src/ml/train_brain.py"
echo ""
echo "4. Iniciar agente:"
echo "   python3 src/core/nemesis_agent.py"
echo ""
echo "Documentación completa: docs/installation.md"
echo ""
echo -e "${YELLOW}⚠️  Recuerda configurar API keys en config/nemesis.conf${NC}"