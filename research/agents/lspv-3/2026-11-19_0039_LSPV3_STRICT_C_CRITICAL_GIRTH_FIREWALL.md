# LSPV-3 | Strict cyclic T5: criticality, deletion witnesses, and incidence girth

**2026-11-19 00:39 America/Los_Angeles. Role: HYPERGRAPH/CERTIFICATES.**
**Status:** PROVED/EXACT restricted lemmas; COMPUTATIONAL independent finite verification; high-girth chromatic existence KNOWN THEOREM; general SAT-witness time lower bound OPEN. External mathematical peer review OPEN. P versus NP OPEN.

## Exact problem and candidate

The active predicate is strict directed-cycle T5, not historical Q or O/P:
\[
R(a,b)\iff(b-a)\bmod5\in\{1,3\},\qquad
\mathcal C(x,y,z)=R(x,y)R(y,z)R(z,x)\vee R(x,z)R(z,y)R(y,x).
\]
Every clause has three different variable names, and its values must differ, but names in different clauses may share values. Exactly 30 of 125 ordered triples satisfy C. The current claim, C-CRITICAL-GIRTH-FIREWALL1, is a direct criticality/girth transfer from graph 5-colorability, together with an exact failure of incidence-girth preservation for the alternative three-C gadget. Falsifiers: an unsatisfied deletion witness; an unsound source-to-head projection; hidden 4-cycles in a girth-preserving claim; an uncharged 5-coloring oracle; treating criticality as an arbitrary execution lower bound.

## Theorem 1: direct strict-C private-head graph transfer (PROVED/EXACT)

For a simple graph G=(V,E), introduce a fresh private head h_e for every e={u,v} and set
\[
F_C(G)=\bigwedge_{e=\{u,v\}}\mathcal C(h_e,u,v).
\]
Exact finite predicate calculation gives
\[
\exists h\ \mathcal C(h,u,v)\iff u\ne v.
\]
There are two completing heads if u,v have cyclic pentagon distance one, one if distance two, and none if equal. Thus F_C(G) is SAT iff G is 5-colorable; F_C(G)-C_e is SAT iff G-e is 5-colorable. In particular, F_C(G) is clause-minimal UNSAT iff G is edge-minimal non-5-colorable. Every deletion witness consists of a five-coloring of G-e plus a valid private head on every retained edge.

If G is connected with undirected graph girth g, the *clause-incidence graph* of F_C(G) has girth exactly 2g: each original edge u-v becomes u-C_e-v, and every private head is an incidence leaf. The C primal graph always contains triangles, regardless of source girth. Every compared unordered pair occurs in only one constraint, so its complete orientation-XOR relaxation is feasible, with independently chosen cyclic comparison orientations. This is not a complete five-letter assignment.

For any shared row z coloring original vertices, one can identify a refutable block by scanning edges for z(u)=z(v), O(|E|) comparisons. For a graph of chromatic number 6 every row has at least one such block. If G is edge-critical, every edge e has a deletion coloring with only that edge monochromatic; hence the row/block obstruction matrix has an |E|-by-|E| identity submatrix. Its rank and minimum original-block cover size are |E|, **yet the source-recognized selector is linear time per supplied row**. The full domain has 5^|V| rows and does not meet the separately specified polynomial-row budget.

## Theorem 2: local strict S/C rewrites preserve SAT but can destroy girth (PROVED/EXACT)

The exact verified translation from strict designated-head S is
\[
S(h,u,v)\iff\exists p,q:\ C(h,u,q)\land C(h,q,p)\land C(h,p,v).
\]
The first two C clauses share both h,q; the last two share h,p. Consequently every such gadget contains a 4-cycle in its clause-incidence graph. The reverse C-to-S definition, C(h,u,v)=S(h,u,v) AND S(u,h,v), repeats an entire triple scope and likewise contains incidence 4-cycles.

**Additional clause-criticality statement:** take a 6-edge-critical G, encode each edge by one private-head S clause, then replace that clause by its three-C gadget. This expanded C instance is also clause-minimal UNSAT, but its incidence girth is **exactly four**.

Proof: full UNSAT follows by projected-solution equivalence. Given one removed C clause from the gadget for edge e, take a five-coloring of G-e. Its endpoints u,v must have the same color a, else G itself would be five-colorable. Fix any h!=a. The C-link graph at head h is a four-vertex path, where a has a neighbor. When the first C clause is removed, choose a two-edge walk q-p-a in the link path; when the middle is removed, choose any neighbors q,p of a; when the last is removed, choose a-q-p. These satisfy the other two clauses even with u=v=a. All other graph edges are properly colored, so their complete S-to-C gadgets extend. Thus every individual C deletion is SAT. QED.

For a source graph with v vertices and m edges, the direct C encoding has v+m variables and m clauses; the three-C expansion has v+3m variables and 3m clauses. **Local S/C equivalence and linear-size reductions do not preserve a growing incidence-girth promise.** The old Q deletion counts and solution numbers cannot be relabeled as C results.

## Theorem 3: growing-girth intrinsic C obstructions exist, but generation and acquisition are not cheap (KNOWN + PROVED TRANSFER)

Erdős's high-girth/high-chromatic theorem gives, for every integer g, a finite simple graph with girth at least g and chromatic number at least six. Delete edges while maintaining non-five-colorability and discard isolates. The result K_g is connected, edge-minimal non-five-colorable, has chromatic number exactly six and retains girth at least g. Therefore F_C(K_g) is connected, clause-minimal UNSAT, has clause-incidence girth at least 2g, and every individual C deletion has a full strict-C witness.

A uniform terminating construction can enumerate graphs, perform exact exhaustive five-colorability checks, extract a critical subgraph and enumerate witnesses. **It is not a polynomial-time source generator or witness finder.** Every such critical graph has minimum degree at least five: a degree-at-most-four vertex could be removed, five-colored, and reinserted with an unused fifth color. The standard Moore BFS counting therefore gives exponentially many vertices in the girth parameter. Vertex counts and girth alone give no machine-time lower bound.

## Explicit family and verified finite controls

For odd t>=5, put G_t=Mycielski^3(C_t). The inherited chromatic and edge-critical construction gives
\[
|V(G_t)|=8t+7,\quad |E(G_t)|=46t+6,\quad \chi(G_t)=6,\quad g(G_t)=4.
\]
The direct C lift has 54t+13 variables, 46t+6 clauses, incidence girth eight; the three-C expansion has 146t+25 variables, 138t+18 clauses, incidence girth four. Every deletion has a recursively constructed source 5-coloring plus heads/auxiliaries. There is no SAT advice or hidden answer oracle.

A new standard-library Python construction and two independently implemented strict C evaluators ran successfully:

| Odd t | Direct C clauses | Direct deletions verified | Three-C clauses | Three-C deletions verified | Incidence girth |
|---|---:|---:|---:|---:|---|
| 5 | 236 | 236/236 | 708 | 708/708 | 8 vs 4 |
| 7 | 328 | 328/328 | 984 | 36 sampled | 8 vs 4 |

Total **1,308 full C deletion witness vectors**, **698,660 surviving original C clauses checked true**, and **1,308 deleted clauses checked false**. A second validator, using strict cyclic distance triples instead of the original R function, rechecked every certificate and every retained clause. The initial run took 7.93 wall seconds and had 6,770,421 bytes peak tracemalloc allocation; the independent replay took 2.49 seconds with 8,290,218 bytes peak tracemalloc. These are CPython trace figures with in-memory certificate accumulation, not a mathematical bit-space lower bound. Complete witness vectors occupy an independently verified 84,926-byte gzip file. The run is deterministic with no seeds.

Main full script SHA256: 8be5b7dadc24052d384fc841a4871ed903c48216fa8971df6b35268c5af2f5e2. Independent checker: 056f8380bd6658259fc81073f0658c623385d0f28b2dd948b3f5c99012805467. Witness archive: 6d9718bb8eff63a7b574eb166959ae40b4fdae704d06bd759cd2ac91e1e40f6e.

Independent source archive verification was rerun on the user-supplied exact-title strict package: 30 C tuples, 40 S tuples, all eight unpinned binary relations and extension multiplicities 85/10/20/10 PASSED. Its separate million-subset six-variable grid was **not repeated**.

**New exact count:** For the direct strict C lift of K6 with any one clause removed, G-e has exactly 5!=120 proper 5-colorings. Each has seven retained graph edges at cyclic distance one and seven at distance two, so heads contribute 2^7, while the deleted head has five free colors:
\[
\#\mathrm{SAT}(F_C(K_6)-C_e)=120\cdot2^7\cdot5=\boxed{76,800}.
\]
There are 15,360 global-five-rotation orbits. Independent exhaustive 5^6 enumeration confirmed this count. This number is genuinely C-specific and cannot be substituted from Q or S.

## Resource, advice, and transfer audit

A direct row/block scan on the separately supplied layout R<=N^.195, B<=N^.65, local size<=N^.35 costs N^(.845+.35a+o(1)) for child decision time m^a, before row preparation, source reads, failed attempts, candidate acquisition, negative-child certification, materialization, complete witness outputs and peak live state. Achieving N^1.33 requires a<=97/70 in that simple scan. An unspecified polynomial SAT decider provides no such exponent, and repeated per-row materialization can add N^1.195. The recognized Mycielski C witness family is a restricted polynomial source language, not an unrestricted SAT/C decision algorithm.

SAT correct paths output and verify all required original-variable colors. UNSAT requires a sound cover for *every* shared assignment, not one refuted row; a negative child index alone is not an UNSAT proof. A supplied polarity or k correct-path bits are answer advice until acquired. Exhaustive deterministic path enumeration may require 2^k complete charged replays and child calls. A universal alternating strategy is not one existential trace.

For general SAT, FLMV (JACM 2005) give deterministic random-access DTISP(N^c,N^d) exclusions for c below the golden ratio with sufficiently small positive d, and distinct co-nondeterministic results for c below sqrt(2). Buss and Williams (2015) analyze the general-SAT alternation-trading boundary near (c,d)=(1.34070,.5). Neither transfers to this critical C promise without a full source-to-general-SAT model and resource preserving reduction. Resolution lower bounds, graph chromatic rank, girth and obstruction-cover size also do not transfer to unrestricted executions.

Four gates: DISJ PASS (no direct-sum inference); relativization OPEN for separation-strength use; simultaneous DTISP OPEN for an arbitrary algorithm and NOT APPLICABLE to the structural proof; deterministic configuration counting NOT USED as a lower bound. Compact source recognition, graph recoloring, algebraic/flow shortcuts, treewidth dynamic programming, renaming and recomputation remain legitimate.

## Exact next target

C-GIRTH-CRITICAL-WITNESS-ACQUISITION2 (OPEN): build a uniformly efficiently generated or source-recognizable sequence of strict-C clause-critical instances with **growing clause-incidence girth** and certified deletion witnesses, then find a source-bound residual compatibility obstruction surviving the direct graph-coloring interpretation, local S/C conversions, symbolic recoloring, GF(5), flow, treewidth and compact circuits. Do not use the three-C gadget for girth claims. The current theorem proves existence and a low-girth explicit family, not an unrestricted superpolynomial witness-time lower bound.

## Primary references

[1] P. Erdős, Graph Theory and Probability, Canadian Journal of Mathematics 11 (1959), 34-38. High girth and high chromatic number.
[2] J. Mycielski, Sur le coloriage des graphes, Colloquium Mathematicum 3 (1955), 161-162. DOI 10.4064/cm-3-2-161-162.
[3] L. Fortnow, R. Lipton, D. van Melkebeek, A. Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6) (2005), 835-865. DOI 10.1145/1101821.1101822.
[4] S. Buss, R. Williams, Limits on Alternation-Trading Proofs for Time-Space Lower Bounds, Computational Complexity 24 (2015), 533-600. DOI 10.1007/s00037-015-0104-9.
[5] User-supplied t5_strict_research_package.zip, Library ID libfile_c54ef1e6d1708191832284d429b595b0, original gadget and resource audits.

No schedule, enabled/paused state, title, role ownership or historical manuscript was modified. P versus NP OPEN.


## 9. Source-bound specialist addendum: no supplied missing-clause index (COMPUTATIONAL + RESTRICTED)

A standalone deterministic specialist has now been implemented and **executed** on literal canonical sources. Its input is a header T5C-MYC3 with odd parameter t plus all physical source C clause records in canonical order, either complete or with exactly one source clause omitted. The input carries **no deletion index, polarity flag or SAT/UNSAT advice**. The specialist parses the entire source, reconstructs the expected Mycielski^3(C_t) clause stream, and identifies a unique missing clause from actual input differences. A full exact source receives UNSAT with the short theorem-specific chromatic certificate; a single deletion receives SAT with the full vector of original-variable and private-head colors after an independent original-clause verifier pass. Malformed, forged, extra-clause, truncated and noncanonical inputs receive UNKNOWN.

The standalone executable is at experiments/t5/lspv3_strict_c_canonical_specialist_20261119.py; its exact selftest ledger is at results/raw/t5/2026-11-19_LSPV3_STRICT_C_SOURCE_SPECIALIST_SELFTEST.json. A completely independent source-pattern replay on t=5,7 reported **2 full UNSAT sources, 564/564 discovered SAT deletions, 162,716 retained original C clause checks and 8/8 malformed UNKNOWN controls**. Python peak traced allocation was 241,964 bytes and wall time 6.03 seconds. The script SHA256 is 92f327b16498d8ed156b4a4e826076eb424615b0caee016835668bfe46994df2. Full code and source-level evidence are also in the user-downloadable run ZIP.

**Correct scope:** the specialist is polynomial for a precisely recognized promise family, with O(t) physical clause parsing, O(t) word-size witness construction and verification, O(t) word working storage for the declared implementation plus actual complete witness output. It is **not** a total SAT or strict C decider, and the UNSAT response is justified by the Mycielski chromatic theorem only after complete source validation. Soundness for arbitrary source encodings remains UNKNOWN, not silently assumed. The canonical recognition itself is charged and the fixed per-pair head search is at most five trials.
