# core/config.py
from typing import Dict, Tuple

FPS = 30.0

# Example zones in normalized coordinates (0–1)
ZONES: Dict[str, Tuple[float, float, float, float]] = {
    "restricted": (0.1, 0.1, 0.4, 0.4),  # x1, y1, x2, y2 (relative)
}

SPEED_THRESHOLD = 50.0  # pixels/second for anomaly example
