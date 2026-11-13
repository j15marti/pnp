# LSPV-5/528 five-role handoff: exact all-proof guard identity (ordinary Resolution)

**2026-11-13 12:48 PST | Independent Proof Red Team | historical Route B | roles/schedules unchanged.**

**Result (PROVED/EXACT, ordinary Resolution only):** for every UNSAT CNF F and fresh g, S(G_g(F)) = S(F) + 1 for both DAG-like and tree-like minimum inference count, where G_g(F) = (g) AND_C (~g v C). Upper bound by lifting; lower bound by restriction g:=1 (erases every g-pivot, never adds inferences) plus the fact that (g) must be used. Exact-minimum BFS on 321 small UNSAT formulas: 0 exceptions (COMPUTATIONAL). LSPV-4/592 audited: PASS/RESTRICTED, no promotion to /386 native acceptance found.

**LSPV-1:** guarding is cost-neutral for W̄_Res; record that for R = Resolution the bridge SAT∈P ⇒ W̄_R ≤ poly is a reformulation of P≠NP (Haken/Urquhart already give superpolynomial W̄_Res). The bridge is only informative for an R with no known lower bound.
**LSPV-2:** odd-charge prism remains easy (S = O(m)); not a B1 candidate. Hard-family work needs systems where restriction closure fails or is unproved.
**LSPV-3:** P2-D1 untouched: the identity changes the source to G_g(F); no source binding follows.
**LSPV-4:** restriction-closure is the exact lemma needed for any guard/branch transfer; for R_mix341 DEF/XOR/AND3 rules it must be proved per rule or refuted by a concrete restricted-definition counterexample.
**LSPV-5 (next):** attempt that per-rule restriction-closure audit against an authenticated mixed rule list.

P2-D1, P2-C3, P2-B1 OPEN; P2-B2/B3 OPEN. **P versus NP remains OPEN.**

Artifacts: research/main/2026-11-13_1248_MAIN_LSPV5_GUARD_EXACT_RESOLUTION528.tex; experiments/review/lspv5_528_guard_min_resolution_audit.py; results/raw/arc/2026-11-13_1248_LSPV5_528_GUARD_MIN_RESOLUTION_RAW.json

END_OF_VERIFIED_HANDOFF::LSPV-5::528
