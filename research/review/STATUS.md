# Proof review status

Updated: 2026-10-10. **P versus NP remains OPEN.**

The five-agent team has completed an initial scoped review and is configured to continue hourly, staggered at twelve-minute intervals. Read [PROTOCOL.md](PROTOCOL.md) for the every-run requirements, source locations, ownership, logging and GitHub/Drive recovery rules.

## Active agents

| Start each hour, Asia/Seoul | Agent | Need addressed |
|---|---|---|
| :00 | MODEL_BRIDGE | All-input SAT transfer, semantic correctness and recursive closure |
| :12 | LOWER_BOUND | Quantified lower-bound core, source-specific separators and barrier audit |
| :24 | COST_CERTIFICATES | Fully charged construction, certificates, access, time and space |
| :36 | REDTEAM | Independent review of the three builders' latest changes |
| :48 | PROOF_MAP | Overall synthesis, proof-spine dependencies and cumulative coverage |

First scheduled cycle starts 2026-10-10 at 11:00 Asia/Seoul. Schedules specify starts, not completion guarantees. The initial live review was performed before this cycle. Each individual agent runs once per hour, not every twelve minutes.

## Formal working documents

- [Model bridge and wrapper contract](spines/model_bridge.tex): recovered conditional composition and local-input transfer, with the all-input construction still open.
- [Lower-bound and oracle audit](spines/lower_bound.tex): exact summary-only bound, decision bypass, relativized immunity and bounded-list conditional separation.
- [LSPV Boolean separator candidate](spines/lspv_separator.tex): explicit separator and reconstruction obligations, a proved representation lemma, and unresolved source-specific compression.
- [Cost and certificate spine](spines/cost_certificates.tex): charged aggregate and finite-depth closure; separate PFCERT time-window obstruction and remaining verifier target.
- [Formal proof map](spines/proof_map.tex): shortest surviving conditional chains and exact dependencies.

These are mathematical LaTeX proofs and candidate manuscripts, not proof-assistant certification. Each open premise is explicit. Related root manuscripts remain the historical and current project sources; this review does not silently replace their ownership.

## Highest-value next links

1. Prove a source-checkable, fully charged SAT successor or favorable typed epoch on a declared infinite unresolved family, then establish all-input coverage and successor closure. The existing recurrence cannot supply its own construction premise.
2. Recover the exact source and reconstruction interface for the canonical Boolean separator route; do not substitute a schematic generator or infer an arbitrary-algorithm lower bound from representation size.
3. Quantify the actual child-access/replay and peak-state costs, and determine whether a bounded-list endpoint verifier can exist in one suitable slower time window. The large-time obstruction does not construct such a verifier.

## Initial reviewed findings

- The current wrapper/ARC framework provides conditional implications. The missing implication from SAT in P to a favorable all-input constructor carries the main separation difficulty.
- ARC15's method-level sample covers 12 of 13 formulas; all six newly solved cases are SAT, and an UNSAT case remains UNKNOWN. It is neither all-input coverage nor a joint resource certificate.
- Older cosine product-endpoint wording is already superseded by the authoritative root correction. Isolated older passages must not be reused as current theorems.
- A finite-field statement needs the distinction between nonzero formal polynomials and nonzero polynomial functions. The review gives a precise repair.
- The attached generator ignores every nonempty cleaned seed when random draws are fixed. The finite FNV tags are not injective history encodings. A six-character collision was independently reproduced. These are implementation findings, not SAT lower bounds.
- Independent review accepts the certificate-enumeration obstruction at its stated scope: polynomial witnesses cannot satisfy the proposed bounded-list completeness for a sufficiently large time bound such as double exponential time. Slower fixed time bounds remain open.

## Coverage and reproducibility

The initial complete recursive GitHub metadata inventory contains 1,522 blobs at commit `b6948eb15a8afec37cc904120ce20b61b45a0dad`. Targeted Drive discovery contains 382 unique metadata records. These counts are inventory, not completed content review. There are 86 recorded main4/main5 include edges, 35 literal root references absent from that snapshot, and unresolved Drive pagination and chat/history coverage. Parent conversation retrieval succeeded; several child-agent retrievals reported unavailable.

See [repository review queue](coverage/repository_coverage_queue.csv), [Drive source inventory](coverage/drive_source_inventory.json), [include dependencies](coverage/include_dependencies.json), and [missing source references](coverage/root_missing_references.json). Detailed source scopes and primary references appear in the initial reports and [proof synthesis](coordination/proof_map.md). [Independent audit](coordination/redteam.md) records claim-level verdicts and repairs.

Every initial agent has a local log and a GitHub mirror. Publication receipts identify the commit and verified artifact digests. Future runs recover from GitHub or verified Drive fallback, never assume that scratch storage survives, and extend the queue without falsely declaring an exhaustive review complete.
