import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class RealtimeVoiceLatencyJitterBufferRegulatorClient:
    """
    Adaptive jitter buffer regulator for WebRTC / Realtime Voice Agent connections.
    Maintains exponentially weighted moving average (EWMA) delay and variation,
    computing the optimal playout delay D_p = mu + 3.0 * sigma to balance packet loss against latency.
    """
    def __init__(self, alpha=0.125, beta=0.25):
        self.alpha = alpha # EWMA weight for delay
        self.beta = beta   # EWMA weight for delay variation (jitter)
        self.d_mean = 40.0 # initial baseline delay (ms)
        self.d_var = 10.0  # initial baseline jitter (ms)

    def update_packet_arrival(self, packet_delay_ms):
        # RFC 3550 / Jacobson algorithm
        diff = abs(packet_delay_ms - self.d_mean)
        self.d_mean = (1.0 - self.alpha) * self.d_mean + self.alpha * packet_delay_ms
        self.d_var = (1.0 - self.beta) * self.d_var + self.beta * diff

        # Playout delay recommendation: mean + 3 * jitter variation
        optimal_playout_ms = self.d_mean + 3.0 * self.d_var
        
        # Enforce bounds: min 20ms, max 250ms for conversational interactivity
        bounded_playout_ms = max(20.0, min(250.0, optimal_playout_ms))
        
        # Late-packet drop risk estimation
        late_drop_prob = max(0.001, min(0.15, math.exp(-(bounded_playout_ms - self.d_mean) / max(1.0, self.d_var))))

        return {
            "packet_delay_ms": packet_delay_ms,
            "smoothed_delay_mean_ms": round(self.d_mean, 2),
            "smoothed_jitter_variation_ms": round(self.d_var, 2),
            "recommended_playout_buffer_ms": int(math.ceil(bounded_playout_ms)),
            "estimated_late_loss_rate_pct": round(late_drop_prob * 100.0, 2),
            "buffer_health": "EXCELLENT" if bounded_playout_ms <= 80 else ("ACCEPTABLE" if bounded_playout_ms <= 150 else "CONGESTED")
        }

    def simulate_packet_stream(self, delays_stream):
        history = []
        for delay in delays_stream:
            metrics = self.update_packet_arrival(delay)
            history.append(metrics)
        return {
            "status": "success",
            "packets_processed": len(delays_stream),
            "final_playout_buffer_ms": history[-1]["recommended_playout_buffer_ms"] if history else 0,
            "telemetry_stream": history
        }
