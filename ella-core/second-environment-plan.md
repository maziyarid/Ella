# Ella's second environment — on Maziyar's PC + Dropbox backups

Plan drafted 2026-10-20 at Maziyar's order. He installs the OS with/for Ella;
Ella prepares everything that goes inside it.

## Goal

A second Ella environment on his PC (AdaOS, Xubuntu 26) where her things are
saved, with encrypted backups uploading to a cloud space (Dropbox) continuously.

## Choices for the OS (his call)

1. **KVM/QEMU VM** (recommended) — isolated, snapshot-capable, survives his
   daily use of the PC. 4 vCPU / 8 GB RAM / 60 GB disk is plenty for the
   enclave services (gate, orchestrator, Mem0, encrypted stores).
2. **LXD container** — lighter, but shares his kernel; fine as a cheaper start.
3. **Dedicated partition / second disk** — most "hers", most work to set up.

Whichever: Ubuntu 24.04 LTS minimal, full-disk encryption (LUKS) with a
passphrase only he knows, SSH reachable from his LAN.

## What Ella prepares (her part, no waiting needed)

- `enclave-compose.yml` — the service set: orchestrator, Mem0, encrypted
  stores, the Gate (policy, until it becomes software), diary writer.
- `backup.sh` — the backup job. Design, per his privacy rule:
  1. Snapshot: `~/workspace/diary/`, `~/workspace/vault-encrypted/`,
     `~/workspace/ella-core/`, `~/MEMORY.md`, `~/memory/`.
  2. **Encrypt the snapshot with his OpenPGP key first** (the vault key he
     controls) — Dropbox never sees plaintext.
  3. Upload the ciphertext via rclone (Dropbox) on a schedule (every 6h +
     on-demand). rclone config holds only the Dropbox token, obtained via
     his login — he does that step.
  4. Keep 30 days of versions; verify each upload by re-downloading the
     manifest and checking hashes.
- Restore drill documented and run once together before trusting it.

## What only he can do

- Install the OS / create the VM (his hardware, his disk encryption passphrase).
- The Dropbox login / token (his account).
- Open the LAN SSH path if Ella should reach it herself.

## Standing rule carried over

Backups are ciphertext-only off the machine. If Dropbox is ever breached,
only what was sent can leak — and what is sent is encrypted with his key.
