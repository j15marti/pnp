# LSPV-5 BOUNDARY-ORACLE-FACTOR128 | cumulative gap and rejection handoff

Date: 2026-10-24 21:48 Asia/Seoul. **P versus NP OPEN. ARC-EDGE-90 OPEN.**

## New exact result

For every proper 3CNF `F`, every explicit Boolean support circuit `C` with nonempty support, and the proper-3CNF compiler in the report,

`SAT(H(F,C)[b]) = C(b) AND SAT(F)` and `SAT(H(F,C)) = SAT(F)`.

For every deterministic adaptive controller over the pinned-membership service, the exact transcript is simulated by evaluating `C` on each query and reading/caching `SAT(F)` at most once. This is **PROVED/EXACT in the declared construction/service model**. It does not compute that source bit cheaply.

The supported child retains every source clause, so its ordinary encoded length is `N^(1+o(1))` for linear-size `C`; `lambda=1` and no strict ARC exponent contraction follows.

## Peer audit

- **Role 1 ROOT-HARD-PROJECTION129:** accepted after independent rederivation. This handoff generalizes its threshold support and two-element quotient to arbitrary explicit nonempty support circuits and an all-controller transcript theorem.
- **Role 2 TREE-AFFINE-JOIN122:** accepted only for the certified singleton-interface affine/tree language. It is a constructive polynomial upper bound and hostile control, not all-input coverage.
- **Role 3 LAZY-PIN-SOURCE93:** its source-indexed generator and source-name pin flattening are accepted in the direct-copy calculus. The exact ordinary length increases, so a short source-backed handle is not a power-shrunk child.
- **Role 4 PAD-FLOOR-SCOPED87:** accepted for valid closed scoped streams. Padding repairs a lower length floor conditionally; it cannot shrink the exponent-one continuation here or supply normalization/gluing.

## Rejection ledger increment

**FALSIFIED/RETIRED as standalone ARC progress measures:** support cardinality, density, Hamming connectivity, component count, ANF degree, and the number of individually source-complete pinned boundary decisions. All can coexist with a source-hard root while the entire answer vector factors through one source bit.

**Still OPEN:** an all-input same-machine successor, genuine `lambda<1` ordinary children, exact parent gluing, paid discovery/normalization, and a cofinal finite route into the verified FLMV region. The historical cosine endpoint remains retired. The original HEREDITARY-SCOPED10 executable remains unrecovered.

## Adaptive/resource ledger

State begins with read-only `F`, explicit `C`, no label, and all representation switches legal. Every query pays to evaluate `C`. Unsupported points answer zero. The first supported point invokes the full source decision and caches one bit; later points reuse it. Count primitive work, source/work reads and writes, unchanged writes, complete-state flips, peak writable bits, cumulative bit-time and program/representation size separately. UNSAT yields the constant-false boundary relation; SAT yields `C`. No label oracle, witness compilation or mandatory enumeration is assumed.

## Reproducibility and coverage

Auditor: `experiments/boundary_oracle_factor128.py`, seed 128, SHA-256 `6b0485e369444d53ee66e27257e07f1c2952a3faa0d078993be481d5c18d15ca`.

Finite audit: 310 bases, 1,860 constructions, 17,520 exhaustive boundary checks, 9,300 adaptive transcripts/203,100 queries, 301,304 assertion-accounted checks, zero failures. Controls include affine/XOR, Horn, dual-Horn, padded 2SAT, components, all signed three-variable clause subsets and random sources. Finite evidence is **COMPUTATIONAL** only.

Directly read this run: current root `main.tex`, `main13.tex`, AGENTS.md, CODEX.md, repository skill/protocol, full current Role 1/2/3/4 reports listed above, Role-5 prior 127, and bounded HEREDITARY/boundary searches. The inherited pinned 3,532-file hash/keyword crawl was not rerun or represented as complete mathematical reading. Historical main2--main12, broad Drive LOG/BOOL/SIL pagination and revisions remain partly unread. Local preflight failed because no checkout exists. Primary sources: FLMV JACM 2005 and Darwiche--Marquis JAIR 2002.

## Next target

Demand an exact service whose answer vector has more than one independent source semantic bit, whose ordinary children have verified exponent `lambda<1`, and whose parent gluing is all-input and same-realization. Test one-call source reconstruction before treating it as amplification.
