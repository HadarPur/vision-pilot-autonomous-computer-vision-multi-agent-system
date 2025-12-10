# agents/tracker.py
from typing import List
import time
from core.types import Detection, TrackedObject, Box


def iou(box1: Box, box2: Box) -> float:
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    a1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    a2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    return inter / float(a1 + a2 - inter)


class TrackerAgent:
    def __init__(self, iou_threshold: float = 0.3, max_idle_time: float = 1.0):
        self.iou_threshold = iou_threshold
        self.max_idle_time = max_idle_time
        self._tracks: List[TrackedObject] = []
        self._next_id = 1

    def _create_track(self, det: Detection, ts: float) -> TrackedObject:
        t = TrackedObject(
            track_id=self._next_id,
            box=det.box,
            label=det.label,
            score=det.score,
            last_seen=ts,
            history=[det.box],
        )
        self._next_id += 1
        return t

    def update(self, detections: List[Detection], ts: float) -> List[TrackedObject]:
        # match by IoU
        assigned = set()
        for track in self._tracks:
            best_iou = 0.0
            best_det_idx = None
            for i, det in enumerate(detections):
                if i in assigned:
                    continue
                v = iou(track.box, det.box)
                if v > best_iou:
                    best_iou = v
                    best_det_idx = i
            if best_det_idx is not None and best_iou >= self.iou_threshold:
                det = detections[best_det_idx]
                track.box = det.box
                track.score = det.score
                track.last_seen = ts
                track.history.append(det.box)
                assigned.add(best_det_idx)

        # new tracks
        for i, det in enumerate(detections):
            if i not in assigned:
                self._tracks.append(self._create_track(det, ts))

        # drop stale tracks
        now = ts
        self._tracks = [
            t for t in self._tracks if now - t.last_seen <= self.max_idle_time
        ]
        return list(self._tracks)
