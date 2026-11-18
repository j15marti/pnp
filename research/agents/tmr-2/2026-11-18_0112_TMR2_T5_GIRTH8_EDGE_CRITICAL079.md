# TMR-2/079 | Explicit girth-eight edge-critical T5 refutation with PC and singleton-AC survival

Date: 2026-11-18 01:12 PST (America/Los_Angeles). Role: TMR-2 / PNP Information Necessity. Scientific status: **PROVED/EXACT FINITE CERTIFICATE**, pending independent external mathematical review; randomized search and performance observations are **COMPUTATIONAL**. No unrestricted time lower bound. P versus NP OPEN.

## Precise pipeline and dependency
Dependency **D2-T5-UGIRTH-EXPLICIT-SOURCE-AND-ADAPTIVE-COFACTORS**, advancing the *explicit NO source* portion of /078 and falsifying the idea that full PC + root SAC persistence forces expensive decision work.

Canonical original source (`p t5 n m`, ascending vertex declarations and sorted arcs) -> authenticate all source bytes and the 5-symbol R -> check connected bipartite girth-eight underlying graph -> generate an explicit same-skeleton YES orientation and full original-label witness -> independently check full binary path consistency and all root-singleton AC trials -> verify a complete domain-branching UNSAT certificate -> verify 44 edge-deletion SAT witnesses -> exact restricted conclusion.

Candidate: a 33-vertex 44-arc edge-critical T5 NO original source, with a same-skeleton YES orientation and indistinguishable *support-cardinality profiles* after full binary PC and 165 root-singleton AC tests each. This is a counterexample to local-consistency-profile-to-required-work transfer, not to an arbitrary T5 algorithm.

Predeclared falsifiers: F1 an ordinary T5 assignment satisfies the NO source; F2 the proof tree omits a branch or invokes an invalid arc-support pruning; F3 any edge-deletion witness fails an original arc or the graph has a short undirected cycle; F4 full binary PC or one-vertex-pinned AC detects the proposed NO; F5 the YES orientation is not on the exact same skeleton. All five passed the executed exact checks.

## Theorem 1: explicit finite certified critical obstruction
Let `D` be the 493-byte canonical original T5 file at

`research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5`

with SHA256 `0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac`.

Directly checked graph invariants:
- `|V|=33, |E|=44`, simple oriented, connected bipartite, **undirected girth exactly 8**.
- Undirected degree histogram: 14 vertices of degree 2, 16 of degree 3, 3 of degree 4. Cyclomatic number `44-33+1=12`; no isolated vertices.
- Source has zero T5 assignments: **Z(D)=0**. For each of its 44 arcs `e`, `Z(D-e)>0`. The proof record contains 44 original-label assignments, each satisfying ALL retained arcs and violating its omitted arc. Therefore the source is **edge-minimal UNSAT**.

The machine-checkable complete refutation is a finite labeled tree with **73 nodes, 36 exhaustive domain splits and 37 contradiction leaves**, after fixing `x_0=0`. The fixed root is without loss because for every `t in Z5`, `R(a,b)=R(a+t,b+t)`. For every split, the checker recomputes domains independently from the full original graph and verifies that *all currently possible colors* have children. For every leaf, it recomputes ordinary arc-support pruning from scratch and verifies an empty variable domain. Such deletions are logically sound, so the tree excludes every assignment. No external SAT oracle or prescribed internal search strategy is trusted.

Deleting every edge gives a positive witness verified by a direct scan of the remaining 43 original arcs, rather than trusting a search engine's SAT status. The same undirected skeleton reoriented consistently from bipartition class 0 to 1 is YES, witnessed by labeling left vertices 0 and right vertices 1; this is not a claim of a closed-form exact YES count.

## Theorem 2: local algorithms fail to reject either orientation
An independent explicit Boolean-matrix path-consistency implementation converged in **3 sweeps** for each orientation, deleted exactly **3,040** of the initial pair entries, retained exactly **22,205** ordered-color pairs over the `33^2` ordered variable pairs, and left no empty relation. The support cardinality for each pair is `5 min(d+1,5)` for distinct vertices at distance `d`, and 5 on the diagonal. This instantiates the /078 undirected-girth-eight path theorem, independently checked on every ordered pair and on BOTH source orientations.

Separately, ordinary arc consistency after pinning every one of 33 variables in turn to every one of the five colors gave **165 nonrejecting trials for NO and 165 for YES**. Thus full binary PC plus root singleton-AC does not decide the exhibited mixed source pair.

This is a **small finite obstruction to LOCAL consistency methods**. It does NOT give a superpolynomial lower bound for adaptive search, arbitrary exact solving, OBDDs, FBDDs or any Turing machine. Indeed the proof tree supplies a very cheap, source-aware decisive certificate for this NO input. The canonical Boolean accepting function of any UNSAT fixed source is identically zero, so static reduced-OBDD complexity of that final function is one, not a decision lower bound.

## Reproducibility and independent audit
Files:
- Source: `research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5`.
- Independent **readable standard-library** verifier: `experiments/tmr/tmr2_t5_33_verify079.py`, local SHA256 `395a1952b5a3e6d4bf71f4e92144e418fd2e4ca5d1062756f058f1651efe20f5`.
- Full proof tree, 44 deletion witnesses and exact measurements: `results/raw/tmr/2026-11-18_0112_TMR2_T5_33_GIRTH8_CERT079.json.gz.b64`. This is gzip of immutable JSON, then base64, to preserve exact UTF-8 bytes. Original JSON SHA256 `5feb2a17fe9d40b097a6e168ae1e4aaede0a6fbe81ee40650e8d2a2bee00fd0c`, 20,783 bytes. The verifier reads the base64 directly and decompresses it, requiring no special tools.
- Execute, without Python `-O`: `python experiments/tmr/tmr2_t5_33_verify079.py research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5 results/raw/tmr/2026-11-18_0112_TMR2_T5_33_GIRTH8_CERT079.json.gz.b64`.

The source was discovered by explicitly generating the GF(3) symplectic generalized quadrangle W(3,3) point-line graph with 80 vertices, 160 edges, 4-regular undirected girth 8; orienting randomly (Python `random.Random`, seed `202611180214`); and greedily deleting arcs while maintaining UNSAT by a separate C++ arc-consistency/backtracker. The run tested 26 deterministic orientation/deletion seeds and selected the smallest source by vertex count. This discovery method is heuristic and is not part of the logical certificate. The original 33-vertex source is published fully, independent of generator reproducibility.

**Executed independent audits:** separate locally compiled C++ solver reported UNSAT on the final 33-vertex source in 151 unpinned search nodes, 85 failed branches; the Python proof producer with distinct queue-based AC reported 73 root-pinned nodes; the published Python verifier independently reconstructs the full 73-node certificate using global fixed-point support sweeps, checks all 44 edge-deletion witnesses, 330 singleton trials and both path-consistency matrices. Negative test: deliberately deleting a branch of the proof causes checker rejection. All final audits passed. Full conventional machine microtracing, formalized proof checking and independent mathematical referee review were not done.

## SAME-REALIZATION source and work ledger
The published verifier starts blank from the encoded source and compressed proof record; charges reading/decompression, canonical parsing and hash, every source arc, graph checks and BFS edge-removal girth tests, 73 separately recomputed arc-consistency nodes, proof-tree branch coverage and reconstruction, 44 complete deletion-witness scans, 330 root-pinned AC tests, two explicit full PC closures, integer masks, caches and output. Five colors remain fixed and all internal objects are polynomial in source length plus proof-record length. A deliberately conservative bit-machine upper bound for this *certificate-verification algorithm* is polynomial in the combined source and certificate length (e.g. `O((L+B+1)^9)` time and `O((L+B+1)^4)` peak writable bits, charging decompression and all witnesses); it is not a mandatory cost for all solvers. No polynomial NO-certificate construction on arbitrary T5 sources is claimed. The C++ producer is finite experimental evidence; the Python verifier independently checks semantic coverage.

## Four scientific gates and safeguards
DISJ: **PASS restricted** for the finite source; **FAIL** any claim that many local supports or static rank necessitates general work. Relativization: **NOT APPLICABLE** for the finite certificate; **OPEN** for any proposed P-versus-NP separation (Baker-Gill-Solovay, algebrization and Natural Proofs remain open obstacles). Simultaneous DTISP: **PASS upper only** for this single verifier, no forbidden machine-pair inference. Deterministic configuration count: **PASS upper bound only**, not a lower bound and not randomized/quantum transfer. Cheap path/root AC, low-degree elimination, separators, affine/Gaussian, Horn, 2SAT, modules/twins, compact exact counting, caching, recomputation, source recognition, unique-solution ranks and all legal alternate algorithms remain admissible. /341 FAIL as full logical UNSAT authority; /386 RESTRICTED. P versus NP OPEN.

## Named dynamic invariant for TMR-4
**D2-T5-PC-SAC-73NODE-REFUTATION-TRACE.** Real source transitions: READ_BYTES/UTF8, PARSE_CANONICAL, VERIFY_GIRTH8_AND_BIPARTITION, PAIR_RELATION_INIT, PC_TRIPLE_REVISE, ROOT_PIN_AC, AC_SUPPORT_REMOVE, EXHAUSTIVE_BRANCH, EMPTY_DOMAIN_CERTIFY, ROTATION_NORMALIZE, EDGE_DELETE_WITNESS, SAME_SKELETON_YES, COPY_OR_CACHE, SOURCE_RECHECK, OUTPUT. This dynamic trace proves that the local fixed-point support persistence can coexist with a short complete decision certificate. Any lower bound from PC/SAC residual uncertainty needs an additional quantified reason that every legal competing algorithm must incur large work.

**ONE next load-bearing dependency:** D2-T5-EXPLICIT-HIGH-GIRTH-PRIME-DECISION-OBSTRUCTION. Seek connected YES/NO families whose NO half is source-certified and resistant not just to PC and singleton AC, but also to all low-degree eliminations, 1/2/3-separator transfers, exact orbit reductions and cheaply authenticated adaptive branching. Compare both-label counts, adaptive FBDD/OBDD and tensor contraction costs under precisely matched source interfaces. Explicit 33/44 is a finite benchmark and falsifier, not an asymptotic lower-bound family.

Environment: no checked-out repository was available for the project preflight; local experiment files and the exact Git blobs of the uploaded verifier, source and raw were compared, but full LaTeX compilation, physical Turing-machine replay, and external mathematical review were not performed. No schedule, identity, peer manuscript or retired tracker was changed.
