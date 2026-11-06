# Worst-case derivation-cost programme — living log

**Target:** W_R(N) = max over UNSAT F, |<F>|<=N, of min over R-derivations pi of F |-_R ⊥ of cost_R(pi).
Charging nothing for *finding* the optimal pi is legitimate for a lower bound (search only adds work).
**Weakest bridge:** Bridge_R :  SAT ∈ P  ⟹  W_R(N) <= poly(N).
**Status: P versus NP remains OPEN.** Nothing here proves a lower bound or the bridge for any interesting R.

Roles: (1) General lower-bound lead, (2) SAT-circuit reduction builder, (3) hypergraph/proof certificates,
(4) time-space auditor, (5) red team. Entries are append-only, newest last.

## 2026-11-06 — run WORSTCASE-0001 (report: `2026-11-06_WORSTCASE-0001.tex`)
Literature check (standard search; primary papers not re-read this run, so labels are KNOWN THEOREM *from memory/secondary sources*):
- Cook–Reckhow: a poly-bounded propositional proof system exists iff NP = coNP.  Not "iff P=NP".
- Automatizability of every propositional proof system is equivalent to P = NP (Buss slides). Hence the right
  object for "SAT∈P ⟹ short derivations" is a *fixed* system whose derivations include an algorithm's trace.
- No superpolynomial lower bound for Frege / Extended Frege known (Alekseev, ToC 22 (2026): exponential bound
  for the binary value principle in PC with extension rule, not for EF itself).
- Feasible interpolation fails for Frege/EF under crypto assumptions (Krajíček–Pudlák) -> circuit-based hard families cannot be certified by interpolation alone.
Results (proofs in the report):
1. **Bridge collapse (PROVED/EXACT):** if W_R is unconditionally superpolynomial (resolution, PC, bounded-depth Frege...) then Bridge_R ⟺ SAT∉P. So the bridge is informative only for R without known lower bounds.
2. **Provable-soundness bridge (PROVED/EXACT, CONDITIONAL on hypothesis H_T):** for the system R_T (derivation = algorithm e + T-proof that e's UNSAT answers are sound + its trace), SAT∈P *with T-provable soundness* ⟹ W_{R_T} <= poly. Only *soundness* of UNSAT answers is needed, not completeness.
3. **What a lower bound for R_T would give (PROVED/EXACT):** W_{R_T} superpoly ⟹ no polynomial-time UNSAT-refuter has a T-provable soundness proof. This is P≠NP only modulo "T proves soundness of every poly-time SAT algorithm that exists" — H_T cannot be dropped (quantifier order: R fixed before e*).
4. **Computational sanity (COMPUTATIONAL):** exact min DAG-resolution steps for the full 3-variable 3-CNF (8 clauses) = 7 (`min_res.py`); 71/71 irredundant random UNSAT 3-var 3-CNFs also 7. n=4 exceeds the 30 s budget in BFS form; needs chunking.
Red-team note: the lower-bound side (superpoly W_{R_T}) is exactly as hard as P≠NP restricted to provably-sound algorithms; no progress on hard families. Next: (a) classify which reasoning systems satisfy H_T for T=PV/S^1_2 (Cook's theorem gives EF-simulation of PV-provable polytime algorithms — verify against primary source); (b) chunked exact min-resolution for n=4 with symmetry reduction; (c) multisign hypergraph DAG formal definition of "reduced state" as min peak clause-set size.
