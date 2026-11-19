# Strict T5 witness Run8: complete two-anchor separator search
19 November 2026 Pacific. **P versus NP remains OPEN.**

## Theorem (PROVED)
For every legal strict-C instance F on n indexed names with m clauses, every fixed-letter pin map p, and every source whose clauses have a hitting set of at most two variable names, there is a source-uniform deterministic SAT/UNSAT algorithm using O((n+m)5^k) indexed-RAM operations and O(n+m) live writable words, where k is the number of unpinned names in an authenticated separator I=V(F_A)∩V(F_B). The algorithm outputs full original-C SAT witnesses or streams a source-indexed UNSAT certificate, and includes source parsing, decomposition discovery, both child polarities, all failed rows, reconstruction and verification. The output certificate may occupy Theta((n+m)5^k) words and must be charged. For unpinned F with I nonempty, translate one separator color to zero to use 5^(k-1) rows. It returns UNKNOWN, not an unjustified UNSAT answer, when no two-name hitting set exists.

Canonical strict C: colors Z5, R(a,b) iff (b-a) mod5 in {1,3}, C=R(a,b)R(b,c)R(c,a) OR R(a,c)R(c,b)R(b,a), accepting exactly 30/125 triples, three distinct names per physical clause. No Q/P/S substitutions.

**Discovery:** Every size-two hitting set intersects the first clause. For each of its three possible first anchors a, intersect the clauses not containing a to find at most three possible partner names b. In O(m) time enumerate all hitting pairs and both deterministic priorities for allocating doubly anchored clauses. Choose a decomposition with smallest resulting shared-variable separator. Every A clause contains anchor a, every B clause contains b.

**Correctness:** For a fixed separator coloring z, F extending z is satisfiable iff F_A and F_B, each pinned to z, are both satisfiable: their witnesses agree on all and only shared names I. Each pinned common-anchor part is decided exactly by source-indexed bipartition+2SAT (previously independently tested), and physical-C clauses are rechecked after gluing. Exhaustively checking z and keeping an actual UNSAT explanation from at least one child for every z proves full UNSAT. The implementation deliberately evaluates both children on every row; no supplied correct branch or polarity bit. Input is fully materialized and counted as writable O(n+m), so this is NOT the proposed O(N^0.5) global-space solver.

## Exact finite source (COMPUTATIONALLY VERIFIED)
The earlier known four-clause physically critical source, not a new source, is:
F = C(0,1,2)&C(0,2,3)&C(0,2,4)&C(1,3,4).
The discovered cover {0,1} decomposes A=first three clauses and B=last clause on I=(1,3,4). Exact physical-C projections have |π_I SAT(A)|=35, |π_I SAT(B)|=30 and zero intersection. This is an explicit source-level compatibility-information loss despite both blocks being SAT.

There are 125 possible separator assignments. Global color translation reduces to 25 normalized rows. Both children were solved on every row: 50 source-indexed proof/solution records, all independently replayed by the previous GF5-based proof checker. 12 rows have both children UNSAT, 7 refute B alone, 6 refute A alone; none has both SAT. An unrelated pin eliminates translation symmetry: 125 rows and 250 independently replayed child records. A forged implication source index is rejected.

Exhaustive 5^5 physical-C audit: original F UNSAT; deleting clauses 0,1,2,3 respectively has 20,20,20,90 full SAT witnesses. Complete deletion examples in variable order 0..4: [0,2,4,1,3], [0,1,4,2,3], [0,1,4,3,2], [0,1,2,1,1]. Deleted clause false and all remaining clauses true. Incidence girth 4. SHA256 source: 8d36c8f7f885f68d332c6b6f9b88b548aa1408e13c258696b9de61b24ad53b90.

Independent randomized source/pin/relabel controls, seed 2026111908: 650 tests n=4..6, 234 SAT and 416 UNSAT, all matching brute-force 5^n masks, with 67,334 separator rows charged. Unsupported 3-disjoint-clause source correctly UNKNOWN. One independent forged proof rejected.

A family formed by adjoining two fresh anchored K_(t,t) followers to the critical source has n=5+4t, m=4+2t^2, primal treewidth ≥t and the same separator size 3. Cases t=3,10,20,40 all refuted in 25 rows and every four core-clause deletion received a complete independently checked SAT witness. For t=40 n=165,m=3204, the measured implementation took 0.32 seconds for 50 child calls. The scaffolding is NOT physically critical, retains incidence girth 4, and is only an upper-bound control.

## Limits and handoff
**PROVED:** restricted source-uniform two-anchor algorithm and direct compatibility cover.
**FALSIFIED:** separate SAT answers suffice for the union, and large primal treewidth alone forces exponential search for every special source grammar.
**OPEN:** unrestricted strict-C polynomial witness algorithm; complexity when two-anchor separator k is unbounded; source-uniform decomposition for arbitrary strict-C inputs; the N^1.33-time and N^0.5-space resource goals; all unrestricted P-versus-NP conclusions. The Python implementation buffers O(n+m) writable words. Encoding and certificate output are charged.

Reproducibility bundle: T5C_Witness_TwoAnchor_Separator_Run8_20261119.zip, SHA256 198bab675e7a2f976c84d6da3573e2e2f8630c3b86e64bcd3765045b694f0c36. Contains the full report, solver, prior anchored child and independent checker, 25 and 125 row proof ledgers, test code and original-C witnesses, seed, results.json, SHA256 manifest. All previous anchored routines are included; the sole independent checker import was renamed.

Prior work reviewed: actual repository witness reports T5C_CYCLERANK_FEEDBACK_AND_TW30_WITNESS and T5C_FOURCOLOR_COLLAPSE_DISJOINT3CORES_RUN5; user's November 18 strict T5 research PDF read in Library. ZIP named t5_strict_research_package.zip was located but not text-readable in the Library. External background: Dechter (1999), Bucket Elimination, DOI 10.1016/S0004-3702(99)00059-1; Gottlob, Leone, Scarcello (1999), IJCAI, https://ijcai.org/proceedings/1999/57 ; Ganian et al (2019), arXiv:1907.12335. Separator conditioning is standard; no priority claim.
