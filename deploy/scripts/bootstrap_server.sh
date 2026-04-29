#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y python3-venv python3-pip nodejs npm nginx

cd /opt/appmacro
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd frontend
npm install
npm run build

sudo cp /opt/appmacro/deploy/systemd/appmacro-backend.service /etc/systemd/system/
sudo cp /opt/appmacro/deploy/systemd/appmacro-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable appmacro-backend appmacro-frontend
sudo systemctl restart appmacro-backend appmacro-frontend
