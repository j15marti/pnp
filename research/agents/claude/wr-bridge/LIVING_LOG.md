# Living log: worst-case derivation directive (Claude scheduled runs)

Append-only. Statuses: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## 2026-11-11 WR-BRIDGE-0001
- Report: `research/agents/claude/2026-11-11_CLAUDE_WR-BRIDGE-0001.tex`
- PROVED/EXACT: Bridge(R) := [SAT in P => W_R(N) <= poly(N)] is equivalent to [P=NP => R p-bounded].
- PROVED/EXACT: for any R with a known superpolynomial lower bound (Res, PC, CP, AC0-Frege), Bridge(R) is equivalent to P != NP, so it is not a "weaker" target.
- PROVED/EXACT: the bridge gets easier and the lower bound harder as R gets stronger; the two meet only at Frege/EF and beyond, where both are OPEN.
- KNOWN THEOREM: P=NP via an algorithm with PV-provable soundness => EF p-bounded (Cook 1975; Krajicek-Pudlak 1989). Without the provability condition, OPEN.
- CANDIDATE: use random 3-CNF at constant density as the hard family; Tseitin (GF(2)) and PHP (counting) are negative controls.
- COMPUTATIONAL: tiny-instance width-vs-algorithm controls in `width_vs_algorithm_results.jsonl`; not asymptotic.
- Next target (OPEN): find the weakest *algorithm-class* restriction C such that "SAT in C-time => EF/Frege-proofs of poly size" is provable, i.e. identify which deciders have R-simulable traces.
- P versus NP: OPEN.
