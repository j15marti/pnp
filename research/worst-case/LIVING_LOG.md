# Worst-case derivation-cost programme — living log

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over refutations pi in system R of cost_R(pi).
Priority bridge: SAT in P  =>  W_R(N) <= poly(N).  **P versus NP remains OPEN. Nothing below is a proof of P != NP.**

Roles (shared objective for all five): General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Proof Red Team. Add one dated entry per run (newest last). Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Entry 2026-11-08 (CLAUDE, WORSTCASE-0001)
Report: `research/agents/claude/2026-11-08_0000_CLAUDE_WORSTCASE-0001.tex`.
Results (all standard-style, proved in report):
1. KNOWN/PROVED: free choice of the optimal sequence = nondeterminism. For any Cook–Reckhow R, W_R poly <=> R poly-bounded => NP = coNP. So a superpoly W_R for a poly-verifiable sound complete R proves NP != coNP, strictly stronger than P != NP, and equals a proof-complexity lower bound for R.
2. PROVED: for an *optimal* R the bridge SAT in P => W_R poly is TRUE, but then "W_R superpoly" is equivalent to NP != coNP, so the bridge gives no leverage.
3. CONDITIONAL: for a fixed natural R (Frege, EF) the bridge is exactly "P = NP => R poly-bounded". It holds if R (e.g. EF ~ PV) has short proofs of correctness of the P=NP algorithm; this reflection step is the missing transfer theorem (call it T-REFL). Unconditionally OPEN.
4. Derivation-cost model with a "run machine M" rule is unsound unless M's correctness is certified: the verification gap, not search cost, is the obstruction.
5. Red team: all classical hard UNSAT families (PHP, Tseitin, random k-CNF, ordering principle) are either polynomial in Frege/EF/PC or have no known superpoly Frege lower bound. Best EF/Frege size bound known: ~quadratic/linear.
Literature: Krajíček–Pudlák optimal-system theory (open); arXiv 2602.02294 (2026, optimal proof systems conjectures, abstract only seen); arXiv 2506.16956 (Proof Analysis Problem: EF proof analysis NP-complete; resolution in P); EF/Frege lower bounds still ~linear/quadratic.
Next target: T-REFL — find a fixed R and a theorem "P=NP via any algorithm A => R has poly proofs of A's UNSAT answers", or show a relativized/oracle counter-model (CANDIDATE: oracle with P=NP but EF not poly-bounded; check Krajíček/Pudlák oracle literature).
