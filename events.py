from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
import json
import math

class EventKind(str, Enum):
    BAR = "bar"

@dataclass(frozen=True)
class Bar:
    symbol: str
    timestamp: datetime
    timeframe_seconds: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    source: str

    def __post_init__(self):
        if self.timestamp.tzinfo is None or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be timezone aware")
        if not self.symbol.strip() or not self.source.strip():
            raise ValueError("symbol and source required")
        if self.timeframe_seconds <= 0 or self.volume < 0:
            raise ValueError("invalid timeframe or volume")
        prices = (self.open, self.high, self.low, self.close)
        if any(not math.isfinite(p) or p <= 0 for p in prices):
            raise ValueError("prices must be finite and positive")
        if self.high < max(prices) or self.low > min(prices):
            raise ValueError("inconsistent OHLC")

@dataclass(frozen=True)
class MarketEvent:
    event_id: str
    sequence: int
    kind: EventKind
    bar: Bar

    def __post_init__(self):
        if not self.event_id or self.sequence < 0 or self.kind != EventKind.BAR:
            raise ValueError("invalid event")

    def to_json(self):
        d = asdict(self)
        d["kind"] = self.kind.value
        d["bar"]["timestamp"] = self.bar.timestamp.astimezone(timezone.utc).isoformat()
        return json.dumps(d, sort_keys=True, allow_nan=False)

    @classmethod
    def from_json(cls, payload):
        d = json.loads(payload)
        b = d["bar"]
        b["timestamp"] = datetime.fromisoformat(b["timestamp"].replace("Z", "+00:00"))
        return cls(d["event_id"], d["sequence"], EventKind(d["kind"]), Bar(**b))
