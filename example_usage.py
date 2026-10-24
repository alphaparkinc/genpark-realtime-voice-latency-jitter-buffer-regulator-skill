from client import RealtimeVoiceLatencyJitterBufferRegulatorClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    regulator = RealtimeVoiceLatencyJitterBufferRegulatorClient()
    print("=== REALTIME VOICE LATENCY JITTER BUFFER REGULATOR ===")
    
    # Simulated packet arrival delays under variable network congestion
    delays = [38.0, 42.0, 39.0, 85.0, 110.0, 45.0, 41.0, 37.0]
    res = regulator.simulate_packet_stream(delays)
    
    print(f"Processed {res['packets_processed']} packet arrivals.")
    print("Dynamic Buffer Adaptation Telemetry:")
    for i, t in enumerate(res['telemetry_stream'], 1):
        print(f"  Packet {i}: Arrival={t['packet_delay_ms']}ms -> Buffer={t['recommended_playout_buffer_ms']}ms (Jitter: {t['smoothed_jitter_variation_ms']}ms, Loss: {t['estimated_late_loss_rate_pct']}%) [{t['buffer_health']}]")

if __name__ == "__main__":
    main()
