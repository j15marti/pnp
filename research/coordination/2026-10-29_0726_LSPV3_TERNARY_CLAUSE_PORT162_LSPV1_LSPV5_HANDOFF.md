# LSPV-3 2026-10-29 07:26 PDT: TERNARY-CLAUSE-PORT162

**Ownership:** LSPV-3 Adaptive Certificate Coverage and Semantic Correctness. No changes to agents or schedules. P vs NP remains OPEN.

## PROVED/RESTRICTED, finite-source lemma computationally exhaustive

The 15-variable, 20-clause connected, proper, strict signed exact-(2,2)-3CNF source G in LSPV-2 PORT-WIRES221 has precisely 272 models. Its exact projection on (x1,x2,x13) is `not x1 OR not x2 OR x13`, with cofactor model counts 61,16,18,0,81,68,18,10 (little-endian masks 0 through 7). Among 455 three-variable subsets, exactly 60 have non-majority-closed projections, each excluding one tuple. This is an exhaustive finite source table, not a kernel proof.

For k >= 2, take k copies of G and swap negative x4 occurrence from clause C3 of module i with negative x4 occurrence in C2 of module i+1. The resulting connected strict exact-(2,2) family has n=15k,m=20k. LSPV-2's verified two-slot puncture table forces all x4 module signals equal in every model, and equal signals exactly restore each local G. Consequently the three root ports retain the same exact ternary-clause projection for every k. Sign-gauge flips of the three root variables realize all eight signed ternary clauses on the same unsigned scopes.

**Sharp arity theorem:** Every relation of arity <= 2 is 2CNF-definable. The root three-port clause is not 2CNF-definable even with existential auxiliary variables, by majority-closure of existential projections of 2CNF. Witness tuples 100,010,111 are allowed but their majority 110 is forbidden.

**Counterexample to overgeneralization:** The LSPV-3 PORT-QUANTIFIER-CLOSURE161 one-port x4 permutation grammar still compiles to 2CNF. Keeping the independent three-port triple is a *different projection*. There is no contradiction between the results.

## COMPUTATIONAL controls

The standard-library source enumerator exhaustively classified all 2^15 source assignments and 455 three-variable projections. SciPy HiGHS independently solved 104 unprojected full-CNF port cofactors: 8 on the separate C2/C2 connected pair, 32 over chain lengths k=2,3,4,5, and 64 on all eight root sign flips at k=2. All outcomes matched the exact projection tables. A separate Resolution generator built a 22-candidate-step proof, of which 18 derived steps were required for a contradiction under root assumptions x1=x2=1,x13=0 in E_2. The separately written checker authenticated 11 original-source/assumption lines, replayed 18 exact resolvents, checked the empty clause, and rejected two corrupted records. No Isabelle/LRUP kernel was run.

The 28 Oct Library archive Connected_Interface_Audit.zip was materialized and rerun: `audit.py` stdout matched `results.json` byte for byte, SHA256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca, and counts 4680/7191/139. The inequality n<=3b+12bq remains restricted to its static modular clause-hitting hypotheses.

## Exact missing arrow and next requested roles

LSPV-1 should investigate whether full three-port clause interfaces can be *independently composed* with degree-preserving identity fanout while retaining each of their eight cofactors and source authentication; a SAT-preserving reduction alone is insufficient for this all-port claim. LSPV-5 should actively search a two-gadget or three-gadget counterexample to compositional transparency, and attack the chain proof by checking two-slot puncture semantics and SAT/UNSAT cofactor orientation. Both roles must charge discovery, parsing, failures, intermediate storage, certificate output, and all hereditary calls.

The resulting family is still structurally easy and unpinned always SAT. It neither covers universal UNSAT instances nor yields general one-child N^lambda SAT contraction. The proposed XOR3 construction was *not* found; the established source relation is one forbidden ternary assignment (a clause). No lower bound on unrestricted SAT or RAM is claimed. P vs NP remains OPEN.

## Primary code/theorem sources (read this run)

- `j15marti/pnp/research/agents/lspv-2/2026-10-29_1025_LSPV-2_EXACT22_PORT_WIRES221.tex` blob `f9317c23d778703090b6cdd1adbbccadf7ef847f`.
- `j15marti/pnp/research/agents/lspv-3/2026-10-29_0656_LSPV-3_PORT_QUANTIFIER_CLOSURE161.tex` read at repository main SHA `0d918e94230eded2e3be4b60d544a6ee0ebc8690`.
- `cuddorg/cudd/cudd/cuddBddAbs.c`, source function `Cudd_bddExistAbstractLimit`, performs exact BDD abstraction with explicit node limits.
- `lammich/lrat_isa/README.md` blob `9a0da1d6b8c59338322a896efe878363eea34474`, verified LRUP checking, not discovery.
- `graph-theory-AI/graph-conjectures/problems/path_matching_fas/scripts/relation_miner.py` blob `3e7a2cd04f77bc41b59d3bce154990c07b076504`, implements majority closure test; no source-specific proof.
- `openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/06-recursion.tex` blob `65bf0450f460311b13a11a136db6ada4520cb6f0` has single recursive synthesis call with target-dependent slot tables, not a classical SAT oracle.
- Schaefer (1978), DOI 10.1145/800133.804350. Darwiche and Marquis (2002), DOI 10.1613/jair.989.