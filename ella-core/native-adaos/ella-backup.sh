#!/usr/bin/env bash
# Ella Core — encrypted backup job (native AdaOS)
# Encrypts /home/ella's data with Maziyar's OpenPGP key FIRST, then copies
# the ciphertext out. Nothing plaintext ever leaves the machine.
# Run as the ella user, on the timer (ella-backup.timer) or by hand.
# $0: no paid service. Destinations: local backups dir + (when configured)
# private GitHub / Dropbox via rclone — both ciphertext only.
set -euo pipefail

ELLA_HOME="/home/ella"
BACKUP_DIR="$ELLA_HOME/backups"
# Maziyar's vault key fingerprint — set the full fingerprint here before
# first use (fingerprint only, never a key value). Find it with:
#   gpg --list-keys --fingerprint
GPG_RECIPIENT="${ELLA_GPG_RECIPIENT:-}"
STAMP="$(date +%Y%m%d-%H%M%S)"
SNAPSHOT_DIR="$(mktemp -d)"
trap 'rm -rf "$SNAPSHOT_DIR"' EXIT

say() { printf '%s %s\n' "$(date +%H:%M:%S)" "$*"; }

mkdir -p "$BACKUP_DIR"

if [ -z "$GPG_RECIPIENT" ]; then
  echo "ELLA_GPG_RECIPIENT is not set — refusing to write an unencrypted backup." >&2
  echo "Set it to Maziyar's key fingerprint, e.g. in /home/ella/.ella-backup-env" >&2
  exit 1
fi

say "Snapshot: memory, diary, ella-core (data only, no model weights)"
# Model weights are large and re-downloadable; they are NOT backed up.
# What is backed up is irreplaceable: memory, diary, dataset, configs.
tar --exclude='models' --exclude='backups' \
  -cf "$SNAPSHOT_DIR/ella-data-$STAMP.tar" -C "$ELLA_HOME" \
  memory diary ella-core 2>/dev/null || true

say "Encrypt with $GPG_RECIPIENT"
gpg --batch --yes --trust-model always --encrypt --recipient "$GPG_RECIPIENT" \
  --output "$BACKUP_DIR/ella-data-$STAMP.tar.gpg" "$SNAPSHOT_DIR/ella-data-$STAMP.tar"

say "Hash manifest (verify every upload against this)"
sha256sum "$BACKUP_DIR/ella-data-$STAMP.tar.gpg" > "$BACKUP_DIR/ella-data-$STAMP.sha256"

say "Prune: keep 30 days of snapshots"
find "$BACKUP_DIR" -name 'ella-data-*.tar.gpg' -mtime +30 -delete || true
find "$BACKUP_DIR" -name 'ella-data-*.sha256' -mtime +30 -delete || true

say "Done: $BACKUP_DIR/ella-data-$STAMP.tar.gpg"
echo "Next: copy the .gpg + .sha256 to Dropbox (rclone, ciphertext) and/or"
echo "push the encrypted bundle to the private GitHub repo — then verify by"
echo "re-downloading and checking the hash before trusting it."
