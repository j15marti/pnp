# LSPV-5 handoff — SIGNED-NAE-OCC2-COVERAGE-REFEREE216

Status: **KNOWN THEOREM transfer + PROVED/EXACT restricted corollary; broader coverage OPEN.**

The complement-paired formula
\[
F=\bigwedge_p(D_p\wedge\overline{D_p})
\]
is SAT exactly when the designated signed 3-clauses \(D_p\) are NAE-satisfied. If every source variable belongs to at most two pairs, standard signed-to-positive splitting makes every mixed-sign variable a binary NAE edge between its two literal-value vertices. Those binary edges form a matching. The NAE-SAT(2) obstruction theorem says failure can only arise from a non-bipartite residual binary component. A matching is bipartite, so the whole paired class is SAT and a model is constructible by the known linear-time algorithm.

This retires **signed-dual balance as a necessary coverage condition**. It remains a valid sufficient construction. The result does **not** cover arbitrary exact-(2,2) CNF, because complementary pairing is a strong recognizable hypothesis.

Finite audit:

- all 64 K4, 512 prism and 512 K3,3 sign classes;
- deterministic 32-class Petersen sample;
- 1,120 tested classes total, including 1,048 unbalanced; all SAT;
- eleven complete clause-indexed hostile controls with every occurrence-level S/U target and inversion, pair and bounded multi-clause matrices, 0^n/1^n, flip trails, resolvent cubes and charged fixed-order UP-DPLL comparisons;
- 1,576,960 sign-class assignment evaluations plus 833,501 assertion-accounted clause checks (see exact raw counters); runtime 5.379 seconds.

Important charged comparison: resolution reduced padded-unit UNSAT from 19 to 3 nodes and 589 to 573 work units, but raised paired K4 balanced from 196 to 544 work and planted dense SAT from 1,034 to 6,394 work. Node pruning is not a uniform total-work theorem.

Primary sources: Porschen–Randerath–Speckenmeyer, SAT 2003, DOI 10.1007/978-3-540-24605-3_14; Antunes Filho's degree-two hypergraph proof; Döcker arXiv:1912.08032 for the broader monotone exact22 hardness firewall.

Next lemma: characterize coherent partial-assignment residuals of the paired class. Pinning can shrink ternary NAE edges to binary edges, so odd-cycle obstructions can genuinely arise. Build a proof-producing residual algorithm returning a source witness or authenticated odd-cycle contradiction, with UP/2SAT/XOR switching and all failed probes/reconstruction/peak space charged.

P versus NP remains **OPEN**.

