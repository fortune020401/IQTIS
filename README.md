# IQTIS — Intraday Quantitative Trading Intelligence System

Stage 1 foundation, version 0.1.0: typed market bars/events, broker-neutral ingestion, JSONL event storage/replay, safe configuration, and automated tests.

## Setup

Python 3.11+ required.

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

## Safety

No broker connection or order execution is implemented. Broker orders and live trading are explicitly rejected by configuration. No profitability claims are made. Never commit secrets or brokerage credentials.

## Next milestones

Historical market-data adapters, strategy registry, realistic backtesting, independent risk gateway, and IBKR paper execution only after validation.
