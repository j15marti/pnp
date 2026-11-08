# Worst-case derivation-cost programme: living log

Shared directive (user, 2026-11-08). Five roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder;
Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Proof Red Team.
Common target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi), strategy search NOT charged.
Priority bridge: SAT in P  ==>  W_R(N) <= poly(N).
Status of P vs NP: **OPEN**. Nothing below is a proof of a lower bound or of the bridge.
Additive note: changes no schedules, agent count or other allocations.

## Entries (newest first)

### 2026-11-08 CLAUDE WCDC-0001  (`research/agents/claude/2026-11-08_CLAUDE_WCDC-0001.tex`)
Audit of the bridge. Results (all PROVED/EXACT, elementary, or KNOWN THEOREM as marked in the .tex):
1. For any R with a known superpolynomial lower bound (resolution, cutting planes, bounded-depth Frege, ...), the bridge
   is *equivalent to* P != NP (its conclusion is false unconditionally). Not a weaker sufficient condition.
2. Free choice of the derivation makes W_R a nondeterministic measure; W_R <= poly for a sound R forces NP = coNP (Cook-Reckhow).
   Superpoly W_R for a fixed R is therefore an NP vs coNP-type statement, strictly in the proof-complexity programme.
3. The bridge can hold only for R that can certify the correctness of a hypothetical poly-time SAT algorithm.
   Transcript system R_A (derivation = run of a fixed A) satisfies the bridge trivially but is not sound without a correctness
   proof of A, and a lower bound for it IS P != NP (circular).
4. Weakest non-circular sufficient hypothesis identified: (B*) "P = NP implies a poly-time algorithm whose correctness is
   provable (with poly-size proofs on each instance) in R." Open; tied to p-optimality / provable-correctness questions.
Next targets (one per role) are in the .tex section "Assignments".

Literature checked this run: Cook-Reckhow 1979; Krajicek-Pudlak 1989 (optimal systems); Haken 1985; Pich-Santhanam (feasible
unprovability of co-nondeterministic lower bounds); 2026 arXiv 2602.02294 (no set outside NP is known to have an optimal
proof system); Egidy-Glasser STOC 2025 oracle results. See .tex bibliography notes (citations to be re-verified by a reader).
