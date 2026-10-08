from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    paper_trading: bool = True
    live_trading_enabled: bool = False
    broker_orders_enabled: bool = False
    max_position_fraction: float = 0.02
    max_daily_loss_fraction: float = 0.01

    def __post_init__(self):
        if self.live_trading_enabled or self.broker_orders_enabled:
            raise ValueError("broker orders and live trading prohibited in Stage 1")
        if not 0 < self.max_position_fraction <= 1:
            raise ValueError("invalid max position fraction")
        if not 0 < self.max_daily_loss_fraction <= 1:
            raise ValueError("invalid daily loss fraction")
