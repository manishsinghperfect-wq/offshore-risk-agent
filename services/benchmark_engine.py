import json
from pathlib import Path
from typing import Dict, List


class GlobalRiskDatabase:
    """In-memory global risk event database for offshore risk monitoring."""

    def __init__(self, data_dir: str | None = None):
        base_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parent.parent
        self.data_dir = base_dir / "data"
        self.events = self._load_sample_events()

    def _load_sample_events(self) -> List[Dict]:
        data_path = self.data_dir / "sample_incidents.json"
        with data_path.open("r", encoding="utf-8") as f:
            events = json.load(f)
        return events

    def get_all_events(self) -> List[Dict]:
        return self.events

    def get_events_by_operation(self, operation_type: str) -> List[Dict]:
        return [event for event in self.events if event.get("operation_type") == operation_type]

    def get_events_by_region(self, region: str) -> List[Dict]:
        return [event for event in self.events if event.get("region") == region]

    def get_events_by_category(self, risk_category: str) -> List[Dict]:
        return [event for event in self.events if event.get("risk_category") == risk_category]

    def get_event_by_id(self, event_id: str) -> Dict | None:
        for event in self.events:
            if event.get("id") == event_id:
                return event
        return None

    def get_operation_types(self) -> List[str]:
        return sorted({event.get("operation_type") for event in self.events})

    def get_regions(self) -> List[str]:
        return sorted({event.get("region") for event in self.events})

    def get_risk_categories(self) -> List[str]:
        return sorted({event.get("risk_category") for event in self.events})
