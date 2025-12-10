# agents/detector.py
from typing import List
from core.types import Frame, Detection


class DetectorAgent:
    """
    Stub detector: replace later with real model.
    """

    def __init__(self, model_name: str = "stub"):
        self.model_name = model_name

    def detect(self, frame: Frame) -> List[Detection]:
        # TODO: plug real detector (YOLO, etc.)
        # For now: return empty list or a dummy detection
        return []
