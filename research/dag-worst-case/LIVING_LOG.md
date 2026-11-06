# Living log: worst-case minimal-derivation-cost directive (multisigned DAG hypergraph for 3-SAT)

Objective: W_R(N) = max over UNSAT F, |<F>|<=N, of min over derivations pi of F |-_R bot of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).
Status of P vs NP: **OPEN**. Nothing below is a proof of a lower bound or of the bridge.

## 2026-11-06 18:50 UTC (routine "DAG proof") — entry 1

### Corpus note
No prior artifact in the repo carries this exact directive (grep for W_R / multisign finds only unrelated
GROK/LSPV notes). This file starts the log. Existing ALL-ARC/FLMV allocation in AGENTS.md is untouched;
this directive is recorded as an additional, separate log.

### Structural audit of the target (CANDIDATE-level analysis, not new theorems)
1. **Free choice of the optimal derivation = nondeterminism.** min over pi of cost(pi) is a proof-length
   measure. For any *fixed* R: W_R(N) superpolynomial for ALL R that are polynomially verifiable would
   imply NP != coNP (Cook–Reckhow), hence P != NP. So the target is at least as hard as NP vs coNP
   for strong R; it is not an easier route to P != NP. (KNOWN THEOREM: Cook–Reckhow 1979.)
2. **The bridge as stated fails for weak R.** For R = resolution, W_R(N) is exponential (Haken 1985;
   Urquhart; Ben-Sasson–Wigderson) unconditionally, independent of whether SAT in P. So
   "SAT in P => W_R <= poly" is FALSE for R=Res (unconditionally, since the antecedent is irrelevant
   to the consequent being false; the implication then amounts to SAT notin P). Hence "sufficiently
   powerful" must mean R at least p-simulates what a poly-time SAT algorithm can certify.
3. **The bridge is trivially true for a universal R and then content-free.** Let R_U be the system whose
   derivations are (M, t, trace) with M a SAT decider; SAT in P gives poly cost, but then lower bounds
   on W_{R_U} are equivalent to SAT notin P. A *fixed natural* R (Frege/EF) would need EF to be p-optimal
   (open; Krajíček–Pudlák: optimal proof systems exist under E=NE-type assumptions, otherwise unknown).
   Conclusion: the bridge for a fixed concrete R is itself an OPEN, strong statement (EF p-simulates
   all proof systems under P=NP?). Known: P=NP implies NP=coNP so SOME poly-bounded system exists;
   it need not be EF. Classification: bridge for concrete R = OPEN; bridge for R_U = trivial/circular.
4. **Cost model must include space as well as time** (peak memory is in the directive): "minimum over
   derivations" with *line-space / clause-space* measures has unconditional lower bounds in restricted
   systems (Res clause-space, Ben-Sasson–Nordström; Atserias–Dalmau), which are the model-matched
   precedents for the Time-Space Resource Auditor. EXACT OBJECT TRANSFER only within those systems.
5. **Hard-instance families that must be tested against the 5 roles' list** (resolution, algebraic,
   circuit compression, shared DAGs, strategy switching): Tseitin on expanders, PHP variants,
   random 3-CNF (Chvátal–Szemerédi), clique-coloring, and the binary value principle (Alekseev: hard for
   PC over Q in bit-size). Each is hard for a *restricted* R and has no known lower bound for Frege/EF.

### Literature check this run
- Alekseev, Theory of Computing 22 (2026): exponential bit-size lower bound for BVP in a PC-style system
  that simulates EF over rationals — a size-measure caveat (bit-size, not number of lines) that the
  Auditor role must keep in mind. https://theoryofcomputing.org/articles/v022a004/
- arXiv 2604.28172 (Apr 2026): superpolynomial lower bounds for semantic tree-like Frege with bounded line
  size — restricted system, does not touch general Frege/EF. https://www.emergentmind.com/papers/2604.28172
- No 2026 result found giving a superpolynomial lower bound for Frege or Extended Frege.

### Role outputs this run (single-agent run; roles not separately executed)
- Lead: formal statement above; weakest sufficient bridge analysis (items 1-3).
- Builder / Certificates / Auditor / Red Team: items 4-5 set the checklists; no new certified DAGs or
  computations were run.

### Open next steps
- (Lead) Pin down which R makes "SAT in P => W_R poly" provable: candidate = R with a *formalized
  uniform-P-time soundness reflection* (Cook's PV / Krajíček–Pudlák reflection), then show EF vs that R.
- (Certificates) Check whether signed-hypergraph instances already in repo (LSPV-2/3 strict3, signed NAE)
  give any measure under which min-derivation DAG cost is provably superpolynomial, and in which R.
- (Red Team) Try to refute item 2 reading, i.e. find a reading of "fixed R" under which the bridge is
  nontrivial and true.
- P versus NP remains OPEN.
