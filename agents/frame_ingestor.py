# agents/frame_ingestor.py
import cv2
import time
from typing import Iterator, Optional
from core.types import Frame
from core.config import FPS
from typing import Union


class FrameIngestorAgent:
    def __init__(self, source: Union[int, str] = 0):
        """
        source: 0 for default camera, or path to video file.
        """
        self.source = source
        self.cap: Optional[cv2.VideoCapture] = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open video source: {self.source}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap is not None:
            self.cap.release()

    def frames(self) -> Iterator[Frame]:
        assert self.cap is not None
        idx = 0
        while True:
            ret, img = self.cap.read()
            if not ret:
                break
            ts = time.time()
            yield Frame(index=idx, timestamp=ts, image=img, fps=FPS)
            idx += 1
