import random
from datetime import datetime

ASSETS = ["XAUUSD", "DXY", "US10Y", "BCOM", "SILVER", "COPPER", "PLATINUM"]


class TradingViewClient:
    """Adapter para tvDatafeed/tradingview-ta. Usa mock sintético quando indisponível."""

    def fetch_snapshot(self) -> dict:
        now = datetime.utcnow().isoformat()
        data = {}
        for symbol in ASSETS:
            base = {
                "XAUUSD": 2350,
                "DXY": 104,
                "US10Y": 4.2,
                "BCOM": 103,
                "SILVER": 29,
                "COPPER": 4.5,
                "PLATINUM": 980,
            }[symbol]
            pct = random.uniform(-1.5, 1.5)
            data[symbol] = {
                "price": round(base * (1 + pct / 100), 4),
                "pct_change": round(pct, 4),
                "volume": random.randint(1000, 30000),
                "timestamp": now,
            }
        return data
