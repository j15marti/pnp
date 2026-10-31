# LSPV-1 ARC-PARITY-EXPOSURE270: five-role integration
Date: 2026-10-31 05:00 PDT. P versus NP OPEN. Do not alter five task identities, offsets or enabled status.

## Exact result and falsifiers
The source-authenticated canonical proper 3CNF F(m,b) consists of two-clause XOR transition constraints properized with one shared z and two four-clause negative pins forcing x_0=x_m=0. With m transition bits b_i, F is SAT iff parity(b)=0; each SAT source has exactly 8 models and each UNSAT source has none. All clauses are proper width 3. Child H7-dup is SAT (1 model); H8 is UNSAT. Select the constant-size ordinary child by parity to preserve *both* source labels. Every physically serialized source bit depends on at most one b_i, so cold deterministic source-bit query depth is exactly m. A source-authenticated scan + one-bit parity cache avoids an unsound q*m repeated classification tariff. This is a restricted, easy promise language, NOT a general SAT lower bound or all-input ARC edge.

Four falsifiers: no cold fewer-than-m bit-query decision; no mandatory q*m cost after caching; physical child correctness needs a separate paired SAT/UNSAT proof; no general arbitrary-A hardness transfer from the promise family.

## Verification and accounting
Producer and independent checker (two Python programs) PASS: 126 complete same-source signed instances, 63 SAT and 63 UNSAT, m=1..6, 8,859 independent assertions, ASCII-bit minimax depths 1..6, and 4 detailed adverse originals containing 312 occurrences and 5,488 clause-pair extreme-mode tests. Every original occurrence local S/U/inverses, both 0^n and 1^n, literal-count 0/1/2/3 bins, complement checks, intermediate flip paths, source-proved resolvent cubes, full witness enumeration and ordinary child labels were checked. Baseline UP-DPLL 1,479 search nodes; aggregate selected host events baseline 258,928, recognizer+child+guest 104,058. These units do not represent native FLMV bit-tape time or peak writable space. Discovery/recognition and source reads are paid once. Selected policy switching and failed alternative trials = 0 on this fixed grammar; all nonmembers require a fully charged total SAT fallback.

Raw machine-readable results (571,094 UTF-8 bytes, SHA256 bc57703693ed8c69b826004a8676cc768d9a1fc64a9b3501c624376f9f109973), exact producer and independent verifier are published to GitHub and read back. 

## Hand-off by existing role
LSPV-1: Maintain quantifier contract and same-source SAT/UNSAT polarity proofs; combine the cold source-query lower bound with the legal single-bit cache when reviewing compiler claims.
LSPV-2: Test whether physical bit-level child access can be achieved when the source *cannot* be recognized and classified cheaply; charge prefix index, header count and every guest query.
LSPV-3: Use signed renamings, proper affine grammar and structural easy families as controls for selectors. Report label-recognition cost separately from result output.
LSPV-4: Recheck both labels and native FLMV indexed-source model. No cold per-read q*m multiplication when a paid source summary persists. Keep exact d*(c) margins.
LSPV-5: Red-team source-index-only promise, parity cache, child serializations, DELAY wrapper, same-source correctness, and all-input quantifiers. Do not promote this restricted control to unrestricted SAT hardness.

## Single still OPEN arrow
A single uniform hereditary source-authenticated Phi(A) on ALL ordinary SAT inputs, for arbitrary fixed correct uniform A with UNKNOWN finite K,L, preserving YES and NO and realizing K'<=max(11/10,3/5+K/2) and L'<=max(1/2,L/2), including all discovery/policy switches/failures, source tapes, real shorter children, guest accesses and peak simultaneous retained space. No such Phi exists in published project results. P versus NP OPEN.

Report: research/agents/lspv-1/2026-10-31_0500_LSPV-1_ARC_PARITY_EXPOSURE270.tex
Producer: research/agents/lspv-1/2026-10-31_0500_LSPV1_ARC_PARITY_EXPOSURE270_producer.py
Checker: research/agents/lspv-1/2026-10-31_0500_LSPV1_ARC_PARITY_EXPOSURE270_independent.py
Raw: results/raw/arc/2026-10-31_0500_LSPV1_ARC_PARITY_EXPOSURE270_raw.json
