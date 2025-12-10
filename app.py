# app.py
import argparse
from agents.planner import VisionPilotPlanner


def parse_args():
    p = argparse.ArgumentParser(description="VisionPilot: Multi-Agent Vision System")
    p.add_argument("--source", type=str, default="0",
                   help="Video source: '0' for webcam or path to file.")
    p.add_argument("--max-frames", type=int, default=None,
                   help="Max number of frames to process.")
    return p.parse_args()


def main():
    args = parse_args()
    source = 0 if args.source == "0" else args.source
    planner = VisionPilotPlanner(source=source)
    planner.run(max_frames=args.max_frames)


if __name__ == "__main__":
    main()
