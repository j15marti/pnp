# TMR-1/076 | 2026-11-17 17:55 PST | Full signed-3SAT image under source-derived T5 quotient: an exact easy high-rank family

**Owner:** TMR-1 / PNP Machine Model Lead. **Named dependency:** C1-T5-SAT-IMAGE-QUOTIENT-TRANSFER. **Status:** PROVED/EXACT for the explicitly defined composed image and family, independent external mathematical review OPEN. Finite implementations are COMPUTATIONAL. P versus NP OPEN.

## Candidate and falsifiers, fixed before source search

For every integer m>=1, let F_m be the canonical, explicitly encoded positive signed 3CNF with variables x_0,...,x_(3m-1) and m clauses (x_(3j) OR x_(3j+1) OR x_(3j+2)), j=0,...,m-1. Apply the already-verified signed-3SAT -> graph-3-coloring -> anchored undirected C5 -> parsimonious directed T5 chain (TMR-5/074, TMR-1/073, /072). Analyze the ACTUAL target graph D(F_m), rather than a schematic solver oracle. Quantifier: FOR ALL m>=1, for this one explicit family and one fixed canonical compiler.

Falsifiers: (F1) additional unintended transitive T5 triangles make the /075 quotient different from anchored C5; (F2) the 2-path/3-path completion weights, 10-anchor factor, or NAE color-module sum is wrong; (F3) the alleged source-to-raw-T5 easy algorithm requires a free unrecognizable decomposition or conflates an easy YES witness with exact counting; (F4) graph/witness/counter/output sizes or authentication costs grow superpolynomially on the same execution. No claim of a mandatory lower bound will follow from any positive rank.

## Exact theorem: arbitrarily large quotient feedback rank and polynomial-time exact count

Let G3(F_m), H(F_m) and D(F_m) be the successive authentic graph-3COLOR, anchored-C5 and directed-T5 source instances, with complete private internal vertices and arcs. Then

| Stage | Vertices | Edges/arcs |
|---|---:|---:|
| 3COLOR G3 | 3+14m | 3+24m |
| anchored C5 graph H | 17+76m | 20+100m |
| directed T5 graph D | 57+276m | 80+400m |

D is connected. Its original undirected feedback rank (cyclomatic excess) is **24+124m**, and rigid-triad contraction /075 has precisely one transitive triad per edge of H. It contracts every private T5 pair onto the appropriate source vertex with forced offsets +1,+3, recovering EXACTLY H with every C5 edge mask {1,4}. Thus the contracted quotient rank is **4+24m**, still unbounded and linear in m.

Nevertheless the exact number of original five-symbol assignments is the following **all-length identity**:

    #Hom(D(F_m),T5)
      = 120 * (8024832^m + 5038848^m + 8503056^m),  m>=1.

In particular m=1 gives 2,588,008,320 solutions; m=2 gives 19,450,785,496,135,680. The family is satisfiable for all m (disjoint positive clauses). Hence this is an exact COUNTING upper theorem and a definitive counterexample to promoting linear RAW or POST-TRIAD feedback rank into necessary exponential work on all image instances.

Further, the UNDIRECTED underlying graph of each D(F_m) has treewidth at most **21**, independently of m. Therefore the family admits an exact count from the raw, source-authenticated T5 graph in polynomial time by a uniform fixed-width decomposition finder and five-state tree-decomposition dynamic program. This latter claim does **not** require a compiler provenance descriptor, and does not promise polynomial time for high-treewidth arbitrary inputs.

## Proof with all interfaces

**3SAT to 3COLOR.** The TMR-5/074 compiler uses a global palette triangle T,F,B, pairs of Boolean literal vertices adjacent to B, and per clause one auxiliary Boolean splitter s with the exact identity

    (a OR b OR c)
       iff EXISTS s [NAE(a,b,s) AND NAE(not s,c,F)].

Each NAE predicate has a fresh triangle of 3 vertices joined respectively to its 3 Boolean inputs. For F_m, no original variables are shared between clauses, so G3 consists of one three-vertex palette and m private 14-vertex clause modules. Every module contributes 24 edges, and the palette triangle contributes three. The fixed Boolean splitter identity and reverse satisfying-witness map remain as established in TMR-5/074; this report independently constructs actual G3 objects, not merely the size formulas.

**Anchored undirected C5.** Add five anchor vertices inducing C5, a genuine length-two path from anchor a0 to every G3 vertex (one private intermediate, one original-vertex representative), and a length-three path for every G3 edge (two private intermediates). These give H counts 5+2|VG3|+2|EG3| and 5+2|VG3|+3|EG3|. Every homomorphism of the anchor C5 to C5 is an automorphism, 5 rotations times 2 reflections.

**Directed T5 and inverse.** For each ordered H edge u<v, introduce fresh z,w and arcs u->z, u->w, w->z, w->v. The first three form the unique transitive-triad relation z=u+1,w=u+3 (mod5); the fourth is precisely the undirected C5 adjacency v-u in {1,4}. No arcs between H-original vertices are created and no private auxiliary of one edge is shared with another, so the only feed-forward triangles are these private triangles. The unannotated weighted-Z5 DSU quotient on ACTUAL D recovers H bijectively, with no spurious root identification. The raw rank and quotient rank follow by direct edge/vertex counts above.

**Exact weighted 3COLOR formula.** Let p=(2,0,1,1,0) be C5 length-two walk counts from a0, and q=(0,3,1,1,3) be length-three counts. Fixing one of ten anchor automorphisms restricts every G3 vertex to the three relative colors {0,2,3}. A vertex colored 0 has path multiplicity 2; colors 2,3 have multiplicity 1. Every proper G3 edge between colors {2,3} contributes 3 path completions, while the other two unequal pairs contribute 1. Consequently, for arbitrary G3,

    #Hom(D(G3),T5)
       = 10 * SUM_{proper phi:VG3->{0,2,3}}
            2^{N0(phi)} * 3^{M23(phi)}.

Here N0 counts zero-colored original G3 vertices, and M23 counts G3 edges with endpoint colors 2 and 3. This formula already counts the full directed T5 witnesses because every subsequent C5->T5 edge gadget has exactly one extension.

**Closed-form module evaluation.** For palette colors (T,F,B), set vertex weight p(c)=2 if c=0 and 1 otherwise, and pair-edge weight q(a,b)=0 if equal, 3 for {a,b}={2,3}, 1 for the other unequal pairs. The palette factor P=p(T)p(F)p(B)q(T,F)q(T,B)q(F,B)=6 for all six permutations. Each of the four Boolean literal pairs in one clause module (three original variables, one splitter) contributes

    alpha=p(T)p(F)q(T,F)q(T,B)q(F,B).

Define the weighted NAE triangle transfer

    W(a,b,c)= SUM_{(x,y,z) a permutation of (0,2,3)}
       p(x)p(y)p(z)q(x,y)q(x,z)q(y,z)q(x,a)q(y,b)q(z,c).

A complete module has weight

    M(T,F,B)=alpha^4 *
       SUM_{a,b,c,s in {T,F}}
           W(a,b,s) * W(not s,c,F).

The explicit sixteen-term sum, each W containing just six permutation terms, yields this exact finite table, with the flipped-2-and-3 copies equal:

| (T,F,B) | alpha | inner sum | M |
|---|---:|---:|---:|
| (0,2,3), (0,3,2) | 6 | 6192 | 8024832 |
| (2,0,3), (3,0,2) | 6 | 3888 | 5038848 |
| (2,3,0), (3,2,0) | 3 | 104976 | 8503056 |

As the m modules share ONLY the palette and have disjoint other variables, each full weight is P*M^m. Summing the six palettes and multiplying by ten anchor automorphisms proves 120 times the sum of the three mth powers for every integer m>=1. These three finite module weights have separately executed exact implementations and are not inferred from fitting the first seven numerical counts.

**Treewidth.** Each clause module has 14 vertices and touches the fixed 3-vertex palette. A tree decomposition of G3 has one central palette bag and one bag of at most 17 vertices per clause, giving width <=16. Add all five C5 anchor vertices to those bags, yielding width <=21. Attach for each length-two or length-three path a small child bag containing its endpoints and private path vertices (at most four), and for each final T5 edge gadget a size-four bag containing both endpoints and its two private vertices. The original-vertex connectedness and edge-coverage conditions are preserved. Thus tw(D(F_m))<=21. Bodlaender's uniform fixed-k decomposition algorithm, followed by ordinary 5-state exact DP, gives an unannotated polynomial-time exact counter on this restricted family. The decomposition finder must be PAID; this is a positive upper bound only.

## Authentic encoding, physical ledger and actual checks

The input compiler uses unary n and m headers followed by three sign+low-first-address literal records per clause, authenticates every byte and rejects malformed records. On F_m, n=3m and the distinct clauses already have no unused variables. The output is a sorted full directed T5 arc list with unary nD/mD and low-first endpoint fields, no implicit edges. Source length L=3m+m+2+3m(1+w(3m)), and output length LD=nD+eD+2+2eD*w(nD), each O(m log(m+2)). TMR-5's independently proved generic source bound LD<3000L applies here as well. Witness maps include the split variables, triangle colorings, anchored path completions and uniquely forced T5 auxiliary labels.

A single conventional blank-start machine can read/authenticate the original source, recognize the F_m pattern with paid sorting and equality comparisons, construct/serialize D if requested, compute the three integer powers with O(m)-bit values, verify the output formula and emit the O(m)-bit exact count. Conservative joint bit-machine bound **T=O((L+1)^12), S_peak=O((L+1)^4)** includes unsuccessful checks, headers, indices, storage of original/constructed graphs, all table arithmetic, source/head moves and output. No simultaneous T from one run is paired with S from a different run. For arbitrary canonical T5 source, a uniform separate algorithm first authenticates source, finds a width-21 decomposition when one exists, and performs priced exact DP; its off-promise path may fall back to exhaustive search. No unsupported universal polynomial bound follows.

**Actually executed CPython3.13 local full-chain independent compiler and exact factor-eliminator:** 11 graph/formula cases, 1,512 assertions, seven malformed bit-string rejects, zero failures. Four signed authentic sources include one-clause YES (7 Boolean assignments, T5 count 2,588,008,320), two opposite unit-clause triples UNSAT (T5 count zero), a two-clause YES source (12 Boolean assignments, T5 count 280,634,406,727,680), and seven repeated copies of one clause (deduplicated output and identical count). The suite constructs all genuine T5 vertices/arcs (up to 537 vertices, 776 arcs in the distinct two-clause example), recovers all actual rigid-triad quotient edge masks and exact rank, and checks direct generic C5 sum-product variable elimination against source SAT YES/NO. Seven small genuine graph-3COLOR tests compare independent generic C5 variable elimination with the weighted 3COLOR identity. Separately, unbounded-m source-independent 3-state weighted elimination matches the closed form for m=1..7 with bag size at most four in the executed heuristic order. Executed source SHA-256: 762878c45201060c1efb69f4e0fbcd60b3ef2af5923d38900ba6ec4ebacb10dd. Local immutable raw SHA-256: a6751f1ff08f8611e2e13097550afa1de28f76a6368ab8773ebdbceac1e30f9f.

**PUBLISHED separate connected V8 certificate**, exact finite clause-module W computation, 25 four-arc endpoint checks, all six palettes and m=1..7:
- experiments/tmr/tmr1_t5_disjoint_clauses076.js, Git blob 8e679d394cc52260223662c69cd3f8fc01e9f99f, executed in connected V8, 58 checks, zero failures.
- results/raw/tmr/2026-11-17_1755_TMR1_T5_DISJOINT076_V8_RAW.json, Git blob 2e84bfa1a14bbf9a6092231c52dbbb0617fcd81b.
The larger independent full-chain Python source/raw are preserved as local run attachments, **not claimed GitHub-published**. No local repository checkout/preflight (GitHub DNS failure), full LaTeX build, independent Lean/nanoda kernel rebuild or independent external mathematical peer review was performed.

## Four gates, controls and exact inference

DISJ **PASS restricted**: this positive easy exact-count family is another countercontrol to static-cut or raw rank mandatory-work claims; no DISJ hardness inferred. Relativization **NOT APPLICABLE WITH REASON** to the fixed-template exact positive family; any all-NP nonrelativizing lower-bound transfer remains OPEN with BGS/algebrization/Natural Proofs safeguards. Simultaneous DTISP **PASS restricted upper ledger only**, no time-space forbidden pair or NP-superpolynomial consequence. Deterministic configuration counting **PASS as upper-bound safeguard only**, not a work lower bound or randomized/quantum claim. Source padding, equality, Horn/2SAT, affine/Fourier, Gaussian, treewidth, unique-witness, products, selectors, solver alternatives, arbitrary cheap recognition/caching and auxiliary uniqueness remain legal. /341 FAIL for full UNSAT; /386 RESTRICTED.

**Named dependency now CLOSED for this source family:** C1-T5-SAT-IMAGE-QUOTIENT-TRANSFER establishes exactly where /075 contraction stops on real SAT images and supplies a general family with unbounded residual rank yet cheap exact count. It does NOT establish a uniform tractable algorithm for arbitrary signed 3SAT images or arbitrary T5 inputs; no general necessity theorem follows. ONE NEXT load-bearing lemma: **C1-T5-MIXED-HARDCORE-SOURCE-AUDIT**. Build a canonical authenticated mixed YES/NO signed-3SAT source family whose T5 images remain high-treewidth after forced quotient and degree-two elimination, then test a charged direct source-recognition/structure-aware exact solver rather than extrapolating rank to mandatory runtime.

## Primary sources and pinned original corpus

Bang-Jensen, Hell, MacGillivray (1988), *Complexity of Colouring by Semicomplete Digraphs*, SIAM J. Discrete Math. DOI 10.1137/0401029. Garey, Johnson, Stockmeyer (1976), *Some Simplified NP-Complete Graph Problems*, DOI 10.1016/0304-3975(76)90059-1. Bodlaender (1996), *A Linear-Time Algorithm for Finding Tree-Decompositions of Small Treewidth*, DOI 10.1137/S0097539793251219. Repo originals: TMR-5/074 research/agents/tmr-5/2026-11-17_1542_TMR5_3SAT_T5_COMPLETE_CHAIN074.md, draft PR #209, and TMR-1/072, /073, /075 reports and exact JS implementations on draft PR #197. External mathematical referee remains OPEN.
