from app.core.config import settings


class SignalEngine:
    def compute_macro_score(self, snapshot: dict) -> dict:
        score = 50
        reasons = []

        if snapshot["DXY"]["pct_change"] < 0:
            score += settings.score_weight_dxy
            reasons.append("DXY em queda confirma força do ouro")
        if snapshot["US10Y"]["pct_change"] < 0:
            score += settings.score_weight_us10y
            reasons.append("US10Y em queda favorece ouro")
        for symbol, weight in [("SILVER", settings.score_weight_silver), ("COPPER", settings.score_weight_copper), ("PLATINUM", settings.score_weight_platinum), ("BCOM", settings.score_weight_commodities)]:
            if snapshot[symbol]["pct_change"] > 0:
                score += weight
                reasons.append(f"{symbol} confirmando movimento")

        score = max(0, min(100, score))
        direction = "BULLISH" if score >= 60 else "BEARISH" if score <= 40 else "NEUTRAL"
        return {"score": score, "direction": direction, "reason": "; ".join(reasons) or "Sem confirmação robusta"}

    def detect_alerts(self, snapshot: dict, macro_score: dict) -> list[dict]:
        alerts = []
        xau_up = snapshot["XAUUSD"]["pct_change"] > 0.5
        dxy_down = snapshot["DXY"]["pct_change"] < -0.3

        if xau_up and dxy_down and macro_score["score"] >= 70:
            alerts.append({"event_type": "TREND_CONFIRMATION", "severity": "HIGH", "message": "FORÇA COMPRADORA CONFIRMADA NO OURO", "confidence": macro_score["score"]})

        if snapshot["XAUUSD"]["pct_change"] > 0.5 and snapshot["DXY"]["pct_change"] > 0.2 and snapshot["US10Y"]["pct_change"] > 0.2:
            alerts.append({"event_type": "POSSIBLE_REVERSAL", "severity": "MEDIUM", "message": "POSSÍVEL EXAUSTÃO / REVERSÃO NO OURO", "confidence": 100 - macro_score["score"]})

        if abs(snapshot["XAUUSD"]["pct_change"]) > 1.2:
            alerts.append({"event_type": "VOLATILITY_SPIKE", "severity": "HIGH", "message": "Expansão anormal de volatilidade detectada no ouro", "confidence": 80})

        return alerts
