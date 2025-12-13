# agents/attributes.py
from typing import Dict
import math
from core.types import TrackedObject, SceneState
from core.config import FPS, METERS_PER_PIXEL


class AttributeAgent:
    """
    Computes physical motion attributes:
    - velocity (px/frame → px/s → m/s)
    - direction (rad)
    - acceleration (m/s²)
    """

    @staticmethod
    def _center(box):
        x1, y1, x2, y2 = box
        return (0.5 * (x1 + x2), 0.5 * (y1 + y2))

    def compute(self, frame_index: int, ts: float, tracks) -> SceneState:
        attributes: Dict[int, Dict[str, float]] = {}

        dt = 1.0 / FPS  # seconds per frame

        for t in tracks:
            # update history
            t.history.append(t.box)
            if len(t.history) > 5:
                t.history.pop(0)

            speed_m_s = 0.0
            accel_m_s2 = 0.0
            direction_rad = 0.0

            if len(t.history) >= 2:
                c_prev = self._center(t.history[-2])
                c_curr = self._center(t.history[-1])

                dx_px = c_curr[0] - c_prev[0]
                dy_px = c_curr[1] - c_prev[1]

                # px/frame → px/s
                speed_px_s = math.sqrt(dx_px**2 + dy_px**2) * FPS

                # px/s → m/s
                speed_m_s = speed_px_s * METERS_PER_PIXEL

                direction_rad = math.atan2(dy_px, dx_px)

                # acceleration
                t.velocity_history.append(speed_m_s)
                if len(t.velocity_history) > 5:
                    t.velocity_history.pop(0)

                if len(t.velocity_history) >= 2:
                    accel_m_s2 = (
                        t.velocity_history[-1] - t.velocity_history[-2]
                    ) / dt

            attributes[t.track_id] = {
                "speed_px_s": speed_px_s if len(t.history) >= 2 else 0.0,
                "speed_m_s": speed_m_s,
                "accel_m_s2": accel_m_s2,
                "direction_rad": direction_rad,
            }

        return SceneState(
            frame_index=frame_index,
            timestamp=ts,
            tracks=list(tracks),
            attributes=attributes,
        )
