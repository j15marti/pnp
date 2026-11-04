# Living log: worst-case derivation cost  W_R(N) = max_{F in UNSAT,|F|<=N} min_{pi: F |-_R bot} cost_R(pi)

Status of P vs NP: **OPEN**. Nothing in this log proves a lower bound. Entries are append-only.

## 2026-11-04 (scheduled run, Claude) — entry WORSTCASE-0001

### What was done
Surveyed repo: no prior artifact formalizes W_R (grep for "worst-case derivation", "multisign", "reduced logical state" finds nothing relevant). Formalized the bridge and audited it.

### Definitions
R a Cook–Reckhow system: poly-time verifier V(F,pi), sound and complete for UNSAT. cost_R(pi)=time(V)+|pi| (peak space tracked separately). min over pi is free (no search charge).

### Results (status: KNOWN THEOREM unless marked)
1. **Free optimal sequence = nondeterminism.** For poly-time-verifiable R, W_R(N) <= poly(N) implies UNSAT in NP, i.e. NP = coNP (Cook–Reckhow 1979). Conversely NP = coNP gives some p-bounded R. So "W_R poly for some R" <=> NP = coNP. Since P is closed under complement, NP != coNP implies P != NP: the program, if pursued for *all* R, targets a statement **stronger** than P != NP.
2. **Bridge is false for weak R (KNOWN).** SAT in P does not imply W_R poly for R = resolution, bounded-depth Frege, cutting planes etc.: exponential lower bounds are unconditional (Haken 1985; Pudlák 1997 CP; Ajtai/BIKPPW), yet SAT could still be in P (those systems just cannot formalize the solver's correctness). So the bridge `SAT in P => W_R <= poly` fails for every R with unconditional superpoly lower bounds, and a lower bound proven for such R carries no information about P vs NP.
3. **Bridge is trivially true for tailor-made R, and then circular.** R_M := "accepting run of poly-time decider M" gives SAT in P => W_{R_M} <= poly, but a superpoly lower bound for R_M is just SAT not decided by M. No progress.
4. **Bridge for a fixed R from Krajíček–Pudlák (PROVED from KNOWN THEOREMS, CONDITIONAL on the hypothesis).** P = NP => E = NE (padding) => NE = coNE => (K–P 1989) an optimal propositional proof system Q exists; P = NP also gives a p-bounded system, so Q is p-bounded: W_Q <= poly. Hence `SAT in P => W_Q <= poly` holds for the K–P optimal system Q — but Q is only *defined* (as a verifiable system) under NE = coNE, and W_Q superpoly <=> NP != coNP (given NE = coNE). So this is an exact **reformulation** (equivalent to NP != coNP in that world), not progress. Existence of optimal / p-optimal systems is itself open; it is NOT known unconditionally (relativization results, Messner; Köbler–Messner–Torán).
5. **Consequence for the plan (CANDIDATE conclusion).** Any R for which the bridge is provable is either (a) optimal-like, making the lower bound equivalent to NP != coNP, or (b) provably weak, making the bridge false. A usable intermediate must be a *natural* strong R (Extended Frege / Frege) for which "P = NP => R p-bounded" holds: this is the open statement "P = NP implies EF is p-bounded" (related to provability of P = NP in bounded arithmetic; Cook–Krajíček; Krajíček 2019 book). Proving it, or its contrapositive route, is the **single weakest-bridge obligation**. No lower bound for EF/Frege is known (not even for random 3-CNF in Frege).

### Hard-instance survey (for Hypergraph & Proof-Certificate role)
Candidates must survive: resolution (width/size, Ben-Sasson–Wigderson), algebraic (PC/Nullstellensatz degree), CP, shared-DAG compression (Frege vs treelike), circuit compression (EF). Known hard for weak systems: PHP, Tseitin on expanders, random k-CNF, Clique-coloring. All admit poly-size EF proofs or have no known Frege lower bound — so none yields a lower bound for a system satisfying the bridge.

### Time–space audit
Cost model must be fixed to RAM/TM matched model; peak memory of verifying a DAG derivation is O(#nodes) naively, can be tree-unfolded with blow-up (Frege DAG vs tree). Space lower bounds for resolution (Ben-Sasson–Nordström) are unconditional but again for weak R.

### Red-team verdict
The "free optimal sequence" step is legitimate for lower bounds but converts the problem to NP vs coNP (item 1). The cleanest failure mode: choosing R weak (bridge false) or R optimal (reformulation). Open arrows: (A) P=NP => EF p-bounded; (B) any superpoly Frege/EF bound. Both OPEN.

### Literature check (this run)
Krajíček–Pudlák 1989 (NE=coNE => optimal system; E=NE => p-optimal); Köbler–Messner–Torán (NEE/EE refinements); Messner (coNE-hard sets lack optimal systems); MFCS 2023 Boolean-hierarchy p-optimality characterization (arXiv 2304.14702); Egidy 2026 SPARSE-relativization (arXiv 2602.02294, not read in detail). No new lower-bound technique found for Frege.

### Next steps
1. Formalize (A) via bounded arithmetic: does PV/S^1_2 ⊢ "P=NP" structure give EF poly simulation? Check Cook–Krajíček "Consequences of the provability of NP ⊆ P/poly".
2. Test whether multisigned hypergraph encodings (signed-DAG states) admit a Frege-size measure that is monotone under known simulation (candidate potential); needs a hostile control against EF compression.
