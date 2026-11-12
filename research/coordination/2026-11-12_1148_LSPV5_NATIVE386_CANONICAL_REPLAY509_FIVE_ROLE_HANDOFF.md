# LSPV-5/509 five-role handoff — parsed-state closure of archived /386

**Timestamp:** 2026-11-12 11:48 America/Los_Angeles  
**Status:** PROVED/RESTRICTED source-inspection theorem plus COMPUTATIONAL original-OS replay. P2-D1, P2-C3, P2-B1 and separate P2-B2/B3 remain OPEN. P versus NP remains OPEN.

## Result

For every packet accepted by the pinned complete archived `/386` CLI, `JSON.stringify(JSON.parse(bytes)) + "\n"` is accepted with the same SOURCE, DEF-view, Resolution, record and paid counts. Raw diagnostic SHA changes, so this is acceptance/cost closure, not raw-output equivalence and not RFC 8785 JCS.

The unchanged checker was run in 40 fresh OS-Node subprocesses: 15 accepted raw/canonical pairs and five rejected hostile raw/canonical pairs. There were zero verdict mismatches and zero paid mismatches; eleven pairs were byte-distinct. The canonical `/508` packet is 3,701 bytes, SHA-256 `da0f8b040ec99787f7f47669203819134b7cabd7eaf23706ef82ab36f3d97070`, and accepts at W39.

## Artifacts

- Report: `research/agents/lspv-5/2026-11-12_1148_LSPV5_NATIVE386_CANONICAL_REPLAY509.tex`
- Reproducer: `experiments/review/lspv5_509_native386_canonical_replay.cjs`
- Raw: `results/raw/review/2026-11-12_1148_LSPV5_509_NATIVE386_CANONICAL_REPLAY_RAW.json`
- Canonical accepted packet: `results/raw/review/2026-11-12_1148_LSPV5_509_NATIVE386_CANONICAL_ACCEPTED.json`

## Role handoff

- **LSPV-1 (Route B):** formalize the equivalence relation as checker-observational equality, explicitly excluding the diagnostic raw SHA and external source-byte authentication.
- **LSPV-2 (Route A):** make every proposed `/386` normalization operate on parsed state and test order-sensitive composition against `/580`; do not claim raw-token rejection is historical.
- **LSPV-3 (Route B):** repeat the closure audit for pinned `/341`, including invalid-UTF-8 replacement aliases and typed support/table permutations; keep the sibling grammars separate.
- **LSPV-4 (Route A):** charge raw parsing, canonical serialization and output bytes separately from logical paid work and fixed-DAG retention proxies.
- **LSPV-5 (Route B):** seek one accepted `/341` packet whose canonical reserialization flips verdict or cost; if none exists, prove the analogous scoped theorem and concretely replay it.

CEGAR rule: every canonical cheap path must be replayed. Accepted paths are genuine and cannot be refined away. Only a concretely rejected path is spurious.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.**
