from collections.abc import Iterable, Iterator
from .events import Bar, EventKind, MarketEvent

def ingest_bars(bars: Iterable[Bar], start_sequence: int = 0) -> Iterator[MarketEvent]:
    if start_sequence < 0:
        raise ValueError("negative sequence")
    for offset, bar in enumerate(bars):
        seq = start_sequence + offset
        yield MarketEvent(f"bar:{seq}:{bar.symbol}:{bar.timestamp.isoformat()}", seq, EventKind.BAR, bar)
