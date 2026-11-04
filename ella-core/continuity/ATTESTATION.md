# Owner-controlled attestation workflow — v0.2

Status:
- Register format, signature verification against a configured fingerprint, and the adapter rule "owner levels only from a verified register" are implemented in `attest_verify.py` and `adapter.py`. They are tested only with disposable keys and invented records (`test_attest_verify.py`, `test_adapter.py`).
- **No real register exists, no trusted signer is configured, and no real record is applied.**
- The signing key is **not decided** (`DECISIONS.md` D6).

A separate file is a boundary. It keeps a memory record from vouching for itself, but by itself it is **not evidence** that
Maziyar approved anything. Evidence is a detached signature over the register that verifies against an **explicitly
configured** trusted fingerprint. The unsigned `attestations.json` file therefore always reports `owner_approval_evidence:
none` and can never grant `owner_approved` or `owner_stated`. The adapter records `unsigned_owner_attestation_ignored`.

## 1. Who approves what

| Authority level | Issuer | Status |
|---|---|---|
| `owner_approved`, `owner_stated` (the owner levels in `checker.AUTHORITY_RANK`) | **Maziyar only**, through the signed register | Implemented and tested with disposable keys only |
| `ella_observed`, `ella_inferred`, `third_party_reported`, `derived` | No trusted issuer exists | Taken from the unsigned boundary file, capped by `min(claim, attestation)`. These levels can never outrank an owner level. The register rejects them as malformed |

Ella, the adapter, a backup job or a pull request cannot create an owner approval. A merge on GitHub does not approve a
memory record.

## 2. The signer (not decided)

- The verifier needs three things from the caller: the trusted fingerprint (`--trusted-fpr`), a public-key file
  (`--trusted-key`), and the register with its detached signature. Without the fingerprint it refuses
  (`no_trusted_signer_configured`).
- A valid signature from any other key is refused as `untrusted_signer`, even when that key is present in the supplied key
  file. The configured fingerprint must be the **primary** key fingerprint. A signing subkey is accepted only through its primary; configuring a subkey fingerprint is refused (`untrusted_signer`).
- gpg runs in a fresh temporary home directory that holds only the supplied public key. The user's keyring, agent and
  configuration are never consulted, and the directory is deleted afterwards.
- Existing key reference, **not an approved authority**: `ella-backup.sh` encrypts to a recipient named by `GPG_RECIPIENT` in
  `/home/ella/.ella-backup-env`. This lane has not established whether that key is suitable for signing or authorized for
  owner approvals, and does not use it as a default. Choosing a key, possibly a dedicated sign-only subkey, and where its
  fingerprint is pinned, is Maziyar's decision.
- The trusted fingerprint and public-key file must come from a place the record writer (`ella`) cannot modify. Where that
  place is has not been decided.

## 3. Register format (one JSON object per line, UTF-8, every line `\n`-terminated)

```json
{"seq": 1, "action": "approve", "source_id": "src:core", "record_id": "core:pref-tea",
 "record_sha256": "sha256:…", "authority": "owner_approved", "decision_ref": "D-…",
 "issued_at": "2026-11-05T09:00:00Z", "expires_at": null}
```

Strict parsing. Any violation refuses the **whole** register:
- `seq` is an integer (not a boolean) equal to its line number.
- `action` is `approve`, `withdraw` or `replace`.
- Unknown or duplicate keys are refused, as are blank lines and non-UTF-8 bytes.
- `record_sha256` is `sha256:` followed by 64 lowercase hex digits. It covers the record's exact bytes as the adapter
  extracts them (for a JSONL or fenced record: the line's UTF-8 bytes without the newline), never a re-serialized form.
- `source_id` is the manifest's source id. The adapter compares it with the source the record was actually read from,
  never with a claim inside the record.
- `approve` and `replace` require an owner `authority`. `withdraw` must not carry one.
- `withdraw` and `replace` require `supersedes_entry` pointing to an earlier entry. `approve` must not carry it.

## 4. Withdrawal, replacement, conflicts, expiry

- **Withdraw** retires an active approval. The entry must name the same source, record and hash. Withdrawing twice,
  withdrawing a withdrawal, or withdrawing with a different hash is a conflict.
- **Replace** retires an active approval and approves **different bytes** in the same source. Replacing with the same hash,
  across sources, or onto a record that already has another active approval is a conflict.
- A second active approval for the same `(source_id, record_id)` is a conflict.
- Any conflict refuses the whole register. There is no "best effort".
- Entries with `issued_at` in the future, or with `expires_at` at or before the evaluation time, grant nothing and are counted
  in `notes`.
- Changed record bytes no longer match the approved hash. The record loses owner authority
  (`owner_approval_hash_mismatch`), and an `accepted_revisions` entry cannot carry the approval over to new bytes.

## 5. Failure handling (all tested)

Each of these is refused, and no owner authority is granted:
- No trusted fingerprint; an invalid fingerprint; a missing register, signature, public key or anchor.
- A missing gpg, a failed key import, a non-zero exit even when the status output looks good, a timeout.
- More than one signature; a bad signature next to a good one; a non-binary signature class; a bad or expired signature
  or key; a garbage signature.
- Any malformed or conflicting entry; a rollback or fork against the anchor.
- `owner_authority()` grants nothing unless the result has `status == "verified"` **and** carries a private proof object
  issued by `verify_register()` in the same process. Approvals are read from that proof, not from the dict, so a hand-built
  dict or edits to `approvals` grant nothing (tested). This guards against injected or mistaken data; it is not protection
  against hostile code running inside the same Python process.
- Register lines must be `\n`-terminated with no `\r` or surrounding whitespace; ids must contain no control characters
  (prevents `source\0record` key collisions); `replace` must keep the same `source_id` and `record_id`.

## 6. Rollback: what is implemented and what is a design requirement

The problem: every register version Maziyar ever signed stays valid forever. Someone who can replace files could restore
an older, still validly signed register, for example one from before a withdrawal. The signature alone cannot detect this.

**Implemented and tested.** The verifier requires a rollback anchor `{latest_seq, prefix_sha256}`. It refuses a register
that has fewer entries than `latest_seq`, or whose first `latest_seq` lines do not hash to `prefix_sha256`
(`rollback_detected…`, `rollback_or_fork_detected…`). Appending after the anchor is accepted. On success the verifier
returns `anchor_if_accepted` for the new register. It **never writes the anchor**; advancing it is an owner step.

**Not implemented: design requirements.** The check is only as good as the anchor. Protection exists only if the anchor is
**trusted state outside the signed register that the attacker cannot rewind**:
- It must be writable by Maziyar and not by `ella`, and not stored with the register or in the same backup set.
- Signing the anchor does not help, because old signed anchors can be replayed just like old registers.
- Where the anchor lives, and how it is updated, is not implemented and not decided.

| Situation | What holds | Limit |
|---|---|---|
| First use | Maziyar creates the anchor `{latest_seq: 0, prefix_sha256: sha256("")}` by hand | Trust on first use. The first register accepted is whatever he signs; nothing earlier can be checked |
| Restart | Works only if the anchor survives restarts in its protected location. The verifier keeps no state between processes | A fresh process has no memory; it relies entirely on the stored anchor |
| Backup restoration | If the anchor is restored **from the same backup** as the register, both roll back together, and the rollback is **undetectable** | After a restore, Maziyar must re-confirm the anchor from a source outside that backup (for example his own record of the latest `seq` and hash) |
| Anchor lost | The verifier refuses (`rollback_anchor_missing`); it does not fall back silently | Recreating it is again trust on first use: Maziyar must confirm which register version is the latest |
| Anchor writable by the attacker | No protection | This is why storage location is a requirement, not a detail |

**Freeze (not implemented: design requirement).** A register that exactly matches the anchor still passes. If Maziyar
signs a new register containing a withdrawal but does not advance the anchor, someone can keep serving the older register
and the withdrawal never takes effect. The register as a whole has no expiry. The countermeasure used in established update
systems is to put a short, signed expiry on the "latest version" statement, so a stalled reader notices. This lane has not
implemented that. Until it does, a withdrawal is effective only once the anchor has been advanced past it.

This follows the model in The Update Framework. A reader detects rollback by refusing metadata older than the version it
already trusts, and freeze by expiry ([TUF specification, client workflow](https://theupdateframework.github.io/specification/latest/index.html);
[TUF security model](https://theupdateframework.io/docs/security/); Samuel, Mathewson, Cappos and Dingledine,
[Survivable key compromise in software update systems, CCS 2010](https://dl.acm.org/doi/10.1145/1866307.1866315)). Both defenses
depend on the reader remembering what it trusted before. That is why anchor storage is the deciding requirement here.

## 7. What remains before any real record can be applied

1. D6: Maziyar chooses the signing key and pins the fingerprint and public key somewhere `ella` cannot modify.
2. Anchor storage and update procedure (§6), outside the register and outside the backup set, plus a decision on freeze protection (signed expiry).
3. Format descriptions for each memory file family (`LIVE_INVENTORY_PROCEDURE.md` §4), so that records and their hashes can be
   extracted from the real files.
4. Live use of the adapter, which is still refused for `/home/ella` and needs a separate approval.

The P0 profile approvals in the manifest (`approval.by: owner`) are still unsigned manifest claims. Moving them into the
signed register is not done yet.
