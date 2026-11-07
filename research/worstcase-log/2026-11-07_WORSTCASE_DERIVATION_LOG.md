% WORSTCASE LOG::2026-11-07
# Worst-case derivation-cost programme: living log

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); priority bridge SAT in P => W_R(N) <= poly(N).
**P versus NP remains OPEN. Nothing below is a lower bound.** Free choice of the optimal derivation is allowed (search is not charged), so W_R is a *non-uniform proof-size* measure.

## Entry 2026-11-07 (single run, all five roles collapsed into one session)

### 1. Bridge audit (PROVED/EXACT, elementary)
For sound, complete, poly-time-verifiable R (a Cook-Reckhow system):
- (a) Bridge(R) is *equivalent* to the implication "W_R superpolynomial => SAT not in P". With free strategy choice, W_R is exactly the proof-size function p_R(N), so Bridge(R) is the statement "P=NP => R is polynomially bounded".
- (b) Since R is polynomially bounded iff NP=coNP *for that R* (Cook-Reckhow), and P=NP => NP=coNP, some system is poly-bounded under P=NP, but **a fixed R is not forced to be**. So the bridge is not free; it is a nontrivial property of R.
- (c) Therefore "prove W_R superpoly for fixed R" already yields NP != coNP only for R's simulating class, and yields P != NP only via Bridge(R). Bridge(R) is the load-bearing OPEN arrow.

### 2. When Bridge(R) is known (KNOWN THEOREM, Cook 1975 / Krajicek-Pudlak, from memory; unverified against primary text this run)
Bridge holds in the *conditional* form: if SAT has a poly-time algorithm A whose correctness is provable in PV (equivalently in bounded arithmetic), then Extended Frege has poly-size proofs of every UNSAT F (translate PV proof of "A correct" plus the trace of A on F). So:
 **Bridge(EF) holds for P=NP witnessed by a provably-correct algorithm.** Removing "provably correct" is exactly the gap. This is CONDITIONAL, not the unconditional bridge asked for.
Levin-style universal search does not fix it: a universal "run program e" system is unsound for wrong e, and soundness of the true e* is not feasibly provable.

### 3. Consequences for hard-instance design (CANDIDATE guidance)
- Any fixed weak R (resolution, Res(k), PC, cutting planes, bounded-depth Frege) has *known* superpoly/exponential lower bounds (Haken, Ben-Sasson-Wigderson, Tseitin on expanders, PHP) yet SAT-in-P is not contradicted: Bridge fails for them (they are provably not poly-bounded unconditionally, so Bridge(R) for those R would already prove P != NP — evidence Bridge is false for weak R, or at least cannot be proved). **So the bridge can only be targeted at R strong enough to simulate PV-reasoning, i.e. EF-like**, where lower bounds are unknown (only linear/quadratic known).
- "Shared DAGs, adaptive switching, circuit compression" push R toward EF / Frege; the hardness candidates then inherit the open status of Frege lower bounds. Reduced-state/min-work over multisign hypergraph DAGs is a proof-size measure and inherits natural-proofs / relativization-style audits (not yet performed here).

### 4. Open arrows
1. Bridge(R) for R=EF without provable-correctness hypothesis: OPEN.
2. Superpolynomial W_EF(N): OPEN (best known lower bounds are linear/quadratic).
3. Red-team: none of the proposed hypergraph hard families has been shown to resist EF; no shorter-derivation counterexample searched this run (no code run).

### 5. Literature check (this run)
Search found no 2025-26 Frege/EF superpolynomial breakthrough; best known EF lower bound still linear; Filmus-Pitassi-Santhanam: exponential AC0-Frege lower bounds on suitable formulas imply superpoly Frege bounds; Lu-Santhanam-Tzameret (ITCS 2026) gives only conditional AC0[p]-Frege hardness. Unverified secondary listing mentions arXiv:2507.23008. Primary sources not yet read: check ECCC/arXiv before relying.

### 6. Next steps
- Formalise Bridge(R) <=> p_R poly under P=NP, then state the weakest hypothesis H ("PV proves A correct") and test whether any weaker reflection principle suffices.
- Prioritise audit of whether a multisign hypergraph DAG measure is simulated by/simulates EF (determines which known lower-bound technique, if any, applies).
% END_OF_WORKLOG::2026-11-07
