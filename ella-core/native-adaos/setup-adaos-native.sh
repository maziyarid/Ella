#!/usr/bin/env bash
# Ella Core — native AdaOS setup (no VM, no Kali yet)
# Run on AdaOS (Xubuntu 26) with sudo, while the internet is UP.
# UNTESTED on Maziyar's PC (SSH still unreachable 2026-10-24) — read before
# running; every step prints what it is about to do. Safe to re-run: all
# steps are idempotent (they skip work already done).
# $0 only: Ollama, llama.cpp fallback, Qwen3-4B + Qwen2.5-Coder-7B — all free.
# v2 (2026-10-25, Maziyar's direction): strongest the machine can handle
# for everyday shutdown use is a 4B chat model; the 7B coder is the heavier
# second model for leave-running tasks. 14B+ ruled out (too slow on i5-4460).
# v2.1 (2026-10-25): step 5 fixed — HuggingFace split the Q4_K_M GGUF into
# two parts (single file 404s), so download both parts; a fallback-file
# failure no longer kills the install (warn and continue). v1 ran on AdaOS
# 2026-10-25 12:42: steps 1-4 OK (qwen2.5:7b pulled, smoke test "Ella is
# here." passed); step 5 404 stopped it before step 6 (units not installed).
set -euo pipefail

ELLA_USER="ella"
ELLA_HOME="/home/ella"
MODEL="qwen3:4b"
CODER_MODEL="qwen2.5-coder:7b"
# Qwen2.5-7B-Instruct Q4_K_M GGUF, for the llama.cpp fallback path.
# NOTE: as of 2026-10-25 the single file no longer exists on HuggingFace —
# it is split into two parts; llama.cpp loads split files via part 1.
GGUF_PART1="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"
GGUF_PART2="https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf"

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

say "4/6 Download the offline models + verify the everyday one loads"
# Must happen while the internet is up — an offline brain not on disk
# doesn't exist when you need it.
# Everyday brain: 4B chat model (fastest usable on i5-4460, ~6-10 words/sec).
if ollama list 2>/dev/null | grep -q "^$MODEL"; then
  echo "Model $MODEL already present, skipping download."
else
  ollama pull "$MODEL"
fi
# Heavier brain: 7B coder for leave-running tasks (~2-4 words/sec).
if ollama list 2>/dev/null | grep -q "^$CODER_MODEL"; then
  echo "Model $CODER_MODEL already present, skipping download."
else
  ollama pull "$CODER_MODEL"
fi
# Smoke test: one short answer from the everyday model, then stop.
# Proves the model actually runs on this machine.
ollama run "$MODEL" "Say 'Ella is here' and nothing else." < /dev/null | head -c 500
echo

say "5/6 llama.cpp fallback (only the GGUF files, no build yet)"
# Fallback only — Ollama above is the real offline brain. A failure here
# must never kill the install again, so this step warns and continues.
GGUF1="$ELLA_HOME/models/qwen2.5-7b-instruct-q4_k_m-00001-of-00002.gguf"
GGUF2="$ELLA_HOME/models/qwen2.5-7b-instruct-q4_k_m-00002-of-00002.gguf"
if [ -f "$GGUF1" ] && [ -f "$GGUF2" ]; then
  echo "GGUF parts already present, skipping download."
else
  if sudo -u "$ELLA_USER" curl -fsSL -o "$GGUF1" "$GGUF_PART1" \
  && sudo -u "$ELLA_USER" curl -fsSL -o "$GGUF2" "$GGUF_PART2"; then
    echo "Downloaded GGUF parts ($(du -h "$GGUF1" "$GGUF2" | awk '{s+=$1} END {print s}'))"
  else
    echo "WARNING: GGUF download failed (optional fallback only) — continuing." >&2
    rm -f "$GGUF1" "$GGUF2"
  fi
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
echo "  - Everyday offline chat: ollama run $MODEL"
echo "  - Heavier coding work (leave it running): ollama run $CODER_MODEL"
echo "  - Start the model server on demand: sudo systemctl start ella-model"
echo "  - Stop it when done: sudo systemctl stop ella-model"
echo "  - First backup: sudo -u $ELLA_USER bash $ELLA_HOME/ella-core/native-adaos/ella-backup.sh"
echo "  - Then run the restore drill (plan §6) before trusting the backup."
