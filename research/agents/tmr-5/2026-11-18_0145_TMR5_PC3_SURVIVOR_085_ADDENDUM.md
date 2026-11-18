# TMR-5/085 addendum: authentic 143-vertex PC3 false positive

**Date:** 2026-11-18 America/Los_Angeles. **Owner:** TMR-5. **Status:** independently reproduced finite counterexample, not a lower bound.

After finding that generic unanchored path consistency (PC3) refutes all previously proposed /084 Grötzsch NO graphs, a separate deterministic search over seeded random cubic graphs uncovered a **different UNSAT instance that defeats unanchored PC3**.

## Exact construction

Let \(H\) be the undirected cubic graph encoded by the graph6 ASCII string

\`\`\`
YG??S?o????G?A?d??Co?@O??O_?o@O???AECAG?GGAW?O?P?G??gA??
\`\`\`

It has \(26\) vertices, \(39\) edges, all degree \(3\), and girth \(4\). It admits a conventional 3-coloring (an explicit assignment is in the independent evidence package), but **no homomorphism to the undirected \(C_5\)**. This is stronger than simply being 4-chromatic: ordinary 3-colorability does not guarantee \(C_5\)-colorability.

Replace each undirected \(\{u,v\}\), with \(u<v\), by private fresh \(a,b,c\) and genuine T5 arcs \(u\to a\to b\to c,\ u\to c,\ c\to v\). The four-arc forcing component fixes \(a=u+1,b=u+2,c=u+3\pmod5\), while the last arc enforces \(v-u\equiv 1\) or \(4\pmod5\). Consequently the resulting \(D(H)\) has exactly \(26+3(39)=143\) vertices and \(5(39)=195\) directed arcs and is UNSAT, with unique auxiliary extension per valid C5 source assignment.

## Independent verification

1. **Exact source UNSAT:** custom full backtracking with MRV/forward checking and root label 0 (legitimate by \(C_5\)'s rotation symmetry) exhausted 931 recursive calls without a solution; no hidden complexity assumption. Independent SciPy/HiGHS MILP modeled 130 binary color variables, 26 one-color equalities and 585 incompatibility inequalities, returning explicitly *infeasible* (611 constraints total).
2. **Source path consistency:** an 11-line-class pure relational implementation of complete-pair PC3 reaches a nonempty fixed point, although the source has no \(C_5\) solution. It performs 2 in-place scans.
3. **Raw T5 path consistency:** the no-anchor, no-source-recognizer 143-variable T5 bitset PC3 code reaches a nonempty fixed point after 3 scans, leaving all \(143^2=20,449\) ordered pair relations nonempty. An independent compiled C++ synchronous Jacobi PC3 implementation also reaches a nonempty fixed point (6 synchronous rounds, all 20,449 relations nonempty).
4. **Strengthened consistency control:** pinning source vertex 0 to T5 label 0 and re-running path consistency *does* refute the raw 143-variable instance in 2 in-place scans. Therefore this example separates unanchored PC3 from this **particular** anchored-PC3 test, not from all higher local consistency.

The Python raw bitset solver performed 4,416,984 triple-composition checks and removed 62,320 individual ordered-pair tuples before finding the nonempty fixed point. No manual promise-preserving source labels or gadget recognition entered the raw PC3 algorithm.

## Logical consequences

The /084 assertion "anchored AC3 does not solve these instances" remains true but is no protection against ordinary unanchored PC3. Conversely the new 143-variable example **FALSIFIES** the hypothetical claim that unanchored PC3 decides every authentic five-symbol beat-relation CSP, even for a 3-regular source graph with an extremely elementary gadget lift.

The source graph is explicit and small, and its UNSAT status is decided quickly by source-aware exact search; thus this is **NOT** a representation-independent hardness result and it does **NOT** imply time-space lower bounds.

**Ranked chain:**
- Exact T5 NP-completeness: PROVED by [Bang-Jensen, Hell, MacGillivray 1988](https://doi.org/10.1137/0401029), since T5 is semicomplete and contains directed 3-cycles \(0\to1\to2\to0\) and \(0\to3\to4\to0\).
- Exact 5-arc edge gadget and size formulas: independently reproduced, RESTRICTED.
- /084 singleton-AC3 false positive: PROVED FINITE.
- /084 stronger PC3 resistance: FALSIFIED, by generic PC3.
- /085 new 143-vertex UNSAT PC3 false positive: PROVED FINITE, independently crosschecked with bitset Python, synchronous C++, source backtracking, and HiGHS.
- Unrestricted source-aware/adaptive/representation-independent necessary-work lower bounds: OPEN.
- P versus NP: OPEN.

See \`experiments/tmr/tmr5_t5_pc3_survivor_085.py\`, \`results/raw/tmr/tmr5_085_pc3_survivor_summary.json\`, and original /085 report. External mathematical review, full TeX compilation and formal proof kernels not executed.
