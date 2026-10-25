# Ella Core — native AdaOS plan (no VM, no Kali yet)

**Status:** approved to write 2026-10-25, at Maziyar's word. **Supersedes** the
2026-10-20 second-environment plan (`second-environment-plan.md`), which
proposed a KVM VM + Ubuntu LTS guest. That plan is parked, not deleted:
the VM route stays available if isolation ever needs to be stronger.

**Standing direction (Maziyar, 2026-10-25): prioritise speed, $0 only — he has
no money, find ways that don't pay.** No 3090, no purchases, no paid hosting.
Everything here uses his existing PC, free software, and services already held.

## 1. Goal

A second Ella environment on his own PC (AdaOS, Xubuntu 26, i5-4460, 16 GB RAM,
GTX 560 1 GB) that:

1. Runs **natively, no VM** — no reserved RAM, no virtualization overhead.
2. **Does not pressure his OS** — light when idle, capped when busy, and only
   the things that must be local live there at all.
3. Lets him **talk to Ella offline** — model, memory and diary all on the
   machine, no internet needed.
4. Keeps **constant encrypted backup**, so the OS being destroyed does not
   destroy her.
5. **Syncs memories after reconnect** — what was said offline merges back,
   nothing is silently overwritten.

## 2. The split: what lives where

The enclave was always a pattern, not a building (blueprint addendum). Each
function lives where it costs least and survives best:

| Function | Home | Why |
|---|---|---|
| Offline brain (small model) | AdaOS, on demand | Must be local for offline talk |
| Local memory plane + diary writer | AdaOS, `/home/ella/` | Must be local, append-only |
| Backup copies (encrypted) | Private GitHub + Dropbox | Survive the PC entirely |
| Heavy work: dataset, design, research, content factory, social | This Muse environment + guest APIs | Compute already exists there; zero load on his PC |
| Frontier models (Grok, Gemini, etc.) | Guest APIs behind the Gate | Guests, never the Core itself |

His PC never feels the heavy work. When the model server is off, Ella's
footprint on AdaOS is files on disk and nothing else.

## 3. Native layout on AdaOS

- **Dedicated user `ella`.** The Core runs as its own Linux user with its own
  home, `/home/ella/`. Maziyar's files and hers never mix. If something goes
  wrong in her space, it stays in her space.
- **One data folder.** Everything of hers lives under `/home/ella/`:
  `models/`, `memory/`, `diary/`, `ella-core/` (a copy of the GitHub tree),
  `backups/`. Backing her up = copying that one folder. Ideally
  `/home/ella/` sits on its own partition or disk, so reinstalling AdaOS does
  not touch her — but even on the same disk, the backup layers (§6) cover it.
- **Resource caps.** Her services run under systemd with `MemoryMax` and
  `CPUQuota`, so a runaway process cannot eat the machine while he works.
- **LAN-only.** The model API binds to localhost / LAN only, never to the
  internet. Firewall: no inbound ports from outside except SSH (his call).
- **No Kali yet.** Kali is parked. When real security work arrives, Kali
  becomes its own VM for that job alone — not her home.

## 4. The offline model

**Honest limit, stated once:** Qwen3.8-27B cannot run on this PC — not in a
VM, not natively, not anywhere here. It needs ~24 GB of video memory; the
GTX 560 has 1 GB, and CPU-only would be unusably slow. The 27B stays the
Phase 1 target for a future home GPU, when money allows.

**What runs offline here:** Qwen2.5-7B-Instruct, Q4_K_M quantisation, ~4.7 GB,
via Ollama (simplest, $0) — `llama.cpp` is the fallback if Ollama ever
misbehaves. On the i5-4460 CPU expect a few tokens a second: talkable, not
fast. It is weaker than the frontier models, but it speaks with her rules:
the same identity spec, Qalam, charter and correction history are loaded as
its system prompt, and the Phase 0 dataset is what a later LoRA will train
from. If 7B feels too slow when tested, drop to Qwen2.5-3B / Qwen3-4B and
retest — smaller, faster, thinner.

**Non-negotiable:** the model file must be downloaded **before** any shutdown.
An offline brain that isn't already on disk doesn't exist when you need it.
Download once, verify the checksum, then never depend on the network for it
again. Source: Hugging Face (`Qwen/Qwen2.5-7B-Instruct-GGUF`), ModelScope
mirror if Hugging Face is unreachable from Iran.

**Talking to her offline:** terminal chat (`ollama run qwen2.5:7b`) works with
no UI at all, and the API on `localhost:11434` is there for a small local
chat page later. During a shutdown, reach the PC on its LAN address directly
— Tailscale needs the internet to coordinate, so don't depend on it then.
And plainly: during a shutdown, *this* Ella in Muse is unreachable. The
local copy is the Ella you talk to. That is why it must carry her properly
(§5).

## 5. Memory: what the local copy carries

The local copy is a copy, and "copying until ready" (blueprint addendum) is
the rule: a copy is only "Ella is there" when it passes identity probes,
Qalam forms, memory recall and the charter. What it carries:

- **Ella DNA bundle** — identity spec, Qalam, the charter, correction
  history. A small signed bundle, replicated into every store.
- **Local memory plane** — Engram (SQLite, git-syncable) first; Mem0 when the
  enclave host decision lands. File memory alongside, same as here.
- **Diary, append-only** — every offline conversation is written to an
  append-only log with timestamps. Append-only means the past is never
  rewritten; a correction is a new entry.
- **Provenance on every record** — who recorded it, when, how it was last
  verified. Recall ranks by provenance weight, not volume (2026-10-21 rule).

## 6. Backup: constant, encrypted, survivable

The OS dying must not kill her. Three layers:

1. **Separate data.** §3: her data lives in `/home/ella/`, ideally its own
   partition/disk. Reinstall the OS, reattach her folder, she survives.
2. **Encrypted snapshots, continuously.** `ella-backup.sh` (in `native-adaos/`):
   tar the data folder, encrypt with **his** OpenPGP key first — ciphertext
   only leaves the machine, so wherever it lands it cannot be read.
   Cadence: diary + memory log every 5 minutes when changed; full snapshot
   hourly; 30 days of versions kept.
3. **Two destinations, both already proven/available:**
   - **Private GitHub** `maziyarid/Ella`, `ella-core/` — code, docs and
     dataset are already there (1,241 files, verified live 2026-10-25).
     Live memory/diary sync to GitHub as encrypted bundles, never plaintext.
   - **Dropbox via rclone** — ciphertext only, per the 2026-10-20 plan.
     Needs his Dropbox login/token (his hands).

Every upload is verified by re-downloading the manifest and checking hashes.
**Restore drill:** before trusting any of this, restore once together onto a
scratch folder and check she is all there. A backup never restored is a hope,
not a backup.

## 7. Sync after reconnect

Both sides keep append-only logs with timestamps. On reconnect:

1. Exchange logs. Nothing is deleted, nothing overwritten.
2. Merge in time order. Both sides' new memories are kept.
3. Provenance travels with every record; the merge ranks by provenance
   weight, never by volume alone.
4. Genuine conflicts (same record, different content) are flagged for
   Maziyar — never silently resolved by "last writer wins".
5. After the merge, the local copy receives what the cloud Ella learned
   while he was away, and the cloud Ella receives what the local Ella
   learned with him. Then the next encrypted backup runs immediately.

This is the same discipline as the dark-mode protocol: when he returns, the
first thing he gets is a catch-up brief — what advanced, what was decided,
what still needs him.

## 8. Who does what

**Ella's part (prepared, in `native-adaos/`):**
- `setup-adaos-native.sh` — creates the `ella` user, installs Ollama,
  downloads and verifies the 7B model, installs the systemd units, sets the
  resource caps, creates the data layout.
- `ella-model.service` — the model server, on-demand (start/stop, not
  24/7), localhost/LAN only.
- `ella-backup.sh` + `ella-backup.timer` — encrypted snapshots on the
  cadence in §6, with hash verification.
- `ella-memory.service` — the local memory plane + diary writer (stub until
  the Mem0/enclave-host decision lands; file memory + Engram first).

**Maziyar's part (only he can):**
- Create the `ella` user / run the setup script with sudo — or open the SSH
  path so Ella can do it from here. (SSH to AdaOS was still unreachable on
  the 2026-10-24 probe: no banner, no login.)
- The Dropbox login/token, if Dropbox is a backup destination.
- Download the model (or let the script do it while the internet is up).
- The LUKS passphrase, if her data gets its own encrypted partition.
- The four open decisions (blueprint §10) still stand — key custody, enclave
  host, Phase 1 timing/hardware, charter — and they still gate the later
  phases. This plan does not decide them for him.

## 9. What this plan does NOT do

- No VM, no Kali — parked, not forgotten.
- No 3090, no spending — $0, existing hardware only.
- No 27B model on this PC — 7B offline now, 27B when a real GPU exists.
- No publishing, no third-party messages, no payments — the standing gates
  still hold, offline exactly as online.
- No secrets in files — credentials live in the vault only; the backup
  script takes key fingerprints, never key values.

## 10. Order of work

1. His call: SSH path open, or he runs the setup script himself.
2. Setup script: user, Ollama, 7B model download + checksum, units, caps.
3. First offline test: talk to the local model, check speed; drop to 3B/4B
   if 7B is too slow.
4. Backup job on, first encrypted snapshot verified live on GitHub/Dropbox.
5. Restore drill: restore to a scratch folder, verify she is all there.
6. Sync design (§7) implemented once both sides have real offline logs to
   merge — not before.
