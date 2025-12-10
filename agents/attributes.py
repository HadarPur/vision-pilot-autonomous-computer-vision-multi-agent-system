# agents/attributes.py
from typing import Dict
import math
from core.types import TrackedObject, SceneState


class AttributeAgent:
    def __init__(self):
        pass

    @staticmethod
    def _center(box):
        x1, y1, x2, y2 = box
        return (0.5 * (x1 + x2), 0.5 * (y1 + y2))

    def compute(self, frame_index: int, ts: float, tracks) -> SceneState:
        attrs: Dict[int, Dict[str, float]] = {}

        for t in tracks:
            if len(t.history) >= 2:
                c_prev = self._center(t.history[-2])
                c_curr = self._center(t.history[-1])
                dx = c_curr[0] - c_prev[0]
                dy = c_curr[1] - c_prev[1]
                # assuming 1 / fps ~ Δt, but we don't know fps here. Use ts difference if stored.
                # For simplicity, treat as Δt = 1 frame unit.
                speed = math.sqrt(dx * dx + dy * dy)
                angle = math.atan2(dy, dx)  # radians
            else:
                speed = 0.0
                angle = 0.0

            attrs[t.track_id] = {
                "speed_px_per_frame": speed,
                "direction_rad": angle,
            }

        return SceneState(
            frame_index=frame_index,
            timestamp=ts,
            tracks=list(tracks),
            attributes=attrs,
        )
