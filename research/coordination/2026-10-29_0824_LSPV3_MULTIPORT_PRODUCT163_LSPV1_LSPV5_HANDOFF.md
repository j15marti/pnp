# LSPV-3 MULTIPORT-PRODUCT163, 29 October 2026 08:24 PDT

**Scientific status:** PROVED/EXACT RESTRICTED conditional on a completely enumerated finite 15-variable source lemma; COMPUTATIONAL independent original-CNF controls; no kernel verification. General one-child contraction and P versus NP remain OPEN.

## Exact new result (full joint ports, not merely one module)

The authenticated connected 15-variable, 20-clause proper strict signed exact-(2,2)-3CNF source G has ports (a,b,c)=(x1,x2,x13), p=x4, with exact ternary projection R(a,b,c)=not a OR not b OR c. The two negative-p clauses are indexed C3=(not p OR A), A=not x9 OR not x11, and C4=(not p OR B), B=not x8 OR not x11. Remove BOTH clauses. Exhaustive 2^15 assignments show that in G° every satisfying p=0 assignment has A=B=0; the complete puncture signature (p,A,B):count is (0,0,0):153, (1,0,0):153, (1,0,1):85, (1,1,0):25, (1,1,1):119. Each of the seven valid ternary port assignments has a source witness with p=0. The source's 35-vertex variable-clause graph stays connected after the two p-to-clause incidences are deleted.

Make k disjoint copies G_i (k>=1) and connect them by a path, or a simple cycle for k>=3, swapping the negative p_i literal in outgoing C4_i with negative p_j in incoming C3_j. Optional complete variable-wide sign flips f_i on the three local ports. This changes no signed occurrence budget and makes one connected proper strict signed exact-(2,2) formula E_{k,f} with 15k variables, 20k clauses. For all 3k port assignments t_i, the complete exact joint projection is

    exists hidden E_{k,f}(t,hidden)  <=>  AND_i R(t_i XOR f_i).

Proof: the p=0 puncture implication plus both cross-edge clauses forces equal p at each edge, so all p_i coincide. Original local clauses are restored semantically. Conversely choose per-module p=0 source witness for every permitted local triple. Both original and swapped negative p clauses are then true. The product formula is the *exact* projection and has k ternary clauses, 7^k feasible assignments. Each factor violates majority closure, so the joint relation has no existential-2CNF representation. This is not a general SAT complexity result. Every unpinned E_{k,f} is SAT.

The full 4-port relation DOES NOT factor into its 3-port relation times a unary p marginal: the triple (1,0,0) and p=1 are separately feasible but their joint cofactor is empty. Thus unrestricted independence of local marginals is FALSIFIED.

## Verification and models

Untouched user Library Connected_Interface_Audit.zip materialized, its REPORT.tex and audit.py inspected, audit.py rerun; results byte-identical (SHA-256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca), 4,680 boundary subsets, 7,191 local-discovery checks, 139 brute-force comparisons. Its k<=4b, n<=3b+12bq applies to static partitions and clause-hitting only.

New standalone standard-library source audit: 32,768 exhaustive fixed-source assignments, 112 whole network grammar/sign patterns, 248 positive/negative source-certificate checks, independent original strict-exact22 incidence validation. Independent SciPy HiGHS original-physical-formula MILP: 960 pinned cofactors in 15 chunks of 64, 635 SAT with directly checked full assignments, 325 UNSAT solver controls. All pass. This is COMPUTATIONAL, not machine proof verification. All full-CNF tests are included in the archive; no extrapolation.

Constructive algorithm on recognizable grammar: parse and authenticate all 20k original source clauses, module membership, signs, cross-edge swaps, graph topology; retrieve fixed authenticated G° table; output k original-port ternary clauses; for SAT fiber produce and check every source witness; for negative boundary fiber identify an invalid local triple and provide source-indexed exhaustive table certificate plus the port-equality induction. It is not an LRAT proof for the whole formula and not a universal UNSAT certifier.

Conservative resource ledger on one same model at a time: indexed RAM O(N^2) time O(N) work bits, read-only input fixed-multitape O(N^3) time O(N) work bits, single shared read/write tape O(N^6) time O(N) total footprint, fixed universal machine polynomial time with explicit interpreter and output costs. No conversion of transport lower bounds into general SAT hardness. Certificate acquisition, construction, negative justification, preprocessing and failed invalid-grammar checks charged. The actual child of size k is an exact *projection* on this recognizable grammar, not an answer-equivalent recursively closed strict exact22 SAT child of size N^lambda.

## Corpus and primary sources

Prior LSPV-3 TERNARY-CLAUSE-PORT162 already established the first-module ternary relation, not the full simultaneous 3k-port product and internal double-hole closure. Earlier LSPV-2 TWO-SWAP-EXACT-PORT-TRANSPORT223 and CONNECTED-ALLPORT-COMPILER224 already give general pointwise transport and expansive all-port normalization. PARITY-PORT-FORGETTING225 gives a named-port physical-size obstruction. Code examined at GitHub: vardigroup/DPMC README.md (dd5f421e15fc), cuddorg/cudd/cudd/cuddBddAbs.c (62170e3b29aa), arminbiere/cadical/src/elimfast.cpp (0d6c00897acb), crillab/d4/preproc/Forgetting.cc (8f00f7397b70), lammich/lrat_isa/thys/LRAT_Checker_Impl.thy (e50d75e5cd75). OpenAI math/build/sections/06-recursion.tex (65bf0450f460) has a single quantum recursive call but its target Boolean oracle is not proven efficiently classically computable.

## Next LSPV-1 and LSPV-5 tasks

LSPV-1: determine whether there exists any *unconditional* all-ordinary-SAT method to discover a small, exact, source-authenticated moving interface with *all costs charged*, not merely one easy gadget grammar. LSPV-5: independently audit the double-puncture induction and check the negative-fiber verification does not hide an oracle or replace full UNSAT with only pinned UNSAT. Investigate a branching network sharing independent ternary interfaces with both satisfiable and unsatisfiable unpinned instances, including exact22 fanout and closure. If no, record a falsifier rather than a hardness theorem. Every existing role and staggered automation remains unchanged. P versus NP OPEN.
