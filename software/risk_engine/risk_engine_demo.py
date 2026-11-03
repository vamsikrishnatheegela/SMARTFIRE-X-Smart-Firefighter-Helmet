import json
import time
from risk_engine import RiskEngine

engine = RiskEngine()
samples = [
    {"temp_c": 30.5, "ambient_c": 30.4, "humidity_pct": 75.0, "co2_ppm": 819, "mq2_raw": 730},
    {"temp_c": 42.0, "ambient_c": 39.0, "humidity_pct": 74.0, "co2_ppm": 1100, "mq2_raw": 1050},
    {"temp_c": 52.0, "ambient_c": 46.0, "humidity_pct": 72.0, "co2_ppm": 1650, "mq2_raw": 1250},
]
for i, packet in enumerate(samples, 1):
    result = engine.evaluate(packet, time.time() + i)
    print(f"\nSample {i}: {json.dumps(packet)}")
    print(json.dumps(result.to_dict(), indent=2))


# DEMO NOTES
# ----------
# These are illustrative synthetic packets for exercising the rule engine.
# They are not recorded field data and do not validate real-world safety.
# Keep this demo small and reproducible when adding new example scenarios.
