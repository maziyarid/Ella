# Decision register — continuity lane v0.1

Updated 2026-11-03 from the review dispositions. Settled policy is not reopened here.

## Open — needs Maziyar

| ID | Decision | Recommendation | Until decided |
|---|---|---|---|
| D1 | Visibility of `maziyarid/Ella`. `ella-core/README.md` says "Private repo; do not make public", but GitHub reports the repository as PUBLIC. | Make it private, because its own README requires that. Visibility does not change without Maziyar's approval. | Publish only synthetic material. Never point live memory or backups at this repository. |

Making the repository private does not take back copies that were already made (forks, clones, caches). Auditing
exposed content and git history is a separate task, and this lane has not done it.

## Lane directions — recorded, not blocking

| ID | Direction | Effect now |
|---|---|---|
| D2 | `diary/` is the logical Episodic stream. Other event logs (including `memory/` logs) are legacy, read-only inputs until a mapping is accepted. | No migration and no rewrite. The manifest may register only `diary/` as the `episodic` source. |
| D3 | The contract stays in `ella-core/continuity/` for v0.1. Kernel promotion (`00_KERNEL/BOOT.md`, `MANIFEST.md`) is deferred. | No kernel edits. |
| D4 | Settled policy: `blocked` is recoverable. Continuity diagnostics stay separate from the Task schema. | No Ella-Brain or Task schema change. F04 already encodes it. |
| D5 | Paid language-model quality evaluation is deferred. | Does not block deterministic tests or a synthetic end-to-end demonstration. |
