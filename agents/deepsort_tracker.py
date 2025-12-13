# agents/deepsort_tracker.py

from typing import List
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort

from core.types import Detection, TrackedObject


class DeepSortTrackerAgent:
    def __init__(
        self,
        max_age: int = 30,
        n_init: int = 3,
        nms_max_overlap: float = 1.0,
        embedder: str = "mobilenet",
        half: bool = True,
    ):
        self.tracker = DeepSort(
            max_age=max_age,
            n_init=n_init,
            nms_max_overlap=nms_max_overlap,
            embedder=embedder,
            half=half,
        )

    def _detections_to_bbs(self, detections: List[Detection]) -> List[tuple]:
        bbs = []
        for det in detections:
            x1, y1, x2, y2 = det.box
            w = x2 - x1
            h = y2 - y1
            bbs.append(
                (
                    [float(x1), float(y1), float(w), float(h)],
                    float(det.score),
                    det.label,
                )
            )
        return bbs

    def update(
        self,
        detections: List[Detection],
        frame_image: np.ndarray,
        timestamp: float,
    ) -> List[TrackedObject]:
        bbs = self._detections_to_bbs(detections)

        tracks = self.tracker.update_tracks(bbs, frame=frame_image)

        tracked_objects: List[TrackedObject] = []

        print("DeepSORT tracks:", [t.track_id for t in tracks if t.is_confirmed()])

        for trk in tracks:
            if not trk.is_confirmed():
                continue

            # [left, top, right, bottom]
            l, t, r, b = trk.to_ltrb(orig=True)

            # Robustly get class name
            det_class = getattr(trk, "det_class", None)
            if det_class is None:
                # Some versions store it differently or not at all
                det_class = "object"
            else:
                det_class = str(det_class)

            # Robustly get confidence
            raw_conf = getattr(trk, "det_conf", None)
            if raw_conf is None:
                det_conf = 1.0
            else:
                try:
                    det_conf = float(raw_conf)
                except (TypeError, ValueError):
                    det_conf = 1.0

            tracked_objects.append(
                TrackedObject(
                    track_id=int(trk.track_id),
                    box=(int(l), int(t), int(r), int(b)),
                    label=det_class,
                    score=det_conf,
                    last_seen=timestamp,
                    history=[],
                )
            )

        return tracked_objects
