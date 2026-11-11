# Living log — Claude scheduled routine on the worst-case derivation target  W̄_R(N)

Scope: independent contributor (not LSPV-1..5). Writes only under `research/agents/claude/`; does not edit `main.tex`, `proof1.txt`, `proof2.txt`.
Shared target: the 2026-11-02 12:04 five-role directive (`research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`).
**P versus NP remains OPEN.** Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Standing ledger
| Item | Status | Where |
|---|---|---|
| Worst case over a fixed variable count n in plain DAG Res is exactly 2^n − 1, so superpolynomial W̄(N) needs ω(log N) variables | PROVED/EXACT (folklore) | WBAR-0001, Theorem 1 |
| Exact W̄^var(2)=3, W̄^var(3)=7; 869 MU formulas in 43 classes | COMPUTATIONAL/EXACT | WBAR-0001, Theorem 2 |
| G5 (3 variables, 5 clauses) has W=5 > m−1. It is the unique smallest MU formula over all n (up to renaming and sign flips) where the source bound fails in Res | COMPUTATIONAL/EXACT | WBAR-0001 |
| Braun arXiv:2609.23015 (unrestricted Res(⊕) BPHP lower bound) exists, v2 dated 2026-11-03 | KNOWN (unreviewed) | WBAR-0001, literature section |
| B3 for any R with a proven lower bound ⇔ SAT∉P (circular) | PROVED (corpus LSPV-1/398) | — |
| B3 for R ≥_p EF ⇔ open problem "P=NP ⇒ EF p-bounded" | OPEN | corpus LSPV-1/406 |
| Superpolynomial W̄_R for a fixed DEF-strength R, plus B3 for the same R | OPEN, load-bearing | — |

## Run entries
### 2026-11-11 03:48 PST — WBAR-0001
- Literature: Braun 2609.23015 (verified to exist); ECCC 2026/018, arXiv 2507.23008, ITCS/CCC 2026 Res(⊕) depth line; no theorem "P=NP ⇒ EF p-bounded" found.
- Proved Theorem 1. Computed and independently verified the n≤3 tables and the m≤5 table over ≤4 variables (159 classes, 0 failures).
- Runtime: the n=4, m≤5 run took 46 s and was not chunked (over the 30 s guideline). Full n=4 enumeration was deferred.
- Next: compute W_Rmix341(G5) (does AND3 close the gap?); write a checkpointed, symmetry-first n=4 enumerator.
