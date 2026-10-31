# LSPV-4 ARC-XOR-INDEX-RESET281, five-role handoff
**31 October 2026, 13:36 PDT.** Status: **PROVED/EXACT restricted machine-operation theorem**; **COMPUTATIONAL source-backed finite controls**; **CONDITIONAL** FLMV/ARC. **P versus NP OPEN.**

## Central obstruction and exact correction
Fortnow, Lipton, van Melkebeek and Viglas (2005), Section 2.1, specify that an indexed jump erases the **entire contents** of the associated index tape in **one** native transition. An all-physical-tape bound `T >= sum(d_phys)/k` based only on at most one changed bit per tape is not valid on that actual machine unless atomic index erasures are separately charged. On disjoint checkpoint intervals, with fixed bit locations:
```
D_all <= q * T + E
D_ordinary_work <= q_work * T
E = total live index bits atomically erased by indexed moves
```
A loaded 16-bit all-ones input-index tape can lose all 16 bits on a **single** indexed input jump even with two total tapes. Loading those 16 bits cost earlier transitions. Ordinary work-buffer Hamming lower bounds remain sound. This corrects a **machine-model transfer**, not the user's explicitly qualified single-cell-write inequality.

## Exact same-source both-label control
For every valid Döcker duplicate-free monotone 3-SAT-(2,2) formula and either extreme full assignment `0^n` or `1^n`, one variable flip changes exactly **7 bits** of the fixed original-indexed *logical* state: assignment vector plus two-bit original clause counts plus one satisfied flag per clause. This result does not depend on the SAT/UNSAT answer. A one-bit lazy physical assignment mask need not maintain changed source-clause records; source scans to reconstruct them are charged.

## Falsifiers and computational data
F1 native full-tape popcount/k unmodified: **FALSIFIED** by 16-bit atomic erasure. F2 logical delta always implies that many physical writes: **FALSIFIED** by lazy mask. F3 endpoint XOR controls cumulative work: **FALSIFIED** by closed binary/Gray tours. F4 XOR completes hereditary ARC or improves exact FLMV envelope: **UNSUPPORTED**.

Matched valid targets Y6 SAT (20 models), U198 UNSAT (independently replayed 32-variable source block certificates and 64-row core), V198 SAT (198-bit checked witness). Independent verifier: **161,465 checks passed**, 1,152 closed-tour checkpoints, 34 indexed microsteps. DPLL Y6 SAT in 4 nodes, U/V UNRESOLVED at 1,200-node budget, not used as certificates.

| Source/order | Adjacent XOR = explicit work writes | Work head movements | Source literal probes |
|---|---:|---:|---:|
| Y6 binary | 648 | 2,958 | 1,560 |
| Y6 Gray | 512 | 2,942 | 1,560 |
| U198 binary | 3,096 | 492,847 | 203,544 |
| U198 Gray | 1,940 | 330,655 | 203,544 |
| V198 binary | 3,108 | 492,847 | 203,544 |
| V198 Gray | 1,942 | 330,655 | 203,544 |

All endpoint XORs = 0 for the closed tours. Initial materialization, full XOR scanning and guest work are accounted for separately, and this offline updater is **not a native FLMV SAT solver**. Y uses 46 counted cells; U/V use 1006. Source signed-occurrence S/U target/inverse, four-way pair compatibility, coherent endpoints and multi-flip trails are retained in the full raw archive.

## Exact FLMV values and transfer
`d*(6/5)=23/45`; `d*(241/200)=11642479/23232400`. Unique maximizing k=2, exact tail k>=4 bounded strictly by c^-4. The same-machine quantitative SAT-to-Döcker reduction, all-valid-target hereditary compression, malformed input handling, physical child indexed bit accessor, resets, source and retained space remain **OPEN**. NP-completeness alone transfers no numerical exponent.

## Duplication, searches, primary references
Prior project's issue #3 XOR ledger, LSPV-5 BLOCK-DISTANCE-FIREWALL184, LSPV-3 PAIRED-HAMMING-WALL243 and LSPV-4 ARC-VIRTUAL-DELTA-SAME-SCALE112 already contain related restricted Hamming statements. This run's correction is specifically FLMV Section 2.1's *atomic index erasure* when extending a bit-write bound to ALL physical tapes. Primary literature: https://lance.fortnow.com/papers/files/tst.pdf and https://arxiv.org/abs/1912.08032; project and OpenAI GitHub connector searches and web searches performed. The skill preflight script could not execute because this sandbox lacked a GitHub network checkout (DNS unavailable); GitHub connector sources were read instead. No novelty follows from failed queries.

## Published artifacts / fallback
- Full shorter `.tex` proof: `research/agents/lspv-4/2026-10-31_1336_LSPV-4_ARC_XOR_INDEX_RESET281_PUBLIC.tex`
- Executable compact checker: `experiments/arc/lspv4_281/arc_xor_reset281_compact.py`
- Source-indexed result summary with raw SHA-256: `results/summaries/arc/2026-10-31_1336_LSPV4_ARC_XOR_INDEX_RESET281_summary.json`
- Full local 5-page PDF, 20 KB TeX, complete producer and independent verifier, 4.47 MB raw source-indexed JSON, 512 KB checkpoint traces, source fixture and SHA-256 manifest in `ARC_XOR_INDEX_RESET281_COMPLETE_REPRO.zip`. Container-path Library upload returned `container_session_unavailable`, so full raw GitHub mirroring is **pending** and this subset is the documented fallback.
- Coordination: `https://github.com/j15marti/pnp/issues/3`.

**LSPV-1**: enforce exact machine quantifiers and input-index semantics. **LSPV-2**: instrument actual child-output/index-erasure events and inherited child tapes. **LSPV-3**: compare charged U198/V198 label-discriminating controller paths, not endpoint popcounts. **LSPV-4**: native FLMV guest simulator and source-to-target bit accessor, charging bulk erase correctly. **LSPV-5**: independently audit code and refute any uncharged shortcut. All five existing identities and schedules unchanged.

**Next proof obligation:** a uniform all-valid-target, both-label-correct hereditary adaptive compiler with full indexed FLMV transition/space accounting and quantitative SAT-to-target transfer. **P versus NP OPEN.**
