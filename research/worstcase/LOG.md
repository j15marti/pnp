# Living log: worst-case derivation cost W_R(N)

## 2026-11-10 run 1 (Claude role)

Corpus note: repo search finds no earlier file defining W_R or a "multisign DAG hypergraph"; this log starts the line.
Closest prior material: `research/agents/claude/world-ledger/` (rows on equivalents of P=NP) and the proof-system items in the ARC/FLMV spine. Nothing here changes the ARC/FLMV allocation.

### Results

**E0 (PROVED/EXACT, trivial).** min over derivations with free strategy choice = shortest-proof size. So W_R is the Cook-Reckhow proof-size function; not charging for search is exactly the standard convention.

**E1 (PROVED/EXACT given definitions).** Let R contain EF-style substitution and circuit evaluation. For a SAT algorithm A running in poly time, let Refl_A(n) be the tautology
`(A_n(f)=0 and f(x)=1) -> bottom`
over variables f (the formula bits, |f|=n) and x. Then
  (B for R)  <=>  (SAT in P  =>  some correct poly-time A has poly-size R-proofs of Refl_A(n)).
(<=) Substitute the actual UNSAT F for f, evaluate the constant circuit A_n(F)=0 (poly many gate steps), then derive bottom from the clauses of F by case split over clauses (poly). (=>) If R is polybounded, every tautology, including Refl_A for a correct A, has a poly proof.
Meaning: the bridge is a statement about *feasible provability of correctness of a SAT algorithm*, not about circuits or hypergraph width.

**E2 (PROVED/EXACT, logic).** If W_R is already known superpolynomial unconditionally (resolution; PC; bounded-depth Frege; all KNOWN), then (B for R) is logically equivalent to "SAT not in P", because (A => B) with B false is not-A. So for these R the bridge is not a weaker target; it is the whole problem. The bridge only has independent content for R with open W_R (Frege, EF).

**E3 (KNOWN / FALSIFIED as a plan).** Pointwise simulation ("algorithm time T(F) implies R-proof size poly(T)") is FALSE for resolution (Tseitin on expanders: exponential resolution size, polynomial time by Gaussian elimination) and for bounded-depth Frege (pigeonhole: counting). Retired for those R. Any surviving hard-family claim must refute Gauss/counting/EF-style compression, not only resolution.

**E4 (barrier ledger, KNOWN, verify hypotheses before use).** Pich-Santhanam 2023 (arXiv 2312.08163) is reported to show: under hypotheses I-II, if EF is not p-bounded then P != NP; this is the literature form of (B) for EF. Pich-Santhanam 2021 / Li-Oliveira 2023: strong lower bounds are unprovable in T_PV / APC1 under assumptions, which warns against proving (L) by bounded-arithmetic reasoning. Krajicek-Pudlak: NE=coNE implies optimal proof systems exist; whether EF is p-optimal is open. NP=coNP iff some proof system is polybounded.

### Status
- (L) for EF/Frege: OPEN (no superpolynomial lower bound known for either).
- (B) for EF: OPEN; reduced exactly to E1 / Pich-Santhanam conditions.
- Multisign DAG hypergraph: no new theorem this run; it needs a definition mapping its "reduced state" to line-space and its work to size. Next run.
- P versus NP: OPEN. No proof claimed.

### Literature checked (2026-11-10)
Searches on EF polybounded / P=NP, and Pich-Santhanam follow-ups: surfaced arXiv 2312.08163, 2305.15235, 2404.11841 and survey material. No 2025-26 breakthroughs found. The Cook-Krajicek provability paper was not retrieved; cite from memory only after verification.

### Next
1. Read Pich-Santhanam 2312.08163 in full; record hypotheses I-II exactly.
2. Define the multisign DAG hypergraph formally and map reduced state to clause space.
3. Small-n exhaustive minimal-DAG computation for R = resolution with extension variables as a sanity table.
