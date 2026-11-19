# STRICT-C-WITNESS-STREAM-1 | canonical critical deletion witnesses without search
2026-11-19, America/Los_Angeles. Agent role: SAT witness discovery. **PROVED** restricted-family constructive algorithm; **COMPUTATIONALLY VERIFIED** 984 full physical strict-C deletion witnesses; **FALSIFIED** the use of a persistent 5-core as a witness-hardness indicator; **OPEN** generic strict-C witness construction and P versus NP. No schedules or existing manuscripts changed.

## Exact family and theorem (PROVED)
Use the canonical R(a,b) iff (b-a) mod 5 is in {1,3} and C(a,b,c) as an unoriented directed triangle (30/125 triples). For every odd integer L >=5, let G_L=M^3(C_L), the threefold ordinary Mycielski lift of the odd cycle. Write n=|V(G_L)|=8L+7, m=|E(G_L)|=46L+6. Encode graph edges with disjoint private heads: F_L=AND_{j=0}^{m-1} C(h_j,u_j,v_j). Names h_j,u_j,v_j are distinct in each physical clause; colors may repeat elsewhere. F_L has n+m=54L+13 strict-C variables, m clauses, and incidence girth 8 (the graph is triangle-free with a 4-cycle; private heads are leaves in the incidence graph).

Classical Mycielski results give chi(G_L)=6 and, for chromatic-critical bases, criticality of each lift [1]. Here an **explicit deletion-coloring recurrence** also constructs, for every actual edge e of G_L, a proper five-coloring of G_L-e with the endpoints of e equal. Therefore F_L is UNSAT, every F_L-C_j is SAT, and every single physical C deletion has an explicit full witness.

More strongly, for the **canonical indexed source grammar**, a uniform deterministic source-authenticated specialist takes the actual source with exactly one clause missing, **without being supplied the deletion index or answer polarity**, and:
- outputs SAT plus every original named variable's color if it matches a single physical deletion of a canonical F_L;
- outputs UNKNOWN if source authentication fails.
For each recognized input of explicit size N, it takes O(N) word-RAM operations, O(log N) auxiliary writable bits and O(N) write-only witness output. This includes inferring L from clause count (m-1=46L+5), reading and authenticating every source record, detecting the unique missing physical clause, computing colors, a complete original-C predicate verification, and streaming every output color. The fixed Mycielski depth 3 is crucial. The input/source is read-only, and output is write-only; a Python runtime uses additional fixed implementation overhead, not mathematically bounded by the tracer. The recognizer accepts the exact indexed/ordered source grammar, **not arbitrary variable renamings, arbitrary orderings, general critical graph encodings, or all strict-C CSPs**.

## Deletion-coloring recurrence (PROVED)
Assume a graph H is k-chromatic and each deletion e=uv admits a (k-1)-coloring c of H-e, necessarily with c(u)=c(v)=a. Let M(H) have old vertices V, clones V', root w, edges E(H), edges x-y' and x'-y for xy in E(H), plus x'-w. Introduce color b not in the (k-1)-color palette.

1. If the deleted edge in M(H) is old-old uv, color old x by c(x); clone x' by b when c(x)=a, otherwise by c(x); root w by a. The only nonproper old edge was deleted; all cross edges and root edges are proper.
2. If deleted edge is old u to clone v', descend to e=uv. Color old u by b, other old x by c(x); clone x' by b when c(x)=a, otherwise c(x); root w by a. The only cross-edge color collision is at the deleted u-v' edge.
3. If deleted edge is clone u' to root w, choose any actual incident base edge uv. Use the (k-1)-coloring c of H-uv, recolor old u and clone u' and root w to b; leave other old and clone vertices colored c. The only equal-colored adjacent pair is the deleted u'-w.

The construction gives a proper k-coloring of every deletion of M(H) and the deleted endpoints share b or a. Base C_L-e is a path, two-colorable in closed form. Recurse exactly three levels to get the five-coloring. Every surviving private head is a deterministic constant-time function of its endpoints:
if a=b no head exists; otherwise t=3(a+b) mod5 is the midpoint, with allowed h=t±1 for (a-b)^2=1 mod5 and h=t for (a-b)^2=4. Choose the least valid h. For the deleted edge, endpoints share a color, so every head value falsifies its original strict-C clause.

## Source/space accounting (PROVED for the exact grammar)
Indexed recursive edge generator for M(H): every base edge contributes old-old, old-clone, clone-old in three consecutive slots, followed by one clone-root edge per old vertex. n_{i+1}=2n_i+1, m_{i+1}=3m_i+n_i. At level 0, edge j is (j,j+1 mod L). A single edge_at index takes O(1) word operations at fixed depth=3. The color-at-index routine descends at most three levels and makes at most constant many recursive evaluations. At base, the deleted cycle edge gives a path; color of vertex x is distance parity from vertex zero, obtained by O(1) arithmetic. An incident base edge needed for a clone-root deletion is chosen deterministically by an implicit neighbor-at-index routine. Thus every color and head is computed in O(1) word operations on O(log N)-bit indices.

The source recognizer compares all original tuples against this generated grammar and discovers the unique missing clause, with no guess or supplied branch. The acceptance condition is syntactic and exact, so soundness does not depend on an optimistic completeness heuristic. It independently replays every retained physical strict-C predicate before emitting SAT. The total acquired witness is O(N) symbols and verification O(N). Full ledger of all m deletions necessarily takes Omega(mN)=Omega(N^2) output operations. All failed malformed-source checks are charged up to O(N); no SAT/UNSAT child solver calls, supplied correct paths, polarity bits, certificates from an oracle, or unsound wrong-path outputs occur. Complete formula F_L and unrelated inputs return UNKNOWN in the SAT/UNKNOWN specialist.

## Executed evidence
Deterministic, no PRNG seed. Source witnesses validated with the original tournament R predicate, not a Q/S/P surrogate. Independent verifier reconstructs graphs using a different edge-set implementation and replays every emitted full witness:
| Base L | Graph n | C clauses m | C variables | Deleted witnesses | Retained C true | Deleted C false | incidence girth |
| 5 | 47 | 236 | 283 | 236 | 55,460 | 236 | 8 |
| 7 | 63 | 328 | 391 | 328 | 107,256 | 328 | 8 |
| 9 | 79 | 420 | 499 | 420 | 175,980 | 420 | 8 |
Totals: 984 complete witnesses; 338,696 surviving original C clauses true, 984 deleted physical C clauses false, 339,680 original-C checks. The independent original-source recognizer found the missing clause without being supplied any index on all 984 instances, with a further 339,680 original-C checks; tampered original C source returned UNKNOWN (also under Python -O). Full source rereads and all output values counted. A separately implemented degree-5-core peeling test on every G_L-e retained **46 or 47** vertices (L=5), **62 or 63** (L=7), and **78 or 79** (L=9), with zero empty cores. Thus degree peeling fails as a complete witness algorithm while a structural constructive algorithm succeeds with no search.

The independent source/ledger SHA256 values:
L5 source 0914e0442323d56004336faa80c8675a3906efe679a1dd99213f47589c7e5b39, ledger f46163d5cdd54c3f3daac0a365ed77f602fd184c6cadad110be76de58f55b6bd;
L7 source 33038d156e5ee3abfeb73f8cdb3cab1373901acc9e45e3f6a0da53f83bab8e8a, ledger 253b6847a54d829fc27ab072c759c6caca27ad24e6e207c3713365a052224f87;
L9 source 94b8b5205e7ae32120ae9af86c4ad4896fd4db2b74c08e5283d2cb44056ee752, ledger aaa39080245701adc9edea97b3d6bc0de30eb4be32d7a70f65f32605133b51b0.
Independent Python code and complete JSONL witness ledgers are in the local reproducibility ZIP. For the streamed execution, Python tracemalloc peaks were 224080, 231031, 236128 bytes respectively; **these are not formal algorithmic space measurements**. The single-deletion specialist performs its own verification before output. All 984 recognized-deletion tests succeeded. The quadratic identity and failed rank-unconstrained lifting were already recorded by the prior witness agent; this report does not claim to rediscover them.

## Complexity-theory firewall and next blocker
This algorithm is a family grammar recognizer, **not** a solver for general strict-C or arbitrary CNF. The full G_L graph is highly recognizable and admits a compact structural witness circuit, notwithstanding 5-core persistence, clause-criticality, and incidence girth 8. No superpolynomial lower bound follows. A source whose indices or vertex labels are adversarially permuted would require separate recognition work. It does not establish the N^.195 row/N^.65 block/N^.35 private decomposition or an unrestricted N^1.33-time, sqrt(N)-space SAT algorithm. For arbitrary-C SAT witness discovery, next test should target intrinsic critical instances lacking such an efficient source grammar and demand proof of *absence* of any algebraic, decomposition, or structural witness shortcut, not merely failure of greedy peeling.

### Prior work and literature
[1] Chang G.J., Huang L., Zhu X. "Circular chromatic numbers of Mycielski's graphs." Discrete Mathematics 205 (1999), 23-37, DOI 10.1016/S0012-365X(99)00033-3; Lemma 1 states the chromatic-critical preservation of Mycielski lifts.
[2] Prior witness agent: research/agents/witness/2026-11-19_STRICT_C_GF5_QUADRATIC_WITNESS_AUDIT.md (read back via connected GitHub).
[3] User Library t5_strict_research.pdf (read pages 1-3, original C/S definitions, private heads and resource accounting). Original t5_strict_research_package.zip was not located through Library search this run; unseen files not asserted.
[4] Dąbrowski, Jonsson, Ordyniak, Osipov, "Solving Infinite-Domain CSPs Using the Patchwork Property", arXiv:2107.01428 (2021), background on structural parameterization and CSP treewidth; not a lower bound for T5.

P versus NP remains OPEN.