# Living log: worst-case derivation complexity W_R(N)

Target: bar W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi).
Bridge: SAT in P  =>  bar W_R(N) <= poly(N).
**Status: P versus NP remains OPEN.** Nothing below is a lower bound proof. Entries are append-only.

## Entry 1 (2026-11-09) — formalization and the obstruction to the bridge

### Setup (all CONDITIONAL on the model choices stated)
R is a derivation system on 3-CNF (multisigned DAG-hypergraph states), each step checkable in time poly(|state|), and cost_R(pi) >= |pi| (number of steps). Then R is a Cook–Reckhow proof system and bar W_R(N) <= poly(N) iff R is polynomially bounded.

### Observation 1 (KNOWN THEOREM, Cook–Reckhow 1979): free choice of the optimal sequence is exactly nondeterminism.
Min over pi with no charge for finding pi is the proof-size measure of R. So a superpolynomial bar W_R is a superpolynomial *proof-size* lower bound for R. Not charging for search does not weaken the target. It is the standard proof-complexity problem and nothing easier.

### Observation 2 (PROVED/EXACT, short): what the unconditional lower bound buys.
- If R is a fixed natural system (resolution, Frege, EF, "resolution + algebra + shared DAGs") a superpolynomial bar W_R shows only that R is not polynomially bounded. It gives P != NP only if R is *optimal* (simulates every Cook–Reckhow system).
- If R is optimal: bar W_R superpolynomial <=> NP != coNP. This is strictly stronger than P != NP (NP != coNP implies P != NP, converse unknown).
- So the lower-bound half of the program, for any R whose bridge holds for free, is at least as hard as NP != coNP. Cheaper targets need a *non-optimal* R together with a real transfer theorem (below).

### Observation 3 (PROVED/EXACT): the bridge for optimal R is trivial but vacuous.
P = NP => NP = coNP => a polynomially bounded system exists => an optimal R simulates it => bar W_R <= poly. This needs an optimal system, which is not known to exist (Krajicek–Pudlak: existence implies consequences such as NE = coNE-type collapses; oracle results by Egidy–Glasser, STOC 2025).

### Observation 4 (CANDIDATE / OPEN): the bridge for a fixed natural R.
For R = EF the bridge needs: SAT in P => poly-size EF proofs of UNSAT. Failure mode: the SAT algorithm's correctness may not be feasibly provable in EF. Whether P = NP forces poly EF proofs is open. The weakest sufficient transfer theorem therefore is
 T-bridge(R): for every poly-time A deciding SAT, EF (or R) has poly-size proofs of "A rejects F => F unsat" for each instance family. R must prove its own soundness-of-A in the length-bounded form. This is a *reflection* statement, and it is exactly where known barriers (Razborov–Rudich style, bounded-arithmetic independence) sit. Classification: ANALOGY needing a new bridge; not established.

### Observation 5 (PROVED/EXACT): pointwise minimization over *algorithms* collapses.
If derivations are allowed to be arbitrary algorithms/traces and the min is per instance F, hardcoding gives cost O(|F|) for every fixed F, while the max over F of that min is again a proof-size measure. Costs must be charged to uniform objects or the quantity degenerates to nondeterministic complexity.

### Hostile-control checklist for any proposed hard family (for the red team)
Must survive: resolution (width/size), Nullstellensatz/PC/SoS, cutting planes, circuit compression of states, shared DAGs, adaptive switching between systems. Known: PHP, Tseitin on expanders, random 3-CNF are hard for resolution/PC/CP-type weak systems; no superpolynomial lower bound is known for Frege, so none of these families can be used for EF/optimal R.

### Literature clues checked this run
- Cook–Reckhow: polynomially bounded proof system exists iff NP = coNP.
- Egidy 2026 (arXiv 2602.02294) and "The Proof Analysis Problem" (arXiv 2506.16956): P = NP gives a polynomially bounded p-optimal system; related conjectures equivalent to NP != coNP / P != NP. Not read in full; statements above are from search snippets and unverified.
- Egidy–Glasser STOC 2025: oracle constructions for (p-)optimal proof systems.
Transfer class: useful structural analogy (2). No directly transferable lower bound found.

### Role assignments this cycle
- Lower-Bound Lead: decide whether any non-optimal R admits T-bridge(R) with a provable reflection step.
- Reduction Builder: specify R with poly-checkable steps; certify exact shortest DAGs on small N (brute force).
- Hypergraph/Certificates: candidate hard families vs the checklist.
- Resource Auditor: per-step cost accounting, DAG encoding size, peak memory; confirm cost >= |pi|.
- Red Team: attack Observation 2 and 5; seek an R where bridge holds and lower bound is plausibly cheaper than NP != coNP.

### Next target
Find R, not optimal, with (i) poly-checkable steps, (ii) T-bridge(R) provable from SAT in P, (iii) a lower-bound route not implying NP != coNP. Observation 2 suggests (ii)+(iii) together may be impossible for P-simulating systems; prove or refute that.
