import sys
sys.path.insert(0, 'src')

from core.nemesis_agent import NemesisAgent

agent = NemesisAgent()

print("=" * 60)
print("📊 AGENTE NÉMESIS - ESTADÍSTICAS")
print("=" * 60)
print(f"🎯 Threshold: {agent.threshold}")
print(f"🧠 Modelo: {agent.model_path}")
print(f"✅ Whitelist IPs: {agent._whitelist_ips}")
print("=" * 60)