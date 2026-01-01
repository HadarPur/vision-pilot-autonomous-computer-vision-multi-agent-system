# VisionPilot  
**Autonomous Multi-Agent Computer Vision System**

---

## Overview

**VisionPilot** is a modular, real-time, multi-agent computer vision system designed for **scene understanding, motion analysis, and anomaly detection** using modern AI components.

It integrates:
- **YOLOv8** for object detection  
- **DeepSORT** for robust multi-object tracking  
- **Physics-based motion estimation** (m/s, m/s²)  
- **Zone-based semantic reasoning**  
- **Agent-oriented architecture** for scalability and clarity  

The system is designed to resemble **real-world perception stacks** used in robotics, autonomous systems, and intelligent surveillance.

---

## Core Capabilities

✔ Real-time object detection  
✔ Persistent identity tracking  
✔ Physical motion estimation (speed, acceleration)  
✔ Zone-based spatial reasoning  
✔ Anomaly detection  
✔ Modular agent architecture  
✔ Extensible and research-ready  

---

## System Architecture

```
Camera / Video
      ↓
FrameIngestorAgent
      ↓
DetectorAgent (YOLOv8)
      ↓
DeepSortTrackerAgent
      ↓
AttributeAgent (physical motion)
      ↓
SceneUnderstandingAgent
      ↓
AnomalyAgent
      ↓
ReporterAgent
```

Each agent is independent, testable, and replaceable.

---

## Project Structure

```
vision-pilot/
├── agents/
│   ├── frame_ingestor.py
│   ├── detector.py
│   ├── deepsort_tracker.py
│   ├── attributes.py
│   ├── scene_understanding.py
│   ├── anomaly.py
│   ├── reporter.py
│   └── planner.py
│
├── core/
│   ├── config.py
│   └── types.py
│
├── app.py
├── tests/
└── README.md
```

---

## Key Concepts

### Agent-Based Design

Each component has a single responsibility:

| Agent | Responsibility |
|------|----------------|
| FrameIngestor | Video capture |
| Detector | Object detection (YOLOv8) |
| DeepSortTracker | Identity tracking |
| AttributeAgent | Motion physics (m/s, m/s²) |
| SceneUnderstandingAgent | Zone reasoning |
| AnomalyAgent | Behavior analysis |
| ReporterAgent | Human-readable output |

---

## Physical Motion Modeling

VisionPilot converts pixel motion into **real-world units**:

```
px/frame → px/s → m/s → m/s²
```

This enables:
- Speed estimation  
- Acceleration detection  
- Trajectory modeling  
- Physics-aware anomaly detection  

---

## Scene Understanding

Zones are defined in normalized image space:

```python
ZONES = {
    "restricted": (0.1, 0.1, 0.4, 0.4)
}
```

For each frame, the system computes:
- Object count per zone  
- Average speed  
- Maximum speed  

---

## Anomaly Detection

Examples:
- Object entering restricted zone  
- High-speed movement  
- Sudden acceleration  

Example output:

```
[Frame 42]
ZONE_VIOLATION: 1 object in restricted zone
```

---

## Installation

```bash
python -m venv vp-env
source vp-env/bin/activate

pip install ultralytics deep-sort-realtime opencv-python numpy torch
```

---

## Running the System

```bash
python app.py --source 0
```

Or with a video file:

```bash
python app.py --source sample.mp4
```

---

## Configuration

All tunable parameters live in:

```python
core/config.py
```

Includes:
- FPS
- meters-per-pixel calibration
- zone definitions
- anomaly thresholds

---

## Why This Architecture Works

- Modular and extensible  
- Physics-aware  
- Real-time capable  
- Research-grade clarity  

Used in:
- Robotics  
- Autonomous vehicles  
- Surveillance analytics  

---

## Roadmap

- World-coordinate projection (homography)
- Trajectory prediction
- Risk scoring
- Multi-camera fusion
- Analytics dashboard

---

## Acknowledgments

- Ultralytics YOLOv8  
- DeepSORT  
- OpenCV  
