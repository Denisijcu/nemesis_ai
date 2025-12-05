#!/bin/bash
# Genera tráfico HTTP malicioso para testing

echo "🚀 Generando tráfico de prueba..."
echo ""

# Esperar 2 segundos
sleep 2

echo "1. Tráfico normal..."
curl -s http://neverssl.com > /dev/null

sleep 1

echo "2. SQL Injection..."
curl -s "http://httpbin.org/get?id=1' OR '1'='1'--" > /dev/null

sleep 1

echo "3. XSS Attack..."
curl -s "http://httpbin.org/get?search=<script>alert(1)</script>" > /dev/null

sleep 1

echo "4. Path Traversal..."
curl -s "http://httpbin.org/get?file=../../../etc/passwd" > /dev/null

sleep 1

echo "5. Command Injection..."
curl -s "http://httpbin.org/get?cmd=;cat /etc/passwd" > /dev/null

sleep 1

echo "6. Más tráfico normal..."
curl -s http://example.com > /dev/null

echo ""
echo "✅ Tráfico generado!"