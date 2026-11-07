# Worst-case derivation program: living log

Status: **P versus NP remains OPEN.** Nothing here is a proof of a lower bound or of the transfer theorem.
Statuses use the repo scale (PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED).
Append new entries at the bottom, newest last. This file is additive. It changes no schedules, roles or allocations.

## Directive (as given by the user, 2026-11-07)
Objective: for a fixed sufficiently strong inference system R on signed DAG-hypergraph encodings of 3-SAT,
W_R(N) = max over UNSAT F with |<F>| <= N of min over derivations pi: F |-_R bottom of cost_R(pi).
The optimal derivation is chosen for free and strategy discovery is not charged, which is legitimate for lower bounds.
Priority 1 is the weakest sufficient bridge B_R: SAT in P implies W_R(N) <= poly(N).
Priority 2 is superpolynomial W_R(N) for a fixed, sufficiently strong R.
Priority 3 is to test hard instances against resolution, algebraic reasoning, circuit compression, shared DAGs and adaptive strategy switching.
Roles: General Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph and Certificates; Time-Space Auditor; Red Team.

## Entry 1 (2026-11-07, Claude, scoped survey)
Corpus reviewed (scoped, not byte-exhaustive): AGENTS.md, repo tree, research/agents/claude/*, world-ledger README, `git log`, and a repo grep for "derivation cost", "multisign" and "W_R(N)". The grep found only related signed-orbit/min-cost reports by LSPV-1/2/3 (e.g. LSPV-1 SIGNED_ORBIT_MINCOST348, LSPV-2 CLONE_MITER_RES355). No prior statement of this exact program or its bridge exists. A full LSPV-style whole-corpus reconciliation was NOT done this run, and root main.tex was not edited (not an LSPV-owned region).

### Result A (PROVED/EXACT, elementary): free search is already built into proof length
If R is a Cook-Reckhow system (sound, complete, poly-time verifiable) and cost_R(pi) = |pi|, then the inner min over pi is exactly the shortest R-proof. "Grant the best sequence for free" therefore adds nothing: the program with length-cost is the Cook-Reckhow program verbatim.
The free-search relaxation is only new for cost measures that are not verification length, such as time-space, width, or space of a derivation. For those it is a genuine strengthening of the lower-bound target (lower bounds with free search imply lower bounds for any search procedure).

### Result B (PROVED/EXACT): the bridge is a reformulation for every R with a known superpolynomial lower bound
Let B_R be [SAT in P => W_R <= poly].
(i) If W_R is provably superpolynomial (resolution (Haken), cutting planes, bounded-depth Frege (Ajtai, Haastad)), then B_R is equivalent to SAT not in P. Proof: the conclusion of B_R is false, so B_R is true iff its hypothesis is false.
(ii) For such R, "weakest sufficient bridge" is therefore as strong as P != NP, and no weaker.
(iii) For R with W_R open (Frege, EF), B_R is implied by P != NP. A proof of W_R superpolynomial plus a proof of B_R would give P != NP. So B_R is where all the difficulty sits. It must be proved without assuming P != NP, since B_R is vacuously true if P != NP.

### Result C (CONDITIONAL, standard): what a proof of B_EF would need
Fix R = Frege or EF. If some polynomial-time SAT decider M has poly-size R-proofs of the propositional translation Phi_n(f,x): "f(x)=1 implies M accepts f", then substituting a concrete UNSAT F and evaluating M(F)=reject (a poly-size trace) gives a poly-size R-refutation of F. So B_R follows from "SAT in P implies a feasibly-provably-correct decider". That implication is the missing theorem. It is a feasible-provability statement. Bounded-arithmetic unprovability results (Pich-Santhanam STOC 2021; Li-Oliveira on PV1 and APC1; Chen et al.) suggest such correctness cannot be established by feasible arguments alone. This is a CANDIDATE barrier, not a theorem about B_R, and its exact transfer to B_R has not been checked.

### Result D (COMPUTATIONAL, tiny): exact minimum DAG-resolution lengths
`min_res.py` (iterative deepening over SETS of derived clauses, no weakening, 20 s cap per formula) gives:

| formula | clauses | min refutation length |
|---|---|---|
| all four clauses over 2 vars | 4 | 3 |
| Tseitin on C3, odd charge | 6 | 5 |
| Tseitin on C4, odd charge | 8 | 7 |
| PHP_2^3 | 9 | timeout (no value) |
| Tseitin on C5 | 10 | timeout (no value) |

The C3/C4 values fit 2n-1 but this is a two-point observation, not a theorem. Timeouts are inconclusive, not lower bounds. The search is exponential, so this checker is not a scalable certifier. A SAT/ILP-based certifier would be needed for larger instances.

### Literature clues (checked this run, via web search; abstracts only, details unverified)
- Frege superpolynomial lower bounds remain open (Krajicek survey); existence of an optimal proof system is open. This is the exact wall for any "sufficiently powerful R".
- Haastad, small-depth Frege for PHP, TheoretiCS 4 (2025): exp(n^{Omega(1/d)}) bounds. Relevant only to the bounded-depth fragment of R.
- Pich-Santhanam (STOC 2021), Li-Oliveira (2024), and a 2026 arXiv follow-up (2602.19934): unprovability of strong co-nondeterministic lower bounds in PV-type theories. Relevant to Result C.
- Time-space tradeoffs in resolution (Ben-Sasson-Nordstrom; Beame et al.) are the natural home of the "free search is a real relaxation" setting from Result A. Not re-searched this run.
Classification: all are USEFUL STRUCTURAL ANALOGIES requiring a transfer theorem. None is a directly transferable theorem for B_R.

### Next targets (assignable to the five roles)
1. Lead: state B_R for a cost that is not length (time-space) and test whether Result B(i) still collapses, i.e. whether any such R has a provable lower bound unconditionally.
2. Reduction builder: define the combined signed-hypergraph system concretely, and check it p-simulates resolution, Gaussian elimination and cutting planes.
3. Certificates: build a scalable exact certifier (SAT/ILP) replacing min_res.py.
4. Auditor: charge verification cost per inference line, including DAG sharing and encodings.
5. Red team: look for a proof that B_R for Frege/EF is equivalent to a known open statement (e.g. feasible correctness of a SAT decider), or refute Result C's reliance on substitution closure.
