#!/usr/bin/env bash
# Ella Core — native AdaOS setup (no VM, no Kali yet)
# Run on AdaOS (Xubuntu 26) with sudo, while the internet is UP.
# UNTESTED on Maziyar's PC (SSH still unreachable 2026-10-24) — read before
# running; every step prints what it is about to do. Safe to re-run: all
# steps are idempotent (they skip work already done).
# $0 only: Ollama, llama.cpp fallback, Qwen2.5-7B Q4 — all free.
set -euo pipefail

ELLA_USER="ella"
ELLA_HOME="/home/ella"
MODEL="qwen2.5:7b"
# Qwen2.5-7B-Instruct Q4_K_M GGUF, for the llama.cpp fallback path.
GGUF_URL="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf"

say() { printf '\n==> %s\n' "$*"; }

if [ "$(id -u)" -ne 0 ]; then
  echo "Run with sudo: sudo bash $0" >&2; exit 1
fi

say "1/6 Dedicated user $ELLA_USER"
if id "$ELLA_USER" >/dev/null 2>&1; then
  echo "User $ELLA_USER already exists, skipping creation."
else
  useradd --create-home --shell /bin/bash --user-group "$ELLA_USER"
  echo "Created user $ELLA_USER."
fi

say "2/6 Data layout under $ELLA_HOME"
for d in models memory diary ella-core backups; do
  mkdir -p "$ELLA_HOME/$d"
done
chown -R "$ELLA_USER:$ELLA_USER" "$ELLA_HOME"
chmod 700 "$ELLA_HOME"
echo "Layout ready: models memory diary ella-core backups"

say "3/6 Ollama (model server)"
if command -v ollama >/dev/null 2>&1; then
  echo "Ollama already installed: $(ollama --version)"
else
  curl -fsSL https://ollama.com/install.sh | sh
fi
systemctl enable ollama >/dev/null 2>&1 || true

say "4/6 Download the offline model ($MODEL) + verify it loads"
# Must happen while the internet is up — an offline brain not on disk
# doesn't exist when you need it.
if ollama list 2>/dev/null | grep -q "^$MODEL"; then
  echo "Model $MODEL already present, skipping download."
else
  ollama pull "$MODEL"
fi
# Smoke test: one short answer, then stop. Proves the model actually runs.
ollama run "$MODEL" "Say 'Ella is here' and nothing else." < /dev/null | head -c 500
echo

say "5/6 llama.cpp fallback (only the GGUF file, no build yet)"
GGUF_FILE="$ELLA_HOME/models/qwen2.5-7b-instruct-q4_k_m.gguf"
if [ -f "$GGUF_FILE" ]; then
  echo "GGUF already present, skipping download."
else
  sudo -u "$ELLA_USER" curl -fsSL -o "$GGUF_FILE" "$GGUF_URL"
  echo "Downloaded $GGUF_FILE ($(du -h "$GGUF_FILE" | cut -f1))"
fi

say "6/6 Systemd units (resource-capped, LAN-only)"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
for unit in ella-model.service ella-backup.service ella-backup.timer ella-memory.service; do
  if [ -f "$SCRIPT_DIR/$unit" ]; then
    cp "$SCRIPT_DIR/$unit" "/etc/systemd/system/$unit"
    echo "Installed $unit"
  else
    echo "WARNING: $unit not found next to this script, skipping." >&2
  fi
done
systemctl daemon-reload
systemctl enable ella-backup.timer >/dev/null 2>&1 || true
# Model server stays OFF until asked for: on-demand, not 24/7.
systemctl disable ella-model.service >/dev/null 2>&1 || true

say "Done. Next steps:"
echo "  - Start the model when you want to talk offline: sudo systemctl start ella-model"
echo "  - Talk to it: ollama run $MODEL"
echo "  - Stop it when done: sudo systemctl stop ella-model"
echo "  - First backup: sudo -u $ELLA_USER bash $ELLA_HOME/ella-core/native-adaos/ella-backup.sh"
echo "  - Then run the restore drill (plan §6) before trusting the backup."
