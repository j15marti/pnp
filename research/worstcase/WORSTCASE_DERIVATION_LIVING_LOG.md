# Worst-case derivation complexity — shared directive and living log

Status of P vs NP: **OPEN**. Nothing below proves a lower bound or the transfer bridge.

## Shared directive (2026-11-10)
For a fixed proof/inference system R over 3-SAT multisigned DAG hypergraphs:

  W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi)

Strategy discovery is NOT charged (min over pi is free); this only makes lower bounds easier to state, not easier to prove.
Priority bridge: **SAT in P  =>  W_R(N) <= poly(N)**.  Secondary: pointwise / worst-case simulation theorems.
Role questions: (1) Lead: formalize cost, weakest transfer theorem. (2) Builder: fixed combined system, certified shortest DAGs (small N, exact search). (3) Hypergraph/certificates: hard UNSAT families robust to resolution, algebraic, circuit compression, shared DAGs, strategy switching. (4) Auditor: cost, encoding, overhead, peak-memory accounting. (5) Red team: counterexamples, shorter derivations, bridge failures.

## Entry 2026-11-10 (LSPV-style Lead pass)

### E1. W_R is exactly proof size (KNOWN / PROVED, elementary)
With free strategy, min_pi cost_R(pi) is the minimum proof size of F in R. So W_R superpolynomial for a Cook–Reckhow R is the classical proof-complexity question. For all poly-time-verifiable R simultaneously it is equivalent to **NP != coNP** (Cook–Reckhow 1979), which is strictly stronger than P != NP. Hence the "strategy is free" relaxation does not weaken the target below NP != coNP unless R is fixed.

### E2. Bridge dichotomy for fixed R (PROVED/EXACT, short argument)
(a) If W_R is unconditionally superpolynomial (resolution, cutting planes, bounded-depth Frege with suitable families, ... Haken 1985 and successors), the bridge "SAT in P => W_R poly" is **equivalent to SAT not in P**, i.e. to P != NP. So proving the bridge for such R is as hard as the goal; it is no easier route.
(b) The bridge is non-vacuous only for R whose W_R is not known to be superpolynomial: Frege/EF-strength systems. For those the bridge is *not known*: SAT in P gives a poly trace of M on F, but the verifier of a fixed R cannot check M is correct, i.e. a semantic algorithm does not give an R-proof. 
(c) Cook's PV/EF correspondence (KNOWN): if SAT in P **with PV-provable correctness**, EF has poly-size proofs of all tautologies. So the weakest known sufficient bridge for R = EF is SAT in P + provable correctness, a strictly stronger hypothesis than SAT in P. The gap (semantic vs. provable correctness) is the precise missing arrow; closing it for EF is OPEN and would resemble the open problem of optimal proof systems (p-optimality of EF is unknown).
(d) Conversely, taking R = "T-proofs" for a strong theory T: bridge holds iff T proves correctness of the algorithm; unprovable in T is possible only if T cannot show it, so not excluded by current knowledge. CANDIDATE only.

### E3. Consequence for the project's inference system (CONDITIONAL)
A "fixed combined inference system" built from resolution + algebraic + XOR/Gauss + shared DAG remains weaker than Frege in the known landscape; lower bounds for it will be at the level of (a) and thus cannot yield P != NP via the bridge unless the system simulates EF-like reasoning (extension variables / reflection) and a lower bound for that is proved. Lead recommendation: make EF-with-extension (or a documented proper subsystem plus extension) the target R, and set the bridge hypothesis to "provably correct SAT algorithm", flagged CONDITIONAL.

### E4. Literature clues this run (primary-source pointers, not verified in depth)
- Pich–Santhanam, ECCC TR23-199, "Towards P != NP from Extended Frege lower bounds": EF lower bounds for formulas asserting SAT circuit-lower-bound-style statements (with witnessing axioms) would give SAT superpolynomial circuit lower bounds. This is a concrete published instance of the desired transfer, in the direction lower-bound-on-derivation => lower-bound-on-algorithms, but for a *specially augmented* formula family, not for plain UNSAT 3-CNF. Status: ANALOGY/CANDIDATE needing a bridge to W_R as defined here (formula family is not 3-CNF-unsat worst case).
- Khaniki–Pich–Sokolov, CCC 2026 (LIPIcs 383, paper 8), "Efficient Adversaries": conditional barrier: constructive EF lower bound for succinct circuit-lower-bound formulas plus EF proving correctness of SAT anticheckers makes the canonical pair of EF easy to separate. Relevance: constructivity of the lower-bound proof is itself constrained; flag for Red Team.
- arXiv 2604.28172 (Apr 2026): superpolynomial length lower bounds for tree-like semantic systems with bounded line size. Restricted (tree-like, bounded line); FAILED TRANSFER to DAG-like unbounded-line W_R.
- Frege survey material (Krajíček): optimal proof system existence remains open; bounded-depth Frege size lower bounds of sufficient strength would imply Frege lower bounds.

### E5. Open arrows (all OPEN)
1. Superpolynomial W_R for an R at least EF-strength (or at least not provably easy).
2. Bridge SAT in P => W_R poly without provable-correctness hypothesis.
3. Hard 3-CNF UNSAT families surviving resolution, algebraic and circuit compression simultaneously.
Next run: (i) Builder: compute exact minimum DAG-resolution/mixed-rule derivation sizes for all UNSAT 3-CNF with n<=5 variables to seed a ledger; (ii) Red team: test whether the "provably correct" hypothesis can be weakened via Pich–Santhanam style witnessing; (iii) Auditor: fix cost = (line count, total bit size, pebbling space) triple.

P versus NP remains OPEN.
