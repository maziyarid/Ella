# Live memory-layout inventory — procedure for Maziyar to review (v0.1)

Status: **prepared, not run.** Nobody has run this on the AdaOS PC. Running it needs Maziyar's decision, at his machine.

What an inventory can establish: which files exist under `/home/ella/memory` and `/home/ella/diary`, their sizes, and their
exact byte identity (sha256). What it cannot establish: what any file means, how records are delimited, or whether
anything in it is approved. Those come later (sections 4–5), and the adapter keeps real records unapplied until they exist.

## 1. What the script does and does not do

`inventory.py` (Python 3 standard library only, about 300 lines; read it before running).

| Does | Does not |
|---|---|
| Inspect exactly `/home/ella/memory` and `/home/ella/diary`. The base path is a constant; there is no path argument | Read any other location, including the rest of `/home/ella`, `~/.ollama`, `models/`, `backups/` |
| Open every directory and file with `O_NOFOLLOW` relative to an already-open parent directory | Follow, resolve or read the target of any symlink (they are listed as `not_followed`) |
| Hash regular files (sha256) and record their size; flag files that change while being read | Print, parse or decode file contents |
| Report `missing`, `not_accessible`, `symlink_refused`, `not_a_directory`, `not_readable`, `not_listable` explicitly | Open FIFOs, sockets or devices (listed as `not_opened`) |
| Write JSON to standard output only | Create, modify or delete any file; make network calls; start processes or services; call the model |
| Refuse to run if its standard output is a file inside one of the two targets | Upload anything |

## 2. Steps on the PC

Run from Maziyar's own account in a terminal on the PC, with the script copied from the PR branch.

```sh
# 0. Read the script, then record its hash so the run can be tied to the reviewed version.
sha256sum inventory.py

# 1. A private directory outside /home/ella and outside any git checkout.
umask 077
mkdir -p ~/ella-inventory-private

# 2. Private inventory. It runs as `ella` because the setup script intends /home/ella to be mode 700.
#    The script is passed on stdin, so `ella` does not need to read Maziyar's files;
#    the output file is created by Maziyar's shell and owned by Maziyar.
sudo -u ella python3 -I -B - scan < inventory.py > ~/ella-inventory-private/inventory.json

# 3. Sanitized summary (runs as Maziyar and reads only the private inventory).
python3 -I -B inventory.py summarize ~/ella-inventory-private/inventory.json > ~/ella-inventory-private/summary.json

# 4. Review summary.json by eye before sharing it with anyone.
```

If the `ella` user does not exist, step 2 fails at `sudo` with nothing read; report that result instead. Lines starting
with `note:` on the terminal (for example `note: diary: missing`) are expected and are part of the result.

## 3. What stays private and what may be shared

| Artifact | Contains | Handling |
|---|---|---|
| `inventory.json` | Relative paths and filenames, types, sizes, per-file sha256, generation time, owner uid | **Private.** Filenames and paths may themselves be personal (names, dates, topics). Never commit it, never paste it into chat or a PR, never upload it. Keep it for later comparison. |
| `summary.json` | Per target: status, mode, counts by type, files hashed, total bytes, size buckets, counts for a fixed list of extensions (others pooled as `(other)`), maximum depth, hard-link count, counts of non-ok statuses, one aggregate sha256, and the sha256 of `inventory.json` | Shareable **after Maziyar reviews it.** It holds no names, paths, per-file hashes or times. The aggregate and inventory hashes let a later run prove "same bytes" or "changed" without revealing what changed. |

Residual exposure in the summary: counts and size buckets reveal roughly how much is stored. If that is too much, share only
`status` and `aggregate_sha256` per target.

## 4. Minimum format information needed after the inventory

The adapter cannot load a real record until each **file family** (one row per pattern, for example `diary/*.jsonl`) is
described. The preferred way is a locally prepared description — Maziyar or Ella fills this template on the PC — or a
**synthetic example** written in the same shape with invented content. Real memory contents are not requested.

| Field | Why the adapter needs it | Example answer (invented) |
|---|---|---|
| Family pattern and logical store | Map files to Core / Notebook / People / Episodic (D2: `diary/` is the one Episodic stream) | `diary/YYYY-MM-DD.jsonl` → Episodic |
| Encoding | Bytes → text | UTF-8, no BOM |
| Record boundary | What one hashable record is | one JSON object per `\n`-terminated line / fenced block / whole file / SQLite row |
| Record id field | Supersession and attestation bind to it | `id`, unique within the store |
| Time field and zone | Ordering and staleness | `at`, ISO 8601 UTC |
| Author / writer field | Who wrote it (not who approved it) | `recorded_by` |
| Writer process | Whether files change while Ella runs | "Ella via a script", "Maziyar by hand", "none yet" |
| Append-only or rewritten in place | Whether old hashes stay valid | append-only |
| How a correction is expressed | Replacement vs edit | a new record with `supersedes: <id>` |
| Fields that are always present | Validation | `id`, `at`, `text` |
| For SQLite or other binary stores | Schema only | output of `sqlite3 FILE .schema` run locally, reviewed before sharing; never `SELECT` |

A synthetic example is one or two records per family with the same field names, the same nesting and the same delimiter,
and with every value invented. It is enough to write a parser and a test; it is not evidence about any real record.

## 5. What happens afterwards

1. The sanitized summary and the format descriptions go into the PR as **reported by Maziyar**, not as observed by this lane.
2. A family-specific reader is added to `adapter.py` and tested against synthetic examples only.
3. Real records stay unapplied until the owner attestation register in `ATTESTATION.md` exists and its signature check is
   implemented. Until then the adapter's correct output for every real record is "unattested, not applied".

Not part of this procedure: creating a new event log, migrating or rewriting memory, installing or enabling services, and
calling the model.
