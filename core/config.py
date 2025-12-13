# core/config.py
from typing import Dict, Tuple

FPS = 30.0

# === PHYSICAL CALIBRATION ===
# meters per pixel (example: 1 px ≈ 2 cm)
METERS_PER_PIXEL = 0.02

# Optional thresholds (now meaningful!)
SPEED_LIMIT_M_S = 3.0      # running human ~3 m/s
ACC_LIMIT_M_S2 = 6.0       # abrupt acceleration

# ===============================
# Scene zones (normalized coords)
# ===============================
# Each zone is (x1, y1, x2, y2) in [0, 1] image coordinates
ZONES = {
    "restricted": (0.1, 0.1, 0.4, 0.4),
    # add more zones if needed
    # "entrance": (0.6, 0.2, 0.9, 0.6),
}