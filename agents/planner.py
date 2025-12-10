# agents/planner.py
from agents.frame_ingestor import FrameIngestorAgent
from agents.detector import DetectorAgent
from agents.tracker import TrackerAgent
from agents.attributes import AttributeAgent
from agents.scene_understanding import SceneUnderstandingAgent
from agents.anomaly import AnomalyDetectorAgent
from agents.reporter import ReporterAgent
from typing import Optional


class VisionPilotPlanner:
    def __init__(self, source=0):
        self.source = source
        self.detector = DetectorAgent()
        self.tracker = TrackerAgent()
        self.attr_agent = AttributeAgent()
        self.scene_agent = SceneUnderstandingAgent()
        self.anomaly_agent = AnomalyDetectorAgent()
        self.reporter = ReporterAgent(verbose=True)

    def run(self, max_frames: Optional[int] = None):
        from core.config import FPS
        import cv2

        with FrameIngestorAgent(self.source) as ingestor:
            for frame in ingestor.frames():
                if max_frames is not None and frame.index >= max_frames:
                    break

                h, w, _ = frame.image.shape

                detections = self.detector.detect(frame)
                tracks = self.tracker.update(detections, frame.timestamp)
                scene = self.attr_agent.compute(frame.index, frame.timestamp, tracks)
                zone_info = self.scene_agent.enrich_scene(scene, w, h)
                event = self.anomaly_agent.detect(scene, zone_info)
                self.reporter.report(event)

                # Optional: visualize
                for t in tracks:
                    x1, y1, x2, y2 = t.box
                    cv2.rectangle(frame.image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow("VisionPilot", frame.image)
                if cv2.waitKey(int(1000 / FPS)) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()
