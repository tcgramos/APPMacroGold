import { useEffect, useMemo, useState } from "react";

type Snapshot = Record<string, { price: number; pct_change: number }>;

function normalizeBaseUrl() {
  const envBase = process.env.NEXT_PUBLIC_API_BASE_URL;
  if (envBase && envBase.trim()) return envBase.replace(/\/$/, "");
  return "http://localhost:8000";
}

export default function Home() {
  const apiBase = useMemo(() => normalizeBaseUrl(), []);
  const wsBase = useMemo(() => apiBase.replace(/^http/, "ws"), [apiBase]);

  const [snapshot, setSnapshot] = useState<Snapshot>({});
  const [macro, setMacro] = useState({ score: 50, direction: "NEUTRAL", reason: "..." });
  const [alerts, setAlerts] = useState<any[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${apiBase}/api/v1/market/snapshot`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setSnapshot(data.snapshot || {});
        setMacro(data.macro || macro);
        setError("");
      } catch (err) {
        setError(`Falha ao buscar cotações: ${(err as Error).message}`);
      }
    };

    load();
    const timer = setInterval(load, 5000);
    return () => clearInterval(timer);
  }, [apiBase]);

  useEffect(() => {
    const ws = new WebSocket(`${wsBase}/api/v1/ws/alerts`);

    ws.onmessage = (evt) => {
      const payload = JSON.parse(evt.data);
      if (payload.snapshot) setSnapshot(payload.snapshot);
      if (payload.macro) setMacro(payload.macro);
      if (payload.alerts?.length) setAlerts((prev) => [...payload.alerts, ...prev].slice(0, 20));
    };

    ws.onerror = () => {
      setError("WebSocket indisponível no momento. Verifique backend e URL.");
    };

    ws.onopen = () => ws.send("ready");
    return () => ws.close();
  }, [wsBase]);

  return (
    <main style={{ fontFamily: "Inter, sans-serif", padding: 24, background: "#0b1220", color: "#e2e8f0", minHeight: "100vh" }}>
      <h1>APPMacroGold Dashboard</h1>
      <h2>GOLD {macro.direction} SCORE: {macro.score}/100</h2>
      <p>{macro.reason}</p>
      <p style={{ opacity: 0.8 }}>API: {apiBase}</p>
      {error && <p style={{ color: "#f87171" }}>{error}</p>}

      <section style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 12 }}>
        {Object.entries(snapshot).map(([symbol, v]) => (
          <div key={symbol} style={{ border: "1px solid #334155", borderRadius: 8, padding: 12 }}>
            <strong>{symbol}</strong>
            <div>{v.price}</div>
            <div style={{ color: v.pct_change >= 0 ? "#22c55e" : "#ef4444" }}>{v.pct_change}%</div>
          </div>
        ))}
      </section>

      <h3 style={{ marginTop: 20 }}>Alert Feed</h3>
      {alerts.map((a, i) => (
        <div key={i} style={{ marginBottom: 8, borderLeft: "3px solid #f59e0b", paddingLeft: 8 }}>
          {a.message} ({a.confidence}%)
        </div>
      ))}
    </main>
  );
}
