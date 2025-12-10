# core/types.py
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import numpy as np
import time
from typing import Optional


Box = Tuple[int, int, int, int]  # (x1, y1, x2, y2)


@dataclass
class Frame:
    index: int
    timestamp: float
    image: np.ndarray  # HxWx3 BGR (OpenCV)
    fps: float


@dataclass
class Detection:
    box: Box
    score: float
    label: str        # e.g. "person", "car"
    detector_name: str = "stub"


@dataclass
class TrackedObject:
    track_id: Optional[int]
    box: Box
    label: str
    score: float
    last_seen: float
    history: List[Box] = field(default_factory=list)  # past boxes for velocity


@dataclass
class SceneState:
    frame_index: int
    timestamp: float
    tracks: List[TrackedObject]
    attributes: Dict[int, Dict[str, float]]  # track_id -> feature_name -> value
    # e.g. { track_id: {"speed": v, "dir_angle": theta} }


@dataclass
class Anomaly:
    kind: str              # e.g. "speeding", "zone_violation"
    track_id: Optional[int]
    severity: float        # 0–1
    message: str
    timestamp: float


@dataclass
class EventLog:
    frame_index: int
    timestamp: float
    anomalies: List[Anomaly] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
