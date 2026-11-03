# Live memory-layout inventory — procedure for Maziyar to review (v0.1)

Status: **prepared, not run.** Nobody has run this on the AdaOS PC. Running it needs Maziyar's decision, at his machine.

What an inventory can establish: which files exist under `/home/ella/memory` and `/home/ella/diary`, their sizes, and their
exact byte identity (sha256). What it cannot establish: what any file means, how records are delimited, or whether
anything in it is approved. Those come later (sections 4–5), and the adapter keeps real records unapplied until they exist.

## 1. What the script does and does not do

`inventory.py` (Python 3 standard library only, about 340 lines; read it before running).

| Does | Does not |
|---|---|
| Inspect exactly `/home/ella/memory` and `/home/ella/diary`. The base path is a constant; there is no path argument | Read any other location, including the rest of `/home/ella`, `~/.ollama`, `models/`, `backups/` |
| Open every directory and file with `O_NOFOLLOW` relative to an already-open parent directory | Follow, resolve or read the target of any symlink (they are listed as `not_followed`) |
| Hash regular files (sha256) and record their size; flag files that change while being read | Print, parse or decode file contents |
| Report `missing`, `not_accessible`, `symlink_refused`, `not_a_directory`, `not_readable`, `not_listable` explicitly | Open FIFOs, sockets or devices (listed as `not_opened`) |
| Write JSON to standard output only; `compare` and `summarize` print counts and aggregates only | Create, modify or delete any file; make network calls; start processes or services; call the model |
| Refuse to run if its standard output is a file inside one of the two targets | Upload anything |

## 2. Steps on the PC

Run from Maziyar's own account in a terminal on the PC, with the script copied from the PR branch. Ideally Ella is not
writing memory at the time (see §2a).

```sh
# 0. Read the script, then record its hash so the run can be tied to the reviewed version.
sha256sum inventory.py

# 1. A new private directory outside /home/ella and outside any git checkout.
#    set -C makes '>' refuse to overwrite an existing file or follow a pre-placed symlink;
#    mkdir without -p fails if the directory already exists, so it is known to be new.
set -C
umask 077
D=~/ella-inventory-$(date -u +%Y%m%dT%H%M%SZ)
mkdir -m 700 "$D"

# 2. Two private passes. They run as `ella` because the setup script intends /home/ella to be mode 700.
#    The script is passed on stdin, so `ella` does not need to read Maziyar's files;
#    the output files are created by Maziyar's shell and owned by Maziyar.
sudo -u ella python3 -I -B - scan < inventory.py > "$D/inventory-1.json"
sudo -u ella python3 -I -B - scan < inventory.py > "$D/inventory-2.json"

# 3. Did anything change between the passes? Prints counts only.
python3 -I -B inventory.py compare "$D/inventory-1.json" "$D/inventory-2.json" > "$D/compare.json"

# 4. Sanitized summary (runs as Maziyar and reads only the private inventory).
python3 -I -B inventory.py summarize "$D/inventory-2.json" > "$D/summary.json"

# 5. Review summary.json and compare.json by eye before sharing either with anyone.
set +C
```

If the `ella` user does not exist, step 2 fails at `sudo` with nothing read; report that result instead. Lines starting
with `note:` on the terminal (for example `note: diary: missing`) are expected and are part of the result.

### 2a. Files that change during the scan

Each file is hashed from one open file descriptor. Before and after reading, the script compares size, mtime and ctime,
and flags `changed_during_read`; a file swapped between listing and opening is flagged `replaced_during_scan`. Timestamps
have limited resolution (4 ms on the ext4 used for testing), so a same-size rewrite within one tick can go unnoticed.
The second pass and `compare` cover that case: if `identical` is false, files were changing, and the inventory is a
moving snapshot. Repeat it when Ella is idle.

### 2b. Assumptions that remain

| Assumption | Why it matters | What the script does |
|---|---|---|
| `/`, `/home` are root-owned and not attacker-controlled | `O_NOFOLLOW` guards only the last path component of `/home/ella` | Refuses `/home/ella` if it is itself a symlink; everything below it is opened relative to directory descriptors |
| The `python3` that `sudo` runs is the system interpreter | A different interpreter could do anything | `-I` ignores environment variables and user site-packages; the interpreter path is not checked |
| Hard links | A hard link inside `memory/` to a file elsewhere is indistinguishable from a regular file; its bytes are hashed (never printed) | Reports `nlink` per file and a `hardlinked_files` count in the summary |
| Mount points inside the targets | A different `st_dev` (mount point, bind-mounted file) | Not entered or hashed; listed as `other_filesystem_not_entered`. Tested only with a simulated `st_dev`, not a real mount |
| File swapped for a FIFO/device between stat and open | Opened read-only with `O_NONBLOCK|O_NOCTTY|O_NOFOLLOW`, detected by fstat and closed unread | Not literally "never opened" in this race; a device swap needs root. `O_PATH` reopen not implemented |
| Very large files | Hashing reads every byte | No size cap; the run takes as long as the reads take |
| Depth | Each directory level holds one descriptor | Stops at depth 32 and reports `depth_limit_not_descended` |
| Undecodable filenames | Names that are not valid UTF-8 | Escaped and marked `name_not_utf8`; the JSON stays valid |
| `stdout` is a pipe rather than a file | The inside-target check applies only to a regular output file | The documented commands redirect to a file |
| Confirmation attacks on the summary | Someone who already knows every name and every byte can confirm a guess against `aggregate_sha256` | Nothing more can be learned from it; share only `status` if even that is too much |

## 3. What stays private and what may be shared

| Artifact | Contains | Handling |
|---|---|---|
| `inventory-1.json`, `inventory-2.json` | Relative paths and filenames, types, sizes, per-file sha256, generation time, owner uid | **Private.** Filenames and paths may themselves be personal (names, dates, topics). Never commit it, never paste it into chat or a PR, never upload it. Keep it for later comparison. |
| `compare.json` | Counts of changed, added and removed files between the two passes | Shareable after review |
| `summary.json` | Per target: status, mode, counts by type, files hashed, total bytes, size buckets, counts for a fixed list of extensions (others pooled as `(other)`), maximum depth, hard-link count, counts of non-ok statuses, one aggregate sha256, and the sha256 of the private inventory it was made from | Shareable **after Maziyar reviews it.** It holds no names, paths, per-file hashes or times. The aggregate and inventory hashes let a later run prove "same bytes" or "changed" without revealing what changed. |

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
