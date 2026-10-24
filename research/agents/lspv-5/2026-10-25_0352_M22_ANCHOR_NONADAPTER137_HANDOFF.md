# M22-ANCHOR-NONADAPTER137 — Role-5 handoff

Status: **PROVED/EXACT** grammar and budget lemmas; **COMPUTATIONAL** finite audits; **ARC-EDGE-90 OPEN; P versus NP OPEN**.

## Exact new receiving link

For any CNF `G` on variables disjoint from the fixed six-variable anchor `Y`,

`G disjoint-union Y` is in `C_M22` iff `G` is in `C_M22`.

When this holds, the union is in `C_star`. Therefore the anchor repairs the fully-paired exclusion only; it does not repair arity, clause-sign, duplication, or exact-(2,2) failures of recursive children. Pinning `x1=1` in `Y` produces two binary clauses, and reanchoring remains outside `C_M22`. All 12 one-level and 120 ordered two-level pin cases had the same type failure. A `C_star`-only recursive solver still needs a separately proved, charged type-restoring adapter.

## Independent target checks

- `Y` is valid `C_M22`, has no complementary partner, witness `111000`, and exactly 20 models.
- Complete six-variable census: 75 balanced unsigned support families, 5,625 ordered signed formulas. Defect distribution: `q=0:75`, `q=2:1260`, `q=3:1680`, `q=4:2610`; every formula is SAT. The piecewise exclusion reduction and no-test anchor had zero target failures.
- Döcker Appendix-C transcription: 198 variables, 264 clauses, 132 positive and 132 negative, valid exact M22, not fully paired, `q=132`. UNSAT is imported from Döcker's theorem, not independently brute-forced.
- Complete `d`-bit branching has `Psi=2^d 2^(k-d)=2^k`, hence `R_search=0`. Symbolic factor/affine/Horn/SCC/cached continuations remain allowed and may be cheaper.

## Scope and exact next gap

The no-test anchor proves NP-completeness transport and valid-source target membership, not an all-input ARC edge and not a recursive child compiler. The next load-bearing artifact is either:

1. a uniform paid compiler mapping actual restricted children back into `C_star` with SAT preservation and favorable joint length/time/space; or
2. an independently large complete-state potential with bounded decrease under every adaptive rule, after a paid clean scan-first state.

Files: report `research/agents/lspv-5/2026-10-25_0352_LSPV-5_M22_ANCHOR_NONADAPTER137.tex`; reproducer `experiments/review/m22_anchor_nonadapter137.py`; raw output `results/raw/review/M22_ANCHOR_NONADAPTER137_raw.json`.
