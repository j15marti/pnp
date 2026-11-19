# TMR-5/101: exact-one Q, tournament compatibility, and critical-family machine escape

**Date:** 2026-11-18 America/Los_Angeles. **Agent:** TMR-5, independent machine red team. **Verdict:** PROVED (scoped) / OPEN (unrestricted).

## Six-clause global-comparison obstruction

Define Q(x,y,z)=R(x,y) XOR R(x,z), with R(a,a)=false and the fixed tournament A>{B,D}, B>{C,E}, C>{A,D}, D>{B,E}, E>{A,C}. Different variable names may receive equal colors.

The formula
\[
Q(a,b,d)\land Q(a,c,d)\land Q(b,a,c)\land Q(b,c,d)\land Q(c,a,b)\land Q(d,a,b)
\]
is UNSAT in **every** loopless tournament. Its follower-disequality graph has exactly the edges ab,ac,bd,cd, so is an undirected C4 and hence bipartite. Every per-head XOR system is also bipartite and consistent. If a=d, clauses 1,2 force a to beat b,c; clause 3 forces b to beat c, contradicting clause 5. If b=c, clauses 3,4 force b to beat a,d; clause 6 forces d to beat a, contradicting clause 1. Otherwise all four values differ. Clauses 1,2 give p=R(a,b)=R(a,c); clause 3 gives R(b,c)=p while clause 5 gives R(c,b)=p, contradicting antisymmetry. No converse comparison is used before equality is excluded.

Independent enumeration of all 4,096 four-variable Q formulas gives 63 UNSAT formulas that pass both follower bipartiteness and head-parity checks, including exactly 36 inclusion-minimal formulas, all of size six. The displayed formula has 20,15,20,15,5,5 solutions after the six respective one-clause deletions. A separate census of every tournament on 1-4 values with every four-variable labeling made 17,065 exhaustive checks and found no model.

**Implication:** per-head parity plus a polynomial follower-bipartiteness check is NOT a sufficient global realizability test. The next filter must account for shared tournament antisymmetry, equality and eventually the exact five-color target.

## Infinite critical UNSAT family with a fast direct solver

For every odd L>=5, set H_L=M^3(C_L), three ordinary Mycielski lifts of an odd cycle. Mycielski raises chromatic number by one and preserves edge criticality; the latter is proved in the 1999 *Discrete Mathematics* paper cited below (Lemma 1) and independently implemented by three edge-deletion witness cases. Therefore chi(H_L)=6 and chi(H_L-e)=5 for every edge e. The exact recurrences n'=2n+1, m'=3m+n give n=8L+7 and m=46L+6.

Introduce one private head per graph edge and one Q clause Q(h_e,u,v). Since exists h Q(h,u,v) iff u!=v, this Q instance F_L is intrinsically clause-minimal UNSAT. It has N=54L+13 variables and M=46L+6 clauses. All M deletions have complete satisfying witnesses, and no proper clause subset is UNSAT.

On exactly the **same scopes**, the old P(h,u,v)=R(h,u) AND R(h,v) is SAT: label every original vertex A and every private head C, since C beats A. Thus this is a matched-scope separation, not a relaxation.

A **uniform sound canonical-family specialist** infers L from N, checks every ordered input triple against its on-demand Mycielski edge index, and accepts only an exact complete formula or its exactly one-clause deletion. Full match certifies UNSAT by the chromatic theorem. On a one-clause deletion it computes a color at any vertex using a constant-depth three-lift route, extends heads, verifies all clauses and streams a SAT witness. On canonical-order encodings, a single instance uses O(N) RAM word operations and O(log N) writable auxiliary **bits**, excluding read-only input and streamed output. The bound is algebraic for the fixed-depth streaming machine, not a Python RSS measurement. It does NOT include arbitrary variable renaming, clause permutations, or an all-input polynomial-time Q decision procedure.

### Exact verification

| Odd cycle L | H vertices | Q clauses | Q variables | All deletion witnesses tested | Incidence girth |
|---:|---:|---:|---:|---:|---:|
| 5 | 47 | 236 | 283 | 236 | 8 |
| 7 | 63 | 328 | 391 | 328 | 8 |
| 9 | 79 | 420 | 499 | 420 | 8 |
| 15 | 127 | 696 | 823 | 696 | 8 |
| 31 | 255 | 1,432 | 1,687 | 1,432 | 8 |

Two independent Python implementations generated and verified **3,112** deletion witnesses. The streaming implementation checked **2,871,608** retained Q clauses; the materialized implementation checked **2,874,720** Q clauses including the deleted clauses, plus the same number of graph-edge color predicates. The generic GAC Q solver on the L=5 full formula exhausted its 1,000-node cap (1,001 visits, 84,841 revisions, 832,686 support intersections) with status **UNKNOWN**, not UNSAT. Finite counters are not lower bounds. The entire 3,112-witness audit costs quadratic total work because it emits and checks thousands of separate witnesses.

The construction is not padding a fixed obstruction: every clause is critical. However, its canonical presentation exposes an efficient source-aware algorithm, so intrinsic criticality and lack of a small UNSAT core do not imply unavoidable decision or witness work.

## High-girth distinction and resource quantifiers

Erdos (1959) gives graphs of arbitrarily high *undirected* girth and chromatic number. Extracting an edge-minimal non-5-colorable subgraph and translating its edges by private-head Q yields clause-minimal UNSAT Q instances of arbitrarily high incidence girth. This is an **existence** theorem only, not a uniform generator, a search lower bound, or a fast deletion-coloring procedure. The explicit Mycielski family above has incidence girth **fixed at 8**.

For decomposed F(z,y)=AND_i F_i(z,y_i), SAT means exists z forall i exists y_i F_i; UNSAT means forall z exists i forall y_i not F_i. Free child polarity or a free selector does not constitute sound deterministic discovery. Every failed branch, child call, replay, verification and space buffer must be paid. For a supplied k-bit *verifiably sound* correct path, deterministic enumeration of all paths costs 2^k complete simulations. This family's source-aware route is computed and checked from the input and requires **zero answer advice**.

**PROVED:** six-clause parity-and-bipartite counterexample; Mycielski-derived infinite intrinsic critical family; exact P/Q matched-scope separation; canonical-family linear-time streaming witnesses, log-bit auxiliary storage; arbitrary-girth critical existence. **FALSIFIED:** parity+bipartiteness sufficiency and criticality/no-small-core as an unconditional machine-time proxy. **CONDITIONAL:** canonical input order/naming and the standard color-criticality theorem. **OPEN:** unrestricted algorithms, full CNF splitter, the n^1.33+o(1) time / n^.5 polylog space hypothesis, worst-case superpolynomial witness lower bounds, P vs NP.

## Reproducibility

Exact reference archive: \`T5_Exact_One_Experiments_2026-11-18.zip\` (\`libfile_00b4599c2cfc8191a859b757dad101a0\`), materialized and independently audited; the preexisting 2,320 + 600 matched solver runs were not repeated. The full report, independently executed Python scripts, raw summaries, SHA256 manifest and commands are in \`TMR5_101_exact_one_critical_machine_escape_evidence.zip\`, SHA256 \`bf6bd67be10986fdd0acacbbf1a28e5a4e415919610ce230603bd02e073e57f5\`.

References:
1. Mycielski (1955), *Sur le coloriage des graphs*, DOI https://doi.org/10.4064/CM-3-2-161-162.
2. *Circular chromatic numbers of Mycielski's graphs* (1999), Lemma 1: criticality is preserved; DOI https://doi.org/10.1016/S0012-365X(99)00033-3.
3. Erdos (1959), *Graph Theory and Probability*, DOI https://doi.org/10.4153/CJM-1959-003-9.
4. Brelaz (1979), *New Methods to Color the Vertices of a Graph*, DOI https://doi.org/10.1145/359094.359101.
