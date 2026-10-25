# native-adaos/ — Ella Core on AdaOS, native, no VM, no Kali yet

Plan: `../native-adaos-plan-2026-10-25.md` (the authority; read it first).

Files here:

- `setup-adaos-native.sh` — run with sudo on AdaOS while the internet is up.
  Creates the `ella` user, installs Ollama, downloads Qwen2.5-7B Q4, installs
  the units below. Idempotent; read before running; UNTESTED on his PC
  (SSH still unreachable 2026-10-24).
- `ella-model.service` — model server, on-demand, localhost-only, capped at
  10G RAM / 300% CPU.
- `ella-backup.sh` — encrypted backup job. Needs `ELLA_GPG_RECIPIENT` set to
  Maziyar's key fingerprint (in `/home/ella/.ella-backup-env`); refuses to
  run without it. Never backs up model weights (re-downloadable); backs up
  memory, diary, ella-core. Keeps 30 days.
- `ella-backup.service` + `ella-backup.timer` — hourly encrypted snapshots.
- `ella-memory.service` — STUB for the local memory plane (file memory +
  Engram first; Mem0 after the enclave-host decision).

Standing rules: $0 only; no secrets in these files (fingerprints, never key
values); no publishing, no third-party messages, no payments — gates hold
offline exactly as online.
