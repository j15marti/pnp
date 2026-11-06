# Living log: worst-case derivation cost (append-only)

## 2026-11-06 WCDC-0001
- Created directive + report `2026-11-06_WCDC-0001.tex` (theorems T1-T5, red-team table).
- Result: bridge B(R) is tautologically equivalent to P != NP for every R with a known unconditional lower bound
  (Resolution, CP, bounded-depth Frege). Non-trivial only for Frege/EF; there it is equivalent to open problems
  (provable correctness of a SAT algorithm; optimal proof systems).
- Classical hard families (Tseitin, PHP) have poly-size EF/Frege proofs: they do NOT survive a strong fixed R.
- Feasible interpolation (the main source of unconditional bounds) fails for EF under factoring hardness (Krajicek-Pudlak), so
  the lower-bound lead has no known technique for the strong R.
- Literature (standard search, 2026-11-06): no 2026 breakthroughs found; optimal/p-optimal proof system existence still open
  (follows from NE=coNE / E=NE); arXiv 2506.16956 (Proof Analysis Problem for EF is NP-complete).
- Next target: (a) decide whether a *conditional-on-PV-provability* statement can be replaced by unconditional
  reflection for the specific hypergraph rule set; (b) time-space version: does SAT in P give poly (work,space) derivations?
- Status: OPEN. P vs NP not proved.
