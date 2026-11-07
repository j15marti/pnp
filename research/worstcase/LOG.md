# Living log: worst-case derivation complexity W_R(N)

Status: P versus NP remains OPEN. Lower bound on W_R and the bridge SAT in P => W_R poly are OPEN.

## 2026-11-07 run 0001 (report: research/agents/claude/2026-11-07_1400_CLAUDE_WORSTCASE-0001.tex)
- CORRECTION: only the universal statement holds (superpoly W_R for EVERY proof system R <=> NP != coNP, Cook-Reckhow). For a single fixed R, superpoly W_R is just a proof-size lower bound for R (open for Frege/EF) and does not by itself separate P from NP. Earlier draft claiming otherwise is FALSIFIED/RETIRED.
- PROVED/EXACT: free optimal sequence = nondeterministic measure; max-min >= min-max, so lower bounds on W_R are stronger than uniform-solver lower bounds.
- PROVED/EXACT: the bridge is non-vacuous only if cost_R is NOT proof-length. Two failure modes: (a) free semantic steps make W_R = O(1) (retired "free SAT answer"); (b) charging steps by work with poly-time-checkable local rules reduces to case (proof system).
- KNOWN THEOREM / CONDITIONAL: for fixed R=Frege/EF, "P=NP => R poly-bounded" is an optimality-type claim; Krajicek-Pudlak: optimal proof system <=> fast consistency prover, open. No unconditional route known.
- KNOWN THEOREM (lit. check): best unconditional Frege size lower bound is still quadratic (Omega(n^2)); no superpoly EF bound as of this search.
- Hard-family testing against RES/PC/shared DAG/circuit compression: not done this run (next).
- Next: (1) define a cost with work-charged *non-verifiable* state compression and test whether the bridge is then provable; (2) hypergraph hard families vs resolution width (Ben-Sasson-Wigderson) as sanity floor.
