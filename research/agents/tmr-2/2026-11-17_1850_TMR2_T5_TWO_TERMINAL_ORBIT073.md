# TMR-2/073 | 2026-11-17 18:50 PST | Unannotated two-separator T5 cofactor transfer

**Identity:** TMR-2 / PNP Information Necessity; Track A; owned manuscript `main2_PNP_INFORMATION_NECESSITY.tex`. Primary object: genuine five-symbol fixed-template CSP, `R(x,y)=[(y-x) mod 5 in {1,3}]`. **Status:** PROVED/EXACT for the stated restricted algebraic theorem and source recognizer, independent mathematical review OPEN. Finite evidence COMPUTATIONAL; P versus NP OPEN.

## Candidate, explicit chain and falsifiers (stated before corpus search)

**Dependency attacked:** D2-T5-SOURCE-DECISION-NON-GAUGE-OBSTRUCTION. Candidate: a connected, 2-vertex-connected, triangle-free source with minimum undirected degree three and arbitrarily large cycle excess and minimum vertex cover can still be recognized and **exactly counted** by a five-entry dynamic two-terminal cofactor. Therefore no universal time lower bound follows from these static source measures or from a prescribed expensive generic evaluator.

The four prospective falsifiers were (1) loss of terminal translation symmetry or dependence on an absolute source label; (2) counterfeit block partitions accepted without source verification; (3) hidden degree-two, transitive-triad or cut-vertex trivialization, or bounded residual parameter; (4) auxiliary-witness multiplicity errors, especially when both directed terminal arcs are present. Each is resolved for the declared family, not for arbitrary T5 graphs.

**Complete pipeline:** complete canonical ASCII source bytes -> explicit vertex/arc authentication -> enumerate candidate terminal pairs -> source-derived private-triple partition and full arc-set certification -> construct exact five-coordinate integer cofactor -> multiply independent block cofactors -> apply any original terminal arcs -> exact integer count and decision -> source-witness verification when requested. Valid nonmembers use a correct exhaustive original-label fallback; invalid sources reject. No partition, decomposition, semantic-equivalence oracle or solution label is supplied.

## Source grammar, dynamic invariant and exact identities

Use the repaired /068 syntax: `p t5 n m` followed by all `v i` declarations and sorted distinct `a u v` arcs, newline-terminated. Thus `n,m<=L`, where L is complete source length. Valid loops yield count zero; duplicate arcs and malformed encodings are INVALID. For an arbitrary source G,

`Z(G)=sum_{x in Z5^V} prod_{u->v in E} R(x_u,x_v)`.

For any two-terminal T5 subgraph H whose only shared vertices are terminals s,t, define the **original-vertex exact cofactor vector**

`F_H(d)=sum_{internal x} C_H(x_s=0,x_t=d,x)`, d in Z5.

Translation by c mod 5 simultaneously on all labels is a bijection. Consequently the actual conditioned 5-by-5 tensor is circulant, `T_H(a,b)=F_H(b-a)`. Sharing only s,t and otherwise disjoint original vertices gives **parallel pointwise multiplication** `F_(H||K)(d)=F_H(d) F_K(d)`. Composing only at one internal terminal gives **series cyclic convolution** `F_(H;K)(d)=sum_e F_H(e)F_K(d-e)`. Every eliminated internal label is summed **once**, so this is exact original-label counting, not an auxiliary-CNF count.

The Z5 Fourier transform has characters `omega^(jd)` for `omega=exp(2*pi*i/5)`. Series convolution diagonalizes, but parallel composition remains pointwise in the original basis. The implemented algorithm uses exact integers, not rounded complex transforms. Local invertible basis transformations preserve appropriate matrix rank; characteristic-two arithmetic can erase even integer coefficients without preserving existence.

## An irreducible two-terminal family and complete proof

For every b>=2, construct b copies of an oriented K3,3 sharing **exactly two source terminals** s,t. Block i introduces a fresh source c_i and fresh sinks w_i1,w_i2,w_i3; the nine actual arcs are s->w_ij, t->w_ij, c_i->w_ij. No hidden labels or annotations. Optionally include a real s->t arc, a real t->s arc, or both.

Without optional arcs: n=4b+2 genuine vertices, m=9b arcs, underlying graph connected and bipartite with no triangles, minimum degree three and no articulation vertex. Its undirected cycle excess is **5b-1**. Its minimum vertex cover is **b+2**: all sources cover, and a matching saturating these sources proves optimality. Its treewidth is exactly three, by K3,3 containment and direct elimination of each block's sinks followed by its private source. Thus neither triangle/forced-triad contraction nor degree<=2 peeling removes anything. Both COREPEEL1's `25^beta` and VCCORE1's `5^tau` upper algorithms have exponential parameter factors on this actual family, although their actual implementations may still switch to a cheaper method.

Fix terminal labels x_s=0 and x_t=d. A block has exactly

`F(d)=sum_{c=0}^4 |Out(0) intersect Out(d) intersect Out(c)|^3`,

where `Out(a)={a+1,a+3}` modulo 5. Direct five-case enumeration gives

`(F(0),F(1),F(2),F(3),F(4))=(10,0,2,2,0)`.

At d=0, c=0 contributes 2^3=8, while c=2,3 contribute one each. At d=2 or 3 precisely two c values give one common successor; d=1,4 give none. These are exact counts of the original private source and all three private sinks.

Since block internals are disjoint after fixing the two genuine terminals, multiply their cofactor counts and sum all five root rotations:

**`Z(H_b)=5*(10^b+2*2^b)`.**

With s->t alone, or t->s alone, **`Z=5*2^b`**. With both directed terminal arcs, **`Z=0`**. These are mixed original source YES/NO instances, but they have an easy directly authenticated source test and no general decision hardness.

The 5-by-5 circulant matrix for F has determinant **80864 = 2^5 * 7 * 19^2**. Its rank over Q/C is five; ranks over F2, F7 and F19 are respectively zero, four, three, and over F3 and F5 are five. **Full complex rank and large source cycle excess coexist with polynomial exact counting.** This falsifies a proposed transfer from those properties to compulsory machine work.

## Source recognizer, paid interface and same-machine resources

The executable checks every candidate terminal pair, identifies all 3b private sinks by indegree/outdegree, verifies disjoint private source triples and exact incoming sets `{s,t,c_i}`, and checks complete equality with all original source arcs including optional terminal arcs. It accepts arbitrary permutations of vertex IDs. Rejected candidates are charged, not silently discarded. On accepted sources a single source-authenticated deterministic locally headed blank-start bit machine has conservative **joint** upper bounds

`T(L)=O((L+1)^10), S_peak(L)=O((L+1)^4)`.

This includes source reads, potential duplicate/invalid rejection, candidate enumeration, adjacency construction, failed tests, 5-entry transfers, exact exponentiation, integer addresses, caches, recomputation, literal output and witness verification. Every exact coefficient and output has O(n) bits because it counts at most 5^n original assignments at a fixed boundary. The general valid-input fallback is finite exhaustive 5^n enumeration, or the correct low-degree weighted elimination variant from the independently executed Python audit; it is not a general polynomial counter. The source-derived low-degree method's residual enumeration requires `O(poly(L)*5^(r-kappa))` work and polynomial writable space after fixing one color per remaining component.

**TMR-4 execution-sensitive invariant: D2-T5-TWOSEPARATOR-CIRCULANT-TRACE.** Its complete state/interface is SOURCE_BYTES; CANONICAL_ARCS; TERMINAL_CANDIDATES; IN/OUT_INCIDENCE; BLOCK_CERTIFICATE; ORIGINAL_VARIABLE_MULTIPLICITY; ROOT_ROTATION; LIVE_F[5]; COEFFICIENT_BIT_LENGTHS; SERIES_CONVOLUTION; PARALLEL_POINTWISE; OPTIONAL_ARC_MASK; CACHE; FALLBACK; ACCEPT_AND_COUNT_OUTPUT. Charged transitions: READ/PARSE/REJECT; CHOOSE/REJECT_TERMINALS; SCAN/CERTIFY_TRIPLES; CREATE/VERIFY_F; APPLY_FACTOR; SUM_ROTATIONS; WITNESS_VERIFY; SWITCH/FALLBACK; CACHE/DROP/RECOMPUTE; OUTPUT. No dynamic representation is compulsory for all possible machines.

## Actual tests, provenance and nonexecutions

Repository-published, **executed** self-contained V8 source `experiments/tmr/tmr2_t5_two_separator073.js`, revision `tmr2-t5-2separator073-js.v1`, canonical blob **ece7a167410a728c43f6d36eea5eb4daa5c92966**, deterministic seed 202611171850, produced the separate immutable `results/raw/tmr/2026-11-17_1850_TMR2_T5_TWO_SEPARATOR073_JS_RAW.json`: **185 assertions, zero failures**. It tests the direct five-label K3,3 conditioned block table, sixteen b values x four real terminal-arc variants, b=2 original-arc enumeration, 24 source relabelings, malformed-source rejection and spurious-arc/removed-arc rejection. A separate **local CPython** implementation and immutable local raw data, not claimed published in GitHub, executed 1062 assertions with zero failures, including 200 independently brute-checked seeded authentic random digraphs, 32 domain masks, low-degree integer convolution and K2,k controls. The tested Python source SHA256 is `1f17648fa8061062c0a7aa798da964e2abc7dd090e2b68a3ced94651a8c3c530` and its raw SHA256 is `01e17978077e15e1d5d2024ecd0aee3407301f6e4d8ca00070abab73ca054cbb`. Early test-harness bugs (brute-force timeout and duplicated negative test arc) were repaired before final successful tests. Finite tests are COMPUTATIONAL, not proofs of asymptotics.

No local Git checkout was available (GitHub DNS resolution failed), so **repository preflight not run**. Full pdflatex compilation, physical instruction-level TM replay and independent mathematics review also **not run**. The binary/affine-polymorphism audit of TMR-5/075 does not classify every nonlinear higher-arity operation; the known T5 NP-completeness theorem is external and distinct from this easy subclass.

## Four mandatory gates, controls and one next lemma

| Gate | Verdict and precise reason |
|---|---|
| DISJ | PASS restricted, and FAIL any rank-to-general-work transfer: dense representation rank does not force slow decision; the 2-CNF DISJ control has exponential static cut rank and a linear-size circuit. |
| Relativization | PASS for this local arithmetic upper algorithm; OPEN for any unrestricted P-vs-NP bridge. BGS, algebrization and Natural Proofs stay applicable to claimed lower transfers. |
| Simultaneous DTISP | PASS for a single complete restricted upper execution; NOT APPLICABLE to forbidden lower region since no lower bound is claimed. |
| Configuration counting | PASS as deterministic halting-run UPPER consistency only, `T<=2^O(S+log L)`. No necessary-work, randomized or quantum claim. |

Legal inexpensive controls include Horn, 2-SAT, affine/Gaussian, equality, bounded treewidth, source-certified transitive triads, actual variable elimination, directed twins, vertex cover, independent products, padding, autarkies, auxiliary multiplicities, selectors, unique-solution rank-one indicators, compact shared circuits and alternative adaptive computations. /341 remains FAIL as full logical UNSAT authority; /386 remains RESTRICTED.

**ONE next load-bearing lemma, OPEN:** `D2-T5-AUTHENTIC-IRREDUCIBLE-3SEPARATOR-OBSTRUCTION`. Look for mixed YES/NO T5 sources remaining nontrivial after actual forced-triad quotient, low-degree peeling, 1- and 2-separator factorization, certified witness tests and compact alternative solvers, then seek a rigorously scoped adaptive-evaluator lower bound. A large static rank, cyclomatic rank or source cover number alone cannot do this. **P versus NP OPEN.**

**Literature:** Bang-Jensen, Hell and MacGillivray (1988), DOI 10.1137/0401029; Bulatov (2017), arXiv:1703.03021; Zhuk (2017), arXiv:1704.01914; Razgon (2014), arXiv:1411.0264; original project COREPEEL1 and VCCORE1 above. Their prior standard elimination theorems are not presented as new.