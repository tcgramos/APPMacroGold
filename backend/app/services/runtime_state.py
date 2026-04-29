from collections import deque

latest_snapshot = {}
latest_macro_score = {"score": 50, "direction": "NEUTRAL", "reason": "Aguardando dados"}
alerts_feed = deque(maxlen=200)
ws_clients = set()
