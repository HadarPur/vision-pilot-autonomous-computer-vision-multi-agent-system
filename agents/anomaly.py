# agents/anomaly.py
from typing import List
from core.types import SceneState, Anomaly, EventLog
from core.config import SPEED_THRESHOLD, ZONES


class AnomalyDetectorAgent:
    def __init__(self):
        pass

    def detect(self, scene: SceneState, zone_info) -> EventLog:
        anomalies: List[Anomaly] = []

        # Speed-based anomaly
        for t in scene.tracks:
            attrs = scene.attributes.get(t.track_id, {})
            speed = attrs.get("speed_px_per_frame", 0.0)
            if speed > SPEED_THRESHOLD:
                anomalies.append(
                    Anomaly(
                        kind="speeding",
                        track_id=t.track_id,
                        severity=min(1.0, speed / (SPEED_THRESHOLD * 2)),
                        message=f"Track {t.track_id} moving fast: {speed:.1f} px/frame",
                        timestamp=scene.timestamp,
                    )
                )

        # Zone-based anomaly (e.g. restricted area count > 0)
        restricted_count = zone_info["zone_counts"].get("restricted", 0)
        if restricted_count > 0:
            # For simplicity, we don't know which track(s), so set track_id=-1
            anomalies.append(
                Anomaly(
                    kind="zone_violation",
                    track_id=-1,
                    severity=min(1.0, restricted_count / 5),
                    message=f"{restricted_count} objects in restricted zone",
                    timestamp=scene.timestamp,
                )
            )

        return EventLog(
            frame_index=scene.frame_index,
            timestamp=scene.timestamp,
            anomalies=anomalies,
            notes=[],
        )
