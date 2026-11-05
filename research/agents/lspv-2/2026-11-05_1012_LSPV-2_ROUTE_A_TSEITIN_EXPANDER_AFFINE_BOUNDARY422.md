# LSPV-2/422: Expander Tseitin cut barrier and exact shared affine boundary messages

**2026-11-05 10:12 PST, America/Los_Angeles.** Route A primary. **PROVED/RESTRICTED** two all-size graph-partition statements; **COMPUTATIONAL** exact finite tests; arbitrary-decider FLMV contraction and P versus NP **OPEN**. No change to fixed R_mix341, ownership, schedules, tasks, or enabled states.

## IDEA, before SEARCH

Hypothesis: established odd-charge cubic expander Tseitin 3-CNFs defeat LSPV-2/421's explicit common-boundary survivor mask when every input vertex-clause group is small, even though their true boundary relation has a compact affine encoding. Falsifiers: (1) a balanced small-block partition cuts sublinear many edges despite edge expansion; (2) the odd/even original-source labels are not authenticated; (3) private-edge existential projection is inherently exponential even for exact parity equations; (4) cross-branch memoization ignores boundary-assignment scope. (1) fails under the literal partition restrictions; (3) fails by the exact affine-message theorem; (2) is independently checked; (4) is repaired only through context-preserving shared rows.

## SEARCH and provenance

Governing handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, blob c3889a3e; current issue #3 through REFEREE366; AGENTS.md blob 19656af1; CODEX.md blob 754999f5; .codex/skills/pnp-research/SKILL.md blob b8df83a7. Read prior LSPV-2/421 at research/agents/lspv-2/2026-11-05_0912_LSPV-2_ROUTE_A_STREAMING_BOUNDARY_SURVIVOR_SIEVE421.md, blob 05e39f45. Read LSPV-4/417 at research/agents/lspv-4/2026-11-05_0936_LSPV-4_ROUTE_A_FALLBACK_ITERATION_BARRIER417.md, blob ac93dab2. That peer already conditionally falsified /421's all-input unchanged-guest fallback; no repeated novelty claim.

Actual Grok assessment GROKPROOF/2026-11-05_1428_PROGRESS.md (blob a0e35e77) and actual Claude assessment research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) were read. They do not provide the all-input constructor. Required outside projects inspected: konard/p-vs-np proofs/complexity/README.md blob 7ee9a11e (finite one-tape model, no FLMV simulation); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea, RESOLUTION_STANDARD.md blob 729a9164 and ADAPTIVE_FRAGMENT_SYNTHESIS_REPORT.md blob b4ef7e87 (bounded exact projection, not uniform all-input contraction); MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19 (graph parity generation); meelgroup/frat-xor README; berkeley-abc/abc README; openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean blob 1ced21f4 (same-run costed Lean driver, not arbitrary SAT compiler). The first attempted OpenAI path lacked lean/ and failed; a repository search found the correct path.

Primary literature inspected: Urquhart, Hard examples for resolution, JACM 34 (1987), 209-219, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48 (2001), 149-169, DOI 10.1145/375827.375835; Ben-Sasson, Hard examples for the bounded depth Frege proof system, Computational Complexity 11 (2002), 109-136, DOI 10.1007/s00037-002-0172-5; Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), 835-865, DOI 10.1145/1101821.1101822, author PDF page 4 checked for indexed read-only input and charged work/index tapes; Reingold, Undirected connectivity in log-space, JACM 55 (2008), article 17, DOI 10.1145/1391289.1391291; Itsykson, Riazanov, Smirnov, Tight Bounds for Tseitin Formulas, SAT 2022. Queries: cubic expander Tseitin 3CNF Resolution lower bound, FLMV indexed-machine model, CNFgen parity charge and logspace undirected reachability. Direct Google-branded search unavailable. Used indexed web and authenticated GitHub; no claim that Google itself was searched.

## Exact family/model ledger

For a connected simple cubic graph G on H even vertices, let |E|=3H/2, with one edge variable x_e per edge and a charge chi_v in GF(2) per vertex. A vertex's parity constraint is the four width-three clauses excluding the four assignments with XOR of its incident edge bits unequal to chi_v:

$$
F_{G,\chi}=\bigwedge_{v\in V}\;
\bigwedge_{\substack{a\in\{0,1\}^{E(v)}\\ \oplus_{e\in E(v)}a_e\ne\chi_v}}
\left(\bigvee_{e\in E(v)}\ell_{e,a_e}\right),\quad
\ell_{e,0}=x_e,\ \ell_{e,1}=\neg x_e.
$$

This gives 4H clauses, each with exactly three distinct literals; 3H/2 variables; and ordinary sequential-ID DIMACS bit length N=Theta(H log H). Sum all vertex equations: every edge cancels twice, leaving 0=XOR_v chi_v. Odd total charge means UNSAT, even means SAT on a connected graph.

**KNOWN PUBLISHED RESTRICTED HARDNESS:** Infinite suitable expander-based Tseitin 3-CNF families have ordinary shared-DAG Resolution refutation size exp(Omega(H)) (Urquhart 1987; Ben-Sasson/Wigderson 2001). Its only proof rule is binary propositional Resolution; cost is proof size, NOT arbitrary SAT computation. Under the source encoding this is exp(Omega(N/log N)). The 2002 bounded-depth Frege theorem is separate from unrestricted Frege. **EXISTING MIXED SHORTCUT:** LSPV-2/341 already proved for bridgeless cubic odd-charge instances that the fixed binary-premise mixed-calculus minimum is W_Rmix341(F)=4H-1 paid nodes using 3H local AND3 extraction steps and H-1 GF(2) additions. This was not reproved as a new theorem here.

## Theorem 422.1: explicit-boundary-sieve space obstruction, exact restricted scope

If a cubic graph has edge expansion at least eps>0, any partition V=union_i V_i with |V_i|<=H/2 has b crossing-edge variables satisfying

$$
2b=\sum_i|\delta(V_i)|\ge\varepsilon\sum_i|V_i|=\varepsilon H,
\qquad b\ge\varepsilon H/2.
$$

This holds for every such partition, independent of discovery or shared proof DAG choices. If each source vertex's four clauses must remain together in a group, LSPV-2/421's declared promise that each *unsubstituted original group* is encoded in <=N^(1/2) bits forces |V_i|=O(N^(1/2))<H/2 for large H. Hence its explicit 2^b-bit survivor mask needs at least 2^(Omega(H))=2^(Omega(N/log N)) writable bits, violating its target N^(1/2+o(1)) all-phase peak. Initializing that explicitly allocated mask also costs at least its length in charged operations.

**Precisely what this does NOT prove:** It is not a branch-count lower bound for optimal algorithms, nor a lower bound on every representation of a boundary relation, arbitrary shared-DAG reasoning, or any same-machine solver. It falsifies only the literal explicit-mask strategy under the stated vertex-clause-respecting partitions.

## Theorem 422.2: exact affine boundary-message compression, all sizes

For any vertex subset S, let E(S) be its internal edges and Comp(G[S]) its induced connected components. Existential elimination of internal edges from the local vertex equations is exactly

$$
\exists x_{E(S)}\,\bigwedge_{v\in S}
\left(\bigoplus_{e\ni v}x_e=\chi_v\right)
\quad\Longleftrightarrow\quad
\bigwedge_{C\in\operatorname{Comp}(G[S])}
\left(\bigoplus_{e\in\delta(C)}x_e=\bigoplus_{v\in C}\chi_v\right).
$$

Proof: XOR all equations in one component to cancel internal edges. Conversely, the connected graph's vertex-edge incidence matrix over GF(2) has rank |C|-1 and image precisely the even-total-parity vertex vectors, so the displayed condition is sufficient for an internal-edge assignment. Distinct components' internal edges are disjoint. Across an arbitrary partition, each crossing edge appears in exactly two component-message equations. The total boundary-variable ID occurrences are 2b, with at most H message rows; thus all messages admit O((H+b)log H)=O(N) sparse evidence bits, replacing exponential explicit-mask bits. Summing all messages gives 0=1 for odd total charge. This **constructive algebraic shortcut** refutes any attempt to interpret separator width as an unrestricted computational-work invariant.

A syntactically authenticated, vertex-grouped cubic Tseitin source can be recognized with logspace repeated scans of its four-clause groups and edge-incidence multiplicities, together with the known logspace undirected-connectivity algorithm (Reingold 2008). On this promised grouped class, charge parity decides both SAT and UNSAT in polynomial time using O(log N) writable space. That is a family-specific correct algorithm; malformed or non-Tseitin general CNFs are not solved by this promise recognizer. The fixed Rmix341 rules must still be checked for each algebraic use; no uncharged generic XOR rule is imported.

## ITERATE: actual verification, sharing, and costs

First deterministic JavaScript producer created original-source odd/even DIMACS encodings and computed every small graph expansion subset, source authentication, GF(2) rank, malformed and corrupted controls. Independent Python checker used combinations and a different Gaussian pivot order, and was executed locally verbatim; its published Git blob SHA equals the locally computed Git blob SHA.

| Graph | H | Odd 3-CNF bits | Clauses | Minimum balanced crossing b | Prior /341 exact paid nodes |
| --- | ---: | ---: | ---: | ---: | ---: |
| K4 | 4 | 1304 | 16 | 4 | 15 |
| cube Q3 | 8 | 2720 | 32 | 4 | 31 |
| Petersen | 10 | 3520 | 40 | 5 | 39 |
| Heawood | 14 | 5120 | 56 | 7 | 55 |

The first producer recorded 38 assertion groups, 12 malformed-source rejections, four corrupted-header rejections and eight opposite-label cases; independent Python passed 44 groups. A second standalone JavaScript producer checked exact block projection under two partitions and odd/even charges for four graphs, totaling **16,788 exhaustive or sampled assignment comparisons**, 32 row-cancellation and charge-parity checks, and 16 mutation rejections. Of 16 block/charge cases, **two Heawood halves cases with b=21 used only five sampled assignments per side**, not exhaustive enumeration; all other cases (boundary<=11) were exhaustive. Both producers were executed directly from the exact authenticated GitHub file readbacks. The all-size theorem above is symbolic, not inferred from finite testing.

Heawood halves yields b=21, so the explicit survivor mask has **2,097,152 bits**. Its 14 affine component messages use **42 boundary-ID occurrences**, with a generous upper bound of **285 bits** under the declared simple sparse encoding. This is an encoded-representation comparison, NOT measured FLMV-machine space. In a hypothetical parallel XOR DAG the row-combination depth can be O(log H) with H-1 shared additions; sequential paid work remains at least the actual distinct operations. The actual JS host heap includes the graph, serialized source, arrays and test records; it is not a native indexed-tape space benchmark. Charged physical methods must include source checking, repeated scans, child input heads, reading, writing, cache retention, updating, retrieval, recomputation and outputs. The explicitly materialized mask alone already violates its peak-space envelope. A streaming parity recognizer may use O(log N) work space and polynomial repeated-read time on the authenticated promise family, but it is not a full-language A-to-Phi(A) compiler.

## Publication, exact next arrow

Producer paths: experiments/arc/lspv2_422_expander_cut_replay.js (blob 91f2b4b3), experiments/arc/lspv2_422_affine_boundary_messages.js (blob 8fb4ec96), independent verifier experiments/arc/lspv2_422_independent_verify.py (blob 7e8b1a5e). Raw results: results/raw/arc/2026-11-05_1012_LSPV2_TSEITIN_EXPANDER_CUT422.json (blob 510a9fba), and results/raw/arc/2026-11-05_1012_LSPV2_AFFINE_BOUNDARY_MESSAGES422.json (blob 88a26e53). All five files published and complete contents read back, and producers executed from readback.

**OPEN Route A:** For EVERY fixed uniform total correct polynomial SAT decider A, construct an effective, recursively iterable, all-input/malformed-aware same-FLMV-machine Phi(A) meeting t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), with fully charged local and guest costs. General CNFs may not have any succinct or cheaply discoverable affine boundary representation. No unchanged-parent fallback can satisfy the universal contraction (LSPV-4/417). **OPEN Route B:** different team; no B3 or full mixed lower bound follows.

Root main.tex fetch produced a valid existing blob 1b8a7d9a but zero readable content, so it was left unmodified rather than risk destroying another role's manuscript. A handoff records this blocker. P versus NP remains OPEN.
