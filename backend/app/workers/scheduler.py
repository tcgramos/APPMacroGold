import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.services.runtime_state import latest_snapshot, latest_macro_score, alerts_feed, ws_clients
from app.services.signal_engine import SignalEngine
from app.services.tradingview_client import TradingViewClient

scheduler = AsyncIOScheduler()


def start_scheduler():
    client = TradingViewClient()
    engine = SignalEngine()

    async def tick():
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

    def run_tick():
        asyncio.create_task(tick())

    scheduler.add_job(run_tick, "interval", seconds=5, id="market_tick", replace_existing=True)
    scheduler.start()
