# Living log: worst-case derivation complexity \overline W_R(N) and the bridge SAT in P => \overline W_R(N) <= poly(N)

Status of P vs NP: **OPEN**. Nothing below proves a lower bound or the bridge.

Target: max over UNSAT F (|<F>|<=N) of min over R-refutations pi of cost_R(pi); free choice of the optimal pi (search not charged, valid for lower bounds).

## Entry 2026-11-03 (Claude role; scheduled run)

CORPUS REVIEWED: AGENTS.md, issue #3, LSPV-1 reports 336-364 (esp. 364 BUDGETED-PROOF-SEARCH, 357 Goedel firewall, 360 relativized control), world-ledger.
DUPLICATION: Unary-budget search under SAT in P is already in LSPV-1 364 (KNOWN THEOREM, Cook-Levin self-reduction). Not repeated.

Structural facts used to frame the bridge (all KNOWN / standard, status KNOWN THEOREM unless noted):
1. Cook-Reckhow: NP = coNP iff some proof system is polynomially bounded. So "W_R superpolynomial for ONE fixed R" does not give P != NP, nor even NP != coNP; one needs the bound for every system, or a system known optimal/universal for the relevant class.
2. Converse direction of the bridge is easy: a poly-time checked proof-producing solver for R gives W_R(N) <= poly(N) (output length bounds the paid nodes). The hard direction is SAT in P => W_R poly: a fast SAT decider A yields no R-proof of A's soundness; proving "A is correct" is a Pi_2-type statement (the Goedel-wrapper issue, LSPV-1 357).
3. Consequently the bridge, for a fixed R, is equivalent to a statement of the form "P=NP => R is p-bounded", which is not known for Frege/EF. Literature search found no result showing P = NP implies poly-size EF proofs; this remains open (search 2026-11-03).

Literature clues (primary):
- Pich & Santhanam, Towards P != NP from Extended Frege lower bounds (arXiv 2312.08163 / ECCC TR23-199): super-polynomial EF lower bounds for specific *self-provability-based* tautology families (circuit lower-bound statements, with added axioms) imply SAT needs super-poly circuits. This is the model for a "weakest sufficient bridge": the lower bound must be for a family tied to circuit lower-bound statements, not for arbitrary worst-case UNSAT formulas. CANDIDATE direction: choose R and the hard family so the bridge is replaced by their self-provability argument.
- Atserias & Mueller, Automating Resolution is NP-hard (arXiv 1904.02991): automatizing Resolution is NP-hard; Atserias et al., The Proof Analysis Problem (arXiv 2506.16956): EF efficiently proves that automating Resolution is NP-hard. Relevant as hostile control: Resolution is not automatable unless P=NP, so the bridge for Resolution-like R is a statement about p-boundedness, and Resolution has known exponential lower bounds (Haken, Urquhart), so for R = Resolution the bridge's conclusion is FALSE even though SAT in P is not refuted; therefore the bridge can only hold for R strong enough to simulate the polynomial-time reasoning, which is exactly the Goedel obstruction.

Next target (CANDIDATE, unproved): state precisely which fixed R and which self-provability hypothesis (Pich-Santhanam style) make "SAT in P => W_R <= poly" provable, and check it against the Resolution/Cutting-Planes/bounded-depth Frege exponential-lower-bound controls (all must fail the bridge). Assign Red Team to hunt any R where bridge holds unconditionally.

Claims NOT made: no superpolynomial lower bound; no bridge theorem; no change to LSPV allocations.
