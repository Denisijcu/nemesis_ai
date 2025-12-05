#!/usr/bin/env python3
"""
Servidor HTTP local para testing
"""

from http.server import HTTPServer, BaseHTTPRequestHandler

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"📥 Request: {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"OK")
    
    def log_message(self, format, *args):
        pass  # Silenciar logs

print("🚀 Servidor HTTP iniciado en http://localhost:8000")
print("   Usa Ctrl+C para detener")
print()

HTTPServer(('localhost', 8000), TestHandler).serve_forever()