# agents/scene_understanding.py
from typing import Dict
from core.types import SceneState
from core.config import ZONES


class SceneUnderstandingAgent:
    def __init__(self):
        pass

    @staticmethod
    def _in_zone(box, zone_rel, frame_width, frame_height) -> bool:
        x1r, y1r, x2r, y2r = zone_rel
        zx1 = int(x1r * frame_width)
        zy1 = int(y1r * frame_height)
        zx2 = int(x2r * frame_width)
        zy2 = int(y2r * frame_height)
        x1, y1, x2, y2 = box
        cx = 0.5 * (x1 + x2)
        cy = 0.5 * (y1 + y2)
        return zx1 <= cx <= zx2 and zy1 <= cy <= zy2

    def enrich_scene(self, scene: SceneState, frame_width: int, frame_height: int) -> Dict:
        """
        Returns a dict with additional scene-level info, e.g. counts per zone.
        """
        zone_counts = {name: 0 for name in ZONES.keys()}
        for t in scene.tracks:
            for zone_name, zone_rel in ZONES.items():
                if self._in_zone(t.box, zone_rel, frame_width, frame_height):
                    zone_counts[zone_name] += 1

        return {
            "frame_index": scene.frame_index,
            "timestamp": scene.timestamp,
            "zone_counts": zone_counts,
        }
