# Living log: worst-case minimum derivation cost  W_R(N)

Target: W_R(N) = max over UNSAT F, |F|<=N, of min over refutations pi of cost_R(pi). Free choice of the optimal pi; no charge for finding it.
Bridge asked for: SAT in P  =>  W_R(N) <= poly(N), for a FIXED, sufficiently powerful R.
Status of P vs NP: OPEN. Nothing below proves a lower bound. Labels use the repo status discipline.

## Entry 2026-11-07 (WCD-0001, scheduled run)

Corpus: surveyed repo tree and the newest coordination handoffs. Found no earlier file that states W_R(N) or the "SAT in P => W_R poly" bridge.
Related earlier work: LSPV-1 signed-orbit min-cost (348), RUP/native-resolution bridge (412), PROOF_SYSTEM_FALLBACK163 (not re-read in full this run).

Findings (details in 2026-11-07_WCD-0001_bridge_audit.md):
1. KNOWN THEOREM (Cook-Reckhow 1979): W_R(N) <= poly(N) for a proof system R iff R is polynomially bounded; some R is so iff NP = coNP. "Free optimal sequence" is exactly NP-style nondeterminism, so a superpolynomial W_R lower bound is a proof-complexity lower bound for R.
2. PROVED/EXACT (short argument): the bridge is FALSE for weak R. Resolution: PHP_n^{n+1} has exponential minimum refutation size (Haken 1985), yet SAT in P is not contradicted by that. Same for any R with a known superpolynomial lower bound. A genuine bridge requires R at least as strong as every proof system, i.e. an optimal (p-optimal) system.
3. KNOWN THEOREM (Krajicek-Pudlak 1989): if NP = coNP, an optimal proof system exists; existence of one is open. SAT in P implies NP = coNP, so for an optimal R the bridge holds trivially. So: "bridge for a fixed R" is equivalent to "R is optimal-or-better and NP = coNP is consistent with the hypothesis". It adds no content beyond SAT in P => NP = coNP.
4. Consequence: a superpolynomial lower bound on W_R for an OPTIMAL R is equivalent to NP != coNP, strictly stronger than P != NP. For a non-optimal R, the lower bound does not transfer to SAT algorithms. This is the central obstruction to the stated plan. (CANDIDATE fix: change the cost measure so it charges time-space of a *deterministic* derivation, i.e. leave proof systems and use the repo's ARC/FLMV charged-trace route. Open.)
5. Literature: Egidy-Glasser (arXiv 2408.07408, STOC 2025) give oracles with optimal proof systems for sets outside NQP even assuming NP != coNP, so relativizing arguments cannot decide the optimal-system question. Egidy arXiv 2602.02294 (SPARSE-relativization) is recent related work. No 2025-26 result found that decides existence of an optimal system.
6. Hard-instance candidates to test next (multisign hypergraph DAG): Tseitin on expanders, PHP, random 3-CNF near threshold -- each has known bounds in Resolution/Cutting Planes/PC; none known in Frege/EF. The DAG-hypergraph system must be placed in the simulation hierarchy (does it p-simulate Resolution? is it simulated by EF?) before any claim.

Next steps: (a) define the multisign-DAG system precisely and prove its simulation relations; (b) decide whether the lower-bound target is R-specific (honest, provable for weak R) or optimal-R (equivalent to NP != coNP); (c) red team: check whether cost with peak-memory charging escapes Cook-Reckhow via a deterministic-trace model.
