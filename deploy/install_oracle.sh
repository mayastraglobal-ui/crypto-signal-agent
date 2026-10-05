#!/usr/bin/env bash
# Installs the live watcher (instant Telegram alerts) on a fresh Ubuntu server, e.g. Oracle Cloud Always Free.
# Safe to run again: it updates the code and restarts the service. Guide: docs/LIVE_WATCHER.md
#
#   curl -fsSL https://raw.githubusercontent.com/mayastraglobal-ui/crypto-signal-agent/main/deploy/install_oracle.sh | bash
set -euo pipefail

REPO="${REPO:-https://github.com/mayastraglobal-ui/crypto-signal-agent.git}"
DIR="$HOME/crypto-signal-agent"
ENV_FILE="$HOME/.crypto-agent.env"
SERVICE=crypto-watcher

echo "== 1/5 system packages"
sudo apt-get update -qq
sudo apt-get install -y -qq git python3 python3-venv python3-pip >/dev/null
sudo timedatectl set-ntp true || true            # correct clock = alerts right after each candle close

echo "== 2/5 code"
if [ -d "$DIR/.git" ]; then
  git -C "$DIR" pull --ff-only -q
else
  git clone -q "$REPO" "$DIR"
fi

echo "== 3/5 python packages (a few minutes the first time)"
python3 -m venv "$DIR/.venv"
"$DIR/.venv/bin/pip" install -q --upgrade pip
"$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"

echo "== 4/5 Telegram settings file"
if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'EOF'
# Telegram settings for the live watcher (docs/LIVE_WATCHER.md, step 3). Never share this file.
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF
fi
chmod 600 "$ENV_FILE"

echo "== 5/5 background service (starts again by itself after a crash or a reboot)"
sudo tee /etc/systemd/system/$SERVICE.service >/dev/null <<EOF
[Unit]
Description=Crypto Signal Agent - live watcher (Telegram alerts)
After=network-online.target
Wants=network-online.target

[Service]
User=$USER
WorkingDirectory=$DIR
EnvironmentFile=$ENV_FILE
Environment=PYTHONUNBUFFERED=1
ExecStart=$DIR/.venv/bin/python $DIR/live_watcher.py
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable -q $SERVICE

if grep -q '^TELEGRAM_BOT_TOKEN=.\+' "$ENV_FILE" && grep -q '^TELEGRAM_CHAT_ID=.\+' "$ENV_FILE"; then
  sudo systemctl restart $SERVICE
  echo
  echo "Done. The live watcher is running. Check it with:  sudo systemctl status $SERVICE"
else
  echo
  echo "Installed. One step left: put your Telegram bot token and chat id in $ENV_FILE"
  echo "(docs/LIVE_WATCHER.md, step 3), then run:  sudo systemctl restart $SERVICE"
fi
