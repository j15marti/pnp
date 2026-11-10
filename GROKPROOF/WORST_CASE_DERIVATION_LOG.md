# Living log: worst-case minimum-derivation program (W_R)

Shared objective (all five roles):
W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi : F |-_R bot} cost_R(pi).
Strategy discovery is NOT charged (min over all derivations; search only adds work).
Priority bridge B(R): "SAT in P  =>  W_R(N) <= poly(N)". Status of everything below: P vs NP remains OPEN.

## Entry 2026-11-10 (first entry; no earlier shared directive file existed in the repo)

### Analysis of the bridge B(R)  [status: PROVED (elementary logic) / CANDIDATE where marked]
1. **B(R) is false-as-a-theorem-of-simple-form for any R with an unconditional superpolynomial lower bound.**
   For R = Resolution (Haken; Urquhart; Ben-Sasson-Wigderson), W_R is superpolynomial unconditionally, so B(Res) would be
   equivalent to SAT not in P, i.e. P != NP. Hence B(R) is only a meaningful *separate* hypothesis for R strong
   enough that no unconditional lower bound is known (Frege, Extended Frege, DRAT-like). [PROVED/EXACT, trivial]
2. **What B(R) actually requires.** If M is a poly-time SAT decider, the system P_M(pi,F) = "run M on F, accept if it says UNSAT"
   has proofs of size 0. B(R) therefore asks R to p-simulate P_M for every correct M; the part of the simulation that costs
   something is a short R-proof of "M is sound on F" (a reflection / soundness instance). So B(R) holds iff R has
   poly-size proofs of the soundness of each polynomial-time decider M (exponent may depend on M). [PROVED/EXACT as a restatement]
3. **Obstruction (feasible-incompleteness gap).** If P = NP is true but the bounded-arithmetic theory T_R associated to R
   (EF <-> PV/S^1_2) cannot prove "M is correct" for the particular M, B(R) can fail even though SAT in P. So B(R) cannot be
   established by a purely semantic argument; it is a provability statement about R. Consequently the "weakest sufficient
   bridge" is not weaker than: *T_R proves (or R has short proofs of) correctness of every poly-time SAT decider.* [CANDIDATE reading;
   the restatement in item 2 is exact, the incompleteness-gap conclusion is conditional on this being independent]
4. **Non-uniform version is known (literature, KNOWN THEOREM, arXiv 2312.08163):** if SAT_n has circuits of size n^k, then
   EF augmented with the circuit-correctness axiom alpha^{n^k} has poly(n)-size proofs of all tautologies. So B(EF+alpha)
   holds by construction; the content is entirely the extra axiom, i.e. the bridge is purchased by assuming the very thing
   (anti-checker/correctness provability) that a lower bound would need to refute. Cook-Krajicek: an optimal system exists with one bit of advice.
5. **Consequence for hard-instance work (role 3).** A hard family H_N must satisfy W_R(H_N) superpolynomial for an R that provably
   satisfies B(R). Any R for which Hard families are known (Res, PC, bounded-depth Frege, cutting planes, PC+extension-rule/BVP)
   fails item 1 unless extended by the correctness axiom, in which case the lower bound for the extended system is itself
   an open problem at least as strong as EF lower bounds. [CANDIDATE conclusion; no hard family for B-satisfying R is known]

### Literature clues checked this run (primary sources via search; not independently re-proved)
- Proof Analysis Problem (FOCS 2025, rev. May 2026, arXiv 2506.16956): PAP for EF is NP-complete (contrast: in P for Resolution).
  Relevance: certifying properties of EF refutations is already NP-hard, which limits any "auditor" that reads short EF derivations
  as a decision procedure. Transfer: ANALOGY only.
- "Efficient Adversaries" (CCC 2026, LIPIcs.CCC.2026.8): prover-adversary games for EF; conditional on constructive EF lower bounds for
  succinct SAT-circuit-lower-bound formulas + EF proving anti-checker correctness, the canonical pair of EF is easy to separate.
  Relevance: exactly the item-3/4 structure (correctness provability is the load-bearing hypothesis). Transfer: useful structural match, needs own theorem.
- Polynomial Calculus with Extension Rule (Theory of Computing v22 a004, 2026): exponential bit-size lower bound for BVP.
  Relevance: candidate hard family inside an extension-rule system; does NOT meet B(R) (item 5). Status: KNOWN THEOREM, restricted.
- Towards P != NP from EF lower bounds (arXiv 2312.08163): item 4 above.
- Not found: any new DRAT/clausal-proof superpolynomial lower bound or any p-simulation giving B(R) for a natural fixed R.

### Role assignments carried forward (no schedule change)
- General lower-bound lead: decide whether a weaker, *uniform-per-algorithm* bridge (soundness of each M provable in R) is formalizable
  as a hypothesis scheme and whether it is equivalent to an existing statement (e.g. Pudlak/Krajicek optimality conditions).
- Circuit-reduction builder: fix a combined inference system (clause + AND3 + GF(2) + definitions) and certify shortest DAGs on small N by exact search; record sizes.
- Hypergraph/certificates: test Tseitin, PHP-with-extension, BVP, parity-ordering families against the combined system; mark which survive extension.
- Time-space auditor: price each rule (DAG node = O(|clause|) bits, XOR-sum = Gaussian-elimination cost, definition = fresh variable) and peak memory; verify polynomial overhead of encoding.
- Red team: attack item 1-3 (is the incompleteness gap real for EF? any natural R with B(R) provable?).

### Status
P versus NP remains OPEN. No superpolynomial lower bound for a B-satisfying system, and no proof of B(R) for any fixed natural R, is established.
