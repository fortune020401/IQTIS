from pathlib import Path
from collections.abc import Iterable, Iterator
from .events import MarketEvent

def append_events(path: Path, events: Iterable[MarketEvent]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for event in events:
            f.write(event.to_json() + "\n")

def replay_events(path: Path) -> Iterator[MarketEvent]:
    last_sequence = -1
    seen = set()
    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            if not line.strip():
                continue
            event = MarketEvent.from_json(line)
            if event.sequence <= last_sequence or event.event_id in seen:
                raise ValueError(f"out-of-order or duplicate event at line {line_number}")
            last_sequence = event.sequence
            seen.add(event.event_id)
            yield event
