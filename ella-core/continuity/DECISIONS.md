# Decision register — continuity lane v0.1

Updated 2026-11-03 from the review dispositions. Settled policy is not reopened here.

## Decided for the current work period

| ID | Decision | Effect now |
|---|---|---|
| D1 | `maziyarid/Ella` stays **temporarily public** for the current work period, because the agent needs access. It returns to private when that work is finished **and** Maziyar approves the change. (Decided by Maziyar, 2026-11-03.) | Not an open question for this lane. Sensitive data stays off GitHub regardless of visibility: only synthetic material, no inventories, no real filenames, no keys, no fingerprints. The lane never changes visibility itself. |

Making the repository private later does not take back copies already made (forks, clones, caches). Auditing exposed content
and git history is a separate task; this lane has not done it.

## Open — needs Maziyar

| ID | Decision | Status | Until decided |
|---|---|---|---|
| D6 | Which OpenPGP key (or sign-only subkey) is the **trusted signer** for owner attestations, and where its fingerprint is pinned. | **Not decided.** `ella-backup.sh` refers to an existing key through `GPG_RECIPIENT` in `/home/ella/.ella-backup-env`. That is only an existing key reference: its suitability for signing and its authorization as the owner-approval key have **not been established**, and it is not a default. | The verifier has no trusted fingerprint, so it refuses every register. No real record gets owner authority. |
| D7 | Running the local inventory on the PC (`LIVE_INVENTORY_PROCEDURE.md`). | Waits for Maziyar. The lane does not run it, does not repair SSH and does not collect real filenames. | Live layout stays unobserved. |

## Lane directions — recorded, not blocking

| ID | Direction | Effect now |
|---|---|---|
| D2 | `diary/` is the logical Episodic stream. Other event logs (including `memory/` logs) are legacy, read-only inputs until a mapping is accepted. | No migration and no rewrite. The manifest may register only `diary/` as the `episodic` source. |
| D3 | The contract stays in `ella-core/continuity/` for v0.1. Kernel promotion (`00_KERNEL/BOOT.md`, `MANIFEST.md`) is deferred. | No kernel edits. |
| D4 | Settled policy: `blocked` is recoverable. Continuity diagnostics stay separate from the Task schema. | No Ella-Brain or Task schema change. F04 already encodes it. |
| D5 | Paid language-model quality evaluation is deferred. | Does not block deterministic tests or a synthetic end-to-end demonstration. |
