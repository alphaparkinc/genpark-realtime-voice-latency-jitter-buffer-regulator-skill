import sys, json
from client import RealtimeVoiceLatencyJitterBufferRegulatorClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    regulator = RealtimeVoiceLatencyJitterBufferRegulatorClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-realtime-voice-latency-jitter-buffer-regulator-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    delays = req.get("delays", [40.0, 45.0])
    res = regulator.simulate_packet_stream(delays)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
