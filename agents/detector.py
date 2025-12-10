# agents/detector.py
from ultralytics import YOLO
from core.types import Detection, Frame
from typing import List


class DetectorAgent:
    """
    YOLOv8-based object detector.
    """

    def __init__(self, model_path: str = "yolov8n.pt", conf_threshold: float = 0.25):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame: Frame) -> List[Detection]:
        """
        Input:
            frame: Frame object containing BGR image from OpenCV.
        Output:
            List[Detection]: bounding boxes with label + score
        """
        results = self.model(frame.image, verbose=False)[0]
        detections = []

        for box in results.boxes:
            score = float(box.conf[0])
            if score < self.conf_threshold:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            label_idx = int(box.cls[0])
            label = self.model.names[label_idx]

            detections.append(
                Detection(
                    box=(int(x1), int(y1), int(x2), int(y2)),
                    score=score,
                    label=label,
                    detector_name="YOLOv8"
                )
            )

        return detections
