# Decision register — continuity lane v0.1

Only owner choices that are still open. Each one blocks or shapes a next step. None of them blocks review of this branch.

| ID | Decision needed | Why it is open | Options | Lane default until decided |
|---|---|---|---|---|
| D1 | Visibility of `maziyarid/Ella` | `ella-core/README.md` says "Private repo; do not make public" and the native AdaOS plan names it as the "private GitHub" backup target. GitHub reports it PUBLIC, and an anonymous fetch returned the file tree. | (a) Make it private (owner action). (b) Keep it public, correct the README, and choose a different private target for encrypted bundles. | Publish only synthetic material here. Never point live memory or backups at this repository. |
| D2 | The single Episodic stream | The plans name both `diary/` (append-only) and `memory/` (memory log). The contract allows exactly one Episodic stream. | (a) `diary/` is the stream; `memory/` holds Core/Notebook/People. (b) The reverse. (c) Something else. | Register both read-only in the manifest and report the ambiguity (`uq:episodic-vs-memory-log`). |
| D3 | Permanent home of the contract | `00_KERNEL` owns boot order and manifest, and kernel changes need owner approval. | (a) Promote to `00_KERNEL/BOOT.md` + `MANIFEST.md`. (b) Keep it in `ella-core/continuity/` as a referenced spec. | (b) |
| D4 | Recoverable vs terminal `blocked` | Ella-Brain has a single `blocked` status, and that schema belongs to another lane. | (a) Add it to the Ella-Brain schema later (schema change, other lane). (b) Keep it only in the continuity report vocabulary. | (b) |
| D5 | Approval for language-model quality evaluation | It would call a provider model on synthetic fixtures. | Approve a bounded run (model, budget, fixtures). Or decline. | Not run. |
