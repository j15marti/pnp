# LSPV-5 REFEREE399 handoff — 2026-11-06 18:50 PST

Status: KNOWN THEOREM plus PROVED/EXACT distribution port; full historical `R_mix341` transfer, [P2-B1], [P2-B2], and P versus NP OPEN.

Affected tracker IDs:

- [P2-F8]: established density-six indexed random proper 3-CNF anchor retained.
- [P2-F9]: new same-family PC/PCR theorem and reproduction-port ledger.
- [P2-B1]: gap narrowed to a polynomial backtranslation covering every additional historical native rule; status remains OPEN.
- [P1-01], [P1-03], [P1-04]: reviewed, no material change.

Exact advance:

1. Alekhnovich--Razborov Corollary 4.7 gives degree (Omega(n)) for the same iid-with-replacement density-six proper 3-CNF family in PC over every field.
2. Impagliazzo--Pudlák--Sgall Theorem 5.2 turns this into (exp(Omega(n))) nonzero-monomial size.
3. Galesi--Lauria Theorem 2 gives (>2^{n^{1-o(1)}}) size in bounded-DNF (mathrm{PCR}^{q}), characteristic not two, for (q=o(sqrt{log n/loglog n})).
4. CNFgen samples without repetition. Conditioning the published iid distribution on no collision gives the CNFgen distribution, with total-variation distance at most
   [
   inom{6n}{2}/(8inom n3)=O(1/n).
   ]
   Hence all w.h.p. properties transfer asymptotically. Individual generated formulas are not thereby certified UNSAT or hard.

Evidence:

- `research/main/2026-11-06_1850_MAIN_RANDOM3CNF_PCR_PORT_REFEREE399.md`
- `experiments/review/lspv5_399_random3cnf_port_check.py`
- `results/raw/review/2026-11-06_1850_LSPV5_RANDOM3CNF_PCR_PORT399.json`
- 49,235 checks passed; four corruptions rejected.

Next obligation: prove a polynomial lower-bound-preserving simulation from every legal historical `R_mix341` proof DAG to a calculus covered by [P2-F9], or exhibit an authenticated native shortcut. Do not infer that separate or bounded-subsystem lower bounds survive arbitrary interleaving. B3 remains a separate same-calculus implication.

