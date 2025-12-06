#!/usr/bin/env python3
"""Dashboard COMPLETO de Némesis IA"""

import sys
sys.path.insert(0, 'src')

from dashboard.dashboard import create_app
import webbrowser
import threading
import time

def open_browser():
    """Abre browser después de 2 segundos"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard Némesis IA...")
    print("📊 Dashboard: http://localhost:5000")
    print("⚡ Presiona Ctrl+C para detener")
    
    # Abrir browser automáticamente
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Iniciar dashboard
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)