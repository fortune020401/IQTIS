from datetime import datetime, timezone
import pytest
from iqtis.config import Settings
from iqtis.events import Bar, MarketEvent
from iqtis.ingestion import ingest_bars
from iqtis.replay import append_events, replay_events

def sample_bar():
    return Bar("SPY", datetime(2026, 1, 5, 14, 30, tzinfo=timezone.utc), 60, 100, 101, 99, 100.5, 1000, "fixture")

def test_event_roundtrip():
    e = next(ingest_bars([sample_bar()]))
    assert MarketEvent.from_json(e.to_json()) == e

def test_replay(tmp_path):
    events = list(ingest_bars([sample_bar(), sample_bar()]))
    path = tmp_path / "events.jsonl"
    append_events(path, events)
    assert list(replay_events(path)) == events

def test_duplicate_rejected(tmp_path):
    e = next(ingest_bars([sample_bar()]))
    path = tmp_path / "events.jsonl"
    append_events(path, [e, e])
    with pytest.raises(ValueError):
        list(replay_events(path))

def test_invalid_bar():
    with pytest.raises(ValueError):
        Bar("SPY", datetime.now(timezone.utc), 60, 100, 90, 99, 100, 100, "fixture")

def test_live_and_broker_orders_blocked():
    with pytest.raises(ValueError):
        Settings(live_trading_enabled=True)
    with pytest.raises(ValueError):
        Settings(broker_orders_enabled=True)
