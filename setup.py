#!/usr/bin/env python3
"""
Némesis IA - Setup Script

Copyright (C) 2025 Némesis AI Project Contributors
Licensed under GPL-3.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Leer requirements
requirements_file = Path(__file__).parent / "requirements" / "base.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="nemesis-ai",
    version="1.0.0",
    description="Sistema Automatizado de Defensa Cibernética con Inteligencia Artificial",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Némesis AI Project Contributors",
    author_email="contact@nemesis-ai.org",
    url="https://github.com/nemesis-ai/nemesis",
    license="GPL-3.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "nemesis=core.nemesis_agent:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
    ],
    keywords="cybersecurity ai machine-learning threat-detection honeypot post-quantum",
    project_urls={
        "Bug Reports": "https://github.com/nemesis-ai/nemesis/issues",
        "Documentation": "https://github.com/nemesis-ai/nemesis/tree/main/docs",
        "Source": "https://github.com/nemesis-ai/nemesis",
    },
)
