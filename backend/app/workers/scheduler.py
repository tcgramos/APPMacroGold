import asyncio

from app.services.runtime_state import latest_snapshot, latest_macro_score, alerts_feed, ws_clients
from app.services.signal_engine import SignalEngine
from app.services.tradingview_client import TradingViewClient

_runner_task: asyncio.Task | None = None


async def _tick_loop(interval_seconds: int = 5):
    client = TradingViewClient()
    engine = SignalEngine()

    while True:
        snapshot = client.fetch_snapshot()
        macro = engine.compute_macro_score(snapshot)
        alerts = engine.detect_alerts(snapshot, macro)

        latest_snapshot.clear()
        latest_snapshot.update(snapshot)
        latest_macro_score.clear()
        latest_macro_score.update(macro)

        for alert in alerts:
            alerts_feed.appendleft(alert)

        for ws in list(ws_clients):
            try:
                await ws.send_json({"snapshot": snapshot, "macro": macro, "alerts": alerts})
            except Exception:
                ws_clients.discard(ws)

        await asyncio.sleep(interval_seconds)


def start_scheduler():
    global _runner_task
    if _runner_task is None or _runner_task.done():
        _runner_task = asyncio.create_task(_tick_loop())


def stop_scheduler():
    global _runner_task
    if _runner_task and not _runner_task.done():
        _runner_task.cancel()
