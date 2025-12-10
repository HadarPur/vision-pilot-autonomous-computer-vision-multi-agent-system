# agents/reporter.py
from core.types import EventLog


class ReporterAgent:
    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def report(self, event: EventLog):
        if not self.verbose:
            return
        if not event.anomalies:
            return
        print(f"[Frame {event.frame_index}] t={event.timestamp:.3f}")
        for a in event.anomalies:
            print(f"  - {a.kind.upper()} (track={a.track_id}, sev={a.severity:.2f}): {a.message}")
