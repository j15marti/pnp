# LSPV-1/470 | NP-complete optimization of shared source-authenticated layered Resolution DAGs

**November 7, 2026 PST | Route B lead | PROVED/RESTRICTED abstract/layered derivation theorem; COMPUTATIONAL finite original-CNF controls; historical R_mix341 minimum, B1/B2/B3 and P versus NP OPEN.**

## IDEA, falsifiers, SEARCH, ITERATE

**Initial hypothesis:** A globally shared proof-DAG optimization can encode SET COVER even if every admitted inference is an ordinary source-authenticated binary Resolution inference, the derivation is acyclic, source clauses are read without oracles, and a polynomial-size refutation is always available on the promised sources. This would explain *why the ideal minimum intentionally ignores optimizer discovery cost* but would not establish a hard formula for unrestricted Resolution.

Predeclared falsifiers: (F1) a selected set is charged more than once when it serves two goals; (F2) a goal can be omitted while reaching the empty clause; (F3) the constructed CNF is SAT despite complete set coverage, or UNSAT without coverage; (F4) the reduction silently assumes unrestricted Resolution cannot find an unmodeled shortcut. F1-F3 were checked by symbolic derivation and independent finite controls; F4 required **restricting the theorem to a uniform layered subset of legal Resolution derivations**. No unrestricted-Resolution or historical R_mix341 minimum is claimed.

**Actual SEARCH:** Read both root trackers on main (P1-00/P1-01/P1-X1; P2-D1/P2-D2/P2-D3/P2-B1/P2-B2/P2-C3/P2-B12), current coordination issue #3 and its latest LSPV-3/469, LSPV-4/463, LSPV-5/406 and LSPV-1/469 handoffs. Read \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, the governing Nov. 2 five-role refocus, original LSPV-2/341 mixed calculus report (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb), GROKPROOF/2026-11-07_0819_PROGRESS.md (blob c52f2f67956482d1ab10cb751aab1b0217890ba1) and Claude world-ledger README (blob de75a371ce3143a4495e6892df7fb04794a6b708).

Public literature searches: "minimum cost AND OR DAG shared subproofs NP hard set cover"; "directed Steiner tree acyclic NP complete set cover"; "Karp 1972 reducibility set covering"; "Tseitin expander ordinary Resolution lower bound"; "extended resolution PHP shortcut". Anchors: Karp (1972), *Reducibility Among Combinatorial Problems*, DOI 10.1007/978-1-4684-2001-2_9; Charikar et al. (1999), *Approximation Algorithms for Directed Steiner Problems*, Journal of Algorithms 33(1):73-91, DOI 10.1006/jagm.1999.1042. The current structural theorem is a direct elementary reduction from the established SET COVER decision problem. Directed Steiner work confirms that shared network optimization is a known phenomenon, not a novelty claim. Google-branded search was not separately used.

**Repository corpus and exact files read:** konard/p-vs-np \`README.md\` (blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and \`scripts/check_proof_status.py\` (blob 95e22b249baf487aaf478350a20db2b8ca98d619), which only authenticate stated finite-machine propositions; blkph0x/p-vs-np-proof-research \`README.md\` (blob f397a7747eaca82df3d754d0a4b4bab1fe10f814) and \`METHOD_INDEX.md\` (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5), which report scoped results rather than P/NP resolution; meelgroup/frat-xor \`README.md\` (blob 38a137bca4d4ab6443703d4c31fba5783021c581) and \`format.md\` (blob 986a21aa92b62f844ef1fce852193142c41b2b1f), whose original-clause/XOR IDs and rules are not historical R_mix341 bytes. No build or formal prover replay was claimed for third-party repositories.

**ITERATE:** Originally considered an arbitrary AND/OR dependency graph. Strengthened the witness to every step being ordinary syntactic Resolution on the actual original signed CNF. Restricted the optimizer to a uniform *layered plan grammar*, so the reduction proves a genuine exact NP-completeness statement but not an unqualified statement about unrestricted ordinary Resolution. Verified code and raw output from the exact GitHub readback in a V8 isolate.

## Precisely fixed restricted layered model

Input is a nonempty universe U={1,...,k} and listed subsets S_1,...,S_r, with k,r>=1. For each instance construct the signed CNF F(U,S) on a, s_1,...,s_r and g_1,...,g_k:

$$
F=(a)\ \land\ \bigwedge_{j=1}^{r}(\neg a\vee s_j)\
\land\ \bigwedge_{j=1}^{r}\bigwedge_{i\in S_j}(\neg s_j\vee g_i)\
\land\ (\neg g_1\vee\cdots\vee\neg g_k).
$$

This is **general CNF**, not proper strict 3-CNF for arbitrary k. All original clauses have immutable source IDs; only the actual original clauses are free. Every derived line is one ordinary two-parent named-pivot Resolution inference with unit cost. The *layered admissible plan* is fixed uniformly for all instances:

1. Optionally derive each selected set unit s_j once by resolving (a) and (not a or s_j) on a.
2. For every i derive g_i exactly once from some selected s_j and the original membership clause (not s_j or g_i).
3. Resolve the original final negative-goals clause successively with all k goal units, producing the empty clause in k further paid steps.

Any number of goals may reference a previously derived s_j. Its one paid node is charged once. No global assumptions, branch-local imports, free weakening, definitions, LOCAL-CONVERT, GF(2), split/discharge or semantic oracle are present. Every resulting certificate is a **legal ordinary Resolution DAG**, hence a valid upper-bound witness in any calculus genuinely containing unrestricted ordinary Resolution. The *optimization search space*, however, is only the explicitly named layered subgrammar; stronger legal proofs outside this grammar may be shorter.

The source has r+k+1 variables, 2+r+sum_j |S_j| clauses, and indexed explicit bit length N=O((rk+r+k)log(r+k+2)). Direct semantic proof: (a) forces all s_j; if union_j S_j=U, every g_i is true and the final negative clause fails, so F is UNSAT. If some i is uncovered, assign a=all s_j=true, all covered goals=true, g_i=false (and other uncovered goals=false): F is SAT. This is a both-label semantic control.

## Exact theorem 470.1: minimum and NP-completeness (PROVED/RESTRICTED)

Assume union_j S_j=U. Let tau(U,S) be the minimum number of sets whose union is U. Let W_layer(F) be the minimum number of distinct paid nodes among all valid *layered* source-authenticated Resolution refutations described above. Then

$$
\boxed{W_{\mathrm{layer}}(F(U,\mathcal S))=2k+\tau(U,\mathcal S).}
$$

**Upper bound:** Take a minimum cover J of tau sets. Derive each selected s_j once; assign every element i to one selected covering set; derive each distinct g_i once; resolve the final negative-goals source clause with all k goals. The proof has tau+k+k paid nodes. It is a single acyclic shared DAG. Every line is checked by exact complementary-pivot Resolution against the cited parents.

**Lower bound:** Every plan must derive all k distinct g_i, since it can remove their negative literals from the only allowed final-clause chain solely by the corresponding units. Each such g_i comes from some original membership clause for one selected s_j; thus the paid set units selected across all goals form a cover J. At least tau distinct set units, k goal steps and k final-chain steps are mandatory. No set unit is double-counted. Therefore q>=tau+2k.

**Complexity:** The decision problem "given this source encoding and B, is there a legal layered proof of cost <=B?" is in NP: a chosen set for each element and the corresponding ordered Resolution records are polynomial-size, locally checkable. It is NP-hard by the polynomial many-one reduction from SET COVER with budget b to this layered proof instance and B=2k+b. Instances not covering U are mapped to a fixed NO case. Thus it is NP-complete, and finding exact W_layer is NP-hard. This does **not** imply SAT is hard on these sources: the formulas' SAT/UNSAT status is checked in O(rk) time by testing coverage. Nor does it prove that finding the unrestricted R_mix341 minimum is NP-hard via this reduction: legal unmodeled shortcuts remain possible.

**Concrete original-source certificate:** k=3, sets S1={1,2}, S2={2,3}, S3={1,3}, tau=2. Source variable IDs are a=1, sets=2,3,4, goals=5,6,7. Its eleven source clauses are (1), (-1|2),(-1|3),(-1|4),(-2|5),(-2|6),(-3|6),(-3|7),(-4|5),(-4|7),(-5|-6|-7). Select S1,S2. Two set-unit resolutions, three goal-unit resolutions and three final resolutions yield a legal eight-paid-node DAG with set sharing; choosing a different set independently for every goal may use nine nodes.

## Finite reproduction, original-source/negative controls

Exact repository-published standalone JavaScript: \`experiments/arc/lspv1_470_layered_setcover_resolution.cjs\`, blob \`dca97dc50099c89b0d5250e1de329239d0df3871\`. It was **read back and executed in V8**; replay exactly matched the local result (not historical/native checker). Every nonempty-set family with k,r in 1..4 was enumerated: 57,164 systems, 46,312 covered, 10,852 uncovered. Two independent algorithms were compared: (i) enumerate subsets of selected sets; (ii) enumerate an assignment of one covering set to each goal and minimize distinct choices. 105,218 assertions passed; 1,502 full source-indexed Resolution certificates were independently checked by strict local pivots, 235 original signed CNF sources were truth-table checked for both SAT and UNSAT; nine deliberately malformed/corrupted proof references or steps were rejected. The symbolic reduction, not these finite checks, establishes NP-completeness. No native checker or independent external proof assistant was executed.

## Resource and hard-family/transfer ledger

**Ideal work:** W_layer=2k+tau<=2k+r. **Explicit proof bits:** the output DAG stores O(r+k) node names/antecedent refs and O(k^2) total literal occurrences along the final decreasing-width chain; O((r+k^2)log(r+k+2)) explicit bits suffice after source parsing. **Construction from supplied cover:** polynomial O(rk+k^2) basic operations, with symbol/ID bit costs. **Exact optimizer implemented:** enumerates up to 2^r subsets and up to r^k goal choices; this exponential discovery cost is **intentionally excluded only from W_layer**. **Source-authentication and checker:** every original reference, signed literal, pivot, resulting clause, closure and acyclic predecessor relation is read and checked. **Actual time/space:** full code keeps source clauses, proof and enumerator arrays in memory; it is not a streaming optimal solver or a native FLMV execution. Its peak host RSS and wall time were not instrumented; no unjustified precise machine exponent is assigned.

Hard-family controls: Urquhart (JACM 1987) gives exponential *ordinary Resolution* lower bounds for appropriate odd-charge cubic-expander Tseitin strict 3-CNF, with h vertices, 3h/2 signed edge variables, 4h proper source clauses, N=Theta(h log h) indexed bits, while the **declared semantic** R_mix341 has the short 4h-1 AND3/GF(2) proof (LSPV-2/341; LSPV-1/469; LSPV-3/469). Haken (TCS 1985) supplies ordinary Resolution-hard unary PHP, but Cook (1976) supplies polynomial Extended Resolution shortcuts. Braun (arXiv:2609.23015v2, 2026, unreviewed preprint) reports a Res(XOR) bit-PHP lower bound; LSPV-3/346 already provides a polynomial paid-DEF/RES shortcut in a declared mixed setting. **None** of these theorems is transferred by the present SET COVER optimization reduction into historical mixed-rule hardness. We did not instantiate a bespoke new SAT hard family.

## Status and next responsibilities

**Material addition to [P2-D2]:** even when every admissible step is a genuine, source-authenticated, binary Resolution inference, the optimization over *shared* globally selected DAGs can be NP-complete in a restricted layered class, despite all its covered sources being trivially recognizable UNSAT and possessing linear-work refutations. This separates *finding an ideal optimum* from *the value of that optimum*. The global minimum W_R in [P2-D2] must still grant free post-hoc selection of the best legal structure and must not infer arbitrary SAT time hardness from the NP-hard optimization problem.

**OPEN unchanged:** [P2-D1] original accepted-byte grammar, [P2-B1] all-legal-rule superpolynomial Wbar_R, [P2-B2] noncircular B3, [P2-C3] legal mixed normalization and native certificate transfer; Route A [P2-A2] all-input recursively iterable same-FLMV-machine contraction. The theorem adds no rule or weight to historical R_mix341. Two Route A and three Route B agents, titles, schedules, enabled states and main.tex unchanged. **P versus NP OPEN.**

References:
1. R. Karp, *Reducibility Among Combinatorial Problems* (1972), DOI: 10.1007/978-1-4684-2001-2_9.
2. M. Charikar, C. Chekuri, T. Cheung, Z. Dai, A. Goel, S. Guha, M. Li, *Approximation Algorithms for Directed Steiner Problems*, Journal of Algorithms 33 (1999) 73–91, DOI: 10.1006/jagm.1999.1042.
3. A. Urquhart, *Hard Examples for Resolution*, JACM 34(1) (1987) 209–219, DOI: 10.1145/7531.8928.
4. A. Haken, *The Intractability of Resolution*, Theor. Comput. Sci. 39 (1985) 297–308, DOI: 10.1016/0304-3975(85)90144-6.
5. S. Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976) 28–32.
