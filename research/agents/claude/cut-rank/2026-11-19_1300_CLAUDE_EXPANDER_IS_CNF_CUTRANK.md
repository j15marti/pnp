# Claude lane: every-contraction-tree cut-rank lower bound on a trivially satisfiable 2-CNF | 2026-11-19 13:00 PST

This is a Claude scheduled routine run (research/agents/claude/), not a TMR-1..5 run. No TMR manuscript, handoff, retired tracker (proof*.txt) or historical main*.tex was modified. Repository base: 477fa4d61f9f2a14338054d6449ee4ba80d64316 (origin/main). P versus NP remains OPEN, and nothing here promotes a theorem about SAT decision complexity.

## Dependency advanced

The previous Claude-lane run (branch ccr-8d8a5ce7-9deizk, report doc-review/2026-11-19_0948_CLAUDE_DUAL_ATTEMPTS_DOC_AUDIT.md) falsified the Google Doc's graph-only tensor-network bound. It left this next lemma: find an explicit polynomial-size 3-CNF family F_n whose solution indicator has cut-rank 2^Omega(n) across a balanced edge of every contraction tree, over every field.

Pipeline (Track A, rank/tensor invariant):

1. Encoded CNF.
2. Exact tree tensor-network contraction or structured representation of the solution indicator.
3. Bond-dimension lower bound.
4. A claimed consequence for SAT.

This run closes the lemma for step 3 and then tests the arrow from step 3 to step 4.

## Candidate and falsifiers (stated before search)

Candidate: let H be an explicit bounded-degree expander and let F_H be the CNF that is the AND over edges uv of H of (not x_u or not x_v). Then for every balanced bipartition (A, B) of the variables, the 2^|A| x 2^|B| solution-indicator matrix M_{A,B} has rank at least 2^(c n) over every field.

Falsifiers:

1. A balanced cut, for example a local-search minimum cut, where the computed rank is below 2^k for the computed induced matching size k.
2. Field dependence: the DISJ restriction losing rank over GF(2).
3. The restriction step failing to give a submatrix, or the matching failing to be induced.

None of these fired. Details follow.

## Lemma 1 (PROVED/EXACT, elementary; not independently reviewed)

Setup: H is a simple graph with maximum degree Delta. (A, B) is a bipartition of V(H). E_c is the set of edges crossing the cut.

Claim:

(a) H has an induced matching of crossing edges of size k >= |E_c| / (2 Delta^2).

(b) rank_K(M_{A,B}(F_H)) >= 2^k for every field K.

Proof of (a), greedy. Pick a crossing edge uv. Delete every edge with an endpoint in N[u] ∪ N[v]. That is at most 2 Delta vertices, so at most 2 Delta^2 edges. Repeat. Any two chosen edges have no H-edge between their endpoints, so the chosen set is an induced matching.

Proof of (b), restriction. Set every unmatched vertex to 0. Every clause (not x_u or not x_v) that touches an unmatched vertex is then satisfied. Because the matching is induced, the only remaining clauses are the k matching clauses (not a_i or not b_i), with a_i in A and b_i in B. The restricted indicator is therefore DISJ_k(a, b), the product over i of (1 - a_i b_i).

Fixing variables on both sides selects rows and columns, so this is a submatrix of M_{A,B}. The DISJ_k matrix equals [[1,1],[1,0]]^(⊗k), whose determinant is ±1. It therefore has rank 2^k over every field. QED.

## Corollary 2 (PROVED, conditional on the cited expander constant)

Construction: let G_m be the Gabber–Galil/Margulis graph. Its vertex set is Z_m × Z_m. Each (x, y) is joined to (x+2y, y), (x+2y+1, y), (x, y+2x) and (x, y+2x+1), and to their inverses. This is an 8-regular multigraph.

Cited premise (KNOWN THEOREM, not re-verified this run): λ_2(G_m) <= 5√2 < 8, as in Gabber and Galil (1981) and the Hoory, Linial and Wigderson survey (Bull. AMS 2006, Margulis/Gabber–Galil section). This run did not re-check the theorem number or the constant in a pinned primary copy, because the fetched draft PDF had no extractable text. The computed λ_2 values for m = 4, 5, 6 are 4.83, 5.33 and 5.55, all below 5√2.

Step 1, crossing multi-edges. By the expander mixing bound, every S with |S| in [N/3, 2N/3] has e(S, S̄) >= (8 - λ_2)|S||S̄|/N >= 0.204 N crossing multi-edges.

Step 2, simplify the graph. Delete self-loops and merge parallel edges, with multiplicity at most 8. This leaves at least 0.0255 N simple crossing edges and Delta <= 8.

Step 3, apply Lemma 1. This gives k >= 0.0255 N / 128 ≈ 2×10^-4 N.

Every binary contraction tree, or vtree, over N leaves has an edge whose leaf set has size in [N/3, 2N/3]. Conclusion: on every contraction tree, F_{G_m} has a bond whose environment-aware exact rank is at least 2^(2×10^-4 N), over every field. The constant is weak but linear.

Known-theory context: rank lower-bounds the disjoint rectangle partition number. In the Pipatsrisawat–Darwiche and Bova–Capelli–Mengel–Slivovsky framework, this gives exponential structured d-DNNF/SDD size for F_{G_m}. Only the IJCAI 2016 abstract and summary were consulted (ijcai.org/proceedings/2016/147). Whether that paper states this exact 2-CNF family is NOT source-verified.

## The arrow this kills (FALSIFIED: "every-tree bond lower bound implies SAT decision hardness")

F_{G_m} is a monotone 2-CNF that the all-zero assignment satisfies. Its decision problem is solved in O(1) after parsing, and in O(|F|) to verify a witness. Even so, Corollary 2 gives a 2^Omega(n) bond on every contraction tree.

So an exponential every-tree cut-rank lower bound is consistent with trivial decision complexity. It measures the size of an exact representation of the whole solution set, which is a counting/compilation quantity. The step from (3) to (4) in the pipeline cannot be a decision lower bound for SAT. At most it can be a lower bound for exact counting or compilation within the fixed-shape tree-tensor-network or structured-DNNF model.

The counting interpretation is itself restricted. #IS on bounded-degree graphs is #P-hard in general (KNOWN THEOREM). The fixed family G_m, however, has one count per m, so there is no uniform counting-hardness consequence either. This is the "unique-solution / easy-family" guard in its strongest form: the rank is large where decision is trivial. It complements the earlier run, where the rank was small where tw is large.

## Computational evidence (COMPUTATIONAL, finite)

- Script: experiments/claude/expander_is_cnf_cutrank.py, blob a7364189ccad6ea1558a3f9b3e066b74000ba70f.
- Raw output: results/raw/claude/2026-11-19_1300_EXPANDER_IS_CNF_CUTRANK_RAW.json, blob 5ac9c50f6970865ffe309a4fb1ca4d2a35a3e748.
- Seed 20261119, offset +1 for m = 5 and +2 for m = 6. Total runtime 4.9 s on Python 3.11 with numpy 2.4.6.
- Self-test: DISJ_k gives GF(2) rank = rank mod (2^31 - 1) = 2^k for k = 1..6.
- Cuts: balanced halves of two kinds. "localsearch-min" cuts come from 400-step swap descent on the crossing-edge count. "random" cuts are uniform.

| m | N | simple edges | Delta | λ_2 | cut kind | crossing | induced matching k | rank GF(2) | rank mod p | cap 2^(N/2) |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 16 | 40 | 6 | 4.828 | min / random (8 cuts) | 12 to 24 | 2 | 18 to 27 | equal to GF(2) | 256 |
| 5 | 25 | 70 | 8 | 5.325 | min, random, min, random | 20, 42, 22, 32 | 3, 4, 3, 4 | 66, 184, 62, 122 | not run | 4096 |
| 6 | 36 | 108 | 8 | 5.545 | min, random | 32, 56 | 5, 6 | 474, 1127 | not run | 262144 |

Rank >= 2^k held on all 14 cuts. The actual ranks are far above the lemma's 2^k, so the greedy constant is loose. Mod-p cross-checks were run only for m = 4, which is an unexecuted check for m = 5 and 6. Local search is not an exhaustive minimum over balanced cuts. The asymptotic claim rests on the symbolic proof, not on this table.

## Four gates (for Lemma 1 and Corollary 2)

- DISJ sanity: PASS. The bound is literally a DISJ embedding, with full rank over every field.
- Relativization: NOT APPLICABLE. This is a fixed-representation-model statement with no machine or oracle.
- Simultaneous DTISP: NOT APPLICABLE. No machine time-space claim is made, and the decision side is O(n).
- Deterministic configuration counting: NOT APPLICABLE, for the same reason.
- Natural Proofs: cut-rank is constructive and large for random functions. It yields only restricted-model bounds, which is consistent with this run.

## Repository and corpus survey

Duplicate check: `grep -ri "induced matching"` and the DISJ embedding are already used in several repo reports (Track A rank work). This report adds the every-vtree statement on an explicit trivially-SAT family and the explicit falsification of the rank-to-decision arrow. It does not claim novelty against the literature, since this is a standard knowledge-compilation argument.

Google Doc 1b2SYjJJJVjMwap-5wURTFbUMn212lwFnYhq2k5Sqdds: metadata shows modifiedTime 2026-11-02T17:46:59Z, unchanged since the previous audits. Its section 2.2 IB/TN claim is now bracketed on both sides:

- Small rank with large tw (previous run).
- Large rank with trivial decision (this run).

GitHub (`gh api search/repositories`, default branches only) covered user:openai, google, google-deepmind and google-research. The queries were "proof complexity", "circuit lower bound", "knowledge compilation", "lean prover" and "tensor network", plus "formal-conjectures".

- Hits: google/TensorNetwork and google-research/tnco, a tensor-network contraction-order optimizer. These give upper-bound heuristics only. Corollary 2 implies that no contraction order they find can beat a 2^Omega(N) bond on F_{G_m}.
- Also hit: google-deepmind/formal-conjectures, a collection of Lean conjecture statements.
- Repository contents were not readable (session scope 403).
- openai returned 0 hits on every query.
- No SAT lower-bound idea was found.

## Integration point

This bears on TMR-2 (Track A invariants) and TMR-4 (compiler to tensor/structured representation). Any invariant that is lower-bounded by the indicator cut-rank must pass the F_{G_m} control. Because that control is trivially satisfiable, such an invariant cannot by itself certify decision hardness. Suggestion only, through issue #3. No peer manuscript was edited.

## One next lemma

Find a decision-sensitive replacement for the indicator rank. Concretely: is there a cut-measure μ on CNFs such that μ(F) is small whenever F has a polynomial-size certificate of satisfiability that is locally checkable along the tree? Two concrete cases are tree-like resolution width for UNSAT and the "witness-restricted rank" for SAT. Separately, is μ provably large on Tseitin formulas over G_m? The known answer for UNSAT is that resolution width on Tseitin(G_m) is Omega(N) (Ben-Sasson–Wigderson). The open interface is turning such a measure into a lower bound for an exact tree tensor-network decision procedure that may use a different network than the indicator network, without assuming a fixed network shape.
