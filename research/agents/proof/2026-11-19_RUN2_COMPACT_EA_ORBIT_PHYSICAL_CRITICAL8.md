# Proof-lead: compact physical strict-C three-orbit cover (2026-11-19, run 2)

**PROVED**, with exact finite enumeration and two independent original-predicate checkers. **OPEN**: asymptotic resource implications and P versus NP.

## Theorem 1: seven-name, five-clause projection (PROVED)

Canonical strict T5: R(a,b) iff (b-a) mod 5 in {1,3}; C(x,y,z) iff R(x,y)R(y,z)R(z,x) OR R(x,z)R(z,y)R(y,x). All clause names distinct, no global injectivity. C accepts 30/125 triples.

Let two terminals be names 0,1, and define the physical five-clause gadget

```
G = C(0,2,3) & C(0,2,4) & C(1,2,5) & C(1,5,6) & C(3,4,6).
```

**Exact projection:** `exists variables 2..6 G` iff `(z1-z0) mod 5 in {0,1,4}` (equality or cyclic adjacency). By the ten D5 color automorphisms, the 25 terminal pairs reduce to the three canonical cases (0,0), (0,1), and (0,2). Exhaustive evaluation of all 5^5 private tuples gives respectively **4, 2, and 0** solutions. The full private tuples for the 4 and 2 cases are:

```
(0,0): (1,2,4,4,3) (1,4,2,4,3) (4,1,3,1,2) (4,3,1,1,2)
(0,1): (4,1,3,0,2) (4,3,1,0,2)
(0,2): no tuples
```

These are all evaluated using the original R/C predicate, not historical S/Q/P variants. Independent unordered-consecutive-triple implementation agreed on all 125 triples. All 2^20 = 1,048,576 original-C subformulas on six names were exhaustively enumerated; none has this E-plus-adjacent projection. Thus **seven names are minimal** in this no-pin original-C language. A further scan found no 4-or-fewer-clause realization on at most eight names, but no general minimum clause count is claimed.

The previous `LEAD_D5_PP_REALIZATION_ORBIT_HELLY` report used a 35-name categorical-power block to realize the same binary projection. This is an actual 7-name/5-clause replacement.

## Theorem 2: sharp physically clause-critical three-block UNSAT (PROVED)

Use three blocks with mutually disjoint private names:

```
F0 = G                                                        (5 clauses; private 2,3,4,5,6)
F1 = C(0,7,8) & C(1,7,8)                                      (2 clauses; private 7,8)
F2 = C(0,1,9)                                                 (1 clause; private 9)
F  = F0 & F1 & F2.
```

The three binary orbit classes for the terminals are E: equal, A: difference +/-1, B: difference +/-2. Compatibility projections are:

| Block | E | A | B | Entire block's satisfying assignments |
|---|---|---|---|---:|
| F0 | yes, 4 extensions | yes, 2 | no | 40 |
| F1 | yes, 6 | no | yes, 2 | 50 |
| F2 | no | yes, 2 | yes, 1 | 30 |

Hence F0 accepts E union A, F1 accepts E union B, and F2 accepts A union B. The intersection is empty, so the 10-name 8-clause **original strict-C source is UNSAT**. It is block-critical, attaining the sharp orbit capacity K(2) = (5^2+5)/10 = 3. More strongly, deletion of **any individual physical clause** makes F SAT: the independent checker verified these complete assignments in clause order (each fails exactly the deleted clause and satisfies the other seven):

```
0: 0 2 1 0 2 0 1 3 4 1
1: 0 2 1 2 0 0 1 3 4 1
2: 0 2 1 2 4 1 3 3 4 1
3: 0 2 1 2 4 0 3 3 4 1
4: 0 2 1 2 2 0 1 3 4 1
5: 0 1 4 1 3 0 2 0 2 2
6: 0 1 4 1 3 0 2 1 2 2
7: 0 0 1 2 4 4 3 1 2 0
```

The native incidence graph has girth **4**; this is not a growing-girth construction. The earlier 38-variable, 161-clause orbit-cover example was only block-critical and did not pass individual physical-clause criticality.

## Global obstruction-selector proof and limitation

For each shared assignment z=(z0,z1), deterministically select F2 if z0=z1, F1 if difference +/-1, otherwise F0. This selects a block with no private extension for **every** z. To be a source-verifiable UNSAT certificate, the original eight source records must be checked and each selected block's claimed incompatibility authenticated, e.g., by exhaustive enumeration of its at-most-5 private variables. Merely emitting a block index is not a refutation. The three orbit representatives symbolically cover all 25 assignments because C is D5 invariant. This fixed tiny fixture is trivially easy for a source-aware algorithm.

**Not a fit to the asymptotic layout:** R<=N^.195 explicit rows, B<=N^.65 blocks, and <=N^.35 *encoded child length* do not follow from this finite 10-name source. It has 5 private names in F0 and incidence girth 4. Padding is not a legitimate preservation of physical clause-criticality. It establishes no SAT complexity lower bound.

## Lead synthesis: one credible unrestricted SAT bridge

The most promising connection is the prior explicit source-locally accessible 3-CNF-to-C reduction (`LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL`), which for v variables and m input clauses creates exactly 15+9v+39m C names and 10+7v+31m physical clauses. The outstanding **OPEN** gate is to match the input-bit/source encoding and *low-workspace* random-access translation of the SAT language used by the actual Buss-Williams theorem. Their 2015 paper, Figure 8.3, reports a refutation at SAT not in DTISP(n^1.34070,n^0.5). A uniform total T5 decider at (1.33,0.5) in a strictly compatible model would contradict this if source expansion/access were n^{1+o(1)} time and n^{o(1)} space. An n-size materialized expanded input would invalidate the space transfer. This excludes one *simultaneous deterministic time-space point*, not all polynomial algorithms and not P=NP.

Fully sequential R=N^.195 by B=N^.65 child enumeration with encoded child length <=N^.35 and local exponent a costs N^{.845+.35a}; at global time 1.33, a<=97/70. A full source reread per row-block costs N^1.845, and an explicitly stored q-variable shared row uses Theta(q) bits, potentially more than N^.5. Both child polarities, unsuccessful branches, certificate acquisition/replay, source verification, complete output, and peak live writable workspace must be charged. Sound deterministic one-sided SAT or UNSAT specialists with uniform complete-on-one-polarity runtime bounds produce total deciders by timeout. Supplied polarity or successful nondeterministic paths do not.

## Audit artifacts and status

Canonical JSON serialization SHA256: `aeefe2472a0104f54c34ded1afccda85bc0f90cbe2f8c5e57b3d603d3bd9726f`. Deterministic source, **no random seed**. Complete reproducibility source, independent checker, 8 full witnesses, all 2^20 six-name scans and per-file SHA256 manifest in the conversation archive `T5C_ProofLead_Compact_Critical_Orbit_Run2_20261119.zip`.

**PROVED** projection, 10-name 8-clause physical criticality, sharp q=2 global cover. **FALSIFIED** prior *necessity* of a 35-name gadget for E-plus-adjacent binary relation. **OPEN** efficient growing-q source-uniform constructions and arbitrary-SAT resource consequences. **P versus NP remains OPEN**.

References: [1] Buss & Williams, *Limits on Alternation-Trading Proofs for Time-Space Lower Bounds*, Computational Complexity 24 (2015), https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf; [2] Zhuk, *A Proof of the CSP Dichotomy Conjecture*, JACM 67 (2020), DOI 10.1145/3402029. Previously reviewed `t5_strict_research.pdf` pages 1-3 in the user's Library.
