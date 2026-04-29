# APPMacroGold

Plataforma institucional de monitoramento macroeconômico para **XAUUSD (ouro)** com análise de correlação intermarket, score probabilístico e alertas em tempo real.

## Stack
- **Frontend:** Next.js, React, TypeScript, Tailwind, shadcn/ui, Recharts
- **Backend:** FastAPI, SQLAlchemy, APScheduler, WebSocket, PostgreSQL, Redis (opcional), RabbitMQ (opcional)
- **Dados:** adapters TradingView (`tvDatafeed`/`tradingview-ta`) com fallback para providers alternativos
- **Infra:** Docker Compose, Nginx reverse proxy, CI/CD GitHub Actions

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
    api/
    core/
    models/
    schemas/
    services/
    workers/
  tests/
frontend/
  src/
    components/
    lib/
    pages/
infra/
  docker-compose.yml
  Dockerfile.backend
  Dockerfile.frontend
nginx/
  default.conf
.github/workflows/
  ci.yml
```

## Regras de Negócio Implementadas
- Tendência: EMA9/21 (curto), EMA50 (médio), EMA200 (longo).
- Confirmações: RSI, ATR expansion, volume relativo, variação percentual.
- Score macro (0-100) com pesos configuráveis:
  - DXY (inversa): 20
  - US10Y (inversa): 20
  - Silver: 15
  - Copper: 10
  - Platinum: 10
  - Commodities: 10
  - Fed expectations: 15
- Alertas:
  - `TREND_CONFIRMATION`
  - `POSSIBLE_REVERSAL`
  - `VOLATILITY_SPIKE`

## Rodando localmente
```bash
cp .env.example .env
cd infra
docker compose up --build
```

Serviços:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Endpoints principais
- `GET /health`
- `GET /api/v1/market/snapshot`
- `GET /api/v1/alerts`
- `WS /ws/alerts`

## Deploy
1. Build de imagens backend/frontend.
2. Nginx como reverse proxy e TLS (Let's Encrypt).
3. Variáveis seguras via secret manager.
4. Migrations automatizadas na inicialização.

## Observações
- `TradingViewClient` está preparado para integração real, mas em ambiente local sem credenciais usa gerador sintético para manter o fluxo funcional.
- Projeto modular para evoluir para app mobile via React Native/Expo consumindo os mesmos endpoints.
