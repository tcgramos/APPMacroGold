from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.runtime_state import alerts_feed, latest_macro_score, latest_snapshot, ws_clients

router = APIRouter()


@router.get("/market/snapshot")
def market_snapshot():
    return {"snapshot": latest_snapshot, "macro": latest_macro_score}


@router.get("/alerts")
def list_alerts():
    return list(alerts_feed)


@router.websocket("/ws/alerts")
async def ws_alerts(websocket: WebSocket):
    await websocket.accept()
    ws_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_clients.discard(websocket)
