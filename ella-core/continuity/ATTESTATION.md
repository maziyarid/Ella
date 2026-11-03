# Owner-controlled attestation workflow — specification v0.1

Status: **specified, not implemented, no register exists.** A separate file is a boundary. It keeps a memory record from
vouching for itself, but by itself it is **not evidence** that Maziyar approved anything. Evidence is a signature that only
Maziyar's key can produce, checked against a fingerprint that is pinned outside the memory root. The current adapter
checks only the boundary (the file is outside the root and bound to `record_sha256`). It therefore reports
`owner_approval_evidence: none` for the synthetic attestation file, and it must not apply real records.

## 1. Who approves what

| Authority level | Issuer | Status |
|---|---|---|
| `owner_approved`, `owner_stated` (the two owner levels in `checker.AUTHORITY_RANK`) | **Maziyar only** | This workflow |
| `ella_observed`, `ella_inferred`, `third_party_reported`, `derived` | Ella or another process | **No trusted issuer exists.** Until one is specified, an entry at these levels in the register is the only way such a record counts as attested, and the effective authority is still `min(claim, attestation)` as in `checker.py`. None of them can outrank an owner level |

Ella, the adapter, a backup job, or a pull request cannot create an owner approval. A merge on GitHub is not an approval
of a memory record.

## 2. Where the register lives

- One append-only file, for example `/home/maziyar/ella-attest/register.jsonl`, outside `/home/ella/memory` and
  `/home/ella/diary`. It is owned by Maziyar and **not writable by `ella`**. The adapter rejects a register under its root.
- A detached signature next to it: `register.jsonl.asc`.
- The pinned key fingerprint goes in the adapter's manifest, which is also signed. The register itself is not a source
  for the fingerprint. The default is the same OpenPGP key whose fingerprint `ella-backup.sh` reads from
  `/home/ella/.ella-backup-env`, unless Maziyar chooses a separate signing subkey (recommended: a sign-only subkey).
- The register is never committed to GitHub. It names record ids and hashes, which can be sensitive.

## 3. Entry format (one JSON object per line)

```json
{"seq": 7, "action": "approve", "record_id": "core-0003", "source_id": "memory/MEMORY.md",
 "record_sha256": "sha256:…", "authority": "owner_approved", "decision_ref": "DotCollab 2026-11-05 #12",
 "issued_at": "2026-11-05T09:00:00Z", "expires_at": null, "supersedes_entry": null}
```

- `seq` starts at 1 and increases by exactly 1 with no gaps.
- `action` is one of `approve`, `withdraw` or `replace`.
- `record_sha256` is the sha256 of the record's exact bytes as the family format defines them (for a JSONL record: the
  line's UTF-8 bytes without the trailing `\n`; for a fenced block: the bytes between the fences). It is never the hash of
  a re-serialized or normalized form.
- `decision_ref` points to where the decision was made (for example DotCollab). It is a pointer, not the evidence.

## 4. How approval binds to exact bytes

1. Maziyar reads the record on the PC and computes its hash with the adapter's own function, run locally.
2. He appends an `approve` entry with that hash and re-signs the whole register:
   `gpg --local-user <FPR> --armor --detach-sign --output register.jsonl.asc register.jsonl`.
3. At load time the adapter (a) verifies the signature against the pinned fingerprint and refuses everything on failure,
   (b) checks that `seq` is contiguous, (c) recomputes the hash from the bytes it read, and (d) grants the entry's authority only
   when the current, unwithdrawn, unexpired entry for that `(source_id, record_id)` has exactly that hash.
4. If even one byte of the record changes, the hash no longer matches. The record becomes `changed_unreconciled` and loses
   owner authority until a new entry approves the new bytes.

## 5. Withdrawal and replacement

- **Withdraw**: append `{"action": "withdraw", "record_id": …, "record_sha256": …, "supersedes_entry": <seq>}` and re-sign.
  From then on the record is unattested. Nothing is deleted, and the history stays readable.
- **Replace**: the corrected record is written as new bytes, which gives a new hash. Then append
  `{"action": "replace", "record_id": <new id>, "record_sha256": <new hash>, "supersedes_entry": <seq of old approval>}`.
  The old approval is retired by that entry; the old record is not rewritten.
- **Expiry**: if `expires_at` has passed, the entry no longer grants authority. Renewal is a new `approve` entry.

## 6. Rollback and replay

A valid signature over an older register would otherwise let someone restore an earlier approval set. To prevent this, the
signed manifest pins `register_latest_seq` and `register_sha256`. The adapter refuses a register with a lower `seq` or a
different hash at the pinned `seq`. Maziyar updates and re-signs the manifest whenever he signs the register.

## 7. What is needed before real records can be applied

1. Maziyar decides which key or subkey signs, and where the register and manifest live.
2. A verifier is added. It calls `gpg --verify` with an isolated, read-only keyring that holds only the pinned public key,
   or it uses a pure verification library. Tests use an invented throwaway key and are expected to fail closed for: bad
   signature, wrong key, missing signature, `seq` gap, rollback, withdrawn entry, expired entry, and a hash mismatch by
   one byte.
3. The format descriptions from `LIVE_INVENTORY_PROCEDURE.md` §4 exist for each family.

Until all three are in place, real records stay unapplied.
