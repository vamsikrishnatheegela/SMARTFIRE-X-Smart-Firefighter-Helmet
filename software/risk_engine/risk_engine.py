"""
SMARTFIRE-X confidence-aware, rule-based risk engine.
Prototype only: not certified for real-world firefighting or life-safety decisions.
"""
from collections import deque
from dataclasses import dataclass, asdict
import math
import time

@dataclass
class RiskResult:
    level: str
    score: int
    confidence: int
    reasons: list[str]
    data_quality: str
    stale: bool
    def to_dict(self):
        return asdict(self)

class RiskEngine:
    """Rule-based multi-sensor risk scoring with freshness and evidence quality."""
    def __init__(self, history_size: int = 30):
        self.history_size = history_size
        self.history = {}
        self.last_values = {}
        self.stuck_counts = {}
        self.last_update = None

    @staticmethod
    def _number(packet: dict, key: str):
        v = packet.get(key)
        return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) else None

    def evaluate(self, packet: dict, packet_time: float | None = None) -> RiskResult:
        now = time.time() if packet_time is None else packet_time
        reasons = []
        score = 0
        present = 0
        expected = ["temp_c", "ambient_c", "humidity_pct", "co2_ppm", "mq2_raw"]
        values = {k: self._number(packet, k) for k in expected}
        for k, v in values.items():
            if v is not None:
                present += 1
                self.history.setdefault(k, deque(maxlen=self.history_size)).append(v)
        t, amb, co2, mq = values["temp_c"], values["ambient_c"], values["co2_ppm"], values["mq2_raw"]
        if t is not None:
            if t >= 60: score += 45; reasons.append("Object temperature is very high (>=60 °C)")
            elif t >= 50: score += 30; reasons.append("Object temperature exceeds 50 °C")
            elif t >= 40: score += 12; reasons.append("Object temperature is elevated (>=40 °C)")
        if amb is not None:
            if amb >= 60: score += 40; reasons.append("Ambient temperature is very high (>=60 °C)")
            elif amb >= 45: score += 25; reasons.append("Ambient temperature exceeds 45 °C")
            elif amb >= 38: score += 10; reasons.append("Ambient temperature is elevated (>=38 °C)")
        if co2 is not None:
            if co2 >= 3000: score += 35; reasons.append("CO₂ reading is very high (>=3000 ppm)")
            elif co2 >= 1500: score += 22; reasons.append("CO₂ reading exceeds 1500 ppm")
            elif co2 >= 1000: score += 8; reasons.append("CO₂ reading is elevated (>=1000 ppm)")
        if mq is not None:
            if mq >= 1600: score += 25; reasons.append("MQ-2 raw ADC is very high (>=1600)")
            elif mq >= 1200: score += 15; reasons.append("MQ-2 raw ADC exceeds prototype threshold")
        if t is not None and co2 is not None and t >= 40 and co2 >= 1000:
            score += 15; reasons.append("Combined evidence: elevated temperature and CO₂")
        if amb is not None and mq is not None and amb >= 38 and mq >= 1000:
            score += 10; reasons.append("Combined evidence: elevated ambient temperature and MQ-2")
        for key, delta, label in [
            ("temp_c", 2.0, "Object temperature increased by >=2 °C over recent packets"),
            ("ambient_c", 2.0, "Ambient temperature increased by >=2 °C over recent packets"),
            ("co2_ppm", 200.0, "CO₂ increased by >=200 ppm over recent packets"),
            ("mq2_raw", 200.0, "MQ-2 raw reading increased by >=200 ADC counts"),
        ]:
            hist = self.history.get(key)
            if hist and len(hist) >= 5 and hist[-1] - hist[0] >= delta:
                score += 8; reasons.append(label)
        for key in expected:
            v = values[key]
            if v is None: continue
            prev = self.last_values.get(key)
            self.stuck_counts[key] = self.stuck_counts.get(key, 0) + 1 if prev is not None and abs(v - prev) < 1e-9 else 0
            self.last_values[key] = v
        missing = [k for k in expected if values[k] is None]
        stuck = [k for k, n in self.stuck_counts.items() if n >= 20]
        if missing: reasons.append("Missing readings: " + ", ".join(missing))
        if stuck: reasons.append("Possible stuck sensor values: " + ", ".join(stuck))
        score = min(100, score)
        level = "CRITICAL" if score >= 70 else "HIGH" if score >= 45 else "GUARDED" if score >= 20 else "NORMAL"
        coverage = round(100 * present / len(expected))
        confidence = max(0, min(100, coverage - (15 if missing else 0) - (15 if stuck else 0)))
        data_quality = "GOOD" if coverage == 100 and not stuck else "PARTIAL" if present >= 3 else "POOR"
        stale = self.last_update is not None and now - self.last_update > 3
        self.last_update = now
        if stale: reasons.append("Telemetry gap detected before this packet")
        if not reasons: reasons.append("No configured prototype risk rules triggered")
        return RiskResult(level, score, confidence, reasons, data_quality, stale)
