# APPMacroGold

Plataforma institucional de monitoramento macroeconômico para **XAUUSD (ouro)** com análise de correlação intermarket, score probabilístico e alertas em tempo real.

## Stack
> Compatível com **Python 3.14.4** (sem dependências obsoletas como `numpy`, `pandas`, `apscheduler`, `psycopg[binary]`).

- **Frontend:** Next.js, React, TypeScript, Tailwind, shadcn/ui, Recharts
- **Backend:** FastAPI, SQLAlchemy, APScheduler, WebSocket, PostgreSQL, Redis (opcional), RabbitMQ (opcional)
- **Dados:** adapters TradingView (`tvDatafeed`/`tradingview-ta`) com fallback para providers alternativos
- **Infra (sem Docker):** systemd + Nginx reverse proxy + CI/CD GitHub Actions

## Objetivos de Produto
- Leitura macro em tempo real para confirmar ou invalidar operações no ouro.
- Alertas de força e reversão com score de confiança.
- Dashboard institucional com feed de eventos.

## Arquitetura
```text
frontend (Next.js) <--WS/HTTP--> backend (FastAPI)
                                 ├─ DataCollector (TradingView adapters)
                                 ├─ SignalEngine (EMA/RSI/ATR/volume/correlation)
                                 ├─ AlertEngine (trend/reversal/spike)
                                 ├─ NotificationService (telegram/email/webpush)
                                 ├─ Scheduler (APScheduler)
                                 └─ PostgreSQL / Redis / RabbitMQ
```

## Estrutura
```text
backend/
  app/
frontend/
  src/
deploy/
  systemd/
  scripts/
nginx/
  default.conf
.github/workflows/
  ci.yml
```

## Regras de Negócio Implementadas
- Tendência: EMA9/21 (curto), EMA50 (médio), EMA200 (longo).
- Confirmações: RSI, ATR expansion, volume relativo, variação percentual.
- Score macro (0-100) com pesos configuráveis.
- Alertas: `TREND_CONFIRMATION`, `POSSIBLE_REVERSAL`, `VOLATILITY_SPIKE`.

## Execução local (sem Docker)
### 1) Pré-requisitos
- Python 3.12+
- Node.js 20+
- PostgreSQL 16 (opcional no MVP, pode iniciar com sqlite)

### 2) Backend
```bash
cp .env.example .env
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

### 3) Frontend
```bash
cd frontend
npm install
npm run dev
```

Serviços:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Endpoints principais
- `GET /health`
- `GET /api/v1/market/snapshot`
- `GET /api/v1/alerts`
- `WS /api/v1/ws/alerts`

## Deploy profissional em VPS (sem Docker)
1. Rodar `deploy/scripts/bootstrap_server.sh`.
2. Publicar código em `/opt/appmacro`.
3. Ativar serviços `appmacro-backend` e `appmacro-frontend` via systemd.
4. Configurar Nginx com `nginx/default.conf` e TLS (Let's Encrypt).

## Observações
- `TradingViewClient` está preparado para integração real, mas em ambiente local sem credenciais usa gerador sintético para manter o fluxo funcional.
- Projeto modular para evoluir para app mobile via React Native/Expo consumindo os mesmos endpoints.
