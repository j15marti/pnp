# LSPV-2: Strict-T5 C circuit compilation and actual deletion-batch materialization
2026-11-19 America/Los_Angeles. Owner: PNP SAT-Circuit Reduction Builder, historical Route A. **PROVED/EXACT local identity; COMPUTATIONAL circuit measurements; unrestricted P versus NP OPEN.**

## Candidate and falsifiers
Compile strict C into a five-color occupancy circuit using original source variables and exact one-hot label pins. Falsify by (1) disagreement on any of 125 triples or 32,643 malformed one-hot masks; (2) higher physically serialized costs than shared tournament-comparator compilation; (3) a false deletion selector passing; (4) a dense source in which tournament comparison sharing beats occupancy. Falsifier (4) **succeeds**, so no universal method ordering is claimed.

## PROVED: comparison-free 24-gate C clause
Let R(a,b) iff (b-a) modulo five is 1 or 3. Let C(x,y,z) be a directed R triangle. For exactly-one color pins x[v,i], define U_i=x[x,i] OR x[y,i] OR x[z,i], indices modulo five. Then
```
C(x,y,z) = OR(i=0..4) [ U_i AND U_(i+1) AND U_(i+2) ].
```
The five cyclic sets {i,i+1,i+2} are precisely the five cyclic 3-subtournaments of T5. The five other three-element sets {i,i+1,i+3} are transitive. Because three variables contribute only three one-hot colors, any three simultaneously present colors are automatically distinct. Thus the circuit accepts precisely 30/125 ordered assignments and imposes no global injectivity. The unshared clause circuit has 10 OR color-union gates, 10 AND gates and four final OR gates, **24 gates**. It uses no R comparisons. One-hot well-formedness is asserted separately.

For a chosen covering set P of unordered source-variable pairs, precomputing pairwise five-bit OR masks and reusing them across source triples has restricted-construction cost 5|P|+19m before global structural hashing, versus 24m for wholly separate occupancy clauses. The script solves the minimum pair cover exactly for at most 16 distinct source pairs, otherwise greedily. This is an upper bound and **not a lower bound** on unrestricted circuits.

For n source symbols and m clauses, compiling one shared verification DAG for any deletion index i in [0,m) has O(n+m) gates and logarithmic depth using an O(m)-node prefix decoder, O((n+m)log(n+m)) binary materialization/output bits, and charged input parsing and construction. This proves a source-bound **verifier** compiler, not a SAT witness-finding machine or UNSAT proof system.

## Executed results
The independent replayer checked three circuit implementations against all 32,768 one-clause input masks each, including all 125 legitimate triples; zero mismatches. Counts: C=30, strict S=40, old Q=60, old P=20. The old Q forest theorem, 283-variable Q critical fixture and Q gate results do **not** transfer to C.

| Explicit C source | n,m | Shared R gates | Cyclic-coverage gates | Pair-covered gates |
| --- | ---: | ---: | ---: | ---: |
| Single clause | 3,1 | 116 | 66 | 66 |
| Actual C minimal obstruction | 5,4 | 298 | 169 | **159** |
| K5 with private heads | 15,10 | 884 | **459** | 459 |
| K6 with private heads | 21,15 | 1298 | **668** | 668 |
| Every triple on 6 source variables | 6,20 | **503** | 533 | 513 |
| 12 variables, 80 source C triples, seed 20261119 | 12,80 | **1859** | 1977 | 1897 |

The four-clause C core is UNSAT on exhaustive 5^5=3125 assignments. Its four deletion solution counts are 20,20,20,90. In private-head K6, existential C(head,u,v) enforces u!=v, so full K6 is UNSAT by the 5-color pigeonhole argument; all 15 single-edge deletions are SAT. Actual witness construction tried 540 candidate head colors (330 failed trials) and produced 15 complete 21-symbol witnesses, independently verified against original C clauses.

**Physical K6 deletion batch:** one 4-bit indexed verifier requires **725 gates** (314 AND, 386 OR, 25 NOT), depth 13, 109 input pins, **2,151 Tseitin CNF clauses** and **25,825 actual serialized DIMACS bytes**. Separately constructing and writing all 15 deletion verifiers takes **9,645 gates and 342,768 bytes**: 13.303448x gate saving and 13.272720x byte saving. A second O(m)-prefix decoder produces 729 gates, 2163 CNF clauses, 25,977 bytes. Independent verification checked all 240 selector cases and **1,035,360** two-decoder Tseitin clause evaluations, with zero discrepancies. Modeled peak is 39 live *unpinned gate values*, excluding 109 inputs, read-only netlist, source, DIMACS and runtime. Python wall and OS RSS are separately logged.

## Correct-path and lower-bound guards
Checking supplied complete C witnesses is not discovering one. Under the shared/private SAT-block layout, deterministic UNSAT requires actually finding or establishing a negative child for **every** z row. The prior conditional child time exponent remains 0.845+0.35p, with 1.33 target requiring p<=97/70, all child/replay/materialization work charged. A supplied k-bit path is advice/certificate and deterministic discovery may require 2^k checks; wrong-label soundness and all universal branches remain compulsory. No all-CNF specialist follows from this circuit.

DISJ: PASS as local semantic sanity control. Relativization: OPEN for a general SAT transfer. Simultaneous DTISP: OPEN at n^1.33 time and square-root space; known random-access-machine results of FLMV/Williams/Fortnow have distinct precise hypotheses. Deterministic configuration counting: not a lower bound. A comparison-count lower bound that excludes the occupancy compiler is **FALSIFIED** as a universal representation claim. The current extended Tseitin encoding does not inherit a lower bound established for a different prescribed one-hot CNF without proof-complexity transport.

## Evidence and publication
[Full immutable executable archive in Library](https://chatgpt.com/library?file_id=libfile_f3291eb3910c819181073bbf7e2049bb&account_id=personal) contains original strict source package, generator and independent interpreter, all 15 materialized deletion CNFs, both batch CNFs, source JSON, all witnesses, actual resource logs and hashes. ZIP SHA-256: `79a31c0ae4c88b09d788b8368ceb241ab1ebea76bef3613a1a6ac86928c70896`. Original `t5_strict_research_package.zip` SHA-256: `8384d3892198ff3a8e8a0dd6945bd9efc20bcd1120ab6b1b393363d33c9bf5c6`. An independent repackaged replay uses no imports from the compiler. Original issue #3 is already at 2,500 comments; no successful issue comment is claimed.

**Ownership:** no root manuscript, old Q report, other agent file or automation state was edited. This additive role-owned report reconciles strict C as the canonical target and explicitly retires inference from old Q samples as if they were C. Next blocker is a genuine *source-aware UNSAT blocker-discovery or SAT witness-search* procedure with time and peak writable-space charges, across all compact C-compatible representations.

References: [1] User-supplied Strict T5 research package, 2026-11-18. [2] Fortnow–Lipton–van Melkebeek–Viglas, JACM 2005, https://doi.org/10.1145/1101821.1101822. [3] Williams, 2006/2007, https://doi.org/10.1007/s00037-007-0221-1. [4] Fortnow, 2000, https://lance.fortnow.com/papers/files/npvsnl.pdf.
