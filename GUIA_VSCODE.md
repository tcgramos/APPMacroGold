# Guia rápido: rodar o APPMacroGold no VS Code

Este passo a passo é para ambiente **local sem Docker**.

## 1) Pré-requisitos

Instale no seu sistema:
- **Python 3.12+**
- **Node.js 20+** (com npm)
- **VS Code**

Opcional:
- PostgreSQL (se quiser sair do modo sqlite/local futuramente)

## 2) Abrir o projeto no VS Code

1. Abra o VS Code.
2. Clique em **File > Open Folder...**.
3. Selecione a pasta do projeto `APPMacroGold`.
4. Abra o terminal integrado: **Terminal > New Terminal**.

## 3) Configurar variáveis de ambiente

No terminal (na raiz do projeto):

```bash
cp .env.example .env
```

> No Windows (PowerShell):
```powershell
copy .env.example .env
```

## 4) Subir o backend (FastAPI)

No terminal 1 (raiz do projeto):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

Validação rápida:
- Acesse `http://localhost:8000/health`
- Resposta esperada: `{"status":"ok"}`

## 5) Subir o frontend (Next.js)

Abra um **segundo terminal** no VS Code.

```bash
cd frontend
npm install
npm run dev
```

Validação rápida:
- Acesse `http://localhost:3000`
- Você deve ver o dashboard do APPMacroGold.

## 6) Fluxo diário de uso no VS Code

Sempre que for trabalhar:

### Terminal 1 (backend)
```bash
cd <pasta-do-projeto>
source .venv/bin/activate
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 (frontend)
```bash
cd <pasta-do-projeto>/frontend
npm run dev
```

## 7) Parar a aplicação

Em cada terminal, pressione:
- `Ctrl + C`

## 8) Erros comuns e solução

### Erro: `uvicorn: command not found`
- Ative o ambiente virtual antes:
  - Linux/macOS: `source .venv/bin/activate`
  - Windows: `.\.venv\Scripts\Activate.ps1`

### Erro: porta 8000 ou 3000 em uso
- Feche o processo que está usando a porta ou rode em outra porta.

### Erro de dependências no frontend
- Execute novamente:
```bash
cd frontend
npm install
```

---

Pronto. Com isso, você roda o backend + frontend totalmente dentro do VS Code.
