# Worst-case derivation-cost program — living log

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); weakest bridge SAT in P => W_R(N) <= poly(N).
Status: **P vs NP remains OPEN.** Nothing below is a claim of a lower bound.

## Entry 2026-11-09 (scheduled run)

### Corpus reviewed
Repo tree survey; AGENTS.md; recent LSPV-1/4 reports (grep for W_R / worst-case derivation hits, e.g. LSPV-1 SIGNED_ORBIT_MINCOST348, PHP_COFAC_MITER_HARDNESS_FIREWALL401, BALANCED_MIXED_WORK_SPAN423). No earlier file in this repo states the bridge in the form above; this log is the first dedicated record. Not exhaustively re-read.

### Observation 1 (PROVED/EXACT, elementary): the bridge is trivial or as strong as the goal for any R with a known unconditional lower bound
Let R be sound with poly-time-checkable proofs and cost = proof size.
* If W_R(N) is known to be superpolynomial unconditionally (R = resolution, Haken 1985; cutting planes, etc.), then
  Bridge(R) := [SAT in P => W_R <= poly] is logically equivalent to SAT not in P, i.e. to P != NP. The bridge buys nothing.
* If W_R is polynomial unconditionally, Bridge(R) is true but gives no lower bound.
* So a *useful* bridge needs R with (a) lower bound open, and (b) a proof of Bridge(R) that does not itself decide P vs NP.

### Observation 2 (PROVED/EXACT): where (b) must come from — soundness/reflection
Given a hypothetical poly-time decider A, the one-line "derivation" "run A" is unsound as a fixed-system rule, because the verifier cannot trust an unknown A. A fixed R yields poly-size proofs from A only if R proves (with poly-size proofs) the correctness of A on the relevant instances, i.e. R must carry a uniform reflection-type capability for every poly-time A that could decide SAT. Hence Bridge(R) is a statement about R's reflection strength vs. the (unknown) provability of A's correctness, not about the combinatorics of hypergraph DAGs. Free knowledge of the best sequence (not charging search) is compatible with this: the obstruction is soundness verification, not search.
Consequence for the program: the hypergraph-DAG hard-instance work can give lower bounds for specific R, but the transfer to SAT not in P needs R to be (close to) p-optimal. (Literature: a superpolynomial lower bound for a p-optimal system would give lower bounds for all systems, hence NP != coNP; existence of p-optimal systems is open.)

### Observation 3 (CANDIDATE): reformulation of the weakest sufficient bridge
Weakest sufficient condition suggested: choose R = a system that p-simulates Extended Frege and for which SAT in P => (R proves "A decides SAT" with poly-size proofs for some explicit A) — i.e. require the theory-level statement "P=NP is provable in the theory associated with R" (bounded-arithmetic style). This replaces the bridge by a conditional on provability, and would make the final claim "P != NP or P=NP is unprovable in T" — NOT P != NP. Flagged as a barrier: the route via a fixed R cannot yield unconditional P != NP unless R is p-optimal.

### Literature check (this run)
Standard search only; secondary sources. Points: Cook–Reckhow (poly-bounded system iff NP=coNP); no superpolynomial Frege/eFrege lower bounds known; optimal proof system existence open; Cook/Buss reflection results for Frege; p-optimal lower bound => NP != coNP (Krajíček talk). Sources:
- https://karlin.mff.cuni.cz/~krajicek/talk-know-focs-2-22.pdf
- https://arxiv.org/pdf/2007.14835 (Reflection principles, propositional proof systems, and theories)
- https://arxiv.org/pdf/2604.01041 (not read in detail)

### Role assignments (unchanged scope)
Lead: formalize Obs.1–2 for cost = time+space, not just size. Builder: fixed system + shortest-DAG certificates. Hypergraph/Certificates: hard UNSAT families for systems *above* resolution where lower bound is open. Auditor: cost accounting incl. verification of reflection. Red team: attack Obs.2 (is there an R with unconditional Bridge(R) and open lower bound?).

### Stale/overstated claims
None found; the task's phrase "weakest sufficient bridge" is not weaker than P != NP for known-lower-bound R (Obs.1). Not integrated into root main.tex (outside any ownership region).

OPEN: all load-bearing arrows. END_OF_LOG_ENTRY::2026-11-09
